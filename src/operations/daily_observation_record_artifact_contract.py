from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

ALLOWED_RECORD_ROOT = Path("reports/daily_observation_records")
PROHIBITED_PATH_PARTS = frozenset({"live", "private", "raw", "generated"})
PUBLIC_REPORT_FILENAMES = frozenset({"premarket-report.md", "postmarket-report.md"})


@dataclass(frozen=True)
class DailyObservationRecordArtifactPathResult:
    valid: bool
    errors: tuple[str, ...]


def build_daily_observation_record_path(observation_date: str | date) -> Path:
    if isinstance(observation_date, date):
        date_value = observation_date.isoformat()
    else:
        date_value = observation_date
    return ALLOWED_RECORD_ROOT / f"{date_value}.json"


def validate_daily_observation_record_artifact_path(path: str | Path) -> DailyObservationRecordArtifactPathResult:
    candidate = Path(path)
    errors: list[str] = []

    if candidate.is_absolute():
        errors.append("absolute_paths_are_not_allowed")

    normalized = Path(*candidate.parts) if candidate.parts else candidate

    if normalized.name in PUBLIC_REPORT_FILENAMES:
        errors.append("public_report_example_path_not_allowed")

    if any(part in PROHIBITED_PATH_PARTS for part in normalized.parts):
        errors.append("prohibited_path_segment")

    if not normalized.suffix == ".json":
        errors.append("record_path_must_be_json")

    if normalized.parent != ALLOWED_RECORD_ROOT:
        errors.append("record_path_must_use_daily_observation_root")

    stem = normalized.stem
    try:
        date.fromisoformat(stem)
    except ValueError:
        errors.append("record_filename_must_be_iso_date")

    return DailyObservationRecordArtifactPathResult(valid=not errors, errors=tuple(errors))


def validate_daily_observation_record_artifact(record: dict[str, Any], path: str | Path) -> DailyObservationRecordArtifactPathResult:
    path_result = validate_daily_observation_record_artifact_path(path)
    errors = list(path_result.errors)

    expected_path = build_daily_observation_record_path(str(record.get("date", "")))
    if Path(path) != expected_path:
        errors.append("record_path_must_match_record_date")

    return DailyObservationRecordArtifactPathResult(valid=not errors, errors=tuple(errors))
