
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


DATABASE_PATH = Path(
    os.getenv("TASKFLOW_DATABASE_PATH", "data/taskflow.db")
)


def get_connection() -> sqlite3.Connection:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


@contextmanager
def get_db() -> Iterator[sqlite3.Connection]:
    connection = get_connection()

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def init_db() -> None:
    with get_db() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL CHECK(length(title) >= 3),
                description TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'todo'
                    CHECK(status IN ('todo', 'in_progress', 'done')),
                priority TEXT NOT NULL DEFAULT 'medium'
                    CHECK(priority IN ('low', 'medium', 'high', 'critical')),
                assignee TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
