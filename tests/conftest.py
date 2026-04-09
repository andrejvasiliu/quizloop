import pytest
from dotenv import load_dotenv

load_dotenv(".env.testing")

from backend import create_app
from backend.db.database import Base, engine


@pytest.fixture
def app():
    app = create_app()

    Base.metadata.create_all(engine)
    yield app
    Base.metadata.drop_all(engine)


@pytest.fixture
def client(app):
    return app.test_client()
