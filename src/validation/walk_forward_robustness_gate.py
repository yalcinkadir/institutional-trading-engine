"""BT5 walk-forward / out-of-sample robustness gate."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

RESEARCH_ONLY_FOOTER = "Research / Paper Observation Only. Execution is not authorized by this report."
_REQUIRED_METRICS = ("expectancy_r", "sharpe", "max_drawdown_pct", "trade_count")


@dataclass(frozen=True)
class WalkForwardRobustnessConfig:
    required_metrics: tuple[str, ...] = _REQUIRED_METRICS
    primary_metric: str = "expectancy_r"
    min_folds: int = 3
    min_oos_pass_rate_pct: float = 66.67
    min_positive_oos_metric_rate_pct: float = 66.67
    max_primary_metric_degradation_pct: float = 50.0
    max_oos_drawdown_pct: float = 20.0
    min_oos_trades_per_fold: int = 5
    require_research_footer: bool = True


@dataclass(frozen=True)
class WalkForwardFold:
    fold_id: str
    strategy_id: str
    parameter_version: str
    dataset_id: str
    train_start: str
    train_end: str
    oos_start: str
    oos_end: str
    train_metrics: Mapping[str, float | int]
    oos_metrics: Mapping[str, float | int]
    tags: tuple[str, ...] = ("demo", "public_safe")
    notes: str = ""
    footer: str = RESEARCH_ONLY_FOOTER

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "WalkForwardFold":
        return cls(
            fold_id=str(payload.get("fold_id", "")).strip(),
            strategy_id=str(payload.get("strategy_id", "")).strip(),
            parameter_version=str(payload.get("parameter_version", "")).strip(),
            dataset_id=str(payload.get("dataset_id", "")).strip(),
            train_start=str(payload.get("train_start", "")).strip(),
            train_end=str(payload.get("train_end", "")).strip(),
            oos_start=str(payload.get("oos_start", "")).strip(),
            oos_end=str(payload.get("oos_end", "")).strip(),
            train_metrics=dict(payload.get("train_metrics", {})),
            oos_metrics=dict(payload.get("oos_metrics", {})),
            tags=tuple(str(tag).strip() for tag in payload.get("tags", ("demo", "public_safe"))),
            notes=str(payload.get("notes", "")).strip(),
            footer=str(payload.get("footer", RESEARCH_ONLY_FOOTER)).strip(),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "fold_id": self.fold_id,
            "strategy_id": self.strategy_id,
            "parameter_version": self.parameter_version,
            "dataset_id": self.dataset_id,
            "train_start": self.train_start,
            "train_end": self.train_end,
            "oos_start": self.oos_start,
            "oos_end": self.oos_end,
            "train_metrics": dict(self.train_metrics),
            "oos_metrics": dict(self.oos_metrics),
            "tags": list(self.tags),
            "notes": self.notes,
            "footer": self.footer,
        }


@dataclass(frozen=True)
class WalkForwardRobustnessMetrics:
    fold_count: int
    strategy_count: int
    dataset_count: int
    oos_pass_rate_pct: float
    positive_oos_metric_rate_pct: float
    average_primary_train_metric: float
    average_primary_oos_metric: float
    average_primary_degradation_pct: float
    worst_oos_drawdown_pct: float
    total_oos_trades: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "fold_count": self.fold_count,
            "strategy_count": self.strategy_count,
            "dataset_count": self.dataset_count,
            "oos_pass_rate_pct": round(self.oos_pass_rate_pct, 2),
            "positive_oos_metric_rate_pct": round(self.positive_oos_metric_rate_pct, 2),
            "average_primary_train_metric": round(self.average_primary_train_metric, 4),
            "average_primary_oos_metric": round(self.average_primary_oos_metric, 4),
            "average_primary_degradation_pct": round(self.average_primary_degradation_pct, 2),
            "worst_oos_drawdown_pct": round(self.worst_oos_drawdown_pct, 2),
            "total_oos_trades": self.total_oos_trades,
        }


@dataclass(frozen=True)
class WalkForwardRobustnessGate:
    name: str
    passed: bool
    message: str
    failures: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "passed": self.passed, "message": self.message, "failures": list(self.failures)}


@dataclass(frozen=True)
class WalkForwardRobustnessReport:
    version: str
    generated_at: str
    folds: tuple[WalkForwardFold, ...]
    metrics: WalkForwardRobustnessMetrics
    gates: tuple[WalkForwardRobustnessGate, ...]
    passed: bool
    footer: str = RESEARCH_ONLY_FOOTER

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "generated_at": self.generated_at,
            "passed": self.passed,
            "metrics": self.metrics.to_dict(),
            "gates": [gate.to_dict() for gate in self.gates],
            "folds": [fold.to_dict() for fold in self.folds],
            "footer": self.footer,
        }


def build_walk_forward_robustness_report(folds: Sequence[WalkForwardFold | Mapping[str, Any]], *, config: WalkForwardRobustnessConfig | None = None, version: str = "BT5-v1", generated_at: str | None = None) -> WalkForwardRobustnessReport:
    policy = config or WalkForwardRobustnessConfig()
    normalized = tuple(f if isinstance(f, WalkForwardFold) else WalkForwardFold.from_mapping(f) for f in folds)
    metrics = _build_metrics(normalized, policy)
    gates = _build_gates(normalized, policy, metrics)
    return WalkForwardRobustnessReport(version, generated_at or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"), normalized, metrics, gates, all(g.passed for g in gates))


def load_walk_forward_folds_json(path: str | Path) -> tuple[WalkForwardFold, ...]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    raw = payload.get("folds", payload.get("walk_forward_folds", [])) if isinstance(payload, Mapping) else payload
    if not isinstance(raw, list):
        raise ValueError("Walk-forward JSON must contain a list, 'folds' or 'walk_forward_folds'.")
    return tuple(WalkForwardFold.from_mapping(item) for item in raw)


def demo_walk_forward_folds() -> tuple[WalkForwardFold, ...]:
    return tuple(WalkForwardFold.from_mapping(item) for item in _demo_payloads())


def render_walk_forward_robustness_markdown(report: WalkForwardRobustnessReport) -> str:
    lines = ["# BT5 Walk-Forward / Out-of-Sample Robustness Gate Report", "", f"Generated at: `{report.generated_at}`", f"Overall status: `{'PASS' if report.passed else 'FAIL'}`", "", "## Metrics", "", "| Metric | Value |", "|---|---:|"]
    for key, value in report.metrics.to_dict().items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(["", "## Gates", "", "| Gate | Status | Message |", "|---|---|---|"])
    for gate in report.gates:
        status = "PASS" if gate.passed else "FAIL"
        message = gate.message if not gate.failures else f"{gate.message} Failures: {'; '.join(gate.failures)}"
        lines.append(f"| `{gate.name}` | `{status}` | {message} |")
    lines.extend(["", "## Folds", "", "| Fold | Strategy | Dataset | Train Window | OOS Window | OOS Expectancy R | OOS Sharpe | OOS Trades |", "|---|---|---|---|---|---:|---:|---:|"])
    for fold in report.folds:
        lines.append(f"| `{fold.fold_id}` | `{fold.strategy_id}` | `{fold.dataset_id}` | {fold.train_start} to {fold.train_end} | {fold.oos_start} to {fold.oos_end} | {_metric(fold.oos_metrics, 'expectancy_r'):.4f} | {_metric(fold.oos_metrics, 'sharpe'):.4f} | {int(_metric(fold.oos_metrics, 'trade_count'))} |")
    lines.extend(["", "---", "", report.footer, ""])
    return "\n".join(lines)


def write_walk_forward_robustness_report(report: WalkForwardRobustnessReport, *, output_json: str | Path, output_md: str | Path) -> None:
    json_path = Path(output_json)
    md_path = Path(output_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_walk_forward_robustness_markdown(report), encoding="utf-8")


def _build_metrics(folds: Sequence[WalkForwardFold], policy: WalkForwardRobustnessConfig) -> WalkForwardRobustnessMetrics:
    if not folds:
        return WalkForwardRobustnessMetrics(0, 0, 0, 0.0, 0.0, 0.0, 0.0, 100.0, 0.0, 0)
    train = [_metric(f.train_metrics, policy.primary_metric) for f in folds]
    oos = [_metric(f.oos_metrics, policy.primary_metric) for f in folds]
    avg_train = sum(train) / len(train)
    avg_oos = sum(oos) / len(oos)
    return WalkForwardRobustnessMetrics(
        len(folds),
        len({f.strategy_id for f in folds if f.strategy_id}),
        len({f.dataset_id for f in folds if f.dataset_id}),
        sum(1 for f in folds if _fold_oos_passes(f, policy)) / len(folds) * 100.0,
        sum(1 for f in folds if _metric(f.oos_metrics, policy.primary_metric) > 0) / len(folds) * 100.0,
        avg_train,
        avg_oos,
        _degradation_pct(avg_train, avg_oos),
        max((_metric(f.oos_metrics, "max_drawdown_pct") for f in folds), default=0.0),
        sum(int(_metric(f.oos_metrics, "trade_count")) for f in folds),
    )


def _build_gates(folds: Sequence[WalkForwardFold], policy: WalkForwardRobustnessConfig, metrics: WalkForwardRobustnessMetrics) -> tuple[WalkForwardRobustnessGate, ...]:
    return (
        _gate("non_empty_fold_set", [] if folds else ["no walk-forward folds supplied"], "At least one fold is present."),
        _gate("minimum_fold_count", [] if len(folds) >= policy.min_folds else [f"fold_count {len(folds)} below required minimum {policy.min_folds}"], "Minimum walk-forward fold count is satisfied."),
        _required_fields_gate(folds),
        _chronology_gate(folds),
        _required_metrics_gate(folds, policy),
        _oos_trade_count_gate(folds, policy),
        _oos_drawdown_gate(folds, policy),
        _gate("minimum_oos_pass_rate", [] if metrics.oos_pass_rate_pct >= policy.min_oos_pass_rate_pct else [f"OOS pass rate {metrics.oos_pass_rate_pct:.2f}% below required {policy.min_oos_pass_rate_pct:.2f}%"], "Enough folds satisfy positive OOS expectancy, drawdown and trade-count gates."),
        _gate("positive_oos_primary_metric_rate", [] if metrics.positive_oos_metric_rate_pct >= policy.min_positive_oos_metric_rate_pct else [f"positive OOS {policy.primary_metric} rate {metrics.positive_oos_metric_rate_pct:.2f}% below required {policy.min_positive_oos_metric_rate_pct:.2f}%"], "Primary OOS metric is positive across enough folds."),
        _gate("train_to_oos_degradation_limit", [] if metrics.average_primary_degradation_pct <= policy.max_primary_metric_degradation_pct else [f"average primary metric degradation {metrics.average_primary_degradation_pct:.2f}% exceeds limit {policy.max_primary_metric_degradation_pct:.2f}%"], "Average train-to-OOS primary metric degradation remains within limit."),
        _public_safe_gate(folds),
        _research_footer_gate(folds, policy),
    )


def _gate(name: str, failures: Sequence[str], success: str) -> WalkForwardRobustnessGate:
    return WalkForwardRobustnessGate(name, not failures, success if not failures else "Gate failed.", tuple(failures))


def _required_fields_gate(folds: Sequence[WalkForwardFold]) -> WalkForwardRobustnessGate:
    required = ("fold_id", "strategy_id", "parameter_version", "dataset_id", "train_start", "train_end", "oos_start", "oos_end")
    failures = []
    for fold in folds:
        missing = [name for name in required if not fold.to_dict().get(name)]
        if missing:
            failures.append(f"{fold.fold_id or '<missing-fold-id>'}: missing {', '.join(missing)}")
    return _gate("required_fields_complete", failures, "Required fold identity and window fields are complete.")


def _chronology_gate(folds: Sequence[WalkForwardFold]) -> WalkForwardRobustnessGate:
    failures = []
    parsed = []
    for fold in folds:
        try:
            ts, te, os, oe = map(_parse_date, (fold.train_start, fold.train_end, fold.oos_start, fold.oos_end))
        except ValueError as exc:
            failures.append(f"{fold.fold_id or '<missing-fold-id>'}: {exc}")
            continue
        if ts > te:
            failures.append(f"{fold.fold_id}: train_start after train_end")
        if os > oe:
            failures.append(f"{fold.fold_id}: oos_start after oos_end")
        if te >= os:
            failures.append(f"{fold.fold_id}: train window overlaps or touches OOS window")
        parsed.append((os, oe, fold.fold_id))
    for previous, current in zip(sorted(parsed), sorted(parsed)[1:]):
        if previous[1] >= current[0]:
            failures.append(f"{current[2]}: OOS window overlaps previous fold {previous[2]}")
    return _gate("chronological_walk_forward_windows", failures, "Train and OOS windows are chronological and non-overlapping.")


def _required_metrics_gate(folds: Sequence[WalkForwardFold], policy: WalkForwardRobustnessConfig) -> WalkForwardRobustnessGate:
    failures = []
    for fold in folds:
        for scope, metrics in (("train", fold.train_metrics), ("oos", fold.oos_metrics)):
            for metric in policy.required_metrics:
                if metric not in metrics:
                    failures.append(f"{fold.fold_id}: missing {scope} metric {metric}")
                elif not _is_number(metrics[metric]):
                    failures.append(f"{fold.fold_id}: non-numeric {scope} metric {metric}")
    return _gate("required_metrics_present", failures, "Required train and OOS metrics are present and numeric.")


def _oos_trade_count_gate(folds: Sequence[WalkForwardFold], policy: WalkForwardRobustnessConfig) -> WalkForwardRobustnessGate:
    failures = [f"{f.fold_id}: OOS trade_count {int(_metric(f.oos_metrics, 'trade_count'))} below minimum {policy.min_oos_trades_per_fold}" for f in folds if _metric(f.oos_metrics, "trade_count") < policy.min_oos_trades_per_fold]
    return _gate("minimum_oos_trade_count", failures, "Each OOS fold has enough trades for a public-safe robustness smoke gate.")


def _oos_drawdown_gate(folds: Sequence[WalkForwardFold], policy: WalkForwardRobustnessConfig) -> WalkForwardRobustnessGate:
    failures = [f"{f.fold_id}: OOS max_drawdown_pct {_metric(f.oos_metrics, 'max_drawdown_pct')} exceeds limit {policy.max_oos_drawdown_pct}" for f in folds if _metric(f.oos_metrics, "max_drawdown_pct") > policy.max_oos_drawdown_pct]
    return _gate("oos_drawdown_within_limit", failures, "OOS drawdown remains within configured public demo limit.")


def _public_safe_gate(folds: Sequence[WalkForwardFold]) -> WalkForwardRobustnessGate:
    failures = [f"{f.fold_id}: missing required demo/public_safe tags" for f in folds if not {"demo", "public_safe"}.issubset(set(f.tags))]
    return _gate("public_safe_demo_tags", failures, "Folds are marked demo and public_safe.")


def _research_footer_gate(folds: Sequence[WalkForwardFold], policy: WalkForwardRobustnessConfig) -> WalkForwardRobustnessGate:
    failures = [f"{f.fold_id}: missing research-only footer" for f in folds if policy.require_research_footer and f.footer != RESEARCH_ONLY_FOOTER]
    return _gate("research_footer_present", failures, "Research-only footer is present on every fold.")


def _fold_oos_passes(fold: WalkForwardFold, policy: WalkForwardRobustnessConfig) -> bool:
    return _metric(fold.oos_metrics, policy.primary_metric) > 0 and _metric(fold.oos_metrics, "max_drawdown_pct") <= policy.max_oos_drawdown_pct and _metric(fold.oos_metrics, "trade_count") >= policy.min_oos_trades_per_fold


def _metric(metrics: Mapping[str, Any], name: str) -> float:
    value = metrics.get(name, 0.0)
    return float(value) if _is_number(value) else 0.0


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def _degradation_pct(train: float, oos: float) -> float:
    if train <= 0:
        return 0.0 if oos >= train else 100.0
    return max(0.0, (train - oos) / abs(train) * 100.0)


def _parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"invalid date {value!r}") from exc


def _demo_payloads() -> list[dict[str, Any]]:
    return [
        {"fold_id": "bt5-demo-fold-001", "strategy_id": "demo_trend_following", "parameter_version": "demo-params-v1", "dataset_id": "synthetic-wf-demo-v1", "train_start": "2024-01-01", "train_end": "2024-03-31", "oos_start": "2024-04-01", "oos_end": "2024-04-30", "train_metrics": {"expectancy_r": 0.42, "sharpe": 1.35, "max_drawdown_pct": 8.4, "trade_count": 42}, "oos_metrics": {"expectancy_r": 0.26, "sharpe": 1.02, "max_drawdown_pct": 9.8, "trade_count": 11}, "tags": ["demo", "public_safe"], "notes": "Synthetic public-safe fold. Not production edge.", "footer": RESEARCH_ONLY_FOOTER},
        {"fold_id": "bt5-demo-fold-002", "strategy_id": "demo_trend_following", "parameter_version": "demo-params-v1", "dataset_id": "synthetic-wf-demo-v1", "train_start": "2024-02-01", "train_end": "2024-04-30", "oos_start": "2024-05-01", "oos_end": "2024-05-31", "train_metrics": {"expectancy_r": 0.38, "sharpe": 1.22, "max_drawdown_pct": 7.9, "trade_count": 39}, "oos_metrics": {"expectancy_r": 0.21, "sharpe": 0.88, "max_drawdown_pct": 10.2, "trade_count": 9}, "tags": ["demo", "public_safe"], "notes": "Synthetic public-safe fold. Not production edge.", "footer": RESEARCH_ONLY_FOOTER},
        {"fold_id": "bt5-demo-fold-003", "strategy_id": "demo_mean_reversion_placeholder", "parameter_version": "demo-params-v1", "dataset_id": "synthetic-wf-demo-v1", "train_start": "2024-03-01", "train_end": "2024-05-31", "oos_start": "2024-06-01", "oos_end": "2024-06-30", "train_metrics": {"expectancy_r": 0.31, "sharpe": 1.05, "max_drawdown_pct": 9.1, "trade_count": 37}, "oos_metrics": {"expectancy_r": 0.17, "sharpe": 0.76, "max_drawdown_pct": 11.7, "trade_count": 8}, "tags": ["demo", "public_safe"], "notes": "Synthetic public-safe fold. Not production edge.", "footer": RESEARCH_ONLY_FOOTER},
    ]
