from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

REVIEW_INDEX_PATH = Path("reports/daily_observation_automation/review_index.json")
DEFAULT_RETENTION_DAYS = 180
VALID_AUTOMATION_STATUSES = ("PASSED", "BLOCKED")


@dataclass(frozen=True)
class DailyObservationArtifactReviewIndexResult:
    valid: bool
    errors: tuple[str, ...]
    index: dict[str, Any]


def _as_int(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_tuple(value: Any) -> tuple[Any, ...]:
    if isinstance(value, tuple):
        return value
    if isinstance(value, list):
        return tuple(value)
    return ()


def _artifact_date(artifact: Mapping[str, Any]) -> str:
    return str(artifact.get("observation_date", ""))


def _artifact_path(observation_date: str) -> str:
    return f"reports/daily_observation_automation/{observation_date}.json"


def build_daily_observation_artifact_review_index(
    artifacts: Iterable[Mapping[str, Any]],
    *,
    retention_days: int = DEFAULT_RETENTION_DAYS,
) -> DailyObservationArtifactReviewIndexResult:
    """Build a deterministic review index for PO10/PO11 automation artifacts.

    PO12 makes generated daily automation artifacts reviewable without granting
    live trading, broker execution or production deployment.
    """

    errors: list[str] = []
    entries: list[dict[str, Any]] = []
    seen_dates: set[str] = set()
    status_counts = {status: 0 for status in VALID_AUTOMATION_STATUSES}

    if retention_days < 1:
        errors.append("retention_days_must_be_positive")

    for artifact in sorted((dict(item) for item in artifacts), key=_artifact_date):
        observation_date = _artifact_date(artifact)
        automation_status = str(artifact.get("automation_status", ""))
        artifact_errors = _as_tuple(artifact.get("errors"))
        gate = dict(artifact.get("gate", {})) if isinstance(artifact.get("gate"), Mapping) else {}
        summary = dict(artifact.get("summary", {})) if isinstance(artifact.get("summary"), Mapping) else {}

        if not observation_date:
            errors.append("artifact_missing_observation_date")

        if observation_date in seen_dates:
            errors.append(f"duplicate_artifact_date:{observation_date}")
        seen_dates.add(observation_date)

        if automation_status not in VALID_AUTOMATION_STATUSES:
            errors.append(f"artifact:{observation_date}:invalid_automation_status")
        else:
            status_counts[automation_status] += 1

        if artifact.get("live_trading_authorized") is not False:
            errors.append(f"artifact:{observation_date}:live_trading_must_remain_false")

        if artifact.get("broker_execution_mode") != "paper_only":
            errors.append(f"artifact:{observation_date}:broker_execution_mode_must_be_paper_only")

        if gate.get("live_trading_authorized") is not False:
            errors.append(f"artifact:{observation_date}:gate_live_trading_must_remain_false")

        if gate.get("broker_execution_mode") != "paper_only":
            errors.append(f"artifact:{observation_date}:gate_broker_execution_mode_must_be_paper_only")

        expected_path = _artifact_path(observation_date)
        recorded_path = str(artifact.get("artifact_path", expected_path))
        if recorded_path != expected_path:
            errors.append(f"artifact:{observation_date}:artifact_path_must_be_canonical")

        entries.append(
            {
                "observation_date": observation_date,
                "artifact_path": expected_path,
                "automation_status": automation_status,
                "review_ready": bool(summary.get("review_ready", False)),
                "gate_status": str(gate.get("gate_status", "")),
                "approved_for_review": bool(gate.get("approved_for_review", False)),
                "blocker_count": len(_as_tuple(gate.get("blockers"))),
                "error_count": len(artifact_errors),
                "total_records": _as_int(summary.get("total_records")),
                "accepted_count": _as_int(summary.get("accepted_count")),
                "rejected_count": _as_int(summary.get("rejected_count")),
                "needs_review_count": _as_int(summary.get("needs_review_count")),
                "live_trading_authorized": False,
                "broker_execution_mode": "paper_only",
            }
        )

    total_artifacts = len(entries)
    blocked_count = status_counts["BLOCKED"]
    passed_count = status_counts["PASSED"]
    review_ready_count = sum(1 for entry in entries if entry["review_ready"] is True)

    index = {
        "index_path": str(REVIEW_INDEX_PATH),
        "artifact_root": "reports/daily_observation_automation",
        "retention_days": retention_days,
        "total_artifacts": total_artifacts,
        "status_counts": status_counts,
        "passed_count": passed_count,
        "blocked_count": blocked_count,
        "review_ready_count": review_ready_count,
        "artifacts": entries,
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }

    return DailyObservationArtifactReviewIndexResult(valid=not errors, errors=tuple(errors), index=index)


def write_daily_observation_artifact_review_index(
    *,
    artifacts: Iterable[Mapping[str, Any]],
    output_path: str | Path | None = None,
    retention_days: int = DEFAULT_RETENTION_DAYS,
    indent: int = 2,
) -> DailyObservationArtifactReviewIndexResult:
    result = build_daily_observation_artifact_review_index(artifacts, retention_days=retention_days)
    if not result.valid:
        return result

    path = Path(output_path) if output_path is not None else REVIEW_INDEX_PATH
    if path != REVIEW_INDEX_PATH:
        return DailyObservationArtifactReviewIndexResult(
            valid=False,
            errors=("review_index_path_must_be_canonical",),
            index=result.index,
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result.index, indent=indent, sort_keys=True) + "\n", encoding="utf-8")
    return result
