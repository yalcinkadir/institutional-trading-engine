from datetime import UTC, datetime, timedelta

import jwt
import pytest
from fastapi import HTTPException

from src.api.jwt_auth import (
    JWT_ALGORITHM,
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


def test_jwt_auth_fails_closed_with_blank_configured_secret(monkeypatch):
    monkeypatch.setenv(JWT_SECRET_ENV, "   ")

    with pytest.raises(JWTSecretNotConfiguredError):
        create_access_token("institutional-user")

    with pytest.raises(JWTSecretNotConfiguredError):
        validate_access_token("x.y.z")


def test_validate_access_token_rejects_token_signed_with_wrong_secret(monkeypatch):
    monkeypatch.setenv(JWT_SECRET_ENV, "correct-unit-test-jwt-key")
    forged_token = jwt.encode(
        {
            "sub": "institutional-user",
            "role": "admin",
            "exp": datetime.now(UTC) + timedelta(minutes=60),
        },
        "wrong-unit-test-jwt-key",
        algorithm=JWT_ALGORITHM,
    )

    with pytest.raises(HTTPException) as exc_info:
        validate_access_token(forged_token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid JWT token"


def test_validate_access_token_rejects_expired_token(monkeypatch):
    monkeypatch.setenv(JWT_SECRET_ENV, "unit-test-jwt-key")
    expired_token = jwt.encode(
        {
            "sub": "institutional-user",
            "role": "admin",
            "exp": datetime.now(UTC) - timedelta(minutes=1),
        },
        "unit-test-jwt-key",
        algorithm=JWT_ALGORITHM,
    )

    with pytest.raises(HTTPException) as exc_info:
        validate_access_token(expired_token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid JWT token"


def test_validate_access_token_rejects_invalid_role(monkeypatch):
    monkeypatch.setenv(JWT_SECRET_ENV, "unit-test-jwt-key")
    token = jwt.encode(
        {
            "sub": "institutional-user",
            "role": "superuser",
            "exp": datetime.now(UTC) + timedelta(minutes=60),
        },
        "unit-test-jwt-key",
        algorithm=JWT_ALGORITHM,
    )

    with pytest.raises(HTTPException) as exc_info:
        validate_access_token(token)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Invalid role"
