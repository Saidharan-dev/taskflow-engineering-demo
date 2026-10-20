
from fastapi.testclient import TestClient

from app import database
from app.main import app


def setup_test_database(monkeypatch, tmp_path):
    test_db_path = tmp_path / "api_test.db"
    monkeypatch.setattr(database, "DATABASE_PATH", test_db_path)
    return test_db_path


def test_create_and_retrieve_task(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    with TestClient(app) as client:
        create_response = client.post(
            "/tasks",
            json={
                "title": "Investigate API latency",
                "description": "Measure slow endpoints",
                "priority": "high",
            },
        )

        assert create_response.status_code == 201
        created = create_response.json()
        assert created["title"] == "Investigate API latency"

        get_response = client.get(f"/tasks/{created['id']}")

        assert get_response.status_code == 200
        assert get_response.json()["id"] == created["id"]


def test_create_task_rejects_invalid_title(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    with TestClient(app) as client:
        response = client.post(
            "/tasks",
            json={"title": "AB"},
        )

        assert response.status_code == 422


def test_missing_task_returns_404(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    with TestClient(app) as client:
        response = client.get("/tasks/9999")

        assert response.status_code == 404
