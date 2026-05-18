from __future__ import annotations

from datetime import datetime, UTC

from src.storage.sqlite_store import SQLiteStore


class TelemetryTracker:
    def __init__(self, store: SQLiteStore | None = None) -> None:
        self.store = store or SQLiteStore()

    def track_metric(
        self,
        metric: str,
        value: float,
        payload: dict | None = None,
    ) -> None:
        self.store.insert_telemetry(
            metric=metric,
            value=value,
            created_at=datetime.now(UTC).isoformat(),
            payload=payload,
        )
