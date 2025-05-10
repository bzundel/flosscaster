import os
import sqlite3
import datetime
import uuid
from flask import Flask, jsonify, request, send_file
from flask_restful import Resource, Api, abort
from flask_cors import CORS
from dataclasses import dataclass
from flasgger import Swagger

DATABASE_FILE = os.getenv("DATABASE_FILE")
UPLOAD_PATH = "uploads"
ALLOWED_EXTENSIONS = {".mp3"}

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

class Ping(Resource):
    def get(self):
        resp = "Pong!"
        return jsonify({"data": resp})

class List(Resource):
    def get(self):
        con = sqlite3.connect(DATABASE_FILE)
        cur = con.cursor()
        cur.execute(f"SELECT * FROM podcasts")

        rows = cur.fetchall()
        podcasts = [Podcast(*row) for row in rows]

        con.close()

        return jsonify(podcasts)

class GetById(Resource):
    def get(self):
        id = request.args.get("id")

        if id == None:
            abort(400, error_message="Must provide an id")

        con = sqlite3.connect(DATABASE_FILE)
        cur = con.cursor()
        cur.execute(f"SELECT * FROM podcasts WHERE id=?", (id))
        rows = cur.fetchall()
        con.close()

        if len(rows) == 0:
            abort(404, error_message="Queried item does not exist")

        return jsonify(Podcast(*rows[0]))

class Create(Resource):
    def post(self):
        title = request.form.get("title")
        description = request.form.get("description")
        audio_file = request.files.get("audio")

        _, extension = os.path.splitext(audio_file.filename)

        if not extension.lower() in ALLOWED_EXTENSIONS:
            abort(400, error_message="Invalid file extension")

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

        return f"{new_id}", 200

class GetFileByFilename(Resource):
    def get(self, filename):
        path = os.path.abspath(os.path.join(UPLOAD_PATH, filename))

        return send_file(path)

api.add_resource(Ping, "/api/ping")
api.add_resource(List, "/api/list")
api.add_resource(GetById, "/api/get")
api.add_resource(Create, "/api/create")
api.add_resource(GetFileByFilename, "/api/get_upload/<path:filename>")

if __name__ == "__main__":
    con = sqlite3.connect(DATABASE_FILE)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS podcasts(id INTEGER PRIMARY KEY, title, description, date, filepath)")
    con.close()
    app.run(host="0.0.0.0", port = 1111, debug = True)
