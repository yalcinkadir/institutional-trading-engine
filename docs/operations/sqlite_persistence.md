# SQLite Persistence Wiring

P34 adds optional SQLite persistence for runtime records.

The existing JSON and JSONL file-based behavior remains valid. SQLite is an additional durable sink for structured runtime records.

## Files

```text
src/operations/sqlite_persistence.py
scripts/check_sqlite_persistence.py
tests/test_sqlite_persistence.py
.github/workflows/sqlite-persistence.yml
```

## Database

Default local path:

```text
data/runtime/runtime.sqlite
```

## Tables

```text
schema_metadata
runtime_records
```

`runtime_records` stores:

```text
record_id
record_type
source
created_at
payload_json
```

## Python API

```python
from src.operations.sqlite_persistence import (
    RuntimeRecord,
    append_record,
    connect,
    fetch_records,
    initialize_schema,
)

with connect("data/runtime/runtime.sqlite") as connection:
    initialize_schema(connection)
    append_record(
        connection,
        RuntimeRecord(
            record_type="decision_log",
            record_id="decision-1",
            source="runtime",
            payload={"symbol": "SPY", "action": "NO_TRADE"},
        ),
    )
    recent = fetch_records(connection, record_type="decision_log", limit=10)
```

## CLI Smoke Check

```bash
python scripts/check_sqlite_persistence.py \
  --db data/runtime/runtime.sqlite \
  --write-smoke-record \
  --json
```

## Tests

```bash
pytest tests/test_sqlite_persistence.py
```

## GitHub Actions

```text
Actions → SQLite Persistence → Run workflow
```

Artifact:

```text
sqlite-persistence-artifacts
```

## Operational Notes

- SQLite persistence is optional.
- JSON and JSONL outputs remain usable.
- Payloads must be JSON serializable.
- Invalid records fail fast with `SQLitePersistenceError`.

## Boundaries

P34 does not add broker connectivity, order execution or trading authorization.
