from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from quiz_routes import routes_bp

app = Flask(__name__, static_folder="static", static_url_path="")

app.register_blueprint(routes_bp)

CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/hello", methods=["GET"])
def hello():
    return jsonify(message="Hello from Flask!")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
