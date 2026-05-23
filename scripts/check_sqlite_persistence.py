#!/usr/bin/env python3
"""Smoke-check optional SQLite runtime persistence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.operations.sqlite_persistence import (  # noqa: E402
    RuntimeRecord,
    SQLitePersistenceError,
    append_record,
    connect,
    count_records,
    fetch_records,
    initialize_schema,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check SQLite runtime persistence")
    parser.add_argument("--db", default="data/runtime/runtime.sqlite", help="SQLite database path")
    parser.add_argument(
        "--write-smoke-record",
        action="store_true",
        help="Append a small smoke-check record after initializing the schema",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    db_path = Path(args.db)

    try:
        with connect(db_path) as connection:
            initialize_schema(connection)
            inserted_id = None
            if args.write_smoke_record:
                inserted_id = append_record(
                    connection,
                    RuntimeRecord(
                        record_type="sqlite_persistence_smoke_check",
                        record_id="sqlite-persistence-smoke-check",
                        source="check_sqlite_persistence",
                        payload={"status": "ok"},
                    ),
                )
            total = count_records(connection)
            recent = fetch_records(connection, limit=5)
    except SQLitePersistenceError as exc:
        print(f"SQLite persistence check failed: {exc}", file=sys.stderr)
        return 2

    result = {
        "status": "PASS",
        "db_path": str(db_path),
        "inserted_id": inserted_id,
        "record_count": total,
        "recent_record_types": [record.record_type for record in recent],
    }

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"SQLite persistence check: {result['status']}")
        print(f"Database: {result['db_path']}")
        print(f"Record count: {result['record_count']}")
        if inserted_id is not None:
            print(f"Inserted smoke record id: {inserted_id}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
