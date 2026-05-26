from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class SequentialEdgeDecayConfig:
    baseline_win_rate: float = 0.55
    degraded_win_rate: float = 0.45
    alpha: float = 0.05
    beta: float = 0.20
    min_observations: int = 20
    max_observations: int = 250
    require_positive_expectancy: bool = True


@dataclass(frozen=True)
class SequentialEdgeDecayMetrics:
    observations: int
    wins: int
    losses: int
    breakeven: int
    win_rate: float
    expectancy_r: float
    cumulative_r: float
    log_likelihood_ratio: float
    accept_baseline_threshold: float
    accept_degraded_threshold: float
    decision: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SequentialEdgeDecayGate:
    name: str
    passed: bool
    value: float | int | str | bool
    threshold: float | int | str | bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SequentialEdgeDecayReport:
    passed: bool
    metrics: SequentialEdgeDecayMetrics
    gates: list[SequentialEdgeDecayGate] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "metrics": self.metrics.to_dict(),
            "gates": [gate.to_dict() for gate in self.gates],
        }


def run_sequential_edge_decay_test(
    records: Iterable[dict[str, Any] | float | int],
    *,
    config: SequentialEdgeDecayConfig = SequentialEdgeDecayConfig(),
    result_field: str = "result_r",
) -> SequentialEdgeDecayReport:
    r_values = _extract_r_values(records, result_field=result_field)
    metrics = _calculate_metrics(r_values, config=config)
    gates = _build_gates(metrics, config=config)
    return SequentialEdgeDecayReport(
        passed=all(gate.passed for gate in gates),
        metrics=metrics,
        gates=gates,
    )


def render_sequential_edge_decay_markdown(report: SequentialEdgeDecayReport) -> str:
    metrics = report.metrics
    lines = [
        "# Sequential Edge Decay Test",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        "",
        "## Metrics",
        "",
        f"- Observations: {metrics.observations}",
        f"- Wins: {metrics.wins}",
        f"- Losses: {metrics.losses}",
        f"- Breakeven: {metrics.breakeven}",
        f"- Win rate: {metrics.win_rate:.2%}",
        f"- Expectancy R: {metrics.expectancy_r:.4f}",
        f"- Cumulative R: {metrics.cumulative_r:.4f}",
        f"- Log-likelihood ratio: {metrics.log_likelihood_ratio:.4f}",
        f"- Accept baseline threshold: {metrics.accept_baseline_threshold:.4f}",
        f"- Accept degraded threshold: {metrics.accept_degraded_threshold:.4f}",
        f"- Decision: {metrics.decision}",
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


def write_sequential_edge_decay_report(
    report: SequentialEdgeDecayReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_sequential_edge_decay_markdown(report), encoding="utf-8")


def _calculate_metrics(values: list[float], *, config: SequentialEdgeDecayConfig) -> SequentialEdgeDecayMetrics:
    wins = sum(1 for value in values if value > 0)
    losses = sum(1 for value in values if value < 0)
    breakeven = len(values) - wins - losses
    informative_observations = wins + losses
    win_rate = wins / informative_observations if informative_observations else 0.0
    expectancy = sum(values) / len(values) if values else 0.0
    cumulative = sum(values)
    llr = _sprt_log_likelihood_ratio(
        wins=wins,
        losses=losses,
        baseline_win_rate=config.baseline_win_rate,
        degraded_win_rate=config.degraded_win_rate,
    )
    accept_baseline_threshold = math.log((1.0 - config.beta) / config.alpha)
    accept_degraded_threshold = math.log(config.beta / (1.0 - config.alpha))
    decision = _classify_decision(
        observations=len(values),
        log_likelihood_ratio=llr,
        accept_baseline_threshold=accept_baseline_threshold,
        accept_degraded_threshold=accept_degraded_threshold,
        max_observations=config.max_observations,
    )
    return SequentialEdgeDecayMetrics(
        observations=len(values),
        wins=wins,
        losses=losses,
        breakeven=breakeven,
        win_rate=round(win_rate, 6),
        expectancy_r=round(expectancy, 6),
        cumulative_r=round(cumulative, 6),
        log_likelihood_ratio=round(llr, 6),
        accept_baseline_threshold=round(accept_baseline_threshold, 6),
        accept_degraded_threshold=round(accept_degraded_threshold, 6),
        decision=decision,
    )


def _build_gates(
    metrics: SequentialEdgeDecayMetrics,
    *,
    config: SequentialEdgeDecayConfig,
) -> list[SequentialEdgeDecayGate]:
    return [
        SequentialEdgeDecayGate(
            name="minimum_observations",
            passed=metrics.observations >= config.min_observations,
            value=metrics.observations,
            threshold=config.min_observations,
            message="Sequential edge-decay test needs enough forward observations before being trusted.",
        ),
        SequentialEdgeDecayGate(
            name="positive_expectancy",
            passed=(not config.require_positive_expectancy) or metrics.expectancy_r > 0,
            value=metrics.expectancy_r,
            threshold=0.0,
            message="Forward expectancy should remain positive while edge is monitored.",
        ),
        SequentialEdgeDecayGate(
            name="no_degraded_edge_decision",
            passed=metrics.decision != "accept_degraded_edge",
            value=metrics.decision,
            threshold="not accept_degraded_edge",
            message="SPRT should not accept the degraded-edge hypothesis.",
        ),
    ]


def _sprt_log_likelihood_ratio(
    *,
    wins: int,
    losses: int,
    baseline_win_rate: float,
    degraded_win_rate: float,
) -> float:
    baseline = _clamp_probability(baseline_win_rate)
    degraded = _clamp_probability(degraded_win_rate)
    return wins * math.log(baseline / degraded) + losses * math.log((1.0 - baseline) / (1.0 - degraded))


def _classify_decision(
    *,
    observations: int,
    log_likelihood_ratio: float,
    accept_baseline_threshold: float,
    accept_degraded_threshold: float,
    max_observations: int,
) -> str:
    if log_likelihood_ratio >= accept_baseline_threshold:
        return "accept_baseline_edge"
    if log_likelihood_ratio <= accept_degraded_threshold:
        return "accept_degraded_edge"
    if observations >= max_observations:
        return "inconclusive_max_observations"
    return "continue_observation"


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


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _clamp_probability(value: float) -> float:
    return min(0.999999, max(0.000001, float(value)))


def _format_value(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)
