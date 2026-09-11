import pytest

import app.settings as settings_module
from app.settings import ConfigurationError, get_settings


def test_get_settings_requires_an_openai_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(settings_module, "load_dotenv", lambda: False)

    with pytest.raises(ConfigurationError, match="OPENAI_API_KEY"):
        get_settings()


def test_get_settings_uses_environment_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "test-model")
    monkeypatch.setenv("OPENAI_TIMEOUT_SECONDS", "15")
    monkeypatch.setenv("OPENAI_MAX_RETRIES", "1")
    monkeypatch.setenv("OPENAI_MAX_OUTPUT_TOKENS", "500")

    settings = get_settings()

    assert settings.openai_api_key == "test-key"
    assert settings.openai_model == "test-model"
    assert settings.openai_timeout_seconds == 15.0
    assert settings.openai_max_retries == 1
    assert settings.openai_max_output_tokens == 500