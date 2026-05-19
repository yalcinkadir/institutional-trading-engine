import os

from fastapi.testclient import TestClient

from src.api.app import app


client = TestClient(app)


def test_metrics_requires_authentication():
    os.environ["INSTITUTIONAL_API_KEY"] = "secret"

    response = client.get("/metrics")

    assert response.status_code == 401


def test_metrics_accepts_valid_api_key():
    os.environ["INSTITUTIONAL_API_KEY"] = "secret"

    response = client.get(
        "/metrics",
        headers={"x-api-key": "secret"},
    )

    assert response.status_code == 200
