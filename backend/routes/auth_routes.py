import jwt
from datetime import datetime, timedelta
from flask import Blueprint, request, current_app, g
from db.db import SessionLocal
from db.models import User

auth_routes_bp = Blueprint("auth_routes", __name__)


def token_required(f):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return {"error": "Missing or invalid token"}, 401

        token = auth_header.split(" ")[1]
        secret = current_app.config["JWT_SECRET_KEY"]

        try:
            payload = jwt.decode(token, secret, algorithms=["HS256"])
            g.current_user_id = payload["sub"]
        except jwt.ExpiredSignatureError:
            return {"error": "Token expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}, 401

        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__  # keep function name
    return wrapper


@auth_routes_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username, email, password = (
        data.get("username"),
        data.get("email"),
        data.get("password"),
    )
    session = SessionLocal()

    try:
        existing_user = (
            session.query(User)
            .filter((User.username == username) | (User.email == email))
            .first()
        )

        if existing_user:
            return {"error": "Username or email already exists"}, 400

        user = User(username=username, email=email)
        user.set_password(password)

        session.add(user)
        session.commit()

        return {"username": username, "message": "User registered successfully"}, 201

    finally:
        session.close()


@auth_routes_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username, password = data.get("username"), data.get("password")
    session = SessionLocal()

    try:
        user = session.query(User).filter(User.username == username).first()
        if not user or not user.check_password(password):
            return {"error": "Invalid username or password"}, 401

        secret = current_app.config["JWT_SECRET_KEY"]
        exp_hours = current_app.config["JWT_EXP_HOURS"]

        payload = {
            "sub": user.id,
            "username": user.username,
            "exp": datetime.utcnow() + timedelta(hours=exp_hours),
            "iat": datetime.utcnow(),
        }

        token = jwt.encode(payload, secret, algorithm="HS256")

        return {
            "access_token": token,
            "username": username,
            "message": "Login successful",
        }, 200

    finally:
        session.close()


@auth_routes_bp.route("/me", methods=["GET"])
@token_required
def profile():
    return {"username": g.current_user_id, "message": "Profile accessed"}, 200
