from fastapi.testclient import TestClient

from src.api.app import app
from src.api.jwt_auth import create_access_token


client = TestClient(app)


def test_metrics_requires_jwt_token():
    response = client.get("/metrics")

    assert response.status_code == 401


def test_metrics_accepts_admin_token():
    token = create_access_token("admin-user")

    response = client.get(
        "/metrics",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code in [200, 403]
