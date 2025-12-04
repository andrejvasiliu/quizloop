from db.models import User
from sqlalchemy.exc import IntegrityError
from utils.exceptions import UserAlreadyExistsError


def create_user(session, user):
    try:
        session.add(user)
        session.flush()
        return user
    except IntegrityError:
        raise UserAlreadyExistsError()


def login_user(session, username):
    return session.query(User).filter(User.username == username).first()
