from __future__ import annotations

import json
from pathlib import Path

from src.operations.daily_observation_record_index import (
    build_daily_observation_record_index,
    write_daily_observation_record_index,
)
from src.operations.daily_observation_record_writer import build_daily_observation_record


def _record(day: str, **kwargs: object) -> dict[str, object]:
    return build_daily_observation_record(
        observation_date=day,
        created_at=f"{day}T00:00:00Z",
        **kwargs,
    )


def test_po7_builds_sorted_index_with_status_counts() -> None:
    records = [
        _record("2026-06-03", incidents=["review needed"]),
        _record("2026-06-01"),
        _record("2026-06-02", missing_evidence=["daily report"]),
    ]

    result = build_daily_observation_record_index(records)

    assert result.valid is True
    assert result.errors == ()
    assert result.index["record_root"] == "reports/daily_observation_records"
    assert result.index["index_path"] == "reports/daily_observation_records/index.json"
    assert result.index["total_records"] == 3
    assert result.index["status_counts"] == {
        "ACCEPTED": 1,
        "REJECTED": 1,
        "NEEDS_REVIEW": 1,
    }
    assert [entry["date"] for entry in result.index["records"]] == [
        "2026-06-01",
        "2026-06-02",
        "2026-06-03",
    ]


def test_po7_index_entries_include_canonical_paths_and_paper_only_boundary() -> None:
    result = build_daily_observation_record_index([_record("2026-06-01")])

    entry = result.index["records"][0]
    assert entry["path"] == "reports/daily_observation_records/2026-06-01.json"
    assert entry["live_trading_authorized"] is False
    assert entry["broker_execution_mode"] == "paper_only"
    assert result.index["live_trading_authorized"] is False
    assert result.index["broker_execution_mode"] == "paper_only"


def test_po7_rejects_duplicate_record_dates() -> None:
    result = build_daily_observation_record_index([
        _record("2026-06-01"),
        _record("2026-06-01"),
    ])

    assert result.valid is False
    assert "duplicate_record_date:2026-06-01" in result.errors


def test_po7_rejects_invalid_record() -> None:
    invalid = _record("2026-06-01")
    invalid["live_trading_authorized"] = True

    result = build_daily_observation_record_index([invalid])

    assert result.valid is False
    assert "record:2026-06-01:live_trading_must_remain_false" in result.errors


def test_po7_writes_index_json(tmp_path: Path, monkeypatch) -> None:
    output_path = tmp_path / "reports" / "daily_observation_records" / "index.json"

    import src.operations.daily_observation_record_index as index_module

    monkeypatch.setattr(index_module, "INDEX_PATH", output_path)

    result = write_daily_observation_record_index(records=[_record("2026-06-01")])

    assert result.valid is True
    written = json.loads(output_path.read_text(encoding="utf-8"))
    assert written["total_records"] == 1
    assert written["records"][0]["date"] == "2026-06-01"


def test_po7_does_not_write_invalid_index_path(tmp_path: Path) -> None:
    output_path = tmp_path / "wrong" / "index.json"

    result = write_daily_observation_record_index(
        records=[_record("2026-06-01")],
        output_path=output_path,
    )

    assert result.valid is False
    assert "index_path_must_be_canonical" in result.errors
    assert not output_path.exists()
