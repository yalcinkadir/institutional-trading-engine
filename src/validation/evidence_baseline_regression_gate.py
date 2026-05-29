"""BT6 evidence baseline regression gate."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

RESEARCH_ONLY_FOOTER = "Research / Paper Observation Only. Execution is not authorized by this report."
_REQUIRED_METRICS = ("expectancy_r", "sharpe", "max_drawdown_pct", "oos_pass_rate_pct", "trade_count")


@dataclass(frozen=True)
class EvidenceBaselineRegressionConfig:
    required_metrics: tuple[str, ...] = _REQUIRED_METRICS
    max_expectancy_degradation_pct: float = 20.0
    max_sharpe_degradation_pct: float = 25.0
    max_oos_pass_rate_degradation_pct: float = 10.0
    max_drawdown_increase_pct: float = 15.0
    max_trade_count_drop_pct: float = 40.0
    require_same_strategy: bool = True
    require_same_dataset: bool = True
    require_research_footer: bool = True


@dataclass(frozen=True)
class EvidenceSnapshot:
    run_id: str
    strategy_id: str
    dataset_id: str
    parameter_version: str
    evidence_type: str
    metrics: Mapping[str, float | int]
    artifact_hashes: Mapping[str, str] = field(default_factory=dict)
    tags: tuple[str, ...] = ("demo", "public_safe")
    footer: str = RESEARCH_ONLY_FOOTER

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "EvidenceSnapshot":
        return cls(
            run_id=str(payload.get("run_id", "")).strip(),
            strategy_id=str(payload.get("strategy_id", "")).strip(),
            dataset_id=str(payload.get("dataset_id", "")).strip(),
            parameter_version=str(payload.get("parameter_version", "")).strip(),
            evidence_type=str(payload.get("evidence_type", "")).strip(),
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
            "metrics": dict(self.metrics),
            "artifact_hashes": dict(self.artifact_hashes),
            "tags": list(self.tags),
            "footer": self.footer,
        }


@dataclass(frozen=True)
class EvidenceBaselineDelta:
    metric: str
    baseline: float
    current: float
    delta: float
    degradation_pct: float

    def to_dict(self) -> dict[str, Any]:
        return {"metric": self.metric, "baseline": round(self.baseline, 4), "current": round(self.current, 4), "delta": round(self.delta, 4), "degradation_pct": round(self.degradation_pct, 2)}


@dataclass(frozen=True)
class EvidenceBaselineGate:
    name: str
    passed: bool
    message: str
    failures: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "passed": self.passed, "message": self.message, "failures": list(self.failures)}


@dataclass(frozen=True)
class EvidenceBaselineRegressionReport:
    version: str
    generated_at: str
    baseline: EvidenceSnapshot
    current: EvidenceSnapshot
    deltas: tuple[EvidenceBaselineDelta, ...]
    gates: tuple[EvidenceBaselineGate, ...]
    passed: bool
    footer: str = RESEARCH_ONLY_FOOTER

    def to_dict(self) -> dict[str, Any]:
        return {"version": self.version, "generated_at": self.generated_at, "passed": self.passed, "baseline": self.baseline.to_dict(), "current": self.current.to_dict(), "deltas": [d.to_dict() for d in self.deltas], "gates": [g.to_dict() for g in self.gates], "footer": self.footer}


def build_evidence_baseline_regression_report(baseline: EvidenceSnapshot | Mapping[str, Any], current: EvidenceSnapshot | Mapping[str, Any], *, config: EvidenceBaselineRegressionConfig | None = None, version: str = "BT6-v1", generated_at: str | None = None) -> EvidenceBaselineRegressionReport:
    policy = config or EvidenceBaselineRegressionConfig()
    base = baseline if isinstance(baseline, EvidenceSnapshot) else EvidenceSnapshot.from_mapping(baseline)
    cur = current if isinstance(current, EvidenceSnapshot) else EvidenceSnapshot.from_mapping(current)
    deltas = _build_deltas(base, cur, policy)
    gates = _build_gates(base, cur, deltas, policy)
    return EvidenceBaselineRegressionReport(version, generated_at or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"), base, cur, deltas, gates, all(g.passed for g in gates))


def load_evidence_baseline_regression_json(path: str | Path) -> tuple[EvidenceSnapshot, EvidenceSnapshot]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping):
        raise ValueError("BT6 JSON must contain baseline and current objects.")
    return EvidenceSnapshot.from_mapping(payload.get("baseline", {})), EvidenceSnapshot.from_mapping(payload.get("current", {}))


def demo_evidence_baseline_pair() -> tuple[EvidenceSnapshot, EvidenceSnapshot]:
    return load_evidence_baseline_regression_payload(_demo_payload())


def load_evidence_baseline_regression_payload(payload: Mapping[str, Any]) -> tuple[EvidenceSnapshot, EvidenceSnapshot]:
    return EvidenceSnapshot.from_mapping(payload.get("baseline", {})), EvidenceSnapshot.from_mapping(payload.get("current", {}))


def render_evidence_baseline_regression_markdown(report: EvidenceBaselineRegressionReport) -> str:
    lines = ["# BT6 Evidence Baseline Regression Gate Report", "", f"Generated at: `{report.generated_at}`", f"Overall status: `{'PASS' if report.passed else 'FAIL'}`", "", "## Run Pair", "", "| Field | Baseline | Current |", "|---|---|---|"]
    for field_name in ("run_id", "strategy_id", "dataset_id", "parameter_version", "evidence_type"):
        lines.append(f"| `{field_name}` | `{getattr(report.baseline, field_name)}` | `{getattr(report.current, field_name)}` |")
    lines.extend(["", "## Metric Deltas", "", "| Metric | Baseline | Current | Delta | Degradation % |", "|---|---:|---:|---:|---:|"])
    for delta in report.deltas:
        lines.append(f"| `{delta.metric}` | {delta.baseline:.4f} | {delta.current:.4f} | {delta.delta:.4f} | {delta.degradation_pct:.2f} |")
    lines.extend(["", "## Gates", "", "| Gate | Status | Message |", "|---|---|---|"])
    for gate in report.gates:
        status = "PASS" if gate.passed else "FAIL"
        message = gate.message if not gate.failures else f"{gate.message} Failures: {'; '.join(gate.failures)}"
        lines.append(f"| `{gate.name}` | `{status}` | {message} |")
    lines.extend(["", "---", "", report.footer, ""])
    return "\n".join(lines)


def write_evidence_baseline_regression_report(report: EvidenceBaselineRegressionReport, *, output_json: str | Path, output_md: str | Path) -> None:
    json_path = Path(output_json)
    md_path = Path(output_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_evidence_baseline_regression_markdown(report), encoding="utf-8")


def _build_deltas(base: EvidenceSnapshot, cur: EvidenceSnapshot, policy: EvidenceBaselineRegressionConfig) -> tuple[EvidenceBaselineDelta, ...]:
    deltas = []
    for metric in policy.required_metrics:
        b = _metric(base.metrics, metric)
        c = _metric(cur.metrics, metric)
        deltas.append(EvidenceBaselineDelta(metric, b, c, c - b, _degradation_pct(metric, b, c)))
    return tuple(deltas)


def _build_gates(base: EvidenceSnapshot, cur: EvidenceSnapshot, deltas: tuple[EvidenceBaselineDelta, ...], policy: EvidenceBaselineRegressionConfig) -> tuple[EvidenceBaselineGate, ...]:
    by_metric = {d.metric: d for d in deltas}
    return (
        _required_fields_gate(base, cur),
        _same_identity_gate("strategy_id", base.strategy_id, cur.strategy_id, policy.require_same_strategy),
        _same_identity_gate("dataset_id", base.dataset_id, cur.dataset_id, policy.require_same_dataset),
        _required_metrics_gate(base, cur, policy),
        _gate("artifact_hashes_present", [] if base.artifact_hashes and cur.artifact_hashes else ["baseline and current artifact_hashes are required"], "Baseline and current evidence artifacts are hash-referenced."),
        _metric_gate("expectancy_regression", by_metric, "expectancy_r", policy.max_expectancy_degradation_pct, "Expectancy degradation stays within limit."),
        _metric_gate("sharpe_regression", by_metric, "sharpe", policy.max_sharpe_degradation_pct, "Sharpe degradation stays within limit."),
        _metric_gate("oos_pass_rate_regression", by_metric, "oos_pass_rate_pct", policy.max_oos_pass_rate_degradation_pct, "OOS pass-rate degradation stays within limit."),
        _drawdown_gate(by_metric, policy),
        _trade_count_gate(by_metric, policy),
        _public_safe_gate(base, cur),
        _research_footer_gate(base, cur, policy),
    )


def _gate(name: str, failures: list[str], success: str) -> EvidenceBaselineGate:
    return EvidenceBaselineGate(name, not failures, success if not failures else "Gate failed.", tuple(failures))


def _required_fields_gate(base: EvidenceSnapshot, cur: EvidenceSnapshot) -> EvidenceBaselineGate:
    failures = []
    required = ("run_id", "strategy_id", "dataset_id", "parameter_version", "evidence_type")
    for label, snap in (("baseline", base), ("current", cur)):
        missing = [field_name for field_name in required if not getattr(snap, field_name)]
        if missing:
            failures.append(f"{label}: missing {', '.join(missing)}")
    return _gate("required_fields_complete", failures, "Baseline and current identity fields are complete.")


def _same_identity_gate(name: str, base_value: str, current_value: str, required: bool) -> EvidenceBaselineGate:
    failures = [] if (not required or base_value == current_value) else [f"baseline {name} {base_value!r} differs from current {name} {current_value!r}"]
    return _gate(f"same_{name}", failures, f"Baseline and current {name} are comparable.")


def _required_metrics_gate(base: EvidenceSnapshot, cur: EvidenceSnapshot, policy: EvidenceBaselineRegressionConfig) -> EvidenceBaselineGate:
    failures = []
    for label, snap in (("baseline", base), ("current", cur)):
        for metric in policy.required_metrics:
            if metric not in snap.metrics:
                failures.append(f"{label}: missing metric {metric}")
                continue
            try:
                _metric(snap.metrics, metric)
            except ValueError as exc:
                failures.append(f"{label}: {exc}")
    return _gate("required_metrics_valid", failures, "Required baseline and current metrics are present and numeric.")


def _metric_gate(name: str, by_metric: Mapping[str, EvidenceBaselineDelta], metric: str, limit: float, success: str) -> EvidenceBaselineGate:
    d = by_metric[metric]
    failures = [] if d.degradation_pct <= limit else [f"{metric} degradation {d.degradation_pct:.2f}% exceeds limit {limit:.2f}%"]
    return _gate(name, failures, success)


def _drawdown_gate(by_metric: Mapping[str, EvidenceBaselineDelta], policy: EvidenceBaselineRegressionConfig) -> EvidenceBaselineGate:
    d = by_metric["max_drawdown_pct"]
    increase = max(0.0, d.current - d.baseline)
    failures = [] if increase <= policy.max_drawdown_increase_pct else [f"max_drawdown_pct increased by {increase:.2f} points, limit {policy.max_drawdown_increase_pct:.2f}"]
    return _gate("drawdown_regression", failures, "Drawdown increase stays within limit.")


def _trade_count_gate(by_metric: Mapping[str, EvidenceBaselineDelta], policy: EvidenceBaselineRegressionConfig) -> EvidenceBaselineGate:
    d = by_metric["trade_count"]
    drop_pct = max(0.0, _percent_drop(d.baseline, d.current))
    failures = [] if drop_pct <= policy.max_trade_count_drop_pct else [f"trade_count dropped by {drop_pct:.2f}%, limit {policy.max_trade_count_drop_pct:.2f}%"]
    return _gate("trade_count_regression", failures, "Trade-count drop stays within limit.")


def _public_safe_gate(base: EvidenceSnapshot, cur: EvidenceSnapshot) -> EvidenceBaselineGate:
    failures = []
    for label, snap in (("baseline", base), ("current", cur)):
        if "public_safe" not in snap.tags:
            failures.append(f"{label}: missing public_safe tag")
    return _gate("public_safe_tags", failures, "Snapshots are marked public_safe.")


def _research_footer_gate(base: EvidenceSnapshot, cur: EvidenceSnapshot, policy: EvidenceBaselineRegressionConfig) -> EvidenceBaselineGate:
    if not policy.require_research_footer:
        return _gate("research_only_footer", [], "Research-only footer not required by config.")
    failures = []
    for label, snap in (("baseline", base), ("current", cur)):
        if snap.footer != RESEARCH_ONLY_FOOTER:
            failures.append(f"{label}: missing research-only footer")
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


def _degradation_pct(metric: str, baseline: float, current: float) -> float:
    if metric == "max_drawdown_pct":
        return max(0.0, current - baseline)
    return _percent_drop(baseline, current)


def _percent_drop(baseline: float, current: float) -> float:
    if baseline <= 0:
        return 0.0 if current >= baseline else 100.0
    return max(0.0, (baseline - current) / baseline * 100.0)


def _demo_payload() -> dict[str, Any]:
    return {
        "baseline": {"run_id": "bt5-baseline-demo-001", "strategy_id": "demo-momentum-sleeve", "dataset_id": "synthetic-public-oos-v1", "parameter_version": "demo-params-v1", "evidence_type": "walk_forward_oos", "metrics": {"expectancy_r": 0.42, "sharpe": 1.35, "max_drawdown_pct": 9.5, "oos_pass_rate_pct": 75.0, "trade_count": 84}, "artifact_hashes": {"bt5_report": "sha256:baseline-demo"}, "tags": ["demo", "public_safe"]},
        "current": {"run_id": "bt5-current-demo-002", "strategy_id": "demo-momentum-sleeve", "dataset_id": "synthetic-public-oos-v1", "parameter_version": "demo-params-v2", "evidence_type": "walk_forward_oos", "metrics": {"expectancy_r": 0.38, "sharpe": 1.18, "max_drawdown_pct": 11.0, "oos_pass_rate_pct": 70.0, "trade_count": 78}, "artifact_hashes": {"bt5_report": "sha256:current-demo"}, "tags": ["demo", "public_safe"]},
    }
