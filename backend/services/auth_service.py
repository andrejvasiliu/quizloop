from db.models import User
from repositories.auth_repository import create_user, login_user
from utils.auth import create_jwt_token


def register_user_service(session, data):
    username, email, password = (
        data.get("username"),
        data.get("email"),
        data.get("password"),
    )

    user = User(username=username, email=email)
    user.set_password(password)
    user = create_user(session, user)

    token = create_jwt_token(user.id, user.username)

    return {
        "access_token": token,
        "username": username,
    }


def login_user_service(session, data):
    username, password = (data.get("username"), data.get("password"))
    user = login_user(session, username)

    if not user or not user.check_password(password):
        raise ValueError("Invalid username or password")

    token = create_jwt_token(user.id, user.username)

    return {
        "access_token": token,
        "username": username,
    }
