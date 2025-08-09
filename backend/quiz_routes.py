from flask import Blueprint, request, jsonify
import os
import json

routes_bp = Blueprint("routes", __name__)


@routes_bp.route("/upload", methods=["POST"])
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


@routes_bp.route("/quizzes", methods=["GET"])
def list_quizzes():
    try:
        quizzes = [f for f in os.listdir("quizzes") if f.endswith(".json")]
        quiz_list = []
        for q in quizzes:
            with open(os.path.join("quizzes", q), "r") as f:
                data = json.load(f)
                quiz_list.append(
                    {
                        "title": data.get("title"),
                        "name": os.path.splitext(q)[0],
                    }
                )

        return jsonify({"quizzes": quiz_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes_bp.route("/quiz/<quiz_name>", methods=["POST"])
def start_quiz(quiz_name):
    try:
        filepath = os.path.join("quizzes", quiz_name + ".json")
        if not os.path.exists(filepath):
            return jsonify({"error": "Quiz not found"}), 404

        with open(filepath, "r") as file:
            quiz_data = json.load(file)

        return jsonify({"quiz": quiz_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# @routes_bp.route("/submit/<quiz_name>", methods=["POST"])
