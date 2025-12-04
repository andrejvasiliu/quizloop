from flask import Blueprint, request, jsonify, g
from utils.auth import token_required
from services.quiz_service import (
    upload_quiz_service,
    get_all_quizzes_service,
    get_quiz_service,
)
from db.session import get_session
from utils.exceptions import MissingFieldError

quiz_routes_bp = Blueprint("quiz_routes", __name__)


@quiz_routes_bp.route("/upload", methods=["POST"])
@token_required
def upload_quiz():
    if "quiz_json" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["quiz_json"]

    try:
        with get_session() as session:
            upload_quiz_service(session, file, g.current_user_id)
            return jsonify({"success": True}), 201
    except MissingFieldError as e:
        return jsonify({"error": str(e)}), 422


@quiz_routes_bp.route("/quizzes", methods=["GET"])
def list_quizzes():
    with get_session() as session:
        quiz_list = get_all_quizzes_service(session)
        return jsonify({"quizzes": quiz_list}), 200


@quiz_routes_bp.route("/quiz/<int:quiz_id>", methods=["POST"])
@token_required
def start_quiz(quiz_id):
    with get_session() as session:
        quiz_data = get_quiz_service(session, quiz_id)
        return jsonify({"quiz": quiz_data}), 200


# @quiz_routes_bp.route("/submit/<quiz_name>", methods=["POST"])
# @token_required
