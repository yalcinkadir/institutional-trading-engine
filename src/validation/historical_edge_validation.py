from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

from src.validation.statistical_robustness import (
    StatisticalRobustnessMetrics,
    calculate_statistical_robustness,
)

MIN_TOTAL_TRADES = 300
MIN_PROFIT_FACTOR = 1.4
MIN_EXPECTANCY_R = 0.5
MAX_DRAWDOWN_LIMIT = 0.25
MIN_SHARPE_RATIO = 0.10
MIN_DEFLATED_SHARPE_PROBABILITY = 0.95
SHARPE_DEFINITION_VERSION = "per-trade-sharpe-2026.05.29-v1"


@dataclass(frozen=True)
class HistoricalEdgeValidationConfig:
    min_total_trades: int = MIN_TOTAL_TRADES
    min_profit_factor: float = MIN_PROFIT_FACTOR
    min_expectancy_r: float = MIN_EXPECTANCY_R
    max_drawdown_limit: float = MAX_DRAWDOWN_LIMIT
    min_sharpe_ratio: float = MIN_SHARPE_RATIO
    min_deflated_sharpe_probability: float = MIN_DEFLATED_SHARPE_PROBABILITY
    estimated_trials: int = 1
    bootstrap_iterations: int = 1000
    bootstrap_confidence_level: float = 0.95
    bootstrap_seed: int = 7
    require_positive_expectancy_ci_lower_bound: bool = False


@dataclass(frozen=True)
class HistoricalEdgeMetrics:
    total_trades: int
    wins: int
    losses: int
    breakeven: int
    win_rate: float
    expectancy_r: float
    profit_factor: float
    max_drawdown: float
    sharpe_ratio: float
    sharpe_tstat: float
    sharpe_definition_version: str
    max_consecutive_losses: int
    recovery_time_trades: int
    cumulative_r: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class HistoricalEdgeGate:
    name: str
    passed: bool
    value: float | int
    threshold: float | int
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class HistoricalEdgeValidationReport:
    passed: bool
    metrics: HistoricalEdgeMetrics
    gates: list[HistoricalEdgeGate] = field(default_factory=list)
    statistical_robustness: StatisticalRobustnessMetrics | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "metrics": self.metrics.to_dict(),
            "gates": [gate.to_dict() for gate in self.gates],
            "statistical_robustness": (
                self.statistical_robustness.to_dict() if self.statistical_robustness else None
            ),
        }


def validate_historical_edge(
    records: Iterable[dict[str, Any]],
    *,
    config: HistoricalEdgeValidationConfig = HistoricalEdgeValidationConfig(),
    result_field: str = "result_r",
) -> HistoricalEdgeValidationReport:
    r_values = extract_r_values(records, result_field=result_field)
    metrics = calculate_historical_edge_metrics(r_values)
    statistical_robustness = calculate_statistical_robustness(
        r_values,
        observed_sharpe=metrics.sharpe_ratio,
        estimated_trials=config.estimated_trials,
        bootstrap_iterations=config.bootstrap_iterations,
        confidence_level=config.bootstrap_confidence_level,
        seed=config.bootstrap_seed,
    )
    gates = build_historical_edge_gates(
        metrics,
        config=config,
        statistical_robustness=statistical_robustness,
    )

    return HistoricalEdgeValidationReport(
        passed=all(gate.passed for gate in gates),
        metrics=metrics,
        gates=gates,
        statistical_robustness=statistical_robustness,
    )


def extract_r_values(
    records: Iterable[dict[str, Any]],
    *,
    result_field: str = "result_r",
) -> list[float]:
    values: list[float] = []
    for record in records:
        if not isinstance(record, dict):
            continue
        raw_value = record.get(result_field, record.get("r_multiple"))
        value = _safe_float(raw_value)
        if value is not None:
            values.append(value)
    return values


