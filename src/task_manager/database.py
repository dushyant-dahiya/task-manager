import sqlite3
from pathlib import Path

from task_manager.models import Task

DB_PATH = Path("tasks.db")


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def initialize_database() -> None:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title NOT NULL,
            priority TEXT NOT NULL,
            due_date TEXT NOT NULL,
            done TEXT NOT NULL
            )

        """
    )
    connection.commit()
    connection.close()


def add_task(task: Task) -> Task:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
            INSERT INTO tasks (title,priority,due_date,done)
            VALUES(?,?,?,?)

        """,
        (task.title, task.priority.value, task.due_date.isoformat(), task.done),
    )

    connection.commit()
    new_id = cursor.lastrowid
    connection.close()
    return Task(
        title=task.title, priority=task.priority, due_date=task.due_date, done=task.done, id=new_id
    )
