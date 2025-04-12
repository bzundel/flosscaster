from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Ping(Resource):
    def get(self):
        resp = "Pong!"
        return jsonify({"data": resp})

api.add_resource(Ping, "/api/ping")

if __name__ == "__main__":
    app.run(debug = True)
