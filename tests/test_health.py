from fastapi.testclient import TestClient

from app.main import app


def test_health_check_returns_ok() -> None:
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_index_serves_the_research_interface() -> None:
    response = TestClient(app).get("/")

    assert response.status_code == 200
    assert "One Deep Claw" in response.text
    assert 'id="chat-form"' in response.text