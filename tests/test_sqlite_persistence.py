from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from src.operations.sqlite_persistence import (
    RuntimeRecord,
    SQLitePersistenceError,
    append_record,
    append_records,
    connect,
    count_records,
    fetch_records,
    initialize_database,
    initialize_schema,
)


def test_initialize_database_creates_schema(tmp_path: Path) -> None:
    db_path = tmp_path / "runtime" / "runtime.sqlite"

    initialize_database(db_path)

    assert db_path.exists()
    with connect(db_path) as connection:
        row = connection.execute(
            "SELECT value FROM schema_metadata WHERE key = 'schema_version'"
        ).fetchone()
    assert row["value"] == "1"


def test_append_and_fetch_runtime_record(tmp_path: Path) -> None:
    db_path = tmp_path / "runtime.sqlite"

    with connect(db_path) as connection:
        initialize_schema(connection)
        record_id = append_record(
            connection,
            RuntimeRecord(
                record_type="decision_log",
                record_id="decision-1",
                source="unit_test",
                created_at="2026-05-23T12:00:00+00:00",
                payload={"symbol": "SPY", "action": "NO_TRADE"},
            ),
        )
        records = fetch_records(connection, record_type="decision_log")

    assert record_id == 1
    assert len(records) == 1
    assert records[0].record_id == "decision-1"
    assert records[0].record_type == "decision_log"
    assert records[0].source == "unit_test"
    assert records[0].payload == {"symbol": "SPY", "action": "NO_TRADE"}


def test_append_records_and_count_by_type(tmp_path: Path) -> None:
    db_path = tmp_path / "runtime.sqlite"

    with connect(db_path) as connection:
        initialize_schema(connection)
        ids = append_records(
            connection,
            [
                RuntimeRecord(record_type="decision_log", payload={"n": 1}),
                RuntimeRecord(record_type="lifecycle_event", payload={"n": 2}),
                RuntimeRecord(record_type="decision_log", payload={"n": 3}),
            ],
        )

        assert ids == [1, 2, 3]
        assert count_records(connection) == 3
        assert count_records(connection, record_type="decision_log") == 2
        assert count_records(connection, record_type="lifecycle_event") == 1


def test_fetch_records_respects_limit_and_order(tmp_path: Path) -> None:
    db_path = tmp_path / "runtime.sqlite"

    with connect(db_path) as connection:
        initialize_schema(connection)
        append_records(
            connection,
            [
                RuntimeRecord(record_type="event", record_id="one", payload={"n": 1}),
                RuntimeRecord(record_type="event", record_id="two", payload={"n": 2}),
                RuntimeRecord(record_type="event", record_id="three", payload={"n": 3}),
            ],
        )
        records = fetch_records(connection, record_type="event", limit=2)

    assert [record.record_id for record in records] == ["three", "two"]


def test_append_record_rejects_invalid_payload(tmp_path: Path) -> None:
    db_path = tmp_path / "runtime.sqlite"

    with connect(db_path) as connection:
        initialize_schema(connection)
        with pytest.raises(SQLitePersistenceError):
            append_record(
                connection,
                RuntimeRecord(record_type="bad", payload={"not_json": object()}),
            )


def test_append_record_requires_record_type(tmp_path: Path) -> None:
    db_path = tmp_path / "runtime.sqlite"

    with connect(db_path) as connection:
        initialize_schema(connection)
        with pytest.raises(SQLitePersistenceError):
            append_record(connection, RuntimeRecord(record_type="", payload={}))


def test_fetch_records_requires_positive_limit(tmp_path: Path) -> None:
    db_path = tmp_path / "runtime.sqlite"

    with connect(db_path) as connection:
        initialize_schema(connection)
        with pytest.raises(SQLitePersistenceError):
            fetch_records(connection, limit=0)


def test_sqlite_persistence_cli_smoke_check(tmp_path: Path) -> None:
    db_path = tmp_path / "runtime.sqlite"

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/check_sqlite_persistence.py",
            "--db",
            str(db_path),
            "--write-smoke-record",
            "--json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(completed.stdout)
    assert payload["status"] == "PASS"
    assert payload["record_count"] == 1
    assert payload["inserted_id"] == 1
    assert payload["recent_record_types"] == ["sqlite_persistence_smoke_check"]
