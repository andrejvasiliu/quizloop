def test_get_quizzes_returns_200(client, db_session):
    response = client.get("/api/quizzes")
    assert response.status_code == 200
