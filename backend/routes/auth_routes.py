from flask import Blueprint, request, g, jsonify, current_app
from ..utils.auth import token_required
from ..db.session import get_session
from ..services.auth_service import register_user_service, login_user_service
from ..utils.responses import error_response

auth_routes_v1_bp = Blueprint("auth_routes_v1", __name__)


@auth_routes_v1_bp.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return error_response("Request must be JSON", 400)

    data = request.json

    jwt_secret = current_app.config["JWT_SECRET_KEY"]
    jwt_exp_hours = current_app.config["JWT_EXP_HOURS"]

    with get_session() as session:
        token_and_username = register_user_service(
            session, data, jwt_secret, jwt_exp_hours
        )

    return jsonify(
        {
            **token_and_username,
            "message": "User registered successfully",
        }
    ), 201


@auth_routes_v1_bp.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return error_response("Request must be JSON", 400)

    data = request.json

    jwt_secret = current_app.config["JWT_SECRET_KEY"]
    jwt_exp_hours = current_app.config["JWT_EXP_HOURS"]

    with get_session() as session:
        token_and_username = login_user_service(
            session, data, jwt_secret, jwt_exp_hours
        )

    return {
        **token_and_username,
        "message": "Login successful",
    }, 200


@auth_routes_v1_bp.route("/me", methods=["GET"])
@token_required
def profile():
    return jsonify({"username": g.current_username, "message": "Profile accessed"}), 200


@auth_routes_v1_bp.route("/logout", methods=["POST"])
@token_required
def logout():
    return jsonify({"message": "Logout successful"}), 200
