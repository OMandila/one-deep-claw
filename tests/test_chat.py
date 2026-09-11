from fastapi.testclient import TestClient
from openai import OpenAIError

from app.main import RESEARCH_BRIEF_INSTRUCTIONS, app, get_openai_client
from app.settings import ConfigurationError


class StubOpenAIClient:
    def __init__(self, response: str | None = "Research brief") -> None:
        self.response = response
        self.instructions: str | None = None
        self.message: str | None = None

    def get_response(self, instructions: str, user_message: str) -> str:
        self.instructions = instructions
        self.message = user_message
        if self.response is None:
            raise OpenAIError("OpenAI is unavailable")
        return self.response


def test_chat_returns_a_research_brief() -> None:
    stub_client = StubOpenAIClient()
    app.dependency_overrides[get_openai_client] = lambda: stub_client

    try:
        response = TestClient(app).post("/chat", json={"message": "What is Bitcoin?"})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"response": "Research brief"}
    assert stub_client.message == "What is Bitcoin?"
    assert stub_client.instructions == RESEARCH_BRIEF_INSTRUCTIONS


def test_chat_rejects_an_empty_message() -> None:
    response = TestClient(app).post("/chat", json={"message": ""})

    assert response.status_code == 422


def test_chat_returns_a_helpful_provider_error() -> None:
    app.dependency_overrides[get_openai_client] = lambda: StubOpenAIClient(response=None)

    try:
        response = TestClient(app).post("/chat", json={"message": "What is Bitcoin?"})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 502
    assert response.json() == {
        "detail": "The research service is temporarily unavailable. Please try again."
    }


def test_chat_returns_a_helpful_configuration_error() -> None:
    def unavailable_client() -> StubOpenAIClient:
        raise ConfigurationError("OPENAI_API_KEY is not configured")

    app.dependency_overrides[get_openai_client] = unavailable_client

    try:
        response = TestClient(app).post("/chat", json={"message": "What is Bitcoin?"})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json() == {"detail": "The research service is not configured yet."}