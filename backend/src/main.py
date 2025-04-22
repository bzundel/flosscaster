import sqlite3
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from dataclasses import dataclass

DATABASE_PATH = "../flosscaster.db"

app = Flask(__name__)
api = Api(app)

@dataclass
class Podcast:
    title: str
    description: str
    date: str

class Ping(Resource):
    def get(self):
        resp = "Pong!"
        return jsonify({"data": resp})

class List(Resource):
    def get(self):
        con = sqlite3.connect(DATABASE_PATH)
        cur = con.cursor()
        cur.execute(f"SELECT * FROM podcasts")

        rows = cur.fetchall()
        podcasts = [Podcast(*row) for row in rows]

        con.close()
        return jsonify(podcasts)

class Create(Resource):
    def post(self):
        json = request.get_json()

        title = json["title"]
        description = json["description"]
        date = json["date"]

        con = sqlite3.connect(DATABASE_PATH)
        cur = con.cursor()
        cur.execute(f"INSERT INTO podcasts VALUES ('{title}', '{description}', '{date}')")
        con.commit()
        con.close()

        return "", 200

api.add_resource(Ping, "/api/ping")
api.add_resource(List, "/api/list")
api.add_resource(Create, "/api/create")

if __name__ == "__main__":
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS podcasts(title, description, date)")
    con.close()
    app.run(debug = True)
