
from app.database import get_db


def _get_query_plan(connection, query, parameters=()):
    rows = connection.execute(
        f"EXPLAIN QUERY PLAN {query}",
        parameters,
    ).fetchall()
    return [row["detail"] for row in rows]


def test_unfiltered_task_list_query_plan(test_database):
    with get_db() as connection:
        details = _get_query_plan(
            connection,
            """
            SELECT *
            FROM tasks
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            (50, 0),
        )

    assert details
    assert any("tasks" in detail.lower() for detail in details)


def test_status_filtered_task_list_query_plan(test_database):
    with get_db() as connection:
        details = _get_query_plan(
            connection,
            """
            SELECT *
            FROM tasks
            WHERE status = ?
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            ("todo", 50, 0),
        )

    assert details
    assert any("tasks" in detail.lower() for detail in details)


def test_status_priority_task_list_uses_composite_index(test_database):
    with get_db() as connection:
        details = _get_query_plan(
            connection,
            """
            SELECT *
            FROM tasks
            WHERE status = ? AND priority = ?
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            ("todo", "high", 50, 0),
        )

    assert details
    assert any(
        "idx_tasks_status_priority_id" in detail
        for detail in details
    )
