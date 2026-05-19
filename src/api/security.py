from __future__ import annotations

from fastapi import Header, HTTPException

from src.api.jwt_auth import validate_access_token
from src.api.rbac import validate_permission


def require_permission(permission: str):
    def dependency(authorization: str | None = Header(default=None)) -> dict:
        if not authorization:
            raise HTTPException(status_code=401, detail="Missing authorization header")

        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization format")

        token = authorization.replace("Bearer ", "")

        payload = validate_access_token(token)

        role = payload.get("role", "viewer")

        validate_permission(role, permission)

        return payload

    return dependency
