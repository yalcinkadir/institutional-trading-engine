from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SCHEDULED_REPORT_LIVENESS_ROOT = Path("reports/scheduled_report_liveness")
STATUS_PASSED = "PASSED"
STATUS_BLOCKED = "BLOCKED"
MARKET_REPORT_TYPES = {"premarket", "intraday", "postmarket"}
WEEKLY_REPORT_TYPES = {"weekly"}
VALID_REPORT_TYPES = MARKET_REPORT_TYPES | WEEKLY_REPORT_TYPES


@dataclass(frozen=True)
class ScheduledReportLivenessResult:
    valid: bool
    artifact_path: str
    latest_artifact_path: str
    artifact: dict[str, Any]
    errors: tuple[str, ...] = field(default_factory=tuple)


def build_scheduled_report_liveness_artifact_path(report_type: str, run_date: str | None = None) -> Path:
    date_value = run_date or datetime.now(UTC).date().isoformat()
    return SCHEDULED_REPORT_LIVENESS_ROOT / f"{date_value}-{report_type}-liveness.json"


def build_scheduled_report_liveness_artifact(
    *,
    report_type: str,
    report_file: str | Path,
    latest_file: str | Path | None = None,
    signals_file: str | Path | None = None,
    paper_health_file: str | Path | None = None,
    run_timestamp: str | None = None,
    workflow_name: str | None = None,
    commit_sha: str | None = None,
    run_date: str | None = None,
) -> ScheduledReportLivenessResult:
    """Build #192 scheduled report liveness evidence.

    A scheduled report is live only when the expected scheduled artifact exists,
    is non-empty, and its downstream evidence exists. Market reports must also
    have signals and paper-observation health evidence; weekly reports do not
    produce signals and are validated only through report/latest-file evidence.
    """

    normalized_report_type = str(report_type or "").strip().lower()
    errors: list[str] = []
    warnings: list[str] = []

    if normalized_report_type not in VALID_REPORT_TYPES:
        errors.append(f"unknown_report_type:{normalized_report_type or 'missing'}")

    report_path = Path(report_file)
    latest_path = Path(latest_file) if latest_file is not None else None
    signals_path = Path(signals_file) if signals_file is not None else None
    health_path = Path(paper_health_file) if paper_health_file is not None else None

    report_state = _file_state(report_path)
    latest_state = _file_state(latest_path) if latest_path is not None else {"required": False, "exists": False}
    signals_state = _file_state(signals_path) if signals_path is not None else {"required": normalized_report_type in MARKET_REPORT_TYPES, "exists": False}
    health_state = _file_state(health_path) if health_path is not None else {"required": normalized_report_type in MARKET_REPORT_TYPES, "exists": False}

    _collect_required_file_errors("report_file", report_state, errors)
    if latest_path is not None:
        _collect_required_file_errors("latest_file", latest_state, errors)
    else:
        errors.append("latest_file_not_configured")

    if normalized_report_type in MARKET_REPORT_TYPES:
        if signals_path is None:
            errors.append("signals_file_not_configured_for_market_report")
        else:
            _collect_required_file_errors("signals_file", signals_state, errors)
        if health_path is None:
            errors.append("paper_health_file_not_configured_for_market_report")
        else:
            _collect_required_file_errors("paper_health_file", health_state, errors)
    elif normalized_report_type in WEEKLY_REPORT_TYPES:
        if signals_path is not None and not signals_path.exists():
            warnings.append("weekly_signals_file_configured_but_missing")
        if health_path is not None and not health_path.exists():
            warnings.append("weekly_paper_health_file_configured_but_missing")

    status = STATUS_PASSED if not errors else STATUS_BLOCKED
    date_value = run_date or datetime.now(UTC).date().isoformat()
    artifact_path = build_scheduled_report_liveness_artifact_path(normalized_report_type or "unknown", date_value)
    latest_artifact_path = SCHEDULED_REPORT_LIVENESS_ROOT / "latest-scheduled-report-liveness.json"

    artifact = {
        "schema_version": "scheduled_report_liveness.v1",
        "issue": "#192",
        "scheduled_report_status": status,
        "liveness_status": status,
        "report_type": normalized_report_type or "UNKNOWN",
        "run_timestamp": run_timestamp or _now_iso(),
        "workflow_name": workflow_name or "UNKNOWN",
        "commit_sha": commit_sha or "UNKNOWN",
        "report_file": str(report_path),
        "latest_file": str(latest_path) if latest_path is not None else None,
        "signals_file": str(signals_path) if signals_path is not None else None,
        "paper_health_file": str(health_path) if health_path is not None else None,
        "file_evidence": {
            "report_file": report_state,
            "latest_file": latest_state,
            "signals_file": signals_state,
            "paper_health_file": health_state,
        },
        "errors": tuple(errors),
        "warnings": tuple(warnings),
        "productive_report_cycle": status == STATUS_PASSED,
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
        "capital_allocation_authorized": False,
    }

    return ScheduledReportLivenessResult(
        valid=status == STATUS_PASSED,
        artifact_path=str(artifact_path),
        latest_artifact_path=str(latest_artifact_path),
        artifact=artifact,
        errors=tuple(errors),
    )


def write_scheduled_report_liveness_artifact(
    *,
    result: ScheduledReportLivenessResult,
    indent: int = 2,
) -> ScheduledReportLivenessResult:
    artifact_path = Path(result.artifact_path)
    latest_path = Path(result.latest_artifact_path)
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result.artifact, indent=indent, sort_keys=True) + "\n"
    artifact_path.write_text(payload, encoding="utf-8")
    latest_path.write_text(payload, encoding="utf-8")
    return result


def _file_state(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {"required": False, "exists": False, "path": None, "size_bytes": 0, "non_empty": False}
    exists = path.exists()
    size = path.stat().st_size if exists and path.is_file() else 0
    return {
        "required": True,
        "path": str(path),
        "exists": exists,
        "is_file": path.is_file() if exists else False,
        "size_bytes": size,
        "non_empty": size > 0,
    }


def _collect_required_file_errors(name: str, state: dict[str, Any], errors: list[str]) -> None:
    if not state.get("exists"):
        errors.append(f"{name}_missing")
        return
    if not state.get("is_file", False):
        errors.append(f"{name}_not_a_file")
        return
    if not state.get("non_empty"):
        errors.append(f"{name}_empty")


def _now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
