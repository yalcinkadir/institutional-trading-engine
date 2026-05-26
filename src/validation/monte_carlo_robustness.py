from __future__ import annotations

import json
import random
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class MonteCarloRobustnessConfig:
    min_observations: int = 30
    simulations: int = 1000
    confidence_level: float = 0.95
    seed: int = 42
    min_bootstrap_expectancy_lower_r: float = 0.0
    max_drawdown_p95_r: float = 10.0
    min_permutation_p_value: float = 0.05
    require_positive_observed_expectancy: bool = True


@dataclass(frozen=True)
class MonteCarloRobustnessMetrics:
    observations: int
    simulations: int
    confidence_level: float
    observed_expectancy_r: float
    observed_total_r: float
    observed_win_rate: float
    bootstrap_expectancy_lower_r: float
    bootstrap_expectancy_upper_r: float
    bootstrap_total_lower_r: float
    bootstrap_total_upper_r: float
    permutation_p_value: float
    drawdown_p95_r: float
    drawdown_p99_r: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MonteCarloRobustnessGate:
    name: str
    passed: bool
    value: float | int | bool
    threshold: float | int | bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MonteCarloRobustnessReport:
    passed: bool
    metrics: MonteCarloRobustnessMetrics
    gates: list[MonteCarloRobustnessGate] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "metrics": self.metrics.to_dict(),
            "gates": [gate.to_dict() for gate in self.gates],
        }


def run_monte_carlo_robustness(
    records: Iterable[dict[str, Any] | float | int],
    *,
    config: MonteCarloRobustnessConfig = MonteCarloRobustnessConfig(),
    result_field: str = "result_r",
) -> MonteCarloRobustnessReport:
    values = _extract_r_values(records, result_field=result_field)
    metrics = _calculate_metrics(values, config=config)
    gates = _build_gates(metrics, config=config)
    return MonteCarloRobustnessReport(
        passed=all(gate.passed for gate in gates),
        metrics=metrics,
        gates=gates,
    )


