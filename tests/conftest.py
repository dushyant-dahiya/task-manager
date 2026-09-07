from collections.abc import Iterator
from pathlib import Path

import pytest

from task_manager import database


@pytest.fixture
def test_db(tmp_path: Path) -> Iterator[None]:
    database.DB_PATH = tmp_path / "test_tasks.db"
    database.initialize_database()
    yield
    database.DB_PATH = Path("tasks.db")
