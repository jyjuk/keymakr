from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_fetch_users_queues_task():
    with patch("app.main.fetch_and_save_users.delay") as mock_delay:
        response = client.post("/fetch-users")
    assert response.status_code == 202
    assert response.json() == {"message": "Task queued"}
    mock_delay.assert_called_once()
