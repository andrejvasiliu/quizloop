from flask import request, current_app, g
import jwt
from datetime import datetime, timedelta, UTC
from .exceptions import (
    TokenExpiredError,
    InvalidTokenError,
    MissingFieldError,
    InvalidEmailError,
)


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
            raise TokenExpiredError()
        except jwt.InvalidTokenError:
            raise InvalidTokenError()

        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper


def create_jwt_token(user_id, username, secret, exp_hours):
    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": datetime.now(UTC) + timedelta(hours=exp_hours),
        "iat": datetime.now(UTC),
    }

    token = jwt.encode(payload, secret, algorithm="HS256")

    return token


def require_field(data, field):
    value = data.get(field)
    if not value:
        raise MissingFieldError(f"{field} is required")
    return value


def validate_email_format(email):
    if "@" not in email or "." not in email:
        raise InvalidEmailError()
