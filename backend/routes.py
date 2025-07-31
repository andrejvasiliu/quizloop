from flask import request, jsonify
from app import app
import os


@app.route("/upload", methods=["POST"])
def upload_quiz():
    if "quiz_json" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["quiz_json"]

    if file and file.filename.endswith(".json"):
        try:
            filepath = os.path.join("quizzes", file.filename)
            file.save(filepath)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file format"}), 400

    return jsonify({"status": "success"})
