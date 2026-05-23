"""Operational readiness review before live Decision-Support scheduling.

P27 consolidates existing validation artifacts. It does not place trades,
mutate scoring, or contact a broker.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ReadinessGate:
    name: str
    passed: bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class OperationalReadinessReport:
    ready_for_live_decision_support_review: bool
    gates: list[ReadinessGate] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ready_for_live_decision_support_review": self.ready_for_live_decision_support_review,
            "gates": [gate.to_dict() for gate in self.gates],
            "summary": self.summary,
            "notes": self.notes,
        }


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def _metric(payload: dict[str, Any] | None, *keys: str) -> Any:
    current: Any = payload
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def run_operational_readiness_review(
    *,
    backtest_report: Path = Path("reports/backtests/historical-entry-exit-backtest.json"),
    oos_report: Path = Path("reports/backtests/out-of-sample-validation.json"),
    paper_live_report: Path = Path("reports/paper-live/paper-live-observation.json"),
    portfolio_state: Path = Path("data/portfolio_state.json"),
    min_backtest_plans: int = 1,
    min_oos_plans: int = 1,
) -> OperationalReadinessReport:
    backtest = _load_json(backtest_report)
    oos = _load_json(oos_report)
    paper_live = _load_json(paper_live_report)
    portfolio = _load_json(portfolio_state)

    backtest_total = _metric(backtest, "metrics", "total") or 0
    oos_count = _metric(oos, "out_of_sample_count") or 0
    paper_ready = bool(_metric(paper_live, "ready_for_review"))
    drawdown = _metric(portfolio, "drawdown_percent")
    daily_loss = _metric(portfolio, "daily_loss_percent")

    gates = [
        ReadinessGate(
            name="historical_backtest_report_present",
            passed=backtest is not None,
            message=f"path: {backtest_report}",
        ),
        ReadinessGate(
            name="historical_backtest_has_plans",
            passed=int(backtest_total) >= min_backtest_plans,
            message=f"plans: {backtest_total} / required: {min_backtest_plans}",
        ),
        ReadinessGate(
            name="out_of_sample_report_present",
            passed=oos is not None,
            message=f"path: {oos_report}",
        ),
        ReadinessGate(
            name="out_of_sample_has_plans",
            passed=int(oos_count) >= min_oos_plans,
            message=f"out-of-sample plans: {oos_count} / required: {min_oos_plans}",
        ),
        ReadinessGate(
            name="paper_live_report_present",
            passed=paper_live is not None,
            message=f"path: {paper_live_report}",
        ),
        ReadinessGate(
            name="paper_live_ready_for_review",
            passed=paper_ready,
            message=f"ready_for_review: {paper_ready}",
        ),
        ReadinessGate(
            name="portfolio_state_present",
            passed=portfolio is not None,
            message=f"path: {portfolio_state}",
        ),
        ReadinessGate(
            name="portfolio_drawdown_available",
            passed=drawdown is not None,
            message=f"drawdown_percent: {drawdown}",
        ),
        ReadinessGate(
            name="portfolio_daily_loss_available",
            passed=daily_loss is not None,
            message=f"daily_loss_percent: {daily_loss}",
        ),
    ]

    ready = all(gate.passed for gate in gates)
    summary = {
        "backtest_total": backtest_total,
        "backtest_expectancy_r": _metric(backtest, "metrics", "expectancy_r"),
        "out_of_sample_count": oos_count,
        "out_of_sample_expectancy_r": _metric(oos, "out_of_sample_metrics", "expectancy_r"),
        "paper_live_ready_for_review": paper_ready,
        "paper_live_terminal_event_count": _metric(paper_live, "terminal_event_count"),
        "portfolio_drawdown_percent": drawdown,
        "portfolio_daily_loss_percent": daily_loss,
    }
    notes = [
        "Operational readiness review is not a trading authorization.",
        "Live Decision-Support scheduling still requires human review of artifacts.",
        "Broker execution remains out of scope.",
    ]
    return OperationalReadinessReport(
        ready_for_live_decision_support_review=ready,
        gates=gates,
        summary=summary,
        notes=notes,
    )


def render_operational_readiness_markdown(report: OperationalReadinessReport) -> str:
    lines = [
        "# Operational Readiness Review",
        "",
        f"Ready for live Decision-Support review: `{report.ready_for_live_decision_support_review}`",
        "",
        "## Gates",
        "",
        "| Gate | Status | Message |",
        "|---|---:|---|",
    ]
    for gate in report.gates:
        status = "PASS" if gate.passed else "FAIL"
        lines.append(f"| {gate.name} | {status} | {gate.message} |")
    lines.extend(["", "## Summary", "", "| Metric | Value |", "|---|---:|"])
    for key, value in report.summary.items():
        lines.append(f"| {key} | {value} |")
    lines.extend(["", "## Guardrail", ""])
    for note in report.notes:
        lines.append(f"- {note}")
    return "\n".join(lines) + "\n"


def write_operational_readiness_report(
    report: OperationalReadinessReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_operational_readiness_markdown(report), encoding="utf-8")
