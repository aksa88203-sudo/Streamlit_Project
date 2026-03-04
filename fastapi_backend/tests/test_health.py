import os

from fastapi.testclient import TestClient

os.environ["AUTO_CREATE_TABLES"] = "false"

from app.main import app  # noqa: E402


def test_health() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
