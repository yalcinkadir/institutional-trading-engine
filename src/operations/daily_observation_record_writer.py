from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

from src.operations.daily_observation_record_validator import (
    DailyObservationRecordValidationResult,
    validate_daily_observation_record,
)

STATUS_ACCEPTED = "ACCEPTED"
STATUS_REJECTED = "REJECTED"
STATUS_NEEDS_REVIEW = "NEEDS_REVIEW"
SIGNAL_GENERATION_STATUS_PASSED = "PASSED"


def _as_string_list(values: Iterable[str] | None) -> list[str]:
    if values is None:
        return []
    return [str(value) for value in values]


def _missing_artifact_evidence(
    artifact_paths: Iterable[str] | None,
    *,
    artifact_root: str | Path | None = None,
) -> list[str]:
    root = Path(artifact_root) if artifact_root is not None else Path.cwd()
    missing: list[str] = []

    for artifact_path in _as_string_list(artifact_paths):
        path = Path(artifact_path)
        candidate = path if path.is_absolute() else root / path
        if not candidate.exists():
            missing.append(f"missing_artifact:{artifact_path}")

    return missing


def _default_signal_generation_health(signal_generation_status: str) -> dict[str, Any]:
    return {
        "stage": "signal_generation",
        "status": signal_generation_status,
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }


def determine_daily_observation_status(
    *,
    missing_evidence: Iterable[str] | None = None,
    incidents: Iterable[str] | None = None,
) -> tuple[str, bool]:
    missing = _as_string_list(missing_evidence)
    incident_list = _as_string_list(incidents)

    if missing:
        return STATUS_REJECTED, False
    if incident_list:
        return STATUS_NEEDS_REVIEW, True
    return STATUS_ACCEPTED, False


def build_daily_observation_record(
    *,
    observation_date: str | date,
    missing_evidence: Iterable[str] | None = None,
    incidents: Iterable[str] | None = None,
    artifact_paths: Iterable[str] | None = None,
    review_notes: str = "",
    created_at: str | None = None,
    require_artifact_paths_exist: bool = False,
    artifact_root: str | Path | None = None,
    signal_generation_status: str = SIGNAL_GENERATION_STATUS_PASSED,
    signal_generation_health: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if isinstance(observation_date, date):
        observation_date_value = observation_date.isoformat()
    else:
        observation_date_value = observation_date

    signal_status = str(signal_generation_status or SIGNAL_GENERATION_STATUS_PASSED).upper()
    signal_health = dict(signal_generation_health or _default_signal_generation_health(signal_status))

    artifact_path_list = _as_string_list(artifact_paths)
    missing = _as_string_list(missing_evidence)
    if require_artifact_paths_exist:
        missing.extend(
            _missing_artifact_evidence(
                artifact_path_list,
                artifact_root=artifact_root,
            )
        )
    if signal_status != SIGNAL_GENERATION_STATUS_PASSED:
        missing.append(f"signal_generation_status:{signal_status}")
    incident_list = _as_string_list(incidents)
    status, review_required = determine_daily_observation_status(
        missing_evidence=missing,
        incidents=incident_list,
    )

    return {
        "date": observation_date_value,
        "status": status,
        "missing_evidence": missing,
        "incidents": incident_list,
        "artifact_paths": artifact_path_list,
        "review_required": review_required,
        "review_notes": review_notes,
        "signal_generation_status": signal_status,
        "signal_generation_health": signal_health,
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
        "created_at": created_at or datetime.now(timezone.utc).isoformat(),
    }


def write_daily_observation_record(
    *,
    record: dict[str, Any],
    output_path: str | Path,
    indent: int = 2,
) -> DailyObservationRecordValidationResult:
    validation = validate_daily_observation_record(record)
    if not validation.valid:
        return validation

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=indent, sort_keys=True) + "\n", encoding="utf-8")
    return validation