def calculate_historical_edge_metrics(r_values: Iterable[float]) -> HistoricalEdgeMetrics:
    values = [float(value) for value in r_values]
    total = len(values)
    wins = sum(1 for value in values if value > 0)
    losses = sum(1 for value in values if value < 0)
    breakeven = total - wins - losses
    win_rate = wins / total if total else 0.0
    expectancy_r = sum(values) / total if total else 0.0
    profit_factor = calculate_profit_factor(values)
    max_drawdown = calculate_max_drawdown(values)
    sharpe_ratio = calculate_sharpe_ratio(values)
    sharpe_tstat = calculate_sharpe_tstat(values)
    max_consecutive_losses = calculate_max_consecutive_losses(values)
    recovery_time_trades = calculate_recovery_time_trades(values)
    cumulative_r = sum(values)

    return HistoricalEdgeMetrics(
        total_trades=total,
        wins=wins,
        losses=losses,
        breakeven=breakeven,
        win_rate=round(win_rate, 6),
        expectancy_r=round(expectancy_r, 6),
        profit_factor=round(profit_factor, 6),
        max_drawdown=round(max_drawdown, 6),
        sharpe_ratio=round(sharpe_ratio, 6),
        sharpe_tstat=round(sharpe_tstat, 6),
        sharpe_definition_version=SHARPE_DEFINITION_VERSION,
        max_consecutive_losses=max_consecutive_losses,
        recovery_time_trades=recovery_time_trades,
        cumulative_r=round(cumulative_r, 6),
    )


def calculate_profit_factor(r_values: Iterable[float]) -> float:
    gross_profit = sum(value for value in r_values if value > 0)
    gross_loss = abs(sum(value for value in r_values if value < 0))
    if gross_profit <= 0:
        return 0.0
    if gross_loss == 0:
        return math.inf
    return gross_profit / gross_loss


def calculate_max_drawdown(r_values: Iterable[float]) -> float:
    cumulative = 0.0
    peak = 0.0
    max_drawdown = 0.0
    for value in r_values:
        cumulative += value
        peak = max(peak, cumulative)
        drawdown = peak - cumulative
        max_drawdown = max(max_drawdown, drawdown)
    return max_drawdown


def calculate_sharpe_ratio(r_values: Iterable[float]) -> float:
    """Per-trade Sharpe = mean(R) / std(R), independent of sample size.

    The t-statistic is intentionally exposed separately through
    `calculate_sharpe_tstat`. Do not feed the t-statistic into DSR.
    """

    values = [float(value) for value in r_values]
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / (len(values) - 1)
    std_dev = math.sqrt(variance)
    if std_dev == 0:
        return 0.0
    return mean / std_dev


def calculate_sharpe_tstat(r_values: Iterable[float]) -> float:
    """Significance proxy: per-trade Sharpe multiplied by sqrt(N)."""

    values = [float(value) for value in r_values]
    if len(values) < 2:
        return 0.0
    return calculate_sharpe_ratio(values) * math.sqrt(len(values))


def calculate_max_consecutive_losses(r_values: Iterable[float]) -> int:
    max_losses = 0
    current_losses = 0
    for value in r_values:
        if value < 0:
            current_losses += 1
            max_losses = max(max_losses, current_losses)
        else:
            current_losses = 0
    return max_losses


def calculate_recovery_time_trades(r_values: Iterable[float]) -> int:
    cumulative = 0.0
    peak = 0.0
    current_underwater = 0
    max_recovery = 0

    for value in r_values:
        cumulative += value
        if cumulative >= peak:
            peak = cumulative
            max_recovery = max(max_recovery, current_underwater)
            current_underwater = 0
        else:
            current_underwater += 1
            max_recovery = max(max_recovery, current_underwater)

    return max_recovery


