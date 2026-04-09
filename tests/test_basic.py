def test_app_starts(app):
    assert app is not None


def test_example(client):
    response = client.get("/api/quizzes")
    assert response.status_code == 200
