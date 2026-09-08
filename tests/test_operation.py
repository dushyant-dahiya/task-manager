from datetime import date

import pytest

from task_manager import database, operations
from task_manager.models import Priority, Task


def test_add_task_with_validation(test_db: None) -> None:
    bad_task = Task(title="", priority=Priority.HIGH, due_date=date(2026, 9, 25), done=False)

    with pytest.raises(ValueError):
        operations.add_task_with_validation(bad_task)


def test_complete_task_marks_it_done(test_db: None) -> None:
    task = Task(title="do homework", priority=Priority.HIGH, due_date=date(2026, 9, 20), done=False)
    saved_task = database.add_task(task)
    assert saved_task.id is not None

    result = database.complete_task(saved_task.id)

    assert result is True
    all_tasks = database.get_all_tasks()
    assert all_tasks[0].done is True


def test_complete_task_returns_false_when_id_does_not_exist(test_db: None) -> None:
    result = database.complete_task(999)

    assert result is False
