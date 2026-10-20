
import sqlite3

from app.database import get_connection, init_db


def test_init_db_creates_tasks_table(test_database):
    connection = get_connection()

    try:
        result = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = 'tasks'
            """
        ).fetchone()

        assert result is not None
        assert result["name"] == "tasks"
    finally:
        connection.close()


def test_init_db_is_idempotent(test_database):
    init_db()
    init_db()

    connection = get_connection()

    try:
        result = connection.execute(
            "SELECT COUNT(*) AS count FROM tasks"
        ).fetchone()

        assert result["count"] == 0
    finally:
        connection.close()
