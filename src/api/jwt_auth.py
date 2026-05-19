from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta

import jwt
from fastapi import HTTPException

JWT_SECRET_ENV = "INSTITUTIONAL_JWT_SECRET"
JWT_ALGORITHM = "HS256"


def create_access_token(subject: str, expires_minutes: int = 60) -> str:
    secret = os.getenv(JWT_SECRET_ENV, "development-secret")

    payload = {
        "sub": subject,
        "exp": datetime.now(UTC) + timedelta(minutes=expires_minutes),
    }

    return jwt.encode(payload, secret, algorithm=JWT_ALGORITHM)


def validate_access_token(token: str) -> dict:
    secret = os.getenv(JWT_SECRET_ENV, "development-secret")

    try:
        return jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=401, detail="Invalid JWT token") from exc
