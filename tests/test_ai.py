from datetime import date
from unittest.mock import MagicMock, patch

import pytest
from anthropic.types import TextBlock

from task_manager import ai
from task_manager.models import Priority


def test_parse_task_text_returns_valid_task() -> None:
    fake_response = MagicMock()
    fake_response.content = [
        MagicMock(
            spec=TextBlock,
            text='{"title": "call dentist", "priority": "high", "due_date": "2026-09-11"}',
        )
    ]

    with patch("task_manager.ai.anthropic.Anthropic") as mock_anthropic_class:
        mock_anthropic_class.return_value.messages.create.return_value = fake_response

        result = ai.parse_task_text("call the dentist tomorrow, high priority")
    assert result.title == "call dentist"
    assert result.priority == Priority.HIGH.value
    assert result.due_date == date(2026, 9, 11)


def test_parse_task_text_raises_value_error_on_invalid_json() -> None:
    fake_response = MagicMock()
    fake_response.content = [MagicMock(spec=TextBlock, text='{"this is not a valid JSOn"}')]

    with patch("task_manager.ai.anthropic.Anthropic") as mock_anthropic_class:
        mock_anthropic_class.return_value.messages.create.return_value = fake_response

        with pytest.raises(ValueError):
            ai.parse_task_text("this is not JSON")


def test_parse_task_text_raises_value_error_on_invalid_json_format() -> None:
    fake_response = MagicMock()
    fake_response.content = [MagicMock(spec=TextBlock, text='{"title": "call dentist"}')]

    with patch("task_manager.ai.anthropic.Anthropic") as mock_anthropic_class:
        mock_anthropic_class.return_value.messages.create.return_value = fake_response

        with pytest.raises(ValueError):
            ai.parse_task_text("this is not JSON")
