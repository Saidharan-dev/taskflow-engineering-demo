from fastapi.testclient import TestClient

from app.main import app


API_HEADERS = {"X-API-Key": "test-taskflow-key"}


def test_create_and_retrieve_task(monkeypatch, test_database):
    monkeypatch.setenv("TASKFLOW_API_KEY", "test-taskflow-key")

    with TestClient(app) as client:
        create_response = client.post(
            "/tasks",
            headers=API_HEADERS,
            json={
                "title": "Investigate API latency",
                "description": "Measure slow endpoints",
                "priority": "high",
            },
        )

        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        get_response = client.get(
            f"/tasks/{task_id}",
            headers=API_HEADERS,
        )

        assert get_response.status_code == 200
        assert get_response.json()["title"] == "Investigate API latency"


def test_create_task_rejects_invalid_title(monkeypatch, test_database):
    monkeypatch.setenv("TASKFLOW_API_KEY", "test-taskflow-key")

    with TestClient(app) as client:
        response = client.post(
            "/tasks",
            headers=API_HEADERS,
            json={"title": "AB"},
        )

        assert response.status_code == 422


def test_missing_task_returns_404(monkeypatch, test_database):
    monkeypatch.setenv("TASKFLOW_API_KEY", "test-taskflow-key")

    with TestClient(app) as client:
        response = client.get(
            "/tasks/9999",
            headers=API_HEADERS,
        )

        assert response.status_code == 404
