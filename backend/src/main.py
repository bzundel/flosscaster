import os
import sqlite3
import datetime
from flask import Flask, jsonify, request, send_from_directory
from flask_restful import Resource, Api, abort
from flask_cors import CORS
from dataclasses import dataclass
from flasgger import Swagger

DATABASE_PATH = os.getenv("DATABASE_PATH")
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok =True)

app = Flask(__name__)
CORS(app)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
api = Api(app)
swagger = Swagger(app)

ALLOWED_EXTENSIONS = {'mp3'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        con = sqlite3.connect(DATABASE_PATH)
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

        con = sqlite3.connect(DATABASE_PATH)
        cur = con.cursor()
        cur.execute(f"SELECT * FROM podcasts WHERE id=?",(id,))
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

        filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{audio_file.filename}"
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        audio_file.save(file_path)

        date = datetime.datetime.now().strftime("%c")
        con = sqlite3.connect(DATABASE_PATH)
        cur = con.cursor()
        cur.execute("INSERT INTO podcasts (id, title, description, date, filepath) VALUES (NULL, ?,?,?,?)", (title, description, date, filename))
        new_id = cur.lastrowid
        con.commit()
        con.close()

        return f"{new_id}", 200

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

api.add_resource(Ping, "/api/ping")
api.add_resource(List, "/api/list")
api.add_resource(GetById, "/api/get")
api.add_resource(Create, "/api/create")

if __name__ == "__main__":
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS podcasts(id INTEGER PRIMARY KEY, title, description, date, filepath)")
    con.close()
    app.run(host="0.0.0.0", port = 1111, debug = True)
