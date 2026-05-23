"""Scheduled Live Decision-Support dry-run reporting.

P28 wraps readiness review into a scheduled/manual operations report. It never
places trades, never contacts a broker, and never authorizes live execution.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.operations.operational_readiness_review import (
    OperationalReadinessReport,
    run_operational_readiness_review,
)


@dataclass(frozen=True)
class ScheduledDryRunReport:
    run_mode: str
    generated_at_utc: str
    ready_for_live_decision_support_review: bool
    readiness_report: OperationalReadinessReport
    input_paths: dict[str, str]
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_mode": self.run_mode,
            "generated_at_utc": self.generated_at_utc,
            "ready_for_live_decision_support_review": self.ready_for_live_decision_support_review,
            "readiness_report": self.readiness_report.to_dict(),
            "input_paths": self.input_paths,
            "notes": self.notes,
        }


def run_scheduled_decision_support_dry_run(
    *,
    run_mode: str = "manual",
    backtest_report: Path = Path("reports/backtests/historical-entry-exit-backtest.json"),
    oos_report: Path = Path("reports/backtests/out-of-sample-validation.json"),
    paper_live_report: Path = Path("reports/paper-live/paper-live-observation.json"),
    portfolio_state: Path = Path("data/portfolio_state.json"),
    min_backtest_plans: int = 1,
    min_oos_plans: int = 1,
) -> ScheduledDryRunReport:
    readiness = run_operational_readiness_review(
        backtest_report=backtest_report,
        oos_report=oos_report,
        paper_live_report=paper_live_report,
        portfolio_state=portfolio_state,
        min_backtest_plans=min_backtest_plans,
        min_oos_plans=min_oos_plans,
    )
    notes = [
        "Scheduled Decision-Support dry run is observation-only.",
        "No broker execution is performed.",
        "No trading authorization is produced.",
    ]
    return ScheduledDryRunReport(
        run_mode=run_mode,
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        ready_for_live_decision_support_review=readiness.ready_for_live_decision_support_review,
        readiness_report=readiness,
        input_paths={
            "backtest_report": str(backtest_report),
            "oos_report": str(oos_report),
            "paper_live_report": str(paper_live_report),
            "portfolio_state": str(portfolio_state),
        },
        notes=notes,
    )


def render_scheduled_dry_run_markdown(report: ScheduledDryRunReport) -> str:
    lines = [
        "# Scheduled Live Decision-Support Dry Run",
        "",
        f"Run mode: `{report.run_mode}`",
        f"Generated at UTC: `{report.generated_at_utc}`",
        f"Ready for live Decision-Support review: `{report.ready_for_live_decision_support_review}`",
        "",
        "## Input Paths",
        "",
        "| Input | Path |",
        "|---|---|",
    ]
    for key, value in report.input_paths.items():
        lines.append(f"| {key} | {value} |")
    lines.extend(["", "## Readiness Gates", "", "| Gate | Status | Message |", "|---|---:|---|"])
    for gate in report.readiness_report.gates:
        status = "PASS" if gate.passed else "FAIL"
        lines.append(f"| {gate.name} | {status} | {gate.message} |")
    lines.extend(["", "## Readiness Summary", "", "| Metric | Value |", "|---|---:|"])
    for key, value in report.readiness_report.summary.items():
        lines.append(f"| {key} | {value} |")
    lines.extend(["", "## Guardrail", ""])
    for note in report.notes:
        lines.append(f"- {note}")
    return "\n".join(lines) + "\n"


def write_scheduled_dry_run_report(
    report: ScheduledDryRunReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_scheduled_dry_run_markdown(report), encoding="utf-8")
