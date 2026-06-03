from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta

import jwt
from fastapi import HTTPException

JWT_SECRET_ENV = "INSTITUTIONAL_JWT_SECRET"
JWT_ALGORITHM = "HS256"
VALID_ROLES = {"admin", "analyst", "viewer"}


class JWTSecretNotConfiguredError(RuntimeError):
    """Raised when JWT auth is used without an explicit secret."""


def _get_jwt_secret() -> str:
    secret = os.getenv(JWT_SECRET_ENV)
    if secret is None or secret.strip() == "":
        raise JWTSecretNotConfiguredError(
            f"{JWT_SECRET_ENV} must be set. Refusing to use an insecure default JWT secret."
        )
    return secret


def create_access_token(
    subject: str,
    role: str = "viewer",
    expires_minutes: int = 60,
) -> str:
    if role not in VALID_ROLES:
        raise ValueError(f"Invalid role: {role}")

    secret = _get_jwt_secret()

    payload = {
        "sub": subject,
        "role": role,
        "exp": datetime.now(UTC) + timedelta(minutes=expires_minutes),
    }

    return jwt.encode(payload, secret, algorithm=JWT_ALGORITHM)


def validate_access_token(token: str) -> dict:
    secret = _get_jwt_secret()

    try:
        payload = jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=401, detail="Invalid JWT token") from exc

    role = payload.get("role", "viewer")
    if role not in VALID_ROLES:
        raise HTTPException(status_code=403, detail="Invalid role")

    return payload
