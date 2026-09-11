from types import SimpleNamespace
from typing import cast
from unittest.mock import Mock

from openai import OpenAI

from app.openai_client import OpenAIClient
from app.settings import Settings


def test_openai_client_returns_the_sdk_output_text() -> None:
    responses = Mock()
    responses.create.return_value = SimpleNamespace(output_text="Research brief")
    sdk_client = cast(OpenAI, SimpleNamespace(responses=responses))
    settings = Settings("test-key", "test-model", 15.0, 1, 500)

    client = OpenAIClient(settings, client=sdk_client)

    assert client.get_response("Be concise.", "What is Bitcoin?") == "Research brief"
    responses.create.assert_called_once_with(
        model="test-model",
        instructions="Be concise.",
        input="What is Bitcoin?",
        max_output_tokens=500,
    )