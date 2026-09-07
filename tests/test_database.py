from datetime import date

from task_manager import database
from task_manager.models import Priority, Task


def test_initialize_database_creates_table(test_db: None) -> None:

    assert database.DB_PATH.exists()


def test_add_tasks_saves_and_returns_tasks_with_id(test_db: None) -> None:
    new_task = Task(
        title="do homework", priority=Priority.HIGH, due_date=date(2026, 9, 29), done=False
    )
    saved_task = database.add_task(new_task)
    assert saved_task.id is not None
    assert saved_task.title == "do homework"
    assert saved_task.priority == Priority.HIGH
    assert saved_task.done is False


def test_get_all_tasks_returns_all_saved_tasks(test_db: None) -> None:
    task1 = Task(title="do homework", priority=Priority.HIGH, due_date=date(2026, 9, 11), done=True)

    task2 = Task(
        title="do cleaning", priority=Priority.MEDIUM, due_date=date(2026, 9, 15), done=False
    )

    database.add_task(task1)
    database.add_task(task2)

    all_tasks = database.get_all_tasks()

    assert len(all_tasks) == 2
    assert all_tasks[0].title == "do homework"
    assert all_tasks[1].title == "do cleaning"
    assert all_tasks[0].priority == Priority.HIGH
    assert all_tasks[1].priority == Priority.MEDIUM
    assert all_tasks[0].done is True
    assert all_tasks[1].done is False


def test_delete_task_removes_task_from_database(test_db: None) -> None:
    add_task = Task(
        title="do homework", priority=Priority.HIGH, due_date=date(2026, 9, 20), done=False
    )
    saved_task = database.add_task(add_task)
    assert saved_task.id is not None
    deleted_task = database.delete_task(saved_task.id)
    remaining_tasks = database.get_all_tasks()
    assert remaining_tasks == []
    assert deleted_task is True


def test_delete_task_returns_false_when_id_does_not_exist(test_db: None) -> None:

    false_id = database.delete_task(999)
    assert false_id is False
