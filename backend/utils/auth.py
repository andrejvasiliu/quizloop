from flask import request, current_app, g
import jwt
from datetime import datetime, timedelta


def token_required(f):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return {"error": "Missing or invalid token"}, 401

        token = auth_header.split(" ")[1]
        secret = current_app.config["JWT_SECRET_KEY"]

        try:
            payload = jwt.decode(token, secret, algorithms=["HS256"])
            g.current_user_id = int(payload["sub"])
            g.current_username = payload["username"]
        except jwt.ExpiredSignatureError:
            # raise error instead
            return {"error": "Token expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}, 401

        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper


def create_jwt_token(user_id, username):
    secret = current_app.config["JWT_SECRET_KEY"]
    exp_hours = current_app.config["JWT_EXP_HOURS"]

    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": datetime.utcnow() + timedelta(hours=exp_hours),
        "iat": datetime.utcnow(),
    }

    token = jwt.encode(payload, secret, algorithm="HS256")

    return token
