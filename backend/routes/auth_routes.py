from flask import Blueprint, request, g, jsonify
from utils.auth import token_required
from db.session import get_session
from services.auth_service import register_user_service, login_user_service

auth_routes_bp = Blueprint("auth_routes", __name__)


@auth_routes_bp.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.json

    with get_session() as session:
        token_and_username = register_user_service(session, data)

    return jsonify(
        {
            **token_and_username,
            "message": "User registered successfully",
        }
    ), 201


@auth_routes_bp.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.json

    with get_session() as session:
        token_and_username = login_user_service(session, data)

    return {
        **token_and_username,
        "message": "Login successful",
    }, 200


@auth_routes_bp.route("/me", methods=["GET"])
@token_required
def profile():
    return jsonify({"username": g.current_username, "message": "Profile accessed"}), 200


@auth_routes_bp.route("/logout", methods=["POST"])
@token_required
def logout():
    return jsonify({"message": "Logout successful"}), 200
