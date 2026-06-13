#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

SCHEDULED_REPORT_LIVENESS_ROOT = Path("reports/scheduled_report_liveness")
HEALTH_REPORT_LIVENESS_LATEST = Path("reports/health/report-liveness-latest.json")

STATUS_PASSED = "PASSED"
STATUS_DEGRADED = "DEGRADED"
STATUS_BLOCKED = "BLOCKED"

REPORT_LIVENESS_OK = "REPORT_LIVENESS_OK"
REPORT_LIVENESS_DEGRADED = "REPORT_LIVENESS_DEGRADED"
REPORT_LIVENESS_BLOCKED = "REPORT_LIVENESS_BLOCKED"

CURRENT_RUN_VALIDATED = "WORKFLOW_RAN_VALIDATED"
CURRENT_RUN_INCOMPLETE = "WORKFLOW_RAN_BUT_VALIDATION_FAILED_OR_INCOMPLETE"
CURRENT_RUN_MISSING = "NO_CURRENT_OUTPUT_PERSISTED"

MARKET_REPORT_TYPES = {"premarket", "intraday", "postmarket"}
WEEKLY_REPORT_TYPES = {"weekly"}
VALID_REPORT_TYPES = MARKET_REPORT_TYPES | WEEKLY_REPORT_TYPES

REPORT_FAMILY_PATTERNS = {
    "signals": (Path("reports/signals"), re.compile(r"^(\d{4}-\d{2}-\d{2})-signals\.json$")),
    "premarket": (Path("reports/premarket"), re.compile(r"^(\d{4}-\d{2}-\d{2})-premarket\.md$")),
    "intraday": (Path("reports/intraday"), re.compile(r"^(\d{4}-\d{2}-\d{2})-intraday\.md$")),
    "postmarket": (Path("reports/postmarket"), re.compile(r"^(\d{4}-\d{2}-\d{2})-postmarket\.md$")),
    "daily_evidence": (Path("reports/daily_evidence"), re.compile(r"^(\d{4}-\d{2}-\d{2})\.json$")),
}


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


