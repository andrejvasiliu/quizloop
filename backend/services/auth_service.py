from db.models import User
from repositories.auth_repository import create_user, login_user
from utils.auth import create_jwt_token, require_field, validate_email_format
from utils.exceptions import InvalidCredentialsError


def register_user_service(session, data):
    username, email, password = (
        require_field(data, "username"),
        require_field(data, "email"),
        require_field(data, "password"),
    )

    validate_email_format(email)

    user = User(username=username, email=email)
    user.set_password(password)
    user = create_user(session, user)

    token = create_jwt_token(user.id, user.username)

    return {
        "access_token": token,
        "username": user.username,
    }


def login_user_service(session, data):
    username, password = (
        require_field(data, "username"),
        require_field(data, "password"),
    )

    user = login_user(session, username)

    if not user or not user.check_password(password):
        raise InvalidCredentialsError()

    token = create_jwt_token(user.id, user.username)

    return {
        "access_token": token,
        "username": user.username,
    }
