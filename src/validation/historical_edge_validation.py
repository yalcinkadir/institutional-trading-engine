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
SMALL_SAMPLE_WARNING_THRESHOLD = 30


@dataclass(frozen=True)
class NumericCoercionResult:
    ok: bool
    value: float | None
    reason: str | None
    raw_value: Any


def coerce_finite_float(value: Any, *, strict: bool = False) -> float | None | NumericCoercionResult:
    if value is None:
        result = NumericCoercionResult(False, None, "missing", value)
        return result if strict else None
    if isinstance(value, str) and not value.strip():
        result = NumericCoercionResult(False, None, "empty_string", value)
        return result if strict else None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        result = NumericCoercionResult(False, None, "invalid_float", value)
        return result if strict else None
    if not math.isfinite(parsed):
        result = NumericCoercionResult(False, None, "non_finite", value)
        return result if strict else None
    result = NumericCoercionResult(True, parsed, None, value)
    return result if strict else parsed


def coerce_finite_float_or_default(value: Any, default: float) -> float:
    parsed = coerce_finite_float(value)
    return float(default) if parsed is None else float(parsed)


def json_safe_number(value: Any, *, fallback: float | None = None) -> float | None:
    parsed = coerce_finite_float(value)
    return fallback if parsed is None else parsed


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
        return _json_safe(asdict(self))


@dataclass(frozen=True)
class HistoricalEdgeCaveats:
    sharpe_std_method: str
    iid_assumption: str
    small_sample_warning: bool
    not_proof_of_edge: bool
    message: str

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
        return _json_safe(asdict(self))


@dataclass(frozen=True)
class HistoricalEdgeValidationReport:
    passed: bool
    metrics: HistoricalEdgeMetrics
    gates: list[HistoricalEdgeGate] = field(default_factory=list)
    statistical_robustness: StatisticalRobustnessMetrics | None = None
    caveats: HistoricalEdgeCaveats | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "metrics": self.metrics.to_dict(),
            "gates": [gate.to_dict() for gate in self.gates],
            "statistical_robustness": (
                self.statistical_robustness.to_dict() if self.statistical_robustness else None
            ),
            "caveats": self.caveats.to_dict() if self.caveats else None,
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
    gates = build_historical_edge_gates(metrics, config=config, statistical_robustness=statistical_robustness)
    return HistoricalEdgeValidationReport(
        passed=all(gate.passed for gate in gates),
        metrics=metrics,
        gates=gates,
        statistical_robustness=statistical_robustness,
        caveats=build_historical_edge_caveats(metrics),
    )


def extract_r_values(records: Iterable[dict[str, Any]], *, result_field: str = "result_r") -> list[float]:
    values: list[float] = []
    for record in records:
        if not isinstance(record, dict):
            continue
        raw_value = record.get(result_field, record.get("r_multiple"))
        value = coerce_finite_float(raw_value)
        if value is not None:
            values.append(float(value))
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
        max_consecutive_losses=calculate_max_consecutive_losses(values),
        recovery_time_trades=calculate_recovery_time_trades(values),
        cumulative_r=round(sum(values), 6),
    )


def build_historical_edge_caveats(metrics: HistoricalEdgeMetrics) -> HistoricalEdgeCaveats:
    return HistoricalEdgeCaveats(
        sharpe_std_method="population_std",
        iid_assumption="not_verified",
        small_sample_warning=metrics.total_trades < SMALL_SAMPLE_WARNING_THRESHOLD,
        not_proof_of_edge=True,
        message=(
            "Sharpe metrics use per-trade R values and population standard deviation. "
            "IID assumption is not verified; small samples require caution; this is "
            + "not proof of live edge."
        ),
    )


def calculate_profit_factor(r_values: Iterable[float]) -> float:
    gross_profit = sum(value for value in r_values if value > 0)
    gross_loss = abs(sum(value for value in r_values if value < 0))
    if gross_profit <= 0:
        return 0.0
    if gross_loss == 0:
        return math.inf
    return gross_profit / gross_loss


def calculate_profit_factor_degradation(current: float, baseline: float) -> float:
    current_value = float(current)
    baseline_value = float(baseline)
    current_is_inf = math.isinf(current_value)
    baseline_is_inf = math.isinf(baseline_value)
    if current_is_inf and baseline_is_inf:
        return 0.0
    if baseline_is_inf:
        return 1.0 if math.isfinite(current_value) else 0.0
    if current_is_inf:
        return 0.0
    if not math.isfinite(current_value) or not math.isfinite(baseline_value):
        return 1.0
    if baseline_value <= 0:
        return 0.0 if current_value >= baseline_value else 1.0
    degradation = (baseline_value - current_value) / baseline_value
    return round(min(1.0, max(0.0, degradation)), 6)


