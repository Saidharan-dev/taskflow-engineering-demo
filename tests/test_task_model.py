
import pytest
from pydantic import ValidationError

from app.models.task import (
    TaskCreate,
    TaskPriority,
    TaskStatus,
    TaskUpdate,
)


def test_task_create_defaults():
    task = TaskCreate(title="Improve API latency")

    assert task.title == "Improve API latency"
    assert task.priority == TaskPriority.MEDIUM
    assert task.description == ""
    assert task.assignee is None


def test_task_create_rejects_short_title():
    with pytest.raises(ValidationError):
        TaskCreate(title="AB")


def test_task_create_rejects_invalid_priority():
    with pytest.raises(ValidationError):
        TaskCreate(title="Fix API latency", priority="urgent")


def test_task_update_accepts_status_change():
    update = TaskUpdate(status=TaskStatus.IN_PROGRESS)

    assert update.status == TaskStatus.IN_PROGRESS
