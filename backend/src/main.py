import sqlite3
import datetime
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, abort
from dataclasses import dataclass
from flasgger import Swagger

DATABASE_PATH = "/data/flosscaster.db"

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

@dataclass
class Podcast:
    id: int
    title: str
    description: str
    date: str

class Ping(Resource):
    def get(self):
        resp = "Pong!"
        return jsonify({"data": resp})

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
        con = sqlite3.connect(DATABASE_PATH)
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

        con = sqlite3.connect(DATABASE_PATH)
        cur = con.cursor()
        cur.execute(f"SELECT * FROM podcasts WHERE id={id}")
        rows = cur.fetchall()
        con.close()

        assert len(rows) < 2, "Duplicate id found in database?"

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
        json = request.get_json()

        title = json["title"]
        description = json["description"]
        date = datetime.datetime.now().strftime("%c")

        con = sqlite3.connect(DATABASE_PATH)
        cur = con.cursor()
        cur.execute(f"INSERT INTO podcasts (id, title, description, date) VALUES (NULL, '{title}', '{description}', '{date}')")
        new_id = cur.lastrowid
        con.commit()
        con.close()

        return f"{new_id}", 200

api.add_resource(Ping, "/api/ping")
api.add_resource(List, "/api/list")
api.add_resource(GetById, "/api/get")
api.add_resource(Create, "/api/create")

if __name__ == "__main__":
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS podcasts(id INTEGER PRIMARY KEY, title, description, date)")
    con.close()
    app.run(host="0.0.0.0", debug = True)
