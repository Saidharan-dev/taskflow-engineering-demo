
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("TASKFLOW_API_KEY", "test-taskflow-key")

    with TestClient(app) as test_client:
        yield test_client


def test_tasks_endpoint_rejects_missing_api_key(client):
    response = client.get("/tasks")

    assert response.status_code == 401


def test_tasks_endpoint_rejects_invalid_api_key(client):
    response = client.get(
        "/tasks",
        headers={"X-API-Key": "wrong-key"},
    )

    assert response.status_code == 401


def test_tasks_endpoint_accepts_valid_api_key(client):
    response = client.get(
        "/tasks",
        headers={"X-API-Key": "test-taskflow-key"},
    )

    assert response.status_code == 200


def test_health_endpoint_remains_public(client):
    response = client.get("/health")

    assert response.status_code == 200
