from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

REVIEW_INDEX_PATH = Path("reports/daily_observation_automation/review_index.json")
DEFAULT_RETENTION_DAYS = 180
VALID_AUTOMATION_STATUSES = ("PASSED", "BLOCKED")
DURABLE_STATUS_SUCCESS = "SUCCESS"
DURABLE_STATUS_BLOCKED = "BLOCKED"
DURABLE_STATUS_DEGRADED = "DEGRADED"
DURABLE_STATUS_FAILED = "FAILED"
DURABLE_STATUS_NO_TRADE_VALID = "NO_TRADE_VALID"
UNKNOWN = "UNKNOWN"
NOT_AVAILABLE = "not_available"


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


def _as_bool(value: Any, *, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    return default


def _as_non_empty_string(value: Any, *, default: str) -> str:
    text = str(value or "").strip()
    return text if text else default


def _artifact_date(artifact: Mapping[str, Any]) -> str:
    return str(artifact.get("observation_date", ""))


def _artifact_path(observation_date: str) -> str:
    return f"reports/daily_observation_automation/{observation_date}.json"


def _artifact_pointer(artifact: Mapping[str, Any], observation_date: str) -> str:
    return _as_non_empty_string(
        artifact.get("artifact_pointer") or artifact.get("artifact_url") or artifact.get("artifact_path"),
        default=_artifact_path(observation_date),
    )


def _artifact_checksum(artifact: Mapping[str, Any]) -> str:
    return _as_non_empty_string(
        artifact.get("artifact_sha256") or artifact.get("artifact_checksum") or artifact.get("checksum"),
        default=NOT_AVAILABLE,
    )


def _workflow_run_id(artifact: Mapping[str, Any]) -> str:
    return _as_non_empty_string(
        artifact.get("workflow_run_id") or artifact.get("github_run_id") or artifact.get("run_id"),
        default=UNKNOWN,
    )


def _data_mode(artifact: Mapping[str, Any]) -> str:
    health = artifact.get("signal_generation_health")
    if isinstance(health, Mapping):
        candidate = health.get("data_mode") or health.get("selection_mode") or health.get("source_mode")
        if candidate:
            return str(candidate)
    return _as_non_empty_string(artifact.get("data_mode"), default=UNKNOWN)


def _degradation_flags(artifact: Mapping[str, Any]) -> tuple[str, ...]:
    flags = artifact.get("degradation_flags")
    if isinstance(flags, (list, tuple)):
        return tuple(str(flag) for flag in flags if str(flag).strip())

    health = artifact.get("signal_generation_health")
    if isinstance(health, Mapping):
        health_flags = health.get("degradation_flags")
        if isinstance(health_flags, (list, tuple)):
            return tuple(str(flag) for flag in health_flags if str(flag).strip())
        status = str(health.get("status") or health.get("datafeed_status") or "")
        if status in {"DEGRADED", "DATAFEED_BLOCKED", "BLOCKED"}:
            return (status,)

    return ()


def _durable_status(
    *,
    automation_status: str,
    gate_status: str,
    review_ready: bool,
    artifact_errors: tuple[Any, ...],
    degradation_flags: tuple[str, ...],
    approved_for_review: bool,
) -> str:
    if artifact_errors:
        return DURABLE_STATUS_FAILED
    if degradation_flags:
        return DURABLE_STATUS_DEGRADED
    if automation_status == "BLOCKED" or gate_status == "BLOCKED":
        return DURABLE_STATUS_BLOCKED
    if automation_status == "PASSED" and approved_for_review and not review_ready:
        return DURABLE_STATUS_NO_TRADE_VALID
    if automation_status == "PASSED":
        return DURABLE_STATUS_SUCCESS
    return DURABLE_STATUS_FAILED


def build_daily_observation_artifact_review_index(
    artifacts: Iterable[Mapping[str, Any]],
    *,
    retention_days: int = DEFAULT_RETENTION_DAYS,
) -> DailyObservationArtifactReviewIndexResult:
    """Build a deterministic durable review index for Paper Observation artifacts.

    #181 extends the PO12 review index into a long-lived audit index. The index
    stores lightweight metadata only; it does not authorize live trading, broker
    execution or committing large runtime artifacts to main.
    """

    errors: list[str] = []
    entries: list[dict[str, Any]] = []
    seen_dates: set[str] = set()
    status_counts = {status: 0 for status in VALID_AUTOMATION_STATUSES}
    durable_status_counts = {
        DURABLE_STATUS_SUCCESS: 0,
        DURABLE_STATUS_BLOCKED: 0,
        DURABLE_STATUS_DEGRADED: 0,
        DURABLE_STATUS_FAILED: 0,
        DURABLE_STATUS_NO_TRADE_VALID: 0,
    }

    if retention_days < 1:
        errors.append("retention_days_must_be_positive")

    for artifact in sorted((dict(item) for item in artifacts), key=_artifact_date):
        observation_date = _artifact_date(artifact)
        automation_status = str(artifact.get("automation_status", ""))
        artifact_errors = _as_tuple(artifact.get("errors"))
        gate = dict(artifact.get("gate", {})) if isinstance(artifact.get("gate"), Mapping) else {}
        summary = dict(artifact.get("summary", {})) if isinstance(artifact.get("summary"), Mapping) else {}
        degradation_flags = _degradation_flags(artifact)
        review_ready = bool(summary.get("review_ready", False))
        gate_status = str(gate.get("gate_status", ""))
        approved_for_review = bool(gate.get("approved_for_review", False))
        durable_status = _durable_status(
            automation_status=automation_status,
            gate_status=gate_status,
            review_ready=review_ready,
            artifact_errors=artifact_errors,
            degradation_flags=degradation_flags,
            approved_for_review=approved_for_review,
        )
        durable_status_counts[durable_status] += 1

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
                "workflow_run_id": _workflow_run_id(artifact),
                "artifact_path": expected_path,
                "artifact_pointer": _artifact_pointer(artifact, observation_date),
                "artifact_sha256": _artifact_checksum(artifact),
                "data_mode": _data_mode(artifact),
                "degradation_flags": list(degradation_flags),
                "durable_status": durable_status,
                "automation_status": automation_status,
                "review_ready": review_ready,
                "gate_status": gate_status,
                "approved_for_review": approved_for_review,
                "blocker_count": len(_as_tuple(gate.get("blockers"))),
                "error_count": len(artifact_errors),
                "total_records": _as_int(summary.get("total_records")),
                "accepted_count": _as_int(summary.get("accepted_count")),
                "rejected_count": _as_int(summary.get("rejected_count")),
                "needs_review_count": _as_int(summary.get("needs_review_count")),
                "no_trade_valid": durable_status == DURABLE_STATUS_NO_TRADE_VALID,
                "live_trading_authorized": False,
                "broker_execution_mode": "paper_only",
            }
        )

    total_artifacts = len(entries)
    blocked_count = status_counts["BLOCKED"]
    passed_count = status_counts["PASSED"]
    review_ready_count = sum(1 for entry in entries if entry["review_ready"] is True)

    index = {
        "schema_version": "paper_observation_durable_evidence_index.v1",
        "index_path": str(REVIEW_INDEX_PATH),
        "artifact_root": "reports/daily_observation_automation",
        "retention_days": retention_days,
        "large_runtime_artifacts_committed_to_main": False,
        "github_actions_artifacts_are_audit_source": False,
        "durable_history_reconstructable_after_artifact_expiry": True,
        "total_artifacts": total_artifacts,
        "status_counts": status_counts,
        "durable_status_counts": durable_status_counts,
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
