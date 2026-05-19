from __future__ import annotations

import sqlite3
from pathlib import Path


DB_PATH = Path("data/runtime.db")


class SQLiteRuntimeStore:
    def __init__(self) -> None:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(DB_PATH)
        self._initialize()

    def _initialize(self) -> None:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS runtime_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        self.connection.commit()

    def insert_event(
        self,
        event_type: str,
        payload: str,
        created_at: str,
    ) -> None:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO runtime_events (
                event_type,
                payload,
                created_at
            ) VALUES (?, ?, ?)
            """,
            (event_type, payload, created_at),
        )

        self.connection.commit()

    def count_events(self) -> int:
        cursor = self.connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM runtime_events")

        result = cursor.fetchone()

        return int(result[0]) if result else 0
