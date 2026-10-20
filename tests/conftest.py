
import pytest


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    from app import database

    test_db_path = tmp_path / "test_taskflow.db"

    monkeypatch.setattr(database, "DATABASE_PATH", test_db_path)
    database.init_db()

    yield test_db_path
