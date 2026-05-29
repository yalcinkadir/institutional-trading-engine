"""BT7 capacity, turnover and realism gate."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

RESEARCH_ONLY_FOOTER = "Research / Paper Observation Only. Execution is not authorized by this report."
_REQUIRED_METRICS = (
    "median_adv_usd",
    "max_position_adv_pct",
    "portfolio_adv_pct",
    "average_daily_turnover_pct",
    "annual_turnover_pct",
    "round_trip_cost_bps",
    "gross_expectancy_bps",
    "net_expectancy_bps",
    "average_holding_days",
    "trade_count",
    "slippage_model_coverage_pct",
)


@dataclass(frozen=True)
class CapacityTurnoverRealismConfig:
    required_metrics: tuple[str, ...] = _REQUIRED_METRICS
    max_position_adv_pct: float = 5.0
    max_portfolio_adv_pct: float = 20.0
    max_average_daily_turnover_pct: float = 30.0
    max_annual_turnover_pct: float = 1000.0
    max_cost_to_gross_expectancy_pct: float = 50.0
    min_net_expectancy_bps: float = 5.0
    min_average_holding_days: float = 1.0
    min_trade_count: int = 30
    min_slippage_model_coverage_pct: float = 100.0
    require_research_footer: bool = True


@dataclass(frozen=True)
class CapacityTurnoverSnapshot:
    run_id: str
    strategy_id: str
    dataset_id: str
    parameter_version: str
    evidence_type: str
    proposed_capital_usd: float
    symbol_count: int
    metrics: Mapping[str, float | int]
    artifact_hashes: Mapping[str, str] = field(default_factory=dict)
    tags: tuple[str, ...] = ("demo", "public_safe")
    footer: str = RESEARCH_ONLY_FOOTER

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "CapacityTurnoverSnapshot":
        return cls(
            run_id=str(payload.get("run_id", "")).strip(),
            strategy_id=str(payload.get("strategy_id", "")).strip(),
            dataset_id=str(payload.get("dataset_id", "")).strip(),
            parameter_version=str(payload.get("parameter_version", "")).strip(),
            evidence_type=str(payload.get("evidence_type", "")).strip(),
            proposed_capital_usd=float(payload.get("proposed_capital_usd", 0.0) or 0.0),
            symbol_count=int(payload.get("symbol_count", 0) or 0),
            metrics=dict(payload.get("metrics", {})),
            artifact_hashes={str(k): str(v) for k, v in dict(payload.get("artifact_hashes", {})).items()},
            tags=tuple(str(tag).strip() for tag in payload.get("tags", ("demo", "public_safe"))),
            footer=str(payload.get("footer", RESEARCH_ONLY_FOOTER)).strip(),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "strategy_id": self.strategy_id,
            "dataset_id": self.dataset_id,
            "parameter_version": self.parameter_version,
            "evidence_type": self.evidence_type,
            "proposed_capital_usd": self.proposed_capital_usd,
            "symbol_count": self.symbol_count,
            "metrics": dict(self.metrics),
            "artifact_hashes": dict(self.artifact_hashes),
            "tags": list(self.tags),
            "footer": self.footer,
        }


@dataclass(frozen=True)
class CapacityTurnoverGate:
    name: str
    passed: bool
    message: str
    failures: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "passed": self.passed, "message": self.message, "failures": list(self.failures)}


@dataclass(frozen=True)
class CapacityTurnoverRealismReport:
    version: str
    generated_at: str
    snapshot: CapacityTurnoverSnapshot
    gates: tuple[CapacityTurnoverGate, ...]
    passed: bool
    footer: str = RESEARCH_ONLY_FOOTER

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "generated_at": self.generated_at,
            "passed": self.passed,
            "snapshot": self.snapshot.to_dict(),
            "gates": [gate.to_dict() for gate in self.gates],
            "footer": self.footer,
        }


def build_capacity_turnover_realism_report(
    snapshot: CapacityTurnoverSnapshot | Mapping[str, Any],
    *,
    config: CapacityTurnoverRealismConfig | None = None,
    version: str = "BT7-v1",
    generated_at: str | None = None,
) -> CapacityTurnoverRealismReport:
    policy = config or CapacityTurnoverRealismConfig()
    snap = snapshot if isinstance(snapshot, CapacityTurnoverSnapshot) else CapacityTurnoverSnapshot.from_mapping(snapshot)
    gates = _build_gates(snap, policy)
    return CapacityTurnoverRealismReport(
        version=version,
        generated_at=generated_at or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        snapshot=snap,
        gates=gates,
        passed=all(gate.passed for gate in gates),
    )


def load_capacity_turnover_realism_json(path: str | Path) -> CapacityTurnoverSnapshot:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping):
        raise ValueError("BT7 JSON must contain a snapshot object or snapshot fields.")
    source = payload.get("snapshot", payload)
    if not isinstance(source, Mapping):
        raise ValueError("BT7 JSON snapshot must be an object.")
    return CapacityTurnoverSnapshot.from_mapping(source)


def demo_capacity_turnover_snapshot() -> CapacityTurnoverSnapshot:
    return CapacityTurnoverSnapshot.from_mapping(_demo_payload()["snapshot"])


def render_capacity_turnover_realism_markdown(report: CapacityTurnoverRealismReport) -> str:
    snap = report.snapshot
    lines = [
        "# BT7 Capacity / Turnover / Realism Gate Report",
        "",
        f"Generated at: `{report.generated_at}`",
        f"Overall status: `{'PASS' if report.passed else 'FAIL'}`",
        "",
        "## Run Identity",
        "",
        "| Field | Value |",
        "|---|---|",
    ]
    for field_name in ("run_id", "strategy_id", "dataset_id", "parameter_version", "evidence_type", "proposed_capital_usd", "symbol_count"):
        lines.append(f"| `{field_name}` | `{getattr(snap, field_name)}` |")
    lines.extend(["", "## Metrics", "", "| Metric | Value |", "|---|---:|"])
    for metric_name in _REQUIRED_METRICS:
        value = snap.metrics.get(metric_name, "missing")
        lines.append(f"| `{metric_name}` | {value} |")
    lines.extend(["", "## Gates", "", "| Gate | Status | Message |", "|---|---|---|"])
    for gate in report.gates:
        status = "PASS" if gate.passed else "FAIL"
        message = gate.message if not gate.failures else f"{gate.message} Failures: {'; '.join(gate.failures)}"
        lines.append(f"| `{gate.name}` | `{status}` | {message} |")
    lines.extend(["", "---", "", report.footer, ""])
    return "\n".join(lines)


def write_capacity_turnover_realism_report(report: CapacityTurnoverRealismReport, *, output_json: str | Path, output_md: str | Path) -> None:
    json_path = Path(output_json)
    md_path = Path(output_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_capacity_turnover_realism_markdown(report), encoding="utf-8")


def _build_gates(snap: CapacityTurnoverSnapshot, policy: CapacityTurnoverRealismConfig) -> tuple[CapacityTurnoverGate, ...]:
    return (
        _required_fields_gate(snap),
        _required_metrics_gate(snap, policy),
        _positive_scale_gate(snap),
        _capacity_gate(snap, policy),
        _turnover_gate(snap, policy),
        _cost_drag_gate(snap, policy),
        _holding_period_gate(snap, policy),
        _trade_count_gate(snap, policy),
        _slippage_coverage_gate(snap, policy),
        _artifact_hashes_gate(snap),
        _public_safe_gate(snap),
        _research_footer_gate(snap, policy),
    )


def _gate(name: str, failures: list[str], success: str) -> CapacityTurnoverGate:
    return CapacityTurnoverGate(name, not failures, success if not failures else "Gate failed.", tuple(failures))


def _required_fields_gate(snap: CapacityTurnoverSnapshot) -> CapacityTurnoverGate:
    required = ("run_id", "strategy_id", "dataset_id", "parameter_version", "evidence_type")
    missing = [field_name for field_name in required if not getattr(snap, field_name)]
    return _gate("required_fields_complete", missing, "Capacity and turnover identity fields are complete.")


def _required_metrics_gate(snap: CapacityTurnoverSnapshot, policy: CapacityTurnoverRealismConfig) -> CapacityTurnoverGate:
    failures = []
    for metric in policy.required_metrics:
        if metric not in snap.metrics:
            failures.append(f"missing metric {metric}")
            continue
        try:
            _metric(snap.metrics, metric)
        except ValueError as exc:
            failures.append(str(exc))
    return _gate("required_metrics_valid", failures, "Required capacity and turnover metrics are present and numeric.")


def _positive_scale_gate(snap: CapacityTurnoverSnapshot) -> CapacityTurnoverGate:
    failures = []
    if snap.proposed_capital_usd <= 0:
        failures.append("proposed_capital_usd must be positive")
    if snap.symbol_count <= 0:
        failures.append("symbol_count must be positive")
    return _gate("positive_scale", failures, "Proposed capital and symbol count are positive.")


def _capacity_gate(snap: CapacityTurnoverSnapshot, policy: CapacityTurnoverRealismConfig) -> CapacityTurnoverGate:
    max_position = _metric_or_default(snap.metrics, "max_position_adv_pct")
    portfolio = _metric_or_default(snap.metrics, "portfolio_adv_pct")
    failures = []
    if max_position > policy.max_position_adv_pct:
        failures.append(f"max_position_adv_pct {max_position:.2f}% exceeds limit {policy.max_position_adv_pct:.2f}%")
    if portfolio > policy.max_portfolio_adv_pct:
        failures.append(f"portfolio_adv_pct {portfolio:.2f}% exceeds limit {policy.max_portfolio_adv_pct:.2f}%")
    return _gate("capacity_liquidity_limits", failures, "Capacity usage remains inside liquidity limits.")


def _turnover_gate(snap: CapacityTurnoverSnapshot, policy: CapacityTurnoverRealismConfig) -> CapacityTurnoverGate:
    daily = _metric_or_default(snap.metrics, "average_daily_turnover_pct")
    annual = _metric_or_default(snap.metrics, "annual_turnover_pct")
    failures = []
    if daily > policy.max_average_daily_turnover_pct:
        failures.append(f"average_daily_turnover_pct {daily:.2f}% exceeds limit {policy.max_average_daily_turnover_pct:.2f}%")
    if annual > policy.max_annual_turnover_pct:
        failures.append(f"annual_turnover_pct {annual:.2f}% exceeds limit {policy.max_annual_turnover_pct:.2f}%")
    return _gate("turnover_limits", failures, "Turnover remains inside realism limits.")


def _cost_drag_gate(snap: CapacityTurnoverSnapshot, policy: CapacityTurnoverRealismConfig) -> CapacityTurnoverGate:
    cost = _metric_or_default(snap.metrics, "round_trip_cost_bps")
    gross = _metric_or_default(snap.metrics, "gross_expectancy_bps")
    net = _metric_or_default(snap.metrics, "net_expectancy_bps")
    failures = []
    if gross <= 0:
        failures.append("gross_expectancy_bps must be positive")
    else:
        drag = cost / gross * 100.0
        if drag > policy.max_cost_to_gross_expectancy_pct:
            failures.append(f"cost-to-gross expectancy {drag:.2f}% exceeds limit {policy.max_cost_to_gross_expectancy_pct:.2f}%")
    if net < policy.min_net_expectancy_bps:
        failures.append(f"net_expectancy_bps {net:.2f} is below minimum {policy.min_net_expectancy_bps:.2f}")
    return _gate("cost_drag_realism", failures, "Transaction-cost drag leaves sufficient net expectancy.")


def _holding_period_gate(snap: CapacityTurnoverSnapshot, policy: CapacityTurnoverRealismConfig) -> CapacityTurnoverGate:
    holding = _metric_or_default(snap.metrics, "average_holding_days")
    failures = [] if holding >= policy.min_average_holding_days else [f"average_holding_days {holding:.2f} is below minimum {policy.min_average_holding_days:.2f}"]
    return _gate("holding_period_realism", failures, "Average holding period is consistent with the turnover model.")


def _trade_count_gate(snap: CapacityTurnoverSnapshot, policy: CapacityTurnoverRealismConfig) -> CapacityTurnoverGate:
    trade_count = _metric_or_default(snap.metrics, "trade_count")
    failures = [] if trade_count >= policy.min_trade_count else [f"trade_count {trade_count:.0f} is below minimum {policy.min_trade_count}"]
    return _gate("trade_count_floor", failures, "Trade count is sufficient for capacity/turnover review.")


def _slippage_coverage_gate(snap: CapacityTurnoverSnapshot, policy: CapacityTurnoverRealismConfig) -> CapacityTurnoverGate:
    coverage = _metric_or_default(snap.metrics, "slippage_model_coverage_pct")
    failures = [] if coverage >= policy.min_slippage_model_coverage_pct else [f"slippage_model_coverage_pct {coverage:.2f}% is below minimum {policy.min_slippage_model_coverage_pct:.2f}%"]
    return _gate("slippage_model_coverage", failures, "All reviewed trades include transaction-cost/slippage coverage.")


def _artifact_hashes_gate(snap: CapacityTurnoverSnapshot) -> CapacityTurnoverGate:
    failures = [] if snap.artifact_hashes else ["artifact_hashes are required"]
    return _gate("artifact_hashes_present", failures, "Capacity/turnover evidence artifacts are hash-referenced.")


def _public_safe_gate(snap: CapacityTurnoverSnapshot) -> CapacityTurnoverGate:
    failures = [] if "public_safe" in snap.tags else ["missing public_safe tag"]
    return _gate("public_safe_tags", failures, "Snapshot is marked public_safe.")


def _research_footer_gate(snap: CapacityTurnoverSnapshot, policy: CapacityTurnoverRealismConfig) -> CapacityTurnoverGate:
    if not policy.require_research_footer:
        return _gate("research_only_footer", [], "Research-only footer not required by config.")
    failures = [] if snap.footer == RESEARCH_ONLY_FOOTER else ["missing research-only footer"]
    return _gate("research_only_footer", failures, "Research-only footer is present.")


def _metric(metrics: Mapping[str, float | int], name: str) -> float:
    try:
        value = float(metrics[name])
    except KeyError as exc:
        raise ValueError(f"missing metric {name}") from exc
    except (TypeError, ValueError) as exc:
        raise ValueError(f"metric {name} is not numeric") from exc
    if not math.isfinite(value):
        raise ValueError(f"metric {name} is not finite")
    return value


def _metric_or_default(metrics: Mapping[str, float | int], name: str) -> float:
    try:
        return _metric(metrics, name)
    except ValueError:
        return 0.0


def _demo_payload() -> dict[str, Any]:
    return {
        "snapshot": {
            "run_id": "bt7-demo-2026-05-29",
            "strategy_id": "demo-momentum-sleeve",
            "dataset_id": "synthetic-public-demo-capacity-v1",
            "parameter_version": "demo-params-v1",
            "evidence_type": "capacity_turnover_realism",
            "proposed_capital_usd": 100000.0,
            "symbol_count": 25,
            "metrics": {
                "median_adv_usd": 75000000.0,
                "max_position_adv_pct": 1.25,
                "portfolio_adv_pct": 8.5,
                "average_daily_turnover_pct": 12.0,
                "annual_turnover_pct": 620.0,
                "round_trip_cost_bps": 7.5,
                "gross_expectancy_bps": 28.0,
                "net_expectancy_bps": 20.5,
                "average_holding_days": 4.2,
                "trade_count": 120,
                "slippage_model_coverage_pct": 100.0,
            },
            "artifact_hashes": {"capacity_input": "sha256:demo-capacity-input", "turnover_report": "sha256:demo-turnover-report"},
            "tags": ["demo", "public_safe"],
            "footer": RESEARCH_ONLY_FOOTER,
        }
    }
