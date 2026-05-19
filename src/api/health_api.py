from __future__ import annotations

from src.observability.healthcheck import build_healthcheck
from src.observability.runtime_status import runtime_status


def health_response() -> dict:
    return {
        "runtime": runtime_status(),
        "healthcheck": build_healthcheck(),
    }
