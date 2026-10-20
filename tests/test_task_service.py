
from app.models.task import TaskCreate, TaskPriority
from app.services import task_service


def test_create_task_persists_task(test_database):
    payload = TaskCreate(
        title="Investigate API latency",
        description="Measure slow endpoints",
        priority=TaskPriority.HIGH,
        assignee="developer-1",
    )

    task = task_service.create_task(payload)

    assert task["id"] > 0
    assert task["title"] == "Investigate API latency"
    assert task["status"] == "todo"
    assert task["priority"] == "high"
    assert task["assignee"] == "developer-1"


def test_get_task_returns_existing_task(test_database):
    created = task_service.create_task(
        TaskCreate(title="Add request validation")
    )

    task = task_service.get_task(created["id"])

    assert task is not None
    assert task["id"] == created["id"]
    assert task["title"] == "Add request validation"


def test_get_task_returns_none_for_missing_id(test_database):
    assert task_service.get_task(9999) is None
