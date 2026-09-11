import os
from dataclasses import dataclass

from dotenv import load_dotenv


class ConfigurationError(ValueError):
    """Raised when required application configuration is unavailable."""


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    openai_model: str
    openai_timeout_seconds: float
    openai_max_retries: int
    openai_max_output_tokens: int


def get_settings() -> Settings:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ConfigurationError(
            "OPENAI_API_KEY is not configured. Add it to your local .env file."
        )

    return Settings(
        openai_api_key=api_key,
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        openai_timeout_seconds=float(os.getenv("OPENAI_TIMEOUT_SECONDS", "30")),
        openai_max_retries=int(os.getenv("OPENAI_MAX_RETRIES", "2")),
        openai_max_output_tokens=int(os.getenv("OPENAI_MAX_OUTPUT_TOKENS", "1200")),
    )