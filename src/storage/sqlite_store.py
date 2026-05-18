from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

DEFAULT_DB_PATH = Path("data/institutional_engine.db")


class SQLiteStore:
    def __init__(self, db_path: str | Path = DEFAULT_DB_PATH) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_schema(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_type TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    path TEXT NOT NULL,
                    quality_score REAL,
                    payload TEXT
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS signals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    signal_type TEXT NOT NULL,
                    score REAL NOT NULL,
                    payload TEXT
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS telemetry (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric TEXT NOT NULL,
                    value REAL NOT NULL,
                    created_at TEXT NOT NULL,
                    payload TEXT
                )
                """
            )

    def insert_report(
        self,
        report_type: str,
        created_at: str,
        path: str,
        quality_score: float | None = None,
        payload: dict[str, Any] | None = None,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO reports (report_type, created_at, path, quality_score, payload)
                VALUES (?, ?, ?, ?, ?)
                """,
                (report_type, created_at, path, quality_score, json.dumps(payload or {})),
            )

    def insert_signal(
        self,
        ticker: str,
        created_at: str,
        signal_type: str,
        score: float,
        payload: dict[str, Any] | None = None,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO signals (ticker, created_at, signal_type, score, payload)
                VALUES (?, ?, ?, ?, ?)
                """,
                (ticker, created_at, signal_type, score, json.dumps(payload or {})),
            )

    def insert_telemetry(
        self,
        metric: str,
        value: float,
        created_at: str,
        payload: dict[str, Any] | None = None,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO telemetry (metric, value, created_at, payload)
                VALUES (?, ?, ?, ?)
                """,
                (metric, value, created_at, json.dumps(payload or {})),
            )