def build_historical_edge_gates(
    metrics: HistoricalEdgeMetrics,
    *,
    config: HistoricalEdgeValidationConfig,
    statistical_robustness: StatisticalRobustnessMetrics | None = None,
) -> list[HistoricalEdgeGate]:
    effective_drawdown_threshold = config.max_drawdown_limit * max(1.0, abs(metrics.cumulative_r))
    gates = [
        HistoricalEdgeGate(
            name="minimum_sample_size",
            passed=metrics.total_trades >= config.min_total_trades,
            value=metrics.total_trades,
            threshold=config.min_total_trades,
            message="Minimum completed trade count required for edge validation.",
        ),
        HistoricalEdgeGate(
            name="positive_expectancy",
            passed=metrics.expectancy_r >= config.min_expectancy_r,
            value=metrics.expectancy_r,
            threshold=config.min_expectancy_r,
            message="Average result per trade must clear the configured R threshold.",
        ),
        HistoricalEdgeGate(
            name="profit_factor",
            passed=metrics.profit_factor >= config.min_profit_factor,
            value=metrics.profit_factor,
            threshold=config.min_profit_factor,
            message="Gross wins divided by gross losses must clear the configured threshold.",
        ),
        HistoricalEdgeGate(
            name="drawdown_limit",
            passed=metrics.max_drawdown <= effective_drawdown_threshold,
            value=metrics.max_drawdown,
            threshold=round(effective_drawdown_threshold, 6),
            message=(
                "Max drawdown (R) must stay within max_drawdown_limit * max(1, |cumulative_r|). "
                "Threshold shown is the effective absolute R limit."
            ),
        ),
        HistoricalEdgeGate(
            name="sharpe_ratio",
            passed=metrics.sharpe_ratio >= config.min_sharpe_ratio,
            value=metrics.sharpe_ratio,
            threshold=config.min_sharpe_ratio,
            message="Per-trade Sharpe must clear the configured threshold.",
        ),
    ]

    if statistical_robustness is not None:
        gates.append(
            HistoricalEdgeGate(
                name="deflated_sharpe_probability",
                passed=(
                    statistical_robustness.deflated_sharpe_probability
                    >= config.min_deflated_sharpe_probability
                ),
                value=statistical_robustness.deflated_sharpe_probability,
                threshold=config.min_deflated_sharpe_probability,
                message="Per-trade Sharpe must remain significant after multiple-testing deflation.",
            )
        )
        gates.append(
            HistoricalEdgeGate(
                name="bootstrap_expectancy_lower_bound",
                passed=(
                    not config.require_positive_expectancy_ci_lower_bound
                    or statistical_robustness.expectancy_ci.lower > 0.0
                ),
                value=statistical_robustness.expectancy_ci.lower,
                threshold=0.0,
                message="Bootstrap expectancy lower bound should be positive when strict robustness is required.",
            )
        )

    return gates


def render_historical_edge_markdown(report: HistoricalEdgeValidationReport) -> str:
    metrics = report.metrics
    lines = [
        "# Historical Edge Validation",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        "",
        "## Metrics",
        "",
        f"- Total trades: {metrics.total_trades}",
        f"- Win rate: {metrics.win_rate:.2%}",
        f"- Expectancy R: {metrics.expectancy_r:.4f}",
        f"- Profit factor: {_format_number(metrics.profit_factor)}",
        f"- Max drawdown R: {metrics.max_drawdown:.4f}",
        f"- Sharpe ratio: {metrics.sharpe_ratio:.4f}",
        f"- Sharpe t-stat: {metrics.sharpe_tstat:.4f}",
        f"- Sharpe definition: {metrics.sharpe_definition_version}",
        f"- Max consecutive losses: {metrics.max_consecutive_losses}",
        f"- Recovery time trades: {metrics.recovery_time_trades}",
        f"- Cumulative R: {metrics.cumulative_r:.4f}",
        "",
    ]
    if report.statistical_robustness is not None:
        robustness = report.statistical_robustness
        lines.extend(
            [
                "## Statistical Robustness",
                "",
                f"- Deflated Sharpe probability: {robustness.deflated_sharpe_probability:.2%}",
                f"- Estimated trials: {robustness.estimated_trials}",
                f"- Observations: {robustness.observations}",
                f"- Skewness: {robustness.skewness:.4f}",
                f"- Kurtosis: {robustness.kurtosis:.4f}",
                f"- Expectancy CI ({robustness.expectancy_ci.confidence_level:.0%}): "
                f"[{robustness.expectancy_ci.lower:.4f}, {robustness.expectancy_ci.upper:.4f}]",
                f"- Win-rate CI ({robustness.win_rate_ci.confidence_level:.0%}): "
                f"[{robustness.win_rate_ci.lower:.2%}, {robustness.win_rate_ci.upper:.2%}]",
                "",
            ]
        )
    lines.extend(
        [
            "## Gates",
            "",
            "| Gate | Status | Value | Threshold |",
            "|---|---:|---:|---:|",
        ]
    )
    for gate in report.gates:
        lines.append(
            f"| {gate.name} | {'PASS' if gate.passed else 'FAIL'} | "
            f"{_format_number(gate.value)} | {_format_number(gate.threshold)} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def write_historical_edge_report(
    report: HistoricalEdgeValidationReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    markdown_path.write_text(render_historical_edge_markdown(report), encoding="utf-8")


def _safe_float(value: Any) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(result):
        return None
    return result


def _format_number(value: float | int) -> str:
    if isinstance(value, float):
        if math.isinf(value):
            return "inf"
        return f"{value:.6g}"
    return str(value)