def _required_freshness_families(report_type: str) -> tuple[str, ...]:
    """Return report-family freshness checks that are blocking for this run type.

    Market reports are the productive Paper Observation path and therefore require
    `daily_evidence`.

    Weekly reports are scheduled summary reports. They must not overwrite the
    canonical liveness artifact as blocked merely because daily Paper Observation
    evidence is absent for the weekly run itself. Daily-evidence freshness remains
    visible in the artifact, but is not a blocking family for weekly liveness.
    """

    if report_type in WEEKLY_REPORT_TYPES:
        return ("signals", "premarket", "intraday", "postmarket")
    return tuple(REPORT_FAMILY_PATTERNS.keys())


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
    report_root: str | Path = ".",
    consecutive_miss_block_threshold: int = 2,
) -> ScheduledReportLivenessResult:
    """Build #192 scheduled report liveness evidence.

    A scheduled report is live only when the expected scheduled artifact exists,
    is non-empty, and its downstream evidence exists. The gate also scans the
    persisted report families and blocks after two business days without fresh
    output so old reports cannot make the system look alive.
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
    root = Path(report_root)

    report_state = _file_state(report_path)
    latest_state = _file_state(latest_path) if latest_path is not None else {"required": False, "exists": False}
    signals_state = (
        _file_state(signals_path)
        if signals_path is not None
        else {"required": normalized_report_type in MARKET_REPORT_TYPES, "exists": False}
    )
    health_state = (
        _file_state(health_path)
        if health_path is not None
        else {"required": normalized_report_type in MARKET_REPORT_TYPES, "exists": False}
    )

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

    date_value = run_date or datetime.now(UTC).date().isoformat()
    freshness = build_report_family_freshness_summary(
        report_root=root,
        run_date=date_value,
        consecutive_miss_block_threshold=consecutive_miss_block_threshold,
    )
    required_freshness_families = set(_required_freshness_families(normalized_report_type))

    for family, state in freshness.items():
        status = state["freshness_status"]

        if family not in required_freshness_families:
            continue

        if status == REPORT_LIVENESS_BLOCKED:
            errors.append(f"{family}_stale_or_missing:{state['business_days_without_fresh_output']}")
        elif status == REPORT_LIVENESS_DEGRADED:
            warnings.append(f"{family}_one_business_day_without_fresh_output")

    current_run_state = _derive_current_run_state(
        report_state=report_state,
        latest_state=latest_state,
        signals_state=signals_state,
        health_state=health_state,
        report_type=normalized_report_type,
    )
    if current_run_state == CURRENT_RUN_INCOMPLETE:
        errors.append("workflow_ran_but_validation_failed_or_incomplete")
    elif current_run_state == CURRENT_RUN_MISSING:
        errors.append("workflow_did_not_produce_or_persist_current_output")

    if errors:
        status = STATUS_BLOCKED
        report_liveness_status = REPORT_LIVENESS_BLOCKED
    elif warnings:
        status = STATUS_DEGRADED
        report_liveness_status = REPORT_LIVENESS_DEGRADED
    else:
        status = STATUS_PASSED
        report_liveness_status = REPORT_LIVENESS_OK

    artifact_path = build_scheduled_report_liveness_artifact_path(normalized_report_type or "unknown", date_value)
    latest_artifact_path = SCHEDULED_REPORT_LIVENESS_ROOT / "latest-scheduled-report-liveness.json"

    artifact = {
        "schema_version": "scheduled_report_liveness.v1",
        "issue": "#192",
        "scheduled_report_status": status,
        "liveness_status": report_liveness_status,
        "report_liveness_status": report_liveness_status,
        "current_run_state": current_run_state,
        "report_type": normalized_report_type or "UNKNOWN",
        "run_date": date_value,
        "run_timestamp": run_timestamp or _now_iso(),
        "workflow_name": workflow_name or "UNKNOWN",
        "commit_sha": commit_sha or "UNKNOWN",
        "consecutive_miss_block_threshold_business_days": consecutive_miss_block_threshold,
        "required_freshness_families": tuple(sorted(required_freshness_families)),
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
        "freshness_by_family": freshness,
        "errors": tuple(errors),
        "warnings": tuple(warnings),
        "productive_report_cycle": status == STATUS_PASSED,
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
        "capital_allocation_authorized": False,
    }

    return ScheduledReportLivenessResult(
        valid=status != STATUS_BLOCKED,
        artifact_path=str(artifact_path),
        latest_artifact_path=str(latest_artifact_path),
        artifact=artifact,
        errors=tuple(errors),
    )


def build_report_family_freshness_summary(
    *,
    report_root: str | Path,
    run_date: str,
    consecutive_miss_block_threshold: int = 2,
) -> dict[str, dict[str, Any]]:
    root = Path(report_root)
    run_day = date.fromisoformat(run_date)
    summary: dict[str, dict[str, Any]] = {}

    for family, (relative_dir, pattern) in REPORT_FAMILY_PATTERNS.items():
        latest_day, latest_path = _latest_dated_file(root / relative_dir, pattern)
        if latest_day is None:
            missed = consecutive_miss_block_threshold
            status = REPORT_LIVENESS_BLOCKED
        else:
            missed = _business_days_between_exclusive_start(latest_day, run_day)
            if missed <= 0:
                status = REPORT_LIVENESS_OK
            elif missed >= consecutive_miss_block_threshold:
                status = REPORT_LIVENESS_BLOCKED
            else:
                status = REPORT_LIVENESS_DEGRADED

        summary[family] = {
            "freshness_status": status,
            "latest_output_date": latest_day.isoformat() if latest_day is not None else None,
            "latest_output_path": str(latest_path) if latest_path is not None else None,
            "business_days_without_fresh_output": missed,
        }

    return summary


def write_scheduled_report_liveness_artifact(
    *,
    result: ScheduledReportLivenessResult,
    indent: int = 2,
) -> ScheduledReportLivenessResult:
    artifact_path = Path(result.artifact_path)
    latest_path = Path(result.latest_artifact_path)
    health_latest_path = HEALTH_REPORT_LIVENESS_LATEST

    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    latest_path.parent.mkdir(parents=True, exist_ok=True)
    health_latest_path.parent.mkdir(parents=True, exist_ok=True)

    payload = json.dumps(result.artifact, indent=indent, sort_keys=True) + "\n"
    artifact_path.write_text(payload, encoding="utf-8")
    latest_path.write_text(payload, encoding="utf-8")
    health_latest_path.write_text(payload, encoding="utf-8")

    return result


def _derive_current_run_state(
    *,
    report_state: dict[str, Any],
    latest_state: dict[str, Any],
    signals_state: dict[str, Any],
    health_state: dict[str, Any],
    report_type: str,
) -> str:
    required_states = [report_state, latest_state]
    if report_type in MARKET_REPORT_TYPES:
        required_states.extend([signals_state, health_state])

    any_exists = any(state.get("exists") for state in required_states)
    all_ready = all(
        state.get("exists") and state.get("is_file") and state.get("non_empty")
        for state in required_states
    )

    if all_ready:
        return CURRENT_RUN_VALIDATED
    if any_exists:
        return CURRENT_RUN_INCOMPLETE
    return CURRENT_RUN_MISSING


def _latest_dated_file(directory: Path, pattern: re.Pattern[str]) -> tuple[date | None, Path | None]:
    if not directory.exists():
        return None, None

    latest_day: date | None = None
    latest_path: Path | None = None

    for path in directory.iterdir():
        if not path.is_file():
            continue

        match = pattern.match(path.name)
        if not match:
            continue

        try:
            parsed = date.fromisoformat(match.group(1))
        except ValueError:
            continue

        if latest_day is None or parsed > latest_day:
            latest_day = parsed
            latest_path = path

    return latest_day, latest_path


def _business_days_between_exclusive_start(start: date, end: date) -> int:
    if start >= end:
        return 0

    count = 0
    cursor = start + timedelta(days=1)

    while cursor <= end:
        if cursor.weekday() < 5:
            count += 1
        cursor += timedelta(days=1)

    return count


def _file_state(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {
            "required": False,
            "exists": False,
            "path": None,
            "size_bytes": 0,
            "non_empty": False,
        }

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
    return datetime.now(UTC).isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate scheduled report liveness evidence for #192.")
    parser.add_argument("--report-type", required=True, help="Report type: premarket, intraday, postmarket or weekly.")
    parser.add_argument("--report-file", required=True, help="Expected dated report file produced by the scheduled run.")
    parser.add_argument("--latest-file", required=True, help="Expected latest report file copied by the scheduled run.")
    parser.add_argument("--signals-file", default="reports/signals/latest-signals.json", help="Latest signals JSON required for market reports.")
    parser.add_argument(
        "--paper-health-file",
        default="reports/validation/latest-paper-observation-health.json",
        help="Latest paper observation health JSON required for market reports.",
    )
    parser.add_argument("--report-root", default=".", help="Repository/report root used for family freshness scanning.")
    parser.add_argument("--report-dir", default="reports/scheduled_report_liveness", help="Reserved for workflow clarity; output path remains canonical.")
    parser.add_argument("--run-timestamp", default=os.environ.get("HEALTH_RUN_TIMESTAMP") or os.environ.get("RUN_TIMESTAMP"))
    parser.add_argument("--workflow-name", default=os.environ.get("GITHUB_WORKFLOW"))
    parser.add_argument("--commit-sha", default=os.environ.get("GITHUB_SHA"))
    parser.add_argument("--run-date", default=os.environ.get("RUN_DATE"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = build_scheduled_report_liveness_artifact(
        report_type=args.report_type,
        report_file=args.report_file,
        latest_file=args.latest_file,
        signals_file=args.signals_file,
        paper_health_file=args.paper_health_file,
        run_timestamp=args.run_timestamp,
        workflow_name=args.workflow_name,
        commit_sha=args.commit_sha,
        run_date=args.run_date,
        report_root=args.report_root,
    )
    write_scheduled_report_liveness_artifact(result=result)

    print(f"Scheduled report liveness status: {result.artifact['scheduled_report_status']}")
    print(f"Report liveness status: {result.artifact['report_liveness_status']}")
    print(f"Current run state: {result.artifact['current_run_state']}")
    print(f"Report type: {result.artifact['report_type']}")
    print(f"Artifact: {result.artifact_path}")
    print(f"Latest artifact: {result.latest_artifact_path}")

    if result.errors:
        print("Errors:")
        for error in result.errors:
            print(f"- {error}")

    return 0 if result.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
