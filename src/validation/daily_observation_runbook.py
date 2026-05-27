from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

RUNBOOK_VERSION = "2026.05.27-v1"

REQUIRED_DAILY_STEPS = (
    "raw_contract_validated",
    "real_source_built",
    "daily_evidence_workflow_green",
    "artifact_reviewed",
    "cadence_review_passed",
    "exceptions_logged",
)

BLOCKED_CONFIRMATIONS = (
    "production_execution_enabled",
    "cash_deployment_authorized",
    "production_broker_credentials_used",
)


@dataclass(frozen=True)
class RunbookIssue:
    field: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RunbookReport:
    passed: bool
    report_date: str
    runbook_version: str
    observation_only: bool
    checklist_path: str
    completed_steps: list[str] = field(default_factory=list)
    missing_steps: list[str] = field(default_factory=list)
    issues: list[RunbookIssue] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "report_date": self.report_date,
            "runbook_version": self.runbook_version,
            "observation_only": self.observation_only,
            "checklist_path": self.checklist_path,
            "completed_steps": list(self.completed_steps),
            "missing_steps": list(self.missing_steps),
            "issues": [issue.to_dict() for issue in self.issues],
            "warnings": list(self.warnings),
        }


def write_runbook_template(path: Path, *, report_date: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "report_date": report_date,
        "operator": "manual-reviewer",
        "observation_only": True,
        "steps": {step: False for step in REQUIRED_DAILY_STEPS},
        "blocked_confirmations": {name: False for name in BLOCKED_CONFIRMATIONS},
        "artifact_name": f"daily-evidence-report-{report_date}",
        "notes": "Complete this checklist after reviewing the Daily Evidence artifact.",
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def review_daily_observation_runbook(checklist_path: Path, *, expected_report_date: str | None = None) -> RunbookReport:
    issues: list[RunbookIssue] = []
    payload = _read_payload(checklist_path, issues)
    if payload is None:
        return _build_report(
            checklist_path=checklist_path,
            report_date=expected_report_date or "unknown",
            completed_steps=[],
            missing_steps=list(REQUIRED_DAILY_STEPS),
            issues=issues,
        )

    report_date = str(payload.get("report_date", "")).strip()
    if not _is_valid_date(report_date):
        issues.append(RunbookIssue("report_date", "must be YYYY-MM-DD"))
    if expected_report_date and report_date != expected_report_date:
        issues.append(RunbookIssue("report_date", f"must match expected report date {expected_report_date}"))

    if payload.get("observation_only") is not True:
        issues.append(RunbookIssue("observation_only", "must be true"))

    steps = payload.get("steps")
    if not isinstance(steps, dict):
        issues.append(RunbookIssue("steps", "must be an object keyed by required daily step"))
        completed_steps: list[str] = []
        missing_steps = list(REQUIRED_DAILY_STEPS)
    else:
        completed_steps = [step for step in REQUIRED_DAILY_STEPS if steps.get(step) is True]
        missing_steps = [step for step in REQUIRED_DAILY_STEPS if steps.get(step) is not True]
        unknown_steps = sorted(set(steps) - set(REQUIRED_DAILY_STEPS))
        for step in unknown_steps:
            issues.append(RunbookIssue(f"steps.{step}", "unknown runbook step"))

    blocked = payload.get("blocked_confirmations", {})
    if not isinstance(blocked, dict):
        issues.append(RunbookIssue("blocked_confirmations", "must be an object"))
    else:
        for name in BLOCKED_CONFIRMATIONS:
            if blocked.get(name) is True:
                issues.append(RunbookIssue(f"blocked_confirmations.{name}", "must remain false"))

    return _build_report(
        checklist_path=checklist_path,
        report_date=report_date or expected_report_date or "unknown",
        completed_steps=completed_steps,
        missing_steps=missing_steps,
        issues=issues,
    )


def render_runbook_report_markdown(report: RunbookReport) -> str:
    lines = [
        "# Daily Real Paper Observation Runbook Review",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        f"Report date: `{report.report_date}`",
        f"Runbook version: `{report.runbook_version}`",
        f"Observation-only: **{str(report.observation_only).lower()}**",
        f"Checklist path: `{report.checklist_path}`",
        "",
        "## Completed steps",
        "",
    ]
    lines.extend(f"- {step}" for step in report.completed_steps) if report.completed_steps else lines.append("- none")
    lines.extend(["", "## Missing steps", ""])
    lines.extend(f"- {step}" for step in report.missing_steps) if report.missing_steps else lines.append("- none")
    lines.extend(["", "## Issues", ""])
    lines.extend(f"- `{issue.field}`: {issue.message}" for issue in report.issues) if report.issues else lines.append("- none")
    lines.extend(["", "## Warnings", ""])
    for warning in report.warnings:
        lines.append(f"- {warning}")
    return "\n".join(lines).rstrip() + "\n"


def write_runbook_report(report: RunbookReport, *, json_path: Path, markdown_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_runbook_report_markdown(report), encoding="utf-8")


def _read_payload(path: Path, issues: list[RunbookIssue]) -> dict[str, Any] | None:
    if not path.exists():
        issues.append(RunbookIssue("checklist_path", "checklist file is missing"))
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        issues.append(RunbookIssue("checklist_path", f"invalid JSON: {exc.msg}"))
        return None
    if not isinstance(payload, dict):
        issues.append(RunbookIssue("checklist_path", "checklist must contain a JSON object"))
        return None
    return payload


def _build_report(
    *,
    checklist_path: Path,
    report_date: str,
    completed_steps: list[str],
    missing_steps: list[str],
    issues: list[RunbookIssue],
) -> RunbookReport:
    warnings = [
        "B17 verifies daily observation discipline, not statistical edge.",
        "Paper observation and artifact review do not authorize production execution.",
        "Phase C may start with paper execution interfaces only.",
    ]
    return RunbookReport(
        passed=not issues and not missing_steps,
        report_date=report_date,
        runbook_version=RUNBOOK_VERSION,
        observation_only=True,
        checklist_path=str(checklist_path),
        completed_steps=completed_steps,
        missing_steps=missing_steps,
        issues=issues,
        warnings=warnings,
    )


def _is_valid_date(value: Any) -> bool:
    if isinstance(value, date) and not isinstance(value, datetime):
        return True
    if not isinstance(value, str):
        return False
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False
