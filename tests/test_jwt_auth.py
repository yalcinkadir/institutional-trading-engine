import pytest

from src.api.jwt_auth import (
    JWT_SECRET_ENV,
    JWTSecretNotConfiguredError,
    create_access_token,
    validate_access_token,
)


def test_create_and_validate_token(monkeypatch):
    monkeypatch.setenv(JWT_SECRET_ENV, "unit-test-jwt-key")

    encoded = create_access_token("institutional-user")

    payload = validate_access_token(encoded)

    assert payload["sub"] == "institutional-user"


def test_jwt_auth_fails_closed_without_configured_secret(monkeypatch):
    monkeypatch.delenv(JWT_SECRET_ENV, raising=False)

    with pytest.raises(JWTSecretNotConfiguredError):
        create_access_token("institutional-user")

    with pytest.raises(JWTSecretNotConfiguredError):
        validate_access_token("x.y.z")
