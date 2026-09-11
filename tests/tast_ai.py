from datetime import date
from unittest.mock import MagicMock, patch

from anthropic.types import TextBlock

from task_manager import ai
from task_manager.models import Priority


def test_parse_task_text_returns_valid_task() -> None:
    fake_response = MagicMock()
    fake_response.content = [
        MagicMock(
            spec=TextBlock,
            text='{"title": "call dentist", "priority": "high", "due_date": "2026-9-11"}',
        )
    ]

    with patch("task_manager.ai.anthropic.Anthropic") as mock_anthropic_class:
        mock_anthropic_class.return_value.messages.create.return_value = fake_response

        result = ai.parse_task_text("call the dentist tomorrow, high priority")
    assert result.title == "call dentist"
    assert result.priority == Priority.HIGH.value
    assert result.due_date == date(2026, 9, 11)
