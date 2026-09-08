from datetime import date

from task_manager import database
from task_manager.models import Task


def add_task_with_validation(task: Task) -> Task:
    if not task.title.strip():
        raise ValueError("Title cannot be empty")
    if task.due_date < date.today():
        raise ValueError("Due date cannot be in the past")
    if len(task.title) > 200:
        raise ValueError("Title is too long")
    return database.add_task(task)


def get_all_tasks_sorted() -> list[Task]:
    all_tasks = database.get_all_tasks()
    return sorted(all_tasks, key=lambda task: task.due_date)


def complete_task(task_id: int) -> bool:
    task_update = database.complete_task(task_id)
    return task_update
