
from app.models.task import TaskCreate, TaskPriority, TaskStatus, TaskUpdate
from app.services import task_service


def test_update_task_status_and_priority(test_database):
    created = task_service.create_task(
        TaskCreate(title="Investigate API latency")
    )

    updated = task_service.update_task(
        created["id"],
        TaskUpdate(
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.CRITICAL,
        ),
    )

    assert updated is not None
    assert updated["status"] == "in_progress"
    assert updated["priority"] == "critical"
    assert updated["updated_at"] >= created["updated_at"]


def test_update_missing_task_returns_none(test_database):
    result = task_service.update_task(
        9999,
        TaskUpdate(status=TaskStatus.DONE),
    )

    assert result is None


def test_delete_task_removes_record(test_database):
    created = task_service.create_task(
        TaskCreate(title="Remove obsolete endpoint")
    )

    assert task_service.delete_task(created["id"]) is True
    assert task_service.get_task(created["id"]) is None


def test_delete_missing_task_returns_false(test_database):
    assert task_service.delete_task(9999) is False
