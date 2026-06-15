from contextlib import contextmanager
from . import database

@contextmanager
def get_session():
    session = database.SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()