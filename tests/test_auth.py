import jwt


def test_register_success(client, db_session):
    response = client.post(
        "/api/register",
        json={
            "email": "new@test.com",
            "username": "newuser",
            "password": "password123",
        },
    )

    assert response.status_code == 201
    assert "access_token" in response.json

    decoded = jwt.decode(
        response.json["access_token"],
        client.application.config["JWT_SECRET_KEY"],
        algorithms=["HS256"],
    )
    assert decoded["username"] == "newuser"

    # Verify the user was actually written to the database
    from backend.db.models import User

    user = db_session.query(User).filter_by(email="new@test.com").first()
    assert user is not None
    assert user.username == "newuser"


def test_register_duplicate_email_returns_409(client, db_session, test_user):
    response = client.post(
        "/api/register",
        json={
            "email": "test@test.com",
            "username": "someone_else",
            "password": "password123",
        },
    )
    assert response.status_code == 409


def test_register_missing_fields_returns_422(client):
    response = client.post("/api/register", json={"email": "x@x.com"})
    assert response.status_code == 422


def test_login_success(client, db_session, test_user):
    response = client.post(
        "/api/login",
        json={
            "username": "test",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json


def test_login_wrong_password_returns_401(client, db_session, test_user):
    response = client.post(
        "/api/login",
        json={
            "username": "test",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401


def test_login_unknown_user_returns_401(client, db_session):
    response = client.post(
        "/api/login",
        json={
            "username": "ghost",
            "password": "password123",
        },
    )
    assert response.status_code == 401
