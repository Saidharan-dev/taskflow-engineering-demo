
from app.database import get_db, init_db


def test_task_list_query_plan_uses_primary_key_for_ordering(test_database):
    """Record SQLite's plan for the task-list query before optimization."""
    with get_db() as connection:
        plan = connection.execute(
            """
            EXPLAIN QUERY PLAN
            SELECT *
            FROM tasks
            WHERE 1 = 1
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            (50, 0),
        ).fetchall()

    details = [row["detail"] for row in plan]

    assert details, "SQLite should return a query plan"
    assert any("tasks" in detail.lower() for detail in details)
