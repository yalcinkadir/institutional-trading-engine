"""Optional SQLite persistence for runtime records.

P34 introduces a small, dependency-free SQLite sink for durable runtime records.
It is intentionally optional: existing JSON/JSONL files remain valid fallbacks.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = 1


class SQLitePersistenceError(RuntimeError):
    """Raised when SQLite persistence cannot safely process a record."""


@dataclass(frozen=True)
class RuntimeRecord:
    record_type: str
    payload: dict[str, Any]
    record_id: str | None = None
    created_at: str | None = None
    source: str = "runtime"


@dataclass(frozen=True)
class StoredRuntimeRecord:
    id: int
    record_id: str | None
    record_type: str
    source: str
    created_at: str
    payload: dict[str, Any]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _validate_record(record: RuntimeRecord) -> None:
    if not record.record_type or not record.record_type.strip():
        raise SQLitePersistenceError("record_type is required")
    if not isinstance(record.payload, dict):
        raise SQLitePersistenceError("payload must be a dictionary")
    try:
        json.dumps(record.payload, sort_keys=True)
    except TypeError as exc:
        raise SQLitePersistenceError(f"payload is not JSON serializable: {exc}") from exc


def connect(db_path: Path | str) -> sqlite3.Connection:
    path = Path(db_path)
    _ensure_parent(path)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_schema(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS runtime_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_id TEXT,
            record_type TEXT NOT NULL,
            source TEXT NOT NULL,
            created_at TEXT NOT NULL,
            payload_json TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_runtime_records_type_created
        ON runtime_records(record_type, created_at)
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_runtime_records_record_id
        ON runtime_records(record_id)
        """
    )
    connection.execute(
        """
        INSERT OR REPLACE INTO schema_metadata(key, value)
        VALUES ('schema_version', ?)
        """,
        (str(SCHEMA_VERSION),),
    )
    connection.commit()


def append_record(connection: sqlite3.Connection, record: RuntimeRecord) -> int:
    _validate_record(record)
    created_at = record.created_at or utc_now_iso()
    payload_json = json.dumps(record.payload, sort_keys=True, separators=(",", ":"))
    cursor = connection.execute(
        """
        INSERT INTO runtime_records(record_id, record_type, source, created_at, payload_json)
        VALUES (?, ?, ?, ?, ?)
        """,
        (record.record_id, record.record_type, record.source, created_at, payload_json),
    )
    connection.commit()
    return int(cursor.lastrowid)


def append_records(connection: sqlite3.Connection, records: Iterable[RuntimeRecord]) -> list[int]:
    ids: list[int] = []
    for record in records:
        ids.append(append_record(connection, record))
    return ids


def _row_to_record(row: sqlite3.Row) -> StoredRuntimeRecord:
    return StoredRuntimeRecord(
        id=int(row["id"]),
        record_id=row["record_id"],
        record_type=row["record_type"],
        source=row["source"],
        created_at=row["created_at"],
        payload=json.loads(row["payload_json"]),
    )


def fetch_records(
    connection: sqlite3.Connection,
    *,
    record_type: str | None = None,
    limit: int = 100,
) -> list[StoredRuntimeRecord]:
    if limit <= 0:
        raise SQLitePersistenceError("limit must be positive")

    if record_type:
        rows = connection.execute(
            """
            SELECT id, record_id, record_type, source, created_at, payload_json
            FROM runtime_records
            WHERE record_type = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (record_type, limit),
        ).fetchall()
    else:
        rows = connection.execute(
            """
            SELECT id, record_id, record_type, source, created_at, payload_json
            FROM runtime_records
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [_row_to_record(row) for row in rows]


def count_records(connection: sqlite3.Connection, *, record_type: str | None = None) -> int:
    if record_type:
        row = connection.execute(
            "SELECT COUNT(*) AS count FROM runtime_records WHERE record_type = ?",
            (record_type,),
        ).fetchone()
    else:
        row = connection.execute("SELECT COUNT(*) AS count FROM runtime_records").fetchone()
    return int(row["count"])


def initialize_database(db_path: Path | str) -> Path:
    path = Path(db_path)
    with connect(path) as connection:
        initialize_schema(connection)
    return path
