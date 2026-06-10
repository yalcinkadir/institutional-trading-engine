from __future__ import annotations

import os

from fastapi import Header, HTTPException

from src.api.jwt_auth import JWTSecretNotConfiguredError, validate_access_token
from src.api.rbac import validate_permission


def require_permission(permission: str):
    def dependency(
        authorization: str | None = Header(default=None),
        x_api_key: str | None = Header(default=None),
    ) -> dict:
        expected_api_key = os.getenv("INSTITUTIONAL_API_KEY")
        if expected_api_key and x_api_key == expected_api_key:
            return {
                "sub": "api-key-client",
                "role": "admin",
                "auth_method": "api_key",
            }

        if not authorization:
            raise HTTPException(status_code=401, detail="Missing authorization header")

        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization format")

        token = authorization.removeprefix("Bearer ").strip()
        if not token:
            raise HTTPException(status_code=401, detail="Missing bearer token")

        try:
            payload = validate_access_token(token)
        except JWTSecretNotConfiguredError as exc:
            raise HTTPException(
                status_code=503,
                detail="JWT authentication is not configured",
            ) from exc

        role = payload.get("role", "viewer")

        validate_permission(role, permission)

        return payload

    return dependency
