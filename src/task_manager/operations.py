from datetime import date

from task_manager import database
from task_manager.models import Priority, Task


def validate_task_fields(title: str, due_date: date) -> None:
    if not title.strip():
        raise ValueError("Title cannot be empty")
    if due_date < date.today():
        raise ValueError("Due date cannot be in the past")
    if len(title) > 200:
        raise ValueError("Title is too long")


def add_task_with_validation(task: Task) -> Task:
    validate_task_fields(task.title, task.due_date)
    return database.add_task(task)


def get_all_tasks_sorted() -> list[Task]:
    all_tasks = database.get_all_tasks()
    return sorted(all_tasks, key=lambda task: task.due_date)


def complete_task(task_id: int) -> bool:
    task_update = database.complete_task(task_id)
    return task_update


def edit_task_with_validation(task_id: int, title: str, priority: Priority, due_date: date) -> bool:
    validate_task_fields(title, due_date)
    return database.edit_task(task_id, title, priority, due_date)
