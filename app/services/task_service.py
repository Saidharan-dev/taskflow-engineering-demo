
from datetime import datetime, timezone
from typing import Optional

from app.database import get_db
from app.models.task import TaskCreate, TaskUpdate


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _serialize(row) -> dict:
    return dict(row)


def create_task(payload: TaskCreate) -> dict:
    timestamp = _now()

    with get_db() as connection:
        cursor = connection.execute(
            """
            INSERT INTO tasks (
                title, description, status, priority, assignee,
                created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload.title,
                payload.description,
                "todo",
                payload.priority.value,
                payload.assignee,
                timestamp,
                timestamp,
            ),
        )

        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()

        return _serialize(row)


def get_task(task_id: int) -> Optional[dict]:
    with get_db() as connection:
        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()

        return _serialize(row) if row else None


def list_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> list[dict]:
    query = "SELECT * FROM tasks WHERE 1 = 1"
    parameters = []

    if status is not None:
        query += " AND status = ?"
        parameters.append(status)

    if priority is not None:
        query += " AND priority = ?"
        parameters.append(priority)

    query += " ORDER BY id DESC LIMIT ? OFFSET ?"
    parameters.extend([limit, offset])

    with get_db() as connection:
        rows = connection.execute(query, parameters).fetchall()
        return [_serialize(row) for row in rows]


def update_task(task_id: int, payload: TaskUpdate) -> Optional[dict]:
    updates = payload.model_dump(exclude_unset=True)

    if not updates:
        return get_task(task_id)

    if "status" in updates and updates["status"] is not None:
        updates["status"] = updates["status"].value

    if "priority" in updates and updates["priority"] is not None:
        updates["priority"] = updates["priority"].value

    updates["updated_at"] = _now()

    assignments = ", ".join(f"{column} = ?" for column in updates)
    values = list(updates.values()) + [task_id]

    with get_db() as connection:
        cursor = connection.execute(
            f"UPDATE tasks SET {assignments} WHERE id = ?",
            values,
        )

        if cursor.rowcount == 0:
            return None

        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()

        return _serialize(row)


def delete_task(task_id: int) -> bool:
    with get_db() as connection:
        cursor = connection.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,),
        )

        return cursor.rowcount > 0
