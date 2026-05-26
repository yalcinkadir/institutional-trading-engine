from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class RegimeChangeConfig:
    min_observations: int = 20
    lookback_window: int = 10
    max_change_score: float = 0.65
    max_label_change_rate: float = 0.35
    max_volatility_jump: float = 0.50
    max_correlation_jump: float = 0.35
    max_drawdown_jump: float = 0.08
    require_latest_regime_known: bool = True


@dataclass(frozen=True)
class RegimeChangeMetrics:
    observations: int
    lookback_window: int
    latest_regime: str
    previous_regime: str
    label_change_count: int
    label_change_rate: float
    volatility_previous: float
    volatility_latest: float
    volatility_jump: float
    correlation_previous: float
    correlation_latest: float
    correlation_jump: float
    drawdown_previous: float
    drawdown_latest: float
    drawdown_jump: float
    change_score: float
    state: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RegimeChangeGate:
    name: str
    passed: bool
    value: float | int | str | bool
    threshold: float | int | str | bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RegimeChangeReport:
    passed: bool
    metrics: RegimeChangeMetrics
    gates: list[RegimeChangeGate] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "metrics": self.metrics.to_dict(),
            "gates": [gate.to_dict() for gate in self.gates],
        }


def detect_regime_change(
    records: Iterable[dict[str, Any]],
    *,
    config: RegimeChangeConfig = RegimeChangeConfig(),
) -> RegimeChangeReport:
    normalized = [_normalize_record(record) for record in records if isinstance(record, dict)]
    metrics = _calculate_metrics(normalized, config=config)
    gates = _build_gates(metrics, config=config)
    return RegimeChangeReport(
        passed=all(gate.passed for gate in gates),
        metrics=metrics,
        gates=gates,
    )


