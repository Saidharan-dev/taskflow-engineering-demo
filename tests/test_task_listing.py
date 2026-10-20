
from app.models.task import TaskCreate, TaskPriority, TaskStatus
from app.services import task_service


def test_list_tasks_filters_by_status(test_database):
    first = task_service.create_task(
        TaskCreate(title="Investigate API latency")
    )
    task_service.update_task(
        first["id"],
        __import__(
            "app.models.task", fromlist=["TaskUpdate"]
        ).TaskUpdate(status=TaskStatus.DONE),
    )

    task_service.create_task(
        TaskCreate(title="Add API validation")
    )

    tasks = task_service.list_tasks(status="todo")

    assert len(tasks) == 1
    assert tasks[0]["title"] == "Add API validation"


def test_list_tasks_filters_by_priority(test_database):
    task_service.create_task(
        TaskCreate(title="Add documentation")
    )
    task_service.create_task(
        TaskCreate(
            title="Fix production latency",
            priority=TaskPriority.CRITICAL,
        )
    )

    tasks = task_service.list_tasks(priority="critical")

    assert len(tasks) == 1
    assert tasks[0]["priority"] == "critical"


def test_list_tasks_supports_pagination(test_database):
    for title in [
        "Improve API validation",
        "Improve API logging",
        "Improve API monitoring",
    ]:
        task_service.create_task(TaskCreate(title=title))

    first_page = task_service.list_tasks(limit=2, offset=0)
    second_page = task_service.list_tasks(limit=2, offset=2)

    assert len(first_page) == 2
    assert len(second_page) == 1
    assert first_page[0]["id"] != second_page[0]["id"]
