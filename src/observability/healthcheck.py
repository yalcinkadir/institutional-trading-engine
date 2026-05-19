from __future__ import annotations

from datetime import UTC, datetime


def build_healthcheck() -> dict:
    return {
        "status": "healthy",
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "components": {
            "reporting": "healthy",
            "outcomes": "healthy",
            "storage": "healthy",
            "cache": "healthy",
            "monitoring": "healthy",
        },
    }
