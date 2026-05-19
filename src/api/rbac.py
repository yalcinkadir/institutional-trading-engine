from __future__ import annotations

from dataclasses import dataclass

from fastapi import HTTPException


@dataclass(frozen=True)
class Role:
    name: str


ADMIN = Role(name="admin")
ANALYST = Role(name="analyst")
VIEWER = Role(name="viewer")


ROLE_PERMISSIONS = {
    "admin": {"metrics", "reports", "admin"},
    "analyst": {"metrics", "reports"},
    "viewer": {"reports"},
}


def validate_permission(role: str, permission: str) -> None:
    permissions = ROLE_PERMISSIONS.get(role, set())

    if permission not in permissions:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
