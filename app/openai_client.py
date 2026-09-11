from openai import OpenAI

from app.settings import Settings


class OpenAIClient:
    def __init__(self, settings: Settings, client: OpenAI | None = None) -> None:
        self._model = settings.openai_model
        self._client = client or OpenAI(
            api_key=settings.openai_api_key,
            timeout=settings.openai_timeout_seconds,
        )

    def get_response(self, instructions: str, user_message: str) -> str:
        response = self._client.responses.create(
            model=self._model,
            instructions=instructions,
            input=user_message,
        )
        return response.output_text