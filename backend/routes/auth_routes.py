from flask import Blueprint, request
from db.db import SessionLocal
from db.models import User

auth_routes_bp = Blueprint("auth_routes", __name__)


@auth_routes_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username, email, password = data.get("username"), data.get("email"), data.get("password")
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

        return {"message": "User registered successfully"}, 201

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

        return {"message": "Login successful"}, 200

    finally:
        session.close()