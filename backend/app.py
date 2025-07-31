from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import routes

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/hello", methods=["GET"])
def hello():
    return jsonify(message="Hello from Flask!")


if __name__ == "__main__":
    app.run(debug=True)
