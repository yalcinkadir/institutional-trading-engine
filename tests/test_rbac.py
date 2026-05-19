from fastapi import HTTPException

from src.api.rbac import validate_permission


def test_admin_has_metrics_access():
    validate_permission("admin", "metrics")


def test_viewer_cannot_access_metrics():
    blocked = False

    try:
        validate_permission("viewer", "metrics")
    except HTTPException as exc:
        blocked = exc.status_code == 403

    assert blocked is True
