from __future__ import annotations

from datetime import UTC, datetime

from src.storage.sqlite_store import SQLiteStore


class OutcomeTracker:
    def __init__(self, store: SQLiteStore | None = None) -> None:
        self.store = store or SQLiteStore()

    def track_signal(
        self,
        ticker: str,
        signal_type: str,
        score: float,
        payload: dict | None = None,
    ) -> None:
        self.store.insert_signal(
            ticker=ticker,
            created_at=datetime.now(UTC).isoformat(),
            signal_type=signal_type,
            score=score,
            payload=payload,
        )
