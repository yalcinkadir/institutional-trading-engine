from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class PerformanceDriftConfig:
    min_backtest_observations: int = 30
    min_forward_observations: int = 10
    max_abs_expectancy_drift_r: float = 0.25
    max_abs_win_rate_drift: float = 0.15
    max_abs_cumulative_drift_r: float = 5.0
    max_abs_z_score: float = 2.0
    require_positive_forward_expectancy: bool = True


@dataclass(frozen=True)
class PerformanceDriftMetrics:
    backtest_observations: int
    forward_observations: int
    backtest_expectancy_r: float
    forward_expectancy_r: float
    expectancy_drift_r: float
    backtest_win_rate: float
    forward_win_rate: float
    win_rate_drift: float
    backtest_total_r: float
    forward_total_r: float
    cumulative_drift_r: float
    backtest_std_r: float
    standard_error_r: float
    z_score: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PerformanceDriftGate:
    name: str
    passed: bool
    value: float | int | bool
    threshold: float | int | bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PerformanceDriftReport:
    passed: bool
    metrics: PerformanceDriftMetrics
    gates: list[PerformanceDriftGate] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "metrics": self.metrics.to_dict(),
            "gates": [gate.to_dict() for gate in self.gates],
        }


def detect_performance_drift(
    backtest_records: Iterable[dict[str, Any] | float | int],
    forward_records: Iterable[dict[str, Any] | float | int],
    *,
    config: PerformanceDriftConfig = PerformanceDriftConfig(),
    result_field: str = "result_r",
) -> PerformanceDriftReport:
    backtest_values = _extract_r_values(backtest_records, result_field=result_field)
    forward_values = _extract_r_values(forward_records, result_field=result_field)
    metrics = _calculate_metrics(backtest_values, forward_values)
    gates = _build_gates(metrics, config=config)
    return PerformanceDriftReport(
        passed=all(gate.passed for gate in gates),
        metrics=metrics,
        gates=gates,
    )


def render_performance_drift_markdown(report: PerformanceDriftReport) -> str:
    metrics = report.metrics
    lines = [
        "# Performance Drift Detection",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        "",
        "## Metrics",
        "",
        f"- Backtest observations: {metrics.backtest_observations}",
        f"- Forward observations: {metrics.forward_observations}",
        f"- Backtest expectancy R: {metrics.backtest_expectancy_r:.4f}",
        f"- Forward expectancy R: {metrics.forward_expectancy_r:.4f}",
        f"- Expectancy drift R: {metrics.expectancy_drift_r:.4f}",
        f"- Backtest win rate: {metrics.backtest_win_rate:.2%}",
        f"- Forward win rate: {metrics.forward_win_rate:.2%}",
        f"- Win-rate drift: {metrics.win_rate_drift:.2%}",
        f"- Backtest total R: {metrics.backtest_total_r:.4f}",
        f"- Forward total R: {metrics.forward_total_r:.4f}",
        f"- Cumulative drift R: {metrics.cumulative_drift_r:.4f}",
        f"- Backtest std R: {metrics.backtest_std_r:.4f}",
        f"- Standard error R: {metrics.standard_error_r:.4f}",
        f"- Z-score: {metrics.z_score:.4f}",
        "",
        "## Gates",
        "",
        "| Gate | Status | Value | Threshold |",
        "|---|---:|---:|---:|",
    ]
    for gate in report.gates:
        lines.append(
            f"| {gate.name} | {'PASS' if gate.passed else 'FAIL'} | "
            f"{_format_value(gate.value)} | {_format_value(gate.threshold)} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def write_performance_drift_report(
    report: PerformanceDriftReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_performance_drift_markdown(report), encoding="utf-8")