def calculate_max_drawdown(r_values: Iterable[float]) -> float:
    cumulative = 0.0
    peak = 0.0
    max_drawdown = 0.0
    for value in r_values:
        cumulative += value
        peak = max(peak, cumulative)
        max_drawdown = max(max_drawdown, peak - cumulative)
    return max_drawdown


def calculate_sharpe_ratio(r_values: Iterable[float]) -> float:
    values = [float(value) for value in r_values]
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    std_dev = math.sqrt(variance)
    if std_dev == 0:
        return 0.0
    return mean / std_dev


def calculate_sharpe_tstat(r_values: Iterable[float]) -> float:
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
        HistoricalEdgeGate("minimum_sample_size", metrics.total_trades >= config.min_total_trades, metrics.total_trades, config.min_total_trades, "Minimum completed trade count required for edge validation."),
        HistoricalEdgeGate("positive_expectancy", metrics.expectancy_r >= config.min_expectancy_r, metrics.expectancy_r, config.min_expectancy_r, "Average result per trade must clear the configured R threshold."),
        HistoricalEdgeGate("profit_factor", metrics.profit_factor >= config.min_profit_factor, metrics.profit_factor, config.min_profit_factor, "Gross wins divided by gross losses must clear the configured threshold."),
        HistoricalEdgeGate("drawdown_limit", metrics.max_drawdown <= effective_drawdown_threshold, metrics.max_drawdown, round(effective_drawdown_threshold, 6), "Max drawdown (R) must stay within max_drawdown_limit * max(1, |cumulative_r|). Threshold shown is the effective absolute R limit."),
        HistoricalEdgeGate("sharpe_ratio", metrics.sharpe_ratio >= config.min_sharpe_ratio, metrics.sharpe_ratio, config.min_sharpe_ratio, "Per-trade Sharpe must clear the configured threshold."),
    ]
    if statistical_robustness is not None:
        gates.append(HistoricalEdgeGate("deflated_sharpe_probability", statistical_robustness.deflated_sharpe_probability >= config.min_deflated_sharpe_probability, statistical_robustness.deflated_sharpe_probability, config.min_deflated_sharpe_probability, "Per-trade Sharpe must remain significant after multiple-testing deflation."))
        gates.append(HistoricalEdgeGate("bootstrap_expectancy_lower_bound", not config.require_positive_expectancy_ci_lower_bound or statistical_robustness.expectancy_ci.lower > 0.0, statistical_robustness.expectancy_ci.lower, 0.0, "Bootstrap expectancy lower bound should be positive when strict robustness is required."))
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
    if report.caveats is not None:
        lines.extend([
            "## Sharpe caveats",
            "",
            "- Sharpe uses population standard deviation on per-trade R values.",
            "- IID assumption is not verified.",
            f"- Small sample warning: {'yes' if report.caveats.small_sample_warning else 'no'}.",
            "- These diagnostics are not proof of live edge.",
            "",
        ])
    if report.statistical_robustness is not None:
        robustness = report.statistical_robustness
        lines.extend([
            "## Statistical Robustness",
            "",
            f"- Deflated Sharpe probability: {robustness.deflated_sharpe_probability:.2%}",
            f"- Estimated trials: {robustness.estimated_trials}",
            f"- Observations: {robustness.observations}",
            f"- Skewness: {robustness.skewness:.4f}",
            f"- Kurtosis: {robustness.kurtosis:.4f}",
            f"- Expectancy CI ({robustness.expectancy_ci.confidence_level:.0%}): [{robustness.expectancy_ci.lower:.4f}, {robustness.expectancy_ci.upper:.4f}]",
            f"- Win-rate CI ({robustness.win_rate_ci.confidence_level:.0%}): [{robustness.win_rate_ci.lower:.2%}, {robustness.win_rate_ci.upper:.2%}]",
            "",
        ])
    lines.extend(["## Gates", "", "| Gate | Status | Value | Threshold |", "|---|---:|---:|---:|"])
    for gate in report.gates:
        lines.append(f"| {gate.name} | {'PASS' if gate.passed else 'FAIL'} | {_format_number(gate.value)} | {_format_number(gate.threshold)} |")
    return "\n".join(lines).rstrip() + "\n"


def write_historical_edge_report(report: HistoricalEdgeValidationReport, *, json_path: Path, markdown_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True, allow_nan=False), encoding="utf-8")
    markdown_path.write_text(render_historical_edge_markdown(report), encoding="utf-8")


def _safe_float(value: Any) -> float | None:
    return coerce_finite_float(value)


def _format_number(value: float | int) -> str:
    if isinstance(value, float) and math.isinf(value):
        return "inf" if value > 0 else "-inf"
    if isinstance(value, int):
        return str(value)
    return f"{float(value):.4f}"


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, float):
        if math.isinf(value):
            return "inf" if value > 0 else "-inf"
        if math.isnan(value):
            return "nan"
    return value
