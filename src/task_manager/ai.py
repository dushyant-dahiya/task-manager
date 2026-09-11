import json
from datetime import date

import anthropic
from anthropic.types import TextBlock
from pydantic import BaseModel, ValidationError

from task_manager.config import settings


class ParsedTask(BaseModel):
    title: str
    priority: str
    due_date: date


EXTRACTION_PROMPT = """Extract the task details from the following text and respond with ONLY a 
JSON object, no other text, no markdown formatting, no code blocks.

The JSON must have exactly these fields:
- title: a string (a short description what the task is)
- priority: a short string (high, medium, low)
- due_date: a date in YYYY-MM-DD format (e.g. 2026-09-15)

today_date: {today_date}
Text: {text}

Respond with only the JSON object."""


def parse_task_text(text: str) -> ParsedTask:
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": EXTRACTION_PROMPT.format(today_date=date.today(), text=text),
            }
        ],
    )
    first_block = response.content[0]
    if not isinstance(first_block, TextBlock):
        raise ValueError("Expected a text response from Claude")
    try:
        data = json.loads(first_block.text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Claude did not return valid JSON: {e}") from e
    try:
        return ParsedTask(**data)
    except ValidationError as e:
        raise ValueError(f"Claude's response didn't match the expected format: {e}") from e