def _calculate_metrics(backtest_values: list[float], forward_values: list[float]) -> PerformanceDriftMetrics:
    backtest_expectancy = _mean(backtest_values)
    forward_expectancy = _mean(forward_values)
    backtest_total = sum(backtest_values)
    forward_total = sum(forward_values)
    expected_forward_total = backtest_expectancy * len(forward_values)
    cumulative_drift = forward_total - expected_forward_total
    backtest_std = _sample_std(backtest_values)
    standard_error = backtest_std / math.sqrt(len(forward_values)) if forward_values else 0.0
    z_score = (forward_expectancy - backtest_expectancy) / standard_error if standard_error > 0 else 0.0

    return PerformanceDriftMetrics(
        backtest_observations=len(backtest_values),
        forward_observations=len(forward_values),
        backtest_expectancy_r=round(backtest_expectancy, 6),
        forward_expectancy_r=round(forward_expectancy, 6),
        expectancy_drift_r=round(forward_expectancy - backtest_expectancy, 6),
        backtest_win_rate=round(_win_rate(backtest_values), 6),
        forward_win_rate=round(_win_rate(forward_values), 6),
        win_rate_drift=round(_win_rate(forward_values) - _win_rate(backtest_values), 6),
        backtest_total_r=round(backtest_total, 6),
        forward_total_r=round(forward_total, 6),
        cumulative_drift_r=round(cumulative_drift, 6),
        backtest_std_r=round(backtest_std, 6),
        standard_error_r=round(standard_error, 6),
        z_score=round(z_score, 6),
    )


def _build_gates(metrics: PerformanceDriftMetrics, *, config: PerformanceDriftConfig) -> list[PerformanceDriftGate]:
    return [
        PerformanceDriftGate(
            name="minimum_backtest_observations",
            passed=metrics.backtest_observations >= config.min_backtest_observations,
            value=metrics.backtest_observations,
            threshold=config.min_backtest_observations,
            message="Backtest sample must be large enough to serve as a baseline.",
        ),
        PerformanceDriftGate(
            name="minimum_forward_observations",
            passed=metrics.forward_observations >= config.min_forward_observations,
            value=metrics.forward_observations,
            threshold=config.min_forward_observations,
            message="Forward sample must be large enough before drift is trusted.",
        ),
        PerformanceDriftGate(
            name="positive_forward_expectancy",
            passed=(not config.require_positive_forward_expectancy) or metrics.forward_expectancy_r > 0,
            value=metrics.forward_expectancy_r,
            threshold=0.0,
            message="Forward observation expectancy should stay positive.",
        ),
        PerformanceDriftGate(
            name="expectancy_drift_r",
            passed=abs(metrics.expectancy_drift_r) <= config.max_abs_expectancy_drift_r,
            value=abs(metrics.expectancy_drift_r),
            threshold=config.max_abs_expectancy_drift_r,
            message="Forward expectancy should not drift too far from the backtest baseline.",
        ),
        PerformanceDriftGate(
            name="win_rate_drift",
            passed=abs(metrics.win_rate_drift) <= config.max_abs_win_rate_drift,
            value=abs(metrics.win_rate_drift),
            threshold=config.max_abs_win_rate_drift,
            message="Forward win rate should not drift too far from the backtest baseline.",
        ),
        PerformanceDriftGate(
            name="cumulative_drift_r",
            passed=abs(metrics.cumulative_drift_r) <= config.max_abs_cumulative_drift_r,
            value=abs(metrics.cumulative_drift_r),
            threshold=config.max_abs_cumulative_drift_r,
            message="Total forward R should remain within configured drift tolerance.",
        ),
        PerformanceDriftGate(
            name="z_score",
            passed=abs(metrics.z_score) <= config.max_abs_z_score,
            value=abs(metrics.z_score),
            threshold=config.max_abs_z_score,
            message="Forward expectancy should not deviate too far in standard-error units.",
        ),
    ]


def _extract_r_values(records: Iterable[dict[str, Any] | float | int], *, result_field: str) -> list[float]:
    values: list[float] = []
    for record in records:
        raw_value: Any
        if isinstance(record, dict):
            raw_value = record.get(result_field, record.get("r_multiple", record.get("paper_r")))
        else:
            raw_value = record
        value = _safe_float(raw_value)
        if value is not None:
            values.append(value)
    return values


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _sample_std(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean = _mean(values)
    variance = sum((value - mean) ** 2 for value in values) / (len(values) - 1)
    return math.sqrt(variance)


def _win_rate(values: list[float]) -> float:
    return sum(1 for value in values if value > 0) / len(values) if values else 0.0


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _format_value(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)
