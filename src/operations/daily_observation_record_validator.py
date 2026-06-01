from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Mapping

VALID_STATUSES = frozenset({"ACCEPTED", "REJECTED", "NEEDS_REVIEW"})
BROKER_EXECUTION_MODE = "paper_only"
REQUIRED_FIELDS = (
    "date",
    "status",
    "missing_evidence",
    "incidents",
    "artifact_paths",
    "review_required",
    "review_notes",
    "live_trading_authorized",
    "broker_execution_mode",
    "created_at",
)


@dataclass(frozen=True)
class DailyObservationRecordValidationResult:
    valid: bool
    errors: tuple[str, ...]


def _is_iso_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _is_iso_datetime(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    normalized = value.replace("Z", "+00:00")
    try:
        datetime.fromisoformat(normalized)
    except ValueError:
        return False
    return True


def _is_string_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def validate_daily_observation_record(record: Mapping[str, Any]) -> DailyObservationRecordValidationResult:
    errors: list[str] = []

    missing_fields = [field for field in REQUIRED_FIELDS if field not in record]
    if missing_fields:
        errors.append(f"missing_fields:{','.join(missing_fields)}")

    if "date" in record and not _is_iso_date(record["date"]):
        errors.append("invalid_date")

    status = record.get("status")
    if status not in VALID_STATUSES:
        errors.append("invalid_status")

    for field in ("missing_evidence", "incidents", "artifact_paths"):
        if field in record and not _is_string_list(record[field]):
            errors.append(f"invalid_{field}")

    if "review_required" in record and not isinstance(record["review_required"], bool):
        errors.append("invalid_review_required")

    if "review_notes" in record and not isinstance(record["review_notes"], str):
        errors.append("invalid_review_notes")

    if record.get("live_trading_authorized") is not False:
        errors.append("live_trading_must_remain_false")

    if record.get("broker_execution_mode") != BROKER_EXECUTION_MODE:
        errors.append("broker_execution_mode_must_be_paper_only")

    if "created_at" in record and not _is_iso_datetime(record["created_at"]):
        errors.append("invalid_created_at")

    missing_evidence = record.get("missing_evidence")
    incidents = record.get("incidents")
    review_required = record.get("review_required")

    if status == "ACCEPTED":
        if missing_evidence:
            errors.append("accepted_record_cannot_have_missing_evidence")
        if incidents:
            errors.append("accepted_record_cannot_have_unresolved_incidents")
        if review_required is not False:
            errors.append("accepted_record_review_required_must_be_false")

    if status == "REJECTED":
        if not missing_evidence:
            errors.append("rejected_record_requires_missing_evidence")

    if status == "NEEDS_REVIEW":
        if not incidents:
            errors.append("needs_review_record_requires_incidents")
        if review_required is not True:
            errors.append("needs_review_record_review_required_must_be_true")

    return DailyObservationRecordValidationResult(valid=not errors, errors=tuple(errors))
