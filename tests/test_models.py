from datetime import date

from task_manager.models import Priority, Task


def test_task_saves_all_fields_correctly() -> None:
    task = Task(
        title="do homework",
        priority=Priority.HIGH,
        due_date=date(2026, 9, 25),
    )

    assert task.title == "do homework"
    assert task.priority == Priority.HIGH
    assert task.done is False
    assert task.due_date == date(2026, 9, 25)
    assert task.id is None
