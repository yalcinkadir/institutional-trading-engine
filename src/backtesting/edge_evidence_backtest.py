"""Gated edge-evidence backtest orchestration.

This module activates backtesting as an evidence pipeline, not as a loose script.
It fails closed when the universe is too small, when survivorship audit fails,
or when required historical bars are missing.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Literal

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
    OutOfSampleLockboxReport,
    build_out_of_sample_lockbox,
    write_out_of_sample_lockbox_report,
)
from src.validation.walk_forward_validation import (
    WalkForwardConfig,
    WalkForwardValidationReport,
    build_walk_forward_validation,
    write_walk_forward_report,
)

SurvivorshipMode = Literal["strict", "runtime_active_universe"]


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
    survivorship_mode: SurvivorshipMode = "strict"


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
    survivorship_mode: SurvivorshipMode = "strict"
    diagnostics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "reasons": list(self.reasons),
            "survivorship_mode": self.survivorship_mode,
            "universe_coverage": self.universe_coverage.to_dict(),
            "survivorship_audit": self.survivorship_audit.to_dict(),
            "trade_plan_count": self.trade_plan_count,
            "historical_result_count": self.historical_result_count,
            "walk_forward_passed": self.walk_forward_passed,
            "out_of_sample_passed": self.out_of_sample_passed,
            "output_dir": self.output_dir,
            "artifacts": self.artifacts,
            "diagnostics": self.diagnostics,
        }


def _load_trade_plans_fail_closed(path: Path) -> list[Any]:
    if not path.exists():
        return []
    return load_trade_plans(path)


def _audit_plans(
    universe: Any,
    plan_records: list[dict[str, Any]],
    *,
    survivorship_mode: SurvivorshipMode,
) -> SurvivorshipAuditReport:
    if survivorship_mode == "strict":
        return universe.audit_backtest_records(
            plan_records,
            symbol_field="symbol",
            date_field="signal_date",
        )
    if survivorship_mode == "runtime_active_universe":
        return _audit_runtime_active_universe(universe, plan_records)
    raise ValueError(f"unsupported survivorship_mode: {survivorship_mode}")


def _audit_runtime_active_universe(universe: Any, plan_records: list[dict[str, Any]]) -> SurvivorshipAuditReport:
    """Audit generated plans against a current active runtime universe.

    This mode is explicitly not final survivorship-safe evidence. It allows
    exploratory Polygon runtime backtests where historical bars are available
    but point-in-time lifecycle membership is not yet available. It still fails
    on unknown symbols so bad or unmapped tickers cannot silently pass.
    """
    total = 0
    valid = 0
    unknown = 0
    unknown_samples: list[str] = []
    for record in plan_records:
        if not isinstance(record, dict):
            continue
        total += 1
        symbol = str(record.get("symbol") or "").upper()
        if not symbol or universe.lookup(symbol) is None:
            unknown += 1
            if symbol and len(unknown_samples) < 25 and symbol not in unknown_samples:
                unknown_samples.append(symbol)
            continue
        valid += 1
    return SurvivorshipAuditReport(
        total_records=total,
        valid_records=valid,
        out_of_window_records=0,
        unknown_ticker_records=unknown,
        out_of_window_samples=[],
        unknown_ticker_samples=unknown_samples,
    )


def run_edge_evidence_backtest(config: EdgeEvidenceBacktestConfig) -> EdgeEvidenceBacktestReport:
    config.output_dir.mkdir(parents=True, exist_ok=True)

    universe = load_survivorship_universe(config.universe_path)
    coverage = validate_universe_coverage(
        universe,
        config.as_of,
        minimum_tradeable_count=config.minimum_tradeable_count,
    )
    plans = _load_trade_plans_fail_closed(config.trade_plans_path)
    plan_records = [asdict(plan) for plan in plans]
    audit = _audit_plans(
        universe,
        plan_records,
        survivorship_mode=config.survivorship_mode,
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
            survivorship_mode=config.survivorship_mode,
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

    diagnostics = build_edge_evidence_diagnostics(
        validation_records,
        walk_forward_report=walk_forward_report,
        oos_report=oos_report,
    )
    diagnostics_json = config.output_dir / "edge-evidence-diagnostics.json"
    diagnostics_md = config.output_dir / "edge-evidence-diagnostics.md"
    _write_diagnostics(diagnostics, json_path=diagnostics_json, markdown_path=diagnostics_md)

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
        survivorship_mode=config.survivorship_mode,
        diagnostics=diagnostics,
        artifacts={
            "summary_json": str(summary_json),
            "summary_md": str(summary_md),
            "historical_json": str(historical_json),
            "historical_md": str(historical_md),
            "walk_forward_json": str(walk_forward_json),
            "walk_forward_md": str(walk_forward_md),
            "out_of_sample_json": str(oos_json),
            "out_of_sample_md": str(oos_md),
            "diagnostics_json": str(diagnostics_json),
            "diagnostics_md": str(diagnostics_md),
        },
    )
    _write_summary(report, json_path=summary_json, markdown_path=summary_md)
    return report


def build_edge_evidence_diagnostics(
    validation_records: list[dict[str, Any]],
    *,
    walk_forward_report: WalkForwardValidationReport,
    oos_report: OutOfSampleLockboxReport,
) -> dict[str, Any]:
    result_values: list[float] = []
    missing_result_count = 0
    for record in validation_records:
        value = _extract_result_value(record)
        if value is None:
            missing_result_count += 1
            continue
        result_values.append(value)

    positive = [value for value in result_values if value > 0]
    negative = [value for value in result_values if value < 0]
    breakeven = len(result_values) - len(positive) - len(negative)
    failure_reasons = Counter(str(record.get("reason") or "unknown") for record in validation_records)

    failing_cycles = [result for result in walk_forward_report.cycle_results if not result.passed]
    failed_degradation_checks = [check for check in oos_report.degradation_checks if not check.passed]

    return {
        "historical_results": {
            "total": len(result_values),
            "missing_result_count": missing_result_count,
            "wins": len(positive),
            "losses": len(negative),
            "breakeven": breakeven,
            "win_rate": _safe_ratio(len(positive), len(result_values)),
            "average_r": _rounded(sum(result_values) / len(result_values)) if result_values else 0.0,
            "cumulative_r": _rounded(sum(result_values)),
            "top_result_reasons": dict(failure_reasons.most_common(10)),
        },
        "walk_forward": {
            "passed": walk_forward_report.passed,
            "generated_cycles": walk_forward_report.generated_cycles,
            "passing_cycles": walk_forward_report.passing_cycles,
            "failing_cycles": len(failing_cycles),
            "min_required_cycles": walk_forward_report.min_required_cycles,
            "min_required_passing_cycles": walk_forward_report.min_required_passing_cycles,
            "unassigned_records": walk_forward_report.unassigned_records,
            "failing_cycle_samples": [
                {
                    "cycle": result.cycle.cycle_number,
                    "test_records": result.test_records,
                    "expectancy_r": result.validation_report.metrics.expectancy_r,
                    "profit_factor": result.validation_report.metrics.profit_factor,
                    "sharpe_ratio": result.validation_report.metrics.sharpe_ratio,
                    "failed_gates": [gate.name for gate in result.validation_report.gates if not gate.passed],
                }
                for result in failing_cycles[:10]
            ],
        },
        "out_of_sample": {
            "passed": oos_report.passed,
            "split_date": oos_report.split_date,
            "in_sample_count": oos_report.in_sample_count,
            "out_of_sample_count": oos_report.out_of_sample_count,
            "unassigned_records": oos_report.unassigned_records,
            "in_sample_metrics": oos_report.in_sample_report.metrics.to_dict(),
            "out_of_sample_metrics": oos_report.out_of_sample_report.metrics.to_dict(),
            "failed_degradation_checks": [
                {
                    "metric": check.metric,
                    "in_sample_value": check.in_sample_value,
                    "out_of_sample_value": check.out_of_sample_value,
                    "degradation": check.degradation,
                    "max_allowed_degradation": check.max_allowed_degradation,
                }
                for check in failed_degradation_checks
            ],
            "failed_oos_gates": [gate.name for gate in oos_report.out_of_sample_report.gates if not gate.passed],
        },
    }


def _result_to_validation_record(result: Any) -> dict[str, Any]:
    payload = result.to_dict()
    r_multiple = _optional_float(payload.get("r_multiple"))
    return {
        **payload,
        "result_r": r_multiple,
        "exit_date": payload.get("exit_date") or payload.get("signal_date"),
    }


def _extract_result_value(record: Any) -> float | None:
    if not isinstance(record, dict):
        return None
    if "result_r" in record:
        return _optional_float(record.get("result_r"))
    if "r_multiple" in record:
        return _optional_float(record.get("r_multiple"))
    return None


def _write_diagnostics(diagnostics: dict[str, Any], *, json_path: Path, markdown_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(diagnostics, indent=2), encoding="utf-8")
    markdown_path.write_text(_render_diagnostics(diagnostics), encoding="utf-8")


def _render_diagnostics(diagnostics: dict[str, Any]) -> str:
    historical = diagnostics["historical_results"]
    walk_forward = diagnostics["walk_forward"]
    oos = diagnostics["out_of_sample"]
    lines = [
        "# Edge Evidence Diagnostics",
        "",
        "## Historical Results",
        "",
        f"- Total results: **{historical['total']}**",
        f"- Missing result records: **{historical.get('missing_result_count', 0)}**",
        f"- Wins / losses / breakeven: **{historical['wins']} / {historical['losses']} / {historical['breakeven']}**",
        f"- Win rate: **{historical['win_rate']:.2%}**",
        f"- Average R: **{historical['average_r']:.4f}**",
        f"- Cumulative R: **{historical['cumulative_r']:.4f}**",
        "",
        "### Top Result Reasons",
        "",
    ]
    for reason, count in historical["top_result_reasons"].items():
        lines.append(f"- {reason}: {count}")

    lines.extend(
        [
            "",
            "## Walk-Forward Diagnostics",
            "",
            f"- Status: **{'PASS' if walk_forward['passed'] else 'FAIL'}**",
            f"- Generated cycles: **{walk_forward['generated_cycles']}**",
            f"- Passing cycles: **{walk_forward['passing_cycles']}**",
            f"- Failing cycles: **{walk_forward['failing_cycles']}**",
            f"- Minimum required cycles: **{walk_forward['min_required_cycles']}**",
            f"- Minimum required passing cycles: **{walk_forward['min_required_passing_cycles']}**",
            f"- Unassigned records: **{walk_forward['unassigned_records']}**",
            "",
            "### Failing Cycle Samples",
            "",
            "| Cycle | Test Records | Expectancy R | Profit Factor | Sharpe | Failed Gates |",
            "|---:|---:|---:|---:|---:|---|",
        ]
    )
    for item in walk_forward["failing_cycle_samples"]:
        lines.append(
            f"| {item['cycle']} | {item['test_records']} | {item['expectancy_r']:.4f} | "
            f"{_format_number(item['profit_factor'])} | {item['sharpe_ratio']:.4f} | "
            f"{', '.join(item['failed_gates']) or '-'} |"
        )

    in_metrics = oos["in_sample_metrics"]
    out_metrics = oos["out_of_sample_metrics"]
    lines.extend(
        [
            "",
            "## Out-of-Sample Diagnostics",
            "",
            f"- Status: **{'PASS' if oos['passed'] else 'FAIL'}**",
            f"- Split date: `{oos['split_date']}`",
            f"- In-sample count: **{oos['in_sample_count']}**",
            f"- Out-of-sample count: **{oos['out_of_sample_count']}**",
            f"- Unassigned records: **{oos['unassigned_records']}**",
            "",
            "| Segment | Trades | Expectancy R | Profit Factor | Max DD R | Sharpe |",
            "|---|---:|---:|---:|---:|---:|",
            _diagnostic_metrics_row("in_sample", in_metrics),
            _diagnostic_metrics_row("out_of_sample", out_metrics),
            "",
            "### Failed OOS Gates",
            "",
        ]
    )
    failed_oos_gates = oos["failed_oos_gates"]
    lines.append("- " + (", ".join(failed_oos_gates) if failed_oos_gates else "-"))

    lines.extend(["", "### Failed Degradation Checks", ""])
    if oos["failed_degradation_checks"]:
        for item in oos["failed_degradation_checks"]:
            lines.append(
                f"- {item['metric']}: in-sample={_format_number(item['in_sample_value'])}, "
                f"OOS={_format_number(item['out_of_sample_value'])}, "
                f"degradation={item['degradation']:.2%}, max={item['max_allowed_degradation']:.2%}"
            )
    else:
        lines.append("- -")
    return "\n".join(lines).rstrip() + "\n"


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
        f"Survivorship mode: **{report.survivorship_mode}**",
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
        "## Diagnostics Snapshot",
        "",
    ]
    if report.diagnostics:
        historical = report.diagnostics.get("historical_results", {})
        walk_forward = report.diagnostics.get("walk_forward", {})
        oos = report.diagnostics.get("out_of_sample", {})
        lines.extend(
            [
                f"- Average R: {_format_number(historical.get('average_r', 0.0))}",
                f"- Missing result records: {historical.get('missing_result_count', 0)}",
                f"- Win rate: {float(historical.get('win_rate', 0.0)):.2%}",
                f"- Walk-forward cycles: {walk_forward.get('passing_cycles', 0)}/{walk_forward.get('generated_cycles', 0)} passing",
                f"- OOS records: {oos.get('out_of_sample_count', 0)}",
                "",
            ]
        )
    else:
        lines.extend(["- -", ""])
    lines.extend(["## Artifacts", ""])
    for name, path in sorted(report.artifacts.items()):
        lines.append(f"- {name}: `{path}`")
    return "\n".join(lines).rstrip() + "\n"


def _diagnostic_metrics_row(label: str, metrics: dict[str, Any]) -> str:
    return (
        f"| {label} | {metrics.get('total_trades', 0)} | {_format_number(metrics.get('expectancy_r', 0.0))} | "
        f"{_format_number(metrics.get('profit_factor', 0.0))} | {_format_number(metrics.get('max_drawdown', 0.0))} | "
        f"{_format_number(metrics.get('sharpe_ratio', 0.0))} |"
    )


def _safe_ratio(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 6) if denominator else 0.0


def _rounded(value: float) -> float:
    return round(float(value), 6)


def _optional_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _format_number(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if number == float("inf"):
        return "inf"
    return f"{number:.4f}"
