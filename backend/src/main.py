import os
import sqlite3
import datetime
import uuid
from flask import Flask, jsonify, request, send_file
from flask_restful import Resource, Api, abort
from flask_cors import CORS
from dataclasses import dataclass
from flasgger import Swagger
from tools import rss_helper, masttoot

DATABASE_FILE = os.getenv("DATABASE_FILE")
UPLOAD_PATH = os.getenv("UPLOAD_PATH")
FRONTEND_URL = os.getenv("FRONTEND_URL")
RSS_FILE = os.getenv("RSS_FILE")

os.makedirs(UPLOAD_PATH, exist_ok=True)

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

CORS(app)

@dataclass
class Podcast:
    id: int
    title: str
    description: str
    date: str
    filepath: str

class List(Resource):
    def get(self):
        """Returns all podcasts metadata in the database
        ---
        definitions:
            Podcast:
                type: object
                properties:
                    id:
                        type: integer
                    title:
                        type: string
                    description:
                        type: string
                    date:
                        type: string
        responses:
            200:
                description: A list containing all podcasts
                schema:
                    type: array
                    items:
                        $ref: "#/definitions/Podcast"
                examples:
                    [
                      {
                        'id': 1,
                        'title': '6-Sekunden Podcast',
                        'description': 'Wir hatten keine Zeit um ein Thema anzusprechen.',
                        'date': '2025-04-22T20:00:00Z',
                      },
                      {
                        'id': 2,
                        'title': '6-Sekunden Podcast: Part 2',
                        'description': 'Wir hatten wieder keine Zeit um ein Thema anzusprechen.',
                        'date': '2025-04-23T18:00:00Z',
                      }
                    ]
        """
        con = sqlite3.connect(DATABASE_FILE)
        cur = con.cursor()
        cur.execute(f"SELECT * FROM podcasts")

        rows = cur.fetchall()
        podcasts = [Podcast(*row) for row in rows]

        con.close()

        return jsonify(podcasts)

class GetById(Resource):
    def get(self):
        """Returns all podcasts metadata in the database
        ---
        parameters:
          - name: id
            in: query
            type: integer
            required: true
        responses:
            200:
                description: A podcast object matching the id specified in the parameter
                schema:
                    $ref: "#/definitions/Podcast"
                examples:
                  {
                    'id': 1,
                    'title': '6-Sekunden Podcast',
                    'description': 'Wir hatten keine Zeit um ein Thema anzusprechen.',
                    'date': '2025-04-22T20:00:00Z',
                  }
            400:
                description: No id was provided
            404:
                description: Podcast was not found
        """
        id = request.args.get("id")

        if id == None:
            abort(400, error_message="Must provide an id")

        con = sqlite3.connect(DATABASE_FILE)
        cur = con.cursor()
        cur.execute(f"SELECT * FROM podcasts WHERE id=?", id)
        rows = cur.fetchall()
        con.close()

        if len(rows) == 0:
            abort(404, error_message="Queried item does not exist")

        return jsonify(Podcast(*rows[0]))

class Create(Resource):
    def post(self):
        """Create a podcast and return the new id
        ---
        parameters:
          - name: title
            in: path
            type: string
            required: true
          - name: description
            in: path
            type: string
            required: true
          - name: audio
            in: path
            type: file
            required: true
        responses:
            200:
                description: The internal id of the newly created podcast
                schema:
                    type: integer
                examples:
                    1
            404:
                description: Something went wrong in the process of creating the podcast
        """
        title = request.form.get("title")
        description = request.form.get("description")
        audio_file = request.files.get("audio")
        audio_file_read = audio_file.read()
        file_size = len(audio_file_read)

        if audio_file.mimetype != "audio/mpeg":
            abort(400, error_message="Invalid file format; must be audio/mpeg")

        _, extension = os.path.splitext(audio_file.filename)

        filename = f"{str(uuid.uuid4())}{extension}"
        file_path = os.path.join(UPLOAD_PATH, filename)
        audio_file.save(file_path)

        date = datetime.datetime.now().strftime("%c")
        con = sqlite3.connect(DATABASE_FILE)
        cur = con.cursor()
        cur.execute("INSERT INTO podcasts (id, title, description, date, filepath) VALUES (NULL, ?,?,?,?)", (title, description, date, filename))
        new_id = cur.lastrowid
        con.commit()
        con.close()

        rss_helper.add_episode_to_podcast(title, FRONTEND_URL, description, str(file_size))

        if not os.getenv("MASTODON_ACCESS_TOKEN") is None:
            masttoot.masttoot(title, FRONTEND_URL, description)

        return f"{new_id}", 200

class GetFileByFilename(Resource):
    def get(self, filename):
        """Return the audio file associated to a filename
        ---
        parameters:
          - name: filename
            in: query
            type: string
            required: true
        responses:
            200:
                description: A file corresponding to the passed argument
            404:
                description: No file with the given name was found
        """
        path = os.path.abspath(os.path.join(UPLOAD_PATH, filename))

        if not os.path.exists(path):
            abort(404, error_message="Given file was not found")

        return send_file(path)

class GetRSS(Resource):
    def get(self):
        """Return the RSS feed
        ---
        responses:
            200:
                description: File was found and successfully sent
            304:
                description: File was found and is unmodified, cached version is used
            404:
                description: RSS file was not found in the filesystem
        """
        feed_path = os.path.abspath(RSS_FILE)
        return send_file(feed_path)

api.add_resource(List, "/api/list")
api.add_resource(GetById, "/api/get")
api.add_resource(Create, "/api/create")
api.add_resource(GetFileByFilename, "/api/get_upload/<path:filename>")
api.add_resource(GetRSS, "/rss")

if __name__ == "__main__":
    con = sqlite3.connect(DATABASE_FILE)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS podcasts(id INTEGER PRIMARY KEY, title, description, date, filepath)")
    con.close()
    rss_helper.create_template_if_not_exists()

    app.run(host="0.0.0.0", port = 1111, debug = True)

