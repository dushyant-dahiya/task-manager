from dataclasses import dataclass
from datetime import date
from enum import Enum


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    title: str
    priority: Priority
    due_date: date
    done: bool = False
    id: int | None = None
