from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from src.operations.daily_observation_record_artifact_contract import (
    ALLOWED_RECORD_ROOT,
    build_daily_observation_record_path,
    validate_daily_observation_record_artifact,
)
from src.operations.daily_observation_record_validator import validate_daily_observation_record

INDEX_PATH = ALLOWED_RECORD_ROOT / "index.json"
VALID_INDEX_STATUSES = ("ACCEPTED", "REJECTED", "NEEDS_REVIEW")


@dataclass(frozen=True)
class DailyObservationRecordIndexResult:
    valid: bool
    errors: tuple[str, ...]
    index: dict[str, Any]


def _sort_records(records: Iterable[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    return sorted(records, key=lambda record: str(record.get("date", "")))


def build_daily_observation_record_index(records: Iterable[Mapping[str, Any]]) -> DailyObservationRecordIndexResult:
    errors: list[str] = []
    entries: list[dict[str, Any]] = []
    seen_dates: set[str] = set()
    status_counts: Counter[str] = Counter()

    for record in _sort_records(records):
        record_dict = dict(record)
        date_value = str(record_dict.get("date", ""))

        if date_value in seen_dates:
            errors.append(f"duplicate_record_date:{date_value}")
        seen_dates.add(date_value)

        validation = validate_daily_observation_record(record_dict)
        errors.extend(f"record:{date_value}:{error}" for error in validation.errors)

        expected_path = build_daily_observation_record_path(date_value)
        artifact_validation = validate_daily_observation_record_artifact(record_dict, expected_path)
        errors.extend(f"artifact:{date_value}:{error}" for error in artifact_validation.errors)

        status = str(record_dict.get("status", ""))
        status_counts[status] += 1

        entries.append(
            {
                "date": date_value,
                "status": status,
                "path": str(expected_path),
                "review_required": bool(record_dict.get("review_required", False)),
                "missing_evidence_count": len(record_dict.get("missing_evidence", [])),
                "incident_count": len(record_dict.get("incidents", [])),
                "live_trading_authorized": False,
                "broker_execution_mode": "paper_only",
            }
        )

    index = {
        "record_root": str(ALLOWED_RECORD_ROOT),
        "index_path": str(INDEX_PATH),
        "total_records": len(entries),
        "status_counts": {status: status_counts.get(status, 0) for status in VALID_INDEX_STATUSES},
        "records": entries,
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }

    return DailyObservationRecordIndexResult(valid=not errors, errors=tuple(errors), index=index)


def write_daily_observation_record_index(
    *,
    records: Iterable[Mapping[str, Any]],
    output_path: str | Path | None = None,
    indent: int = 2,
) -> DailyObservationRecordIndexResult:
    result = build_daily_observation_record_index(records)
    if not result.valid:
        return result

    path = Path(output_path) if output_path is not None else INDEX_PATH
    if path != INDEX_PATH:
        return DailyObservationRecordIndexResult(
            valid=False,
            errors=("index_path_must_be_canonical",),
            index=result.index,
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result.index, indent=indent, sort_keys=True) + "\n", encoding="utf-8")
    return result
