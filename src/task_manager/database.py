import sqlite3
from datetime import date
from pathlib import Path

from task_manager.models import Priority, Task

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
            title TEXT NOT NULL,
            priority TEXT NOT NULL,
            due_date TEXT NOT NULL,
            done INTEGER NOT NULL
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


def get_all_tasks() -> list[Task]:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id,title,priority,due_date,done from tasks")
    rows = cursor.fetchall()
    connection.close()

    tasks = []
    for row in rows:
        task = Task(
            id=row[0],
            title=row[1],
            priority=Priority(row[2]),
            due_date=date.fromisoformat(row[3]),
            done=bool(row[4]),
        )
        tasks.append(task)
    return tasks


def delete_task(task_id: int) -> bool:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE from tasks where id = ?", (task_id,))
    connection.commit()
    row_deleted = cursor.rowcount
    connection.close()
    return row_deleted > 0


def complete_task(task_id: int) -> bool:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE tasks 
        SET done = ?
        WHERE id = ?
        """,
        (True, task_id),
    )
    connection.commit()
    updated_row = cursor.rowcount
    connection.close()
    return updated_row > 0


def edit_task(task_id: int, title: str, priority: Priority, due_date: date) -> bool:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE tasks SET title = ?, priority = ?, due_date = ? WHERE id = ?",
        (title, priority.value, due_date.isoformat(), task_id),
    )
    connection.commit()
    rows_updated = cursor.rowcount
    connection.close()
    return rows_updated > 0