def render_monte_carlo_robustness_markdown(report: MonteCarloRobustnessReport) -> str:
    metrics = report.metrics
    lines = [
        "# Monte Carlo Robustness Suite",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        "",
        "## Metrics",
        "",
        f"- Observations: {metrics.observations}",
        f"- Simulations: {metrics.simulations}",
        f"- Confidence level: {metrics.confidence_level:.2%}",
        f"- Observed expectancy R: {metrics.observed_expectancy_r:.4f}",
        f"- Observed total R: {metrics.observed_total_r:.4f}",
        f"- Observed win rate: {metrics.observed_win_rate:.2%}",
        f"- Bootstrap expectancy lower R: {metrics.bootstrap_expectancy_lower_r:.4f}",
        f"- Bootstrap expectancy upper R: {metrics.bootstrap_expectancy_upper_r:.4f}",
        f"- Bootstrap total lower R: {metrics.bootstrap_total_lower_r:.4f}",
        f"- Bootstrap total upper R: {metrics.bootstrap_total_upper_r:.4f}",
        f"- Permutation p-value: {metrics.permutation_p_value:.4f}",
        f"- Drawdown p95 R: {metrics.drawdown_p95_r:.4f}",
        f"- Drawdown p99 R: {metrics.drawdown_p99_r:.4f}",
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


def write_monte_carlo_robustness_report(
    report: MonteCarloRobustnessReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_monte_carlo_robustness_markdown(report), encoding="utf-8")


def _calculate_metrics(values: list[float], *, config: MonteCarloRobustnessConfig) -> MonteCarloRobustnessMetrics:
    rng = random.Random(config.seed)
    observed_expectancy = _mean(values)
    observed_total = sum(values)
    observed_win_rate = _win_rate(values)

    bootstrap_expectancies: list[float] = []
    bootstrap_totals: list[float] = []
    drawdowns: list[float] = []
    permutation_totals: list[float] = []

    if values:
        for _ in range(max(1, config.simulations)):
            sample = [rng.choice(values) for _ in values]
            bootstrap_expectancies.append(_mean(sample))
            bootstrap_totals.append(sum(sample))
            shuffled = list(values)
            rng.shuffle(shuffled)
            drawdowns.append(_max_drawdown_r(shuffled))
            signs = [1 if rng.random() >= 0.5 else -1 for _ in values]
            permutation_totals.append(sum(abs(value) * sign for value, sign in zip(values, signs)))

    lower_q = (1.0 - config.confidence_level) / 2.0
    upper_q = 1.0 - lower_q
    permutation_p_value = _permutation_p_value(observed_total, permutation_totals)

    return MonteCarloRobustnessMetrics(
        observations=len(values),
        simulations=max(1, config.simulations),
        confidence_level=round(config.confidence_level, 6),
        observed_expectancy_r=round(observed_expectancy, 6),
        observed_total_r=round(observed_total, 6),
        observed_win_rate=round(observed_win_rate, 6),
        bootstrap_expectancy_lower_r=round(_quantile(bootstrap_expectancies, lower_q), 6),
        bootstrap_expectancy_upper_r=round(_quantile(bootstrap_expectancies, upper_q), 6),
        bootstrap_total_lower_r=round(_quantile(bootstrap_totals, lower_q), 6),
        bootstrap_total_upper_r=round(_quantile(bootstrap_totals, upper_q), 6),
        permutation_p_value=round(permutation_p_value, 6),
        drawdown_p95_r=round(_quantile(drawdowns, 0.95), 6),
        drawdown_p99_r=round(_quantile(drawdowns, 0.99), 6),
    )


def _build_gates(
    metrics: MonteCarloRobustnessMetrics,
    *,
    config: MonteCarloRobustnessConfig,
) -> list[MonteCarloRobustnessGate]:
    return [
        MonteCarloRobustnessGate(
            name="minimum_observations",
            passed=metrics.observations >= config.min_observations,
            value=metrics.observations,
            threshold=config.min_observations,
            message="Monte Carlo robustness needs enough observations before it is trusted.",
        ),
        MonteCarloRobustnessGate(
            name="positive_observed_expectancy",
            passed=(not config.require_positive_observed_expectancy) or metrics.observed_expectancy_r > 0,
            value=metrics.observed_expectancy_r,
            threshold=0.0,
            message="Observed expectancy should remain positive.",
        ),
        MonteCarloRobustnessGate(
            name="bootstrap_expectancy_lower_bound",
            passed=metrics.bootstrap_expectancy_lower_r >= config.min_bootstrap_expectancy_lower_r,
            value=metrics.bootstrap_expectancy_lower_r,
            threshold=config.min_bootstrap_expectancy_lower_r,
            message="Bootstrap lower bound for expectancy should remain above the configured minimum.",
        ),
        MonteCarloRobustnessGate(
            name="permutation_p_value",
            passed=metrics.permutation_p_value >= config.min_permutation_p_value,
            value=metrics.permutation_p_value,
            threshold=config.min_permutation_p_value,
            message="Permutation p-value should not indicate an unstable or overfit result.",
        ),
        MonteCarloRobustnessGate(
            name="drawdown_p95_r",
            passed=metrics.drawdown_p95_r <= config.max_drawdown_p95_r,
            value=metrics.drawdown_p95_r,
            threshold=config.max_drawdown_p95_r,
            message="95th percentile shuffled-path drawdown should remain within tolerance.",
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


def _permutation_p_value(observed_total: float, permutation_totals: list[float]) -> float:
    if not permutation_totals:
        return 1.0
    extreme_count = sum(1 for total in permutation_totals if abs(total) >= abs(observed_total))
    return (extreme_count + 1) / (len(permutation_totals) + 1)


def _max_drawdown_r(values: list[float]) -> float:
    cumulative = 0.0
    peak = 0.0
    max_drawdown = 0.0
    for value in values:
        cumulative += value
        peak = max(peak, cumulative)
        max_drawdown = max(max_drawdown, peak - cumulative)
    return max_drawdown


def _quantile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int(round((len(ordered) - 1) * q))))
    return ordered[index]


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


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
