import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from dotenv import load_dotenv
import os

load_dotenv(".env.testing")

from backend import create_app
from backend.db.database import Base
from backend.db.models import User


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(
        os.getenv("DATABASE_URI", "sqlite:///:memory:"),
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # one connection reused — critical for in-memory database
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="session")
def app(test_engine):
    application = create_app()
    yield application


@pytest.fixture
def db_connection(test_engine):
    with test_engine.connect() as connection:
        transaction = connection.begin()
        yield connection
        transaction.rollback()


@pytest.fixture
def db_session(db_connection, monkeypatch):
    import backend.db.database as db_module

    session = Session(
        bind=db_connection,
        join_transaction_mode="create_savepoint",
    )

    # Patch the app's SessionLocal so HTTP requests use this same connection.
    # This ensures routes and test fixtures see identical data.
    TestSessionLocal = sessionmaker(
        bind=db_connection,
        join_transaction_mode="create_savepoint",
    )
    monkeypatch.setattr(db_module, "SessionLocal", TestSessionLocal)

    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def test_user(db_session):
    user = User(username="test", email="test@test.com")
    user.set_password("password123")
    db_session.add(user)
    db_session.flush()
    yield user


@pytest.fixture
def auth_client(client, test_user, db_session):
    response = client.post(
        "/api/login", json={"username": "test", "password": "password123"}
    )
    token = response.json["access_token"]
    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    return client
