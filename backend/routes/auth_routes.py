from flask import Blueprint, request, current_app, g, jsonify
from db.db import SessionLocal
from db.models import User
import jwt
from datetime import datetime, timedelta
from utils.auth import token_required
from db.session import get_session
from services.auth_service import register_user_service, login_user_service
from sqlalchemy.exc import IntegrityError

auth_routes_bp = Blueprint("auth_routes", __name__)


@auth_routes_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    try:
        with get_session() as session:
            token_and_username = register_user_service(session, data)

        return jsonify(
            {
                **token_and_username,
                "message": "User registered successfully",
            }
        ), 201
    except IntegrityError:
        return jsonify({"error": "Username or Email already in use"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_routes_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    try:
        with get_session() as session:
            token_and_username = login_user_service(session, data)

        return {
            **token_and_username,
            "message": "Login successful",
        }, 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_routes_bp.route("/me", methods=["GET"])
@token_required
def profile():
    return jsonify({"username": g.current_username, "message": "Profile accessed"}), 200


@auth_routes_bp.route("/logout", methods=["POST"])
@token_required
def logout():
    return jsonify({"message": "Logout successful"}), 200
