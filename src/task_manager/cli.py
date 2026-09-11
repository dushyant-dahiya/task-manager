import argparse
from datetime import date

from task_manager import ai, database, operations
from task_manager.models import Priority, Task


def main() -> None:
    database.initialize_database()
    parser = argparse.ArgumentParser(description="Tasks Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("--title", type=str, required=True)
    add_parser.add_argument("--priority", type=str, required=True)
    add_parser.add_argument("--due_date", type=str, required=True)

    subparsers.add_parser("list", help="List all tasks")
    complete_parser = subparsers.add_parser("complete", help="Mark a task complete")
    complete_parser.add_argument("--id", type=int, required=True)

    edit_parser = subparsers.add_parser("edit", help="Edit a task")
    edit_parser.add_argument("--id", type=int, required=True)
    edit_parser.add_argument("--title", type=str)
    edit_parser.add_argument("--priority", type=str)
    edit_parser.add_argument("--due_date", type=str)

    add_n1_parser = subparsers.add_parser("add-nl", help="Add a task using natural language")
    add_n1_parser.add_argument("text", type=str)

    args = parser.parse_args()

    if args.command == "add":
        try:
            task = Task(
                title=args.title,
                priority=Priority(args.priority),
                due_date=date.fromisoformat(args.due_date),
                done=False,
            )
            saved = operations.add_task_with_validation(task)
            print(
                f"Added task: {saved.title} and  {saved.priority.value} "
                f" and {saved.due_date} and {saved.done} with (id={saved.id})"
            )
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "list":
        all_tasks = operations.get_all_tasks_sorted()
        if not all_tasks:
            print("No tasks added yet")
        else:
            for task in all_tasks:
                status = "[x]" if task.done else "[]"
                print(
                    f"ID: {task.id} Title: {task.title} Priority:  {task.priority.value}"
                    f"   Due Date: {task.due_date} Status {status} "
                )
    elif args.command == "complete":
        task_updated = operations.complete_task(args.id)
        if task_updated:
            print(f"Updated task with id {args.id}")
        else:
            print(f"No task found with id {args.id}")

    elif args.command == "edit":
        try:
            updated = operations.edit_task_with_validation(
                args.id,
                args.title,
                Priority(args.priority),
                date.fromisoformat(args.due_date),
            )
            if updated:
                print(f"Updated task with id {args.id}")
            else:
                print(f"No task found with id {args.id}")
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "add-nl":
        try:
            parsed = ai.parse_task_text(args.text)
            task = Task(
                title=parsed.title,
                priority=Priority(parsed.priority),
                due_date=parsed.due_date,
                done=False,
            )
            saved_task = operations.add_task_with_validation(task)
            print(
                f"Added Task: Id: {saved_task.id} Title: {saved_task.title} "
                f"Priority: {saved_task.priority} Due Date: {saved_task.due_date} "
                f"Status : {saved_task.done}"
            )
        except ValueError as e:
            print(f"Error: {e}")
