from fastapi.testclient import TestClient

from src.api.app import app
from src.api.jwt_auth import JWT_SECRET_ENV, create_access_token


client = TestClient(app)


def test_metrics_requires_jwt_token():
    response = client.get("/metrics")

    assert response.status_code == 401


def test_metrics_accepts_admin_token(monkeypatch):
    monkeypatch.setenv(JWT_SECRET_ENV, "unit-test-jwt-key")
    token = create_access_token(
        "admin-user",
        role="admin",
    )

    response = client.get(
        "/metrics",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200


def test_viewer_cannot_access_metrics(monkeypatch):
    monkeypatch.setenv(JWT_SECRET_ENV, "unit-test-jwt-key")
    token = create_access_token(
        "viewer-user",
        role="viewer",
    )

    response = client.get(
        "/metrics",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403


def test_metrics_rejects_malformed_authorization_header():
    response = client.get(
        "/metrics",
        headers={
            "Authorization": "Token not-a-bearer-token",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authorization format"


def test_metrics_rejects_empty_bearer_token():
    response = client.get(
        "/metrics",
        headers={
            "Authorization": "Bearer    ",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Missing bearer token"


def test_metrics_fails_closed_when_jwt_secret_is_not_configured(monkeypatch):
    monkeypatch.delenv(JWT_SECRET_ENV, raising=False)

    response = client.get(
        "/metrics",
        headers={
            "Authorization": "Bearer x.y.z",
        },
    )

    assert response.status_code == 503
    assert response.json()["detail"] == "JWT authentication is not configured"
