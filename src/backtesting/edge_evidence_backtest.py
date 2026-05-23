"""Gated edge-evidence backtest orchestration.

This module activates backtesting as an evidence pipeline, not as a loose script.
It fails closed when the universe is too small, when survivorship audit fails,
or when required historical bars are missing.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from src.backtesting.historical_entry_exit_backtest import load_trade_plans, run_backtest
from src.backtesting.historical_report import write_report as write_historical_backtest_report
from src.data.survivorship_universe import (
    SurvivorshipAuditReport,
    UniverseCoverageReport,
    load_survivorship_universe,
    validate_universe_coverage,
)
from src.validation.out_of_sample_lockbox import (
    OutOfSampleLockboxConfig,
    build_out_of_sample_lockbox,
    write_out_of_sample_lockbox_report,
)
from src.validation.walk_forward_validation import (
    WalkForwardConfig,
    build_walk_forward_validation,
    write_walk_forward_report,
)


@dataclass(frozen=True)
class EdgeEvidenceBacktestConfig:
    universe_path: Path
    trade_plans_path: Path
    bars_root: Path
    output_dir: Path = Path("reports/edge_evidence")
    as_of: date = date(2026, 5, 24)
    minimum_tradeable_count: int = 500
    oos_split_date: date = date(2024, 1, 1)
    max_bars_per_plan: int = 20


@dataclass(frozen=True)
class EdgeEvidenceBacktestReport:
    passed: bool
    reasons: tuple[str, ...]
    universe_coverage: UniverseCoverageReport
    survivorship_audit: SurvivorshipAuditReport
    trade_plan_count: int
    historical_result_count: int = 0
    walk_forward_passed: bool = False
    out_of_sample_passed: bool = False
    output_dir: str = ""
    artifacts: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "reasons": list(self.reasons),
            "universe_coverage": self.universe_coverage.to_dict(),
            "survivorship_audit": self.survivorship_audit.to_dict(),
            "trade_plan_count": self.trade_plan_count,
            "historical_result_count": self.historical_result_count,
            "walk_forward_passed": self.walk_forward_passed,
            "out_of_sample_passed": self.out_of_sample_passed,
            "output_dir": self.output_dir,
            "artifacts": self.artifacts,
        }


def run_edge_evidence_backtest(config: EdgeEvidenceBacktestConfig) -> EdgeEvidenceBacktestReport:
    config.output_dir.mkdir(parents=True, exist_ok=True)

    universe = load_survivorship_universe(config.universe_path)
    coverage = validate_universe_coverage(
        universe,
        config.as_of,
        minimum_tradeable_count=config.minimum_tradeable_count,
    )
    plans = load_trade_plans(config.trade_plans_path)
    plan_records = [asdict(plan) for plan in plans]
    audit = universe.audit_backtest_records(
        plan_records,
        symbol_field="symbol",
        date_field="signal_date",
    )

    reasons: list[str] = []
    if not coverage.passed:
        reasons.append("universe_coverage_below_minimum")
    if not audit.passed:
        reasons.append("survivorship_audit_failed")
    if not plans:
        reasons.append("no_trade_plans_loaded")

    summary_json = config.output_dir / "edge-evidence-summary.json"
    summary_md = config.output_dir / "edge-evidence-summary.md"

    if reasons:
        report = EdgeEvidenceBacktestReport(
            passed=False,
            reasons=tuple(reasons),
            universe_coverage=coverage,
            survivorship_audit=audit,
            trade_plan_count=len(plans),
            output_dir=str(config.output_dir),
        )
        _write_summary(report, json_path=summary_json, markdown_path=summary_md)
        return report

    backtest_report = run_backtest(
        plans,
        bars_root=config.bars_root,
        max_bars=config.max_bars_per_plan,
    )
    historical_json = config.output_dir / "historical-entry-exit-backtest.json"
    historical_md = config.output_dir / "historical-entry-exit-backtest.md"
    write_historical_backtest_report(
        backtest_report,
        json_path=historical_json,
        markdown_path=historical_md,
    )

    validation_records = [_result_to_validation_record(result) for result in backtest_report.results]

    walk_forward_report = build_walk_forward_validation(
        validation_records,
        config=WalkForwardConfig(),
        date_field="exit_date",
        result_field="result_r",
    )
    walk_forward_json = config.output_dir / "walk-forward-validation.json"
    walk_forward_md = config.output_dir / "walk-forward-validation.md"
    write_walk_forward_report(
        walk_forward_report,
        json_path=walk_forward_json,
        markdown_path=walk_forward_md,
    )

    oos_report = build_out_of_sample_lockbox(
        validation_records,
        config=OutOfSampleLockboxConfig(split_date=config.oos_split_date),
        date_field="exit_date",
        result_field="result_r",
    )
    oos_json = config.output_dir / "out-of-sample-lockbox.json"
    oos_md = config.output_dir / "out-of-sample-lockbox.md"
    write_out_of_sample_lockbox_report(
        oos_report,
        json_path=oos_json,
        markdown_path=oos_md,
    )

    if not walk_forward_report.passed:
        reasons.append("walk_forward_failed")
    if not oos_report.passed:
        reasons.append("out_of_sample_lockbox_failed")

    report = EdgeEvidenceBacktestReport(
        passed=not reasons,
        reasons=tuple(reasons),
        universe_coverage=coverage,
        survivorship_audit=audit,
        trade_plan_count=len(plans),
        historical_result_count=len(backtest_report.results),
        walk_forward_passed=walk_forward_report.passed,
        out_of_sample_passed=oos_report.passed,
        output_dir=str(config.output_dir),
        artifacts={
            "summary_json": str(summary_json),
            "summary_md": str(summary_md),
            "historical_json": str(historical_json),
            "historical_md": str(historical_md),
            "walk_forward_json": str(walk_forward_json),
            "walk_forward_md": str(walk_forward_md),
            "out_of_sample_json": str(oos_json),
            "out_of_sample_md": str(oos_md),
        },
    )
    _write_summary(report, json_path=summary_json, markdown_path=summary_md)
    return report


def _result_to_validation_record(result: Any) -> dict[str, Any]:
    payload = result.to_dict()
    return {
        **payload,
        "result_r": float(payload.get("r_multiple") or 0.0),
        "exit_date": payload.get("exit_date") or payload.get("signal_date"),
    }


def _write_summary(report: EdgeEvidenceBacktestReport, *, json_path: Path, markdown_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(_render_summary(report), encoding="utf-8")


def _render_summary(report: EdgeEvidenceBacktestReport) -> str:
    lines = [
        "# Edge Evidence Backtest",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        f"Reasons: **{', '.join(report.reasons) if report.reasons else '-'}**",
        "",
        "## Gates",
        "",
        f"- Universe coverage: {'PASS' if report.universe_coverage.passed else 'FAIL'} "
        f"({report.universe_coverage.tradeable_count}/{report.universe_coverage.minimum_tradeable_count})",
        f"- Survivorship audit: {'PASS' if report.survivorship_audit.passed else 'FAIL'}",
        f"- Trade plans loaded: {report.trade_plan_count}",
        f"- Historical results: {report.historical_result_count}",
        f"- Walk-forward: {'PASS' if report.walk_forward_passed else 'FAIL'}",
        f"- Out-of-sample lockbox: {'PASS' if report.out_of_sample_passed else 'FAIL'}",
        "",
        "## Artifacts",
        "",
    ]
    for name, path in sorted(report.artifacts.items()):
        lines.append(f"- {name}: `{path}`")
    return "\n".join(lines).rstrip() + "\n"
