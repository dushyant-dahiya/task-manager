from datetime import date
from pathlib import Path

from task_manager import database
from task_manager.models import Priority, Task


def test_initialize_database_creates_table(tmp_path: Path) -> None:
    database.DB_PATH = tmp_path / "test_task.db"
    database.initialize_database()
    assert database.DB_PATH.exists()
    database.DB_PATH = Path("tasks.db")


def test_add_tasks_saves_and_returns_tasks_with_id(tmp_path: Path) -> None:
    database.DB_PATH = tmp_path / "test_task.db"
    database.initialize_database()
    new_task = Task(
        title="do homework", priority=Priority.HIGH, due_date=date(2026, 9, 29), done=False
    )
    saved_task = database.add_task(new_task)
    assert saved_task.id is not None
    assert saved_task.title == "do homework"
    assert saved_task.priority == Priority.HIGH
    assert saved_task.done is False
    database.DB_PATH = Path("tasks.db")