def render_regime_change_markdown(report: RegimeChangeReport) -> str:
    metrics = report.metrics
    lines = [
        "# Regime Change Detection",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        "",
        "## Metrics",
        "",
        f"- Observations: {metrics.observations}",
        f"- Lookback window: {metrics.lookback_window}",
        f"- Previous regime: {metrics.previous_regime}",
        f"- Latest regime: {metrics.latest_regime}",
        f"- Label change count: {metrics.label_change_count}",
        f"- Label change rate: {metrics.label_change_rate:.2%}",
        f"- Volatility previous: {metrics.volatility_previous:.4f}",
        f"- Volatility latest: {metrics.volatility_latest:.4f}",
        f"- Volatility jump: {metrics.volatility_jump:.4f}",
        f"- Correlation previous: {metrics.correlation_previous:.4f}",
        f"- Correlation latest: {metrics.correlation_latest:.4f}",
        f"- Correlation jump: {metrics.correlation_jump:.4f}",
        f"- Drawdown previous: {metrics.drawdown_previous:.4f}",
        f"- Drawdown latest: {metrics.drawdown_latest:.4f}",
        f"- Drawdown jump: {metrics.drawdown_jump:.4f}",
        f"- Change score: {metrics.change_score:.4f}",
        f"- State: {metrics.state}",
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


def write_regime_change_report(
    report: RegimeChangeReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_regime_change_markdown(report), encoding="utf-8")


def _calculate_metrics(records: list[dict[str, Any]], *, config: RegimeChangeConfig) -> RegimeChangeMetrics:
    observations = len(records)
    window = max(1, config.lookback_window)
    latest_window = records[-window:] if records else []
    previous_window = records[-2 * window : -window] if len(records) > window else []
    latest_regime = latest_window[-1]["regime"] if latest_window else "unknown"
    previous_regime = _majority_regime(previous_window) if previous_window else "unknown"
    label_change_count = _count_label_changes(records)
    label_change_rate = label_change_count / max(1, observations - 1)
    volatility_previous = _mean([record["volatility"] for record in previous_window])
    volatility_latest = _mean([record["volatility"] for record in latest_window])
    volatility_jump = _relative_jump(volatility_previous, volatility_latest)
    correlation_previous = _mean([record["correlation"] for record in previous_window])
    correlation_latest = _mean([record["correlation"] for record in latest_window])
    correlation_jump = abs(correlation_latest - correlation_previous)
    drawdown_previous = _mean([record["drawdown"] for record in previous_window])
    drawdown_latest = _mean([record["drawdown"] for record in latest_window])
    drawdown_jump = drawdown_latest - drawdown_previous
    change_score = _change_score(
        label_change_rate=label_change_rate,
        volatility_jump=volatility_jump,
        correlation_jump=correlation_jump,
        drawdown_jump=max(0.0, drawdown_jump),
    )
    state = _classify_state(change_score=change_score, latest_regime=latest_regime, config=config)
    return RegimeChangeMetrics(
        observations=observations,
        lookback_window=window,
        latest_regime=latest_regime,
        previous_regime=previous_regime,
        label_change_count=label_change_count,
        label_change_rate=round(label_change_rate, 6),
        volatility_previous=round(volatility_previous, 6),
        volatility_latest=round(volatility_latest, 6),
        volatility_jump=round(volatility_jump, 6),
        correlation_previous=round(correlation_previous, 6),
        correlation_latest=round(correlation_latest, 6),
        correlation_jump=round(correlation_jump, 6),
        drawdown_previous=round(drawdown_previous, 6),
        drawdown_latest=round(drawdown_latest, 6),
        drawdown_jump=round(drawdown_jump, 6),
        change_score=round(change_score, 6),
        state=state,
    )


def _build_gates(metrics: RegimeChangeMetrics, *, config: RegimeChangeConfig) -> list[RegimeChangeGate]:
    return [
        RegimeChangeGate(
            name="minimum_observations",
            passed=metrics.observations >= config.min_observations,
            value=metrics.observations,
            threshold=config.min_observations,
            message="Regime-change detection needs enough observations before it is trusted.",
        ),
        RegimeChangeGate(
            name="latest_regime_known",
            passed=(not config.require_latest_regime_known) or metrics.latest_regime != "unknown",
            value=metrics.latest_regime,
            threshold="known",
            message="Latest regime label must be known.",
        ),
        RegimeChangeGate(
            name="label_change_rate",
            passed=metrics.label_change_rate <= config.max_label_change_rate,
            value=metrics.label_change_rate,
            threshold=config.max_label_change_rate,
            message="Regime labels should not flip too frequently.",
        ),
        RegimeChangeGate(
            name="volatility_jump",
            passed=metrics.volatility_jump <= config.max_volatility_jump,
            value=metrics.volatility_jump,
            threshold=config.max_volatility_jump,
            message="Recent volatility should not jump beyond tolerance.",
        ),
        RegimeChangeGate(
            name="correlation_jump",
            passed=metrics.correlation_jump <= config.max_correlation_jump,
            value=metrics.correlation_jump,
            threshold=config.max_correlation_jump,
            message="Cross-asset correlation should not jump beyond tolerance.",
        ),
        RegimeChangeGate(
            name="drawdown_jump",
            passed=metrics.drawdown_jump <= config.max_drawdown_jump,
            value=metrics.drawdown_jump,
            threshold=config.max_drawdown_jump,
            message="Recent drawdown stress should not jump beyond tolerance.",
        ),
        RegimeChangeGate(
            name="change_score",
            passed=metrics.change_score <= config.max_change_score,
            value=metrics.change_score,
            threshold=config.max_change_score,
            message="Composite regime-change score should remain below the alert threshold.",
        ),
    ]


def _normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "regime": _normalize_regime(record.get("regime") or record.get("regime_label") or record.get("state")),
        "volatility": _safe_float(record.get("volatility", record.get("volatility_percent", record.get("vix")))) or 0.0,
        "correlation": _safe_float(record.get("correlation", record.get("cross_asset_correlation"))) or 0.0,
        "drawdown": _safe_float(record.get("drawdown", record.get("drawdown_pct"))) or 0.0,
    }


def _normalize_regime(value: Any) -> str:
    if value is None:
        return "unknown"
    text = str(value).strip().lower().replace(" ", "_").replace("-", "_")
    return text if text else "unknown"


def _majority_regime(records: list[dict[str, Any]]) -> str:
    counts: dict[str, int] = {}
    for record in records:
        regime = record["regime"]
        counts[regime] = counts.get(regime, 0) + 1
    if not counts:
        return "unknown"
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0][0]


def _count_label_changes(records: list[dict[str, Any]]) -> int:
    changes = 0
    previous: str | None = None
    for record in records:
        current = record["regime"]
        if previous is not None and current != previous:
            changes += 1
        previous = current
    return changes


def _change_score(*, label_change_rate: float, volatility_jump: float, correlation_jump: float, drawdown_jump: float) -> float:
    score = (
        0.30 * min(1.0, label_change_rate / 0.50)
        + 0.30 * min(1.0, volatility_jump / 1.00)
        + 0.20 * min(1.0, correlation_jump / 0.75)
        + 0.20 * min(1.0, drawdown_jump / 0.20)
    )
    return max(0.0, min(1.0, score))


def _classify_state(*, change_score: float, latest_regime: str, config: RegimeChangeConfig) -> str:
    if latest_regime == "unknown" and config.require_latest_regime_known:
        return "unknown_regime"
    if change_score >= config.max_change_score:
        return "regime_change_alert"
    if change_score >= config.max_change_score * 0.70:
        return "regime_change_watch"
    return "stable"


def _relative_jump(previous: float, latest: float) -> float:
    denominator = max(abs(previous), 1e-9)
    return max(0.0, (latest - previous) / denominator)


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


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
