from db.models import User

def create_user(session, user):
    session.add(user)
    session.flush()
    return user

def login_user(session, username):
    return session.query(User).filter(User.username == username).first()