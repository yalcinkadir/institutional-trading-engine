"""BT4 backtest result quality gate.

BT4 evaluates whether reported historical validation metrics are sufficient for
continued research or paper observation. It does not approve capital use or
execution. It is intentionally fail-closed when data is missing or too thin.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

RESEARCH_ONLY_FOOTER = "Research / Paper Observation Only. Result quality is not execution approval."


@dataclass(frozen=True)
class BacktestResultQualityConfig:
    min_trade_count: int = 30
    max_drawdown_pct_floor: float = -12.0
    min_expectancy_r: float = 0.05
    min_profit_factor: float = 1.15
    min_sharpe: float = 0.75
    max_loss_rate_pct: float = 55.0
    min_regime_count: int = 2
    max_single_regime_trade_share_pct: float = 80.0
    require_public_safe_tags: bool = True
    require_research_footer: bool = True


@dataclass(frozen=True)
class RegimeQualitySlice:
    regime: str
    trade_count: int
    expectancy_r: float
    max_drawdown_pct: float
    profit_factor: float

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "RegimeQualitySlice":
        return cls(
            regime=str(payload.get("regime", "")).strip(),
            trade_count=int(payload.get("trade_count", 0)),
            expectancy_r=float(payload.get("expectancy_r", 0.0)),
            max_drawdown_pct=float(payload.get("max_drawdown_pct", 0.0)),
            profit_factor=float(payload.get("profit_factor", 0.0)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "regime": self.regime,
            "trade_count": self.trade_count,
            "expectancy_r": self.expectancy_r,
            "max_drawdown_pct": self.max_drawdown_pct,
            "profit_factor": self.profit_factor,
        }


@dataclass(frozen=True)
class BacktestResultQualityCase:
    run_id: str
    strategy_id: str
    contract_version: str
    trade_count: int
    max_drawdown_pct: float
    expectancy_r: float
    profit_factor: float
    sharpe: float
    win_rate_pct: float
    loss_rate_pct: float
    total_return_pct: float
    regime_slices: tuple[RegimeQualitySlice, ...]
    tags: tuple[str, ...] = ("demo", "public_safe")
    notes: str = ""
    footer: str = RESEARCH_ONLY_FOOTER

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "BacktestResultQualityCase":
        return cls(
            run_id=str(payload.get("run_id", "")).strip(),
            strategy_id=str(payload.get("strategy_id", "")).strip(),
            contract_version=str(payload.get("contract_version", "")).strip(),
            trade_count=int(payload.get("trade_count", 0)),
            max_drawdown_pct=float(payload.get("max_drawdown_pct", 0.0)),
            expectancy_r=float(payload.get("expectancy_r", 0.0)),
            profit_factor=float(payload.get("profit_factor", 0.0)),
            sharpe=float(payload.get("sharpe", 0.0)),
            win_rate_pct=float(payload.get("win_rate_pct", 0.0)),
            loss_rate_pct=float(payload.get("loss_rate_pct", 0.0)),
            total_return_pct=float(payload.get("total_return_pct", 0.0)),
            regime_slices=tuple(RegimeQualitySlice.from_mapping(item) for item in payload.get("regime_slices", [])),
            tags=tuple(str(tag).strip() for tag in payload.get("tags", ("demo", "public_safe"))),
            notes=str(payload.get("notes", "")).strip(),
            footer=str(payload.get("footer", RESEARCH_ONLY_FOOTER)).strip(),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "strategy_id": self.strategy_id,
            "contract_version": self.contract_version,
            "trade_count": self.trade_count,
            "max_drawdown_pct": self.max_drawdown_pct,
            "expectancy_r": self.expectancy_r,
            "profit_factor": self.profit_factor,
            "sharpe": self.sharpe,
            "win_rate_pct": self.win_rate_pct,
            "loss_rate_pct": self.loss_rate_pct,
            "total_return_pct": self.total_return_pct,
            "regime_slices": [item.to_dict() for item in self.regime_slices],
            "tags": list(self.tags),
            "notes": self.notes,
            "footer": self.footer,
        }


@dataclass(frozen=True)
class BacktestResultQualityGate:
    name: str
    passed: bool
    message: str
    failures: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "passed": self.passed,
            "message": self.message,
            "failures": list(self.failures),
        }


@dataclass(frozen=True)
class BacktestResultQualityMetrics:
    case_count: int
    passing_case_count: int
    failing_case_count: int
    average_trade_count: float
    average_expectancy_r: float
    average_profit_factor: float
    average_sharpe: float
    worst_drawdown_pct: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_count": self.case_count,
            "passing_case_count": self.passing_case_count,
            "failing_case_count": self.failing_case_count,
            "average_trade_count": round(self.average_trade_count, 2),
            "average_expectancy_r": round(self.average_expectancy_r, 4),
            "average_profit_factor": round(self.average_profit_factor, 4),
            "average_sharpe": round(self.average_sharpe, 4),
            "worst_drawdown_pct": round(self.worst_drawdown_pct, 4),
        }


@dataclass(frozen=True)
class BacktestResultQualityReport:
    version: str
    generated_at: str
    cases: tuple[BacktestResultQualityCase, ...]
    gates: tuple[BacktestResultQualityGate, ...]
    metrics: BacktestResultQualityMetrics
    passed: bool
    footer: str = RESEARCH_ONLY_FOOTER

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "generated_at": self.generated_at,
            "passed": self.passed,
            "metrics": self.metrics.to_dict(),
            "gates": [gate.to_dict() for gate in self.gates],
            "cases": [case.to_dict() for case in self.cases],
            "footer": self.footer,
        }


def build_backtest_result_quality_report(
    cases: Sequence[BacktestResultQualityCase | Mapping[str, Any]],
    *,
    config: BacktestResultQualityConfig | None = None,
    version: str = "BT4-v1",
    generated_at: str | None = None,
) -> BacktestResultQualityReport:
    policy = config or BacktestResultQualityConfig()
    normalized = tuple(case if isinstance(case, BacktestResultQualityCase) else BacktestResultQualityCase.from_mapping(case) for case in cases)
    case_gate_results = tuple(_evaluate_case(case, policy) for case in normalized)
    aggregate_gates = _aggregate_gates(normalized, case_gate_results)
    gates = tuple(gate for case_gates in case_gate_results for gate in case_gates) + aggregate_gates
    passing_cases = sum(1 for case_gates in case_gate_results if all(gate.passed for gate in case_gates))
    metrics = _build_metrics(normalized, passing_cases)
    return BacktestResultQualityReport(
        version=version,
        generated_at=generated_at or datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        cases=normalized,
        gates=gates,
        metrics=metrics,
        passed=bool(normalized) and all(gate.passed for gate in gates),
    )


def load_backtest_result_quality_json(path: str | Path) -> tuple[BacktestResultQualityCase, ...]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    raw_cases = payload.get("cases", payload.get("results", [])) if isinstance(payload, Mapping) else payload
    if not isinstance(raw_cases, list):
        raise ValueError("BT4 JSON must contain a list, 'cases' or 'results'.")
    return tuple(BacktestResultQualityCase.from_mapping(item) for item in raw_cases)


def demo_backtest_result_quality_cases() -> tuple[BacktestResultQualityCase, ...]:
    return tuple(BacktestResultQualityCase.from_mapping(item) for item in _demo_payloads())


def render_backtest_result_quality_markdown(report: BacktestResultQualityReport) -> str:
    lines = [
        "# BT4 Backtest Result Quality Report",
        "",
        f"Generated at: `{report.generated_at}`",
        f"Overall status: `{'PASS' if report.passed else 'FAIL'}`",
        "",
        "## Metrics",
        "",
        "| Metric | Value |",
        "|---|---:|",
    ]
    for key, value in report.metrics.to_dict().items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(["", "## Gates", "", "| Gate | Status | Message |", "|---|---|---|"])
    for gate in report.gates:
        status = "PASS" if gate.passed else "FAIL"
        message = gate.message if not gate.failures else f"{gate.message} Failures: {'; '.join(gate.failures)}"
        lines.append(f"| `{gate.name}` | `{status}` | {message} |")
    lines.extend([
        "",
        "## Cases",
        "",
        "| Run | Strategy | Trades | Expectancy R | Profit Factor | Sharpe | Max DD % |",
        "|---|---|---:|---:|---:|---:|---:|",
    ])
    for case in report.cases:
        lines.append(
            f"| `{case.run_id}` | `{case.strategy_id}` | {case.trade_count} | {case.expectancy_r} | "
            f"{case.profit_factor} | {case.sharpe} | {case.max_drawdown_pct} |"
        )
    lines.extend(["", "---", "", report.footer, ""])
    return "\n".join(lines)


def write_backtest_result_quality_report(report: BacktestResultQualityReport, *, output_json: str | Path, output_md: str | Path) -> None:
    json_path = Path(output_json)
    md_path = Path(output_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_backtest_result_quality_markdown(report), encoding="utf-8")


def _evaluate_case(case: BacktestResultQualityCase, policy: BacktestResultQualityConfig) -> tuple[BacktestResultQualityGate, ...]:
    return (
        _required_fields_gate(case),
        _threshold_gate("minimum_trade_count", case.trade_count >= policy.min_trade_count, f"{case.run_id}: trade_count {case.trade_count} < {policy.min_trade_count}"),
        _threshold_gate("max_drawdown_limit", case.max_drawdown_pct >= policy.max_drawdown_pct_floor, f"{case.run_id}: drawdown {case.max_drawdown_pct} < {policy.max_drawdown_pct_floor}"),
        _threshold_gate("positive_expectancy", case.expectancy_r >= policy.min_expectancy_r, f"{case.run_id}: expectancy {case.expectancy_r} < {policy.min_expectancy_r}"),
        _threshold_gate("minimum_profit_factor", case.profit_factor >= policy.min_profit_factor, f"{case.run_id}: profit_factor {case.profit_factor} < {policy.min_profit_factor}"),
        _threshold_gate("minimum_sharpe", case.sharpe >= policy.min_sharpe, f"{case.run_id}: sharpe {case.sharpe} < {policy.min_sharpe}"),
        _threshold_gate("max_loss_rate", case.loss_rate_pct <= policy.max_loss_rate_pct, f"{case.run_id}: loss_rate {case.loss_rate_pct} > {policy.max_loss_rate_pct}"),
        _regime_split_gate(case, policy),
        _single_regime_share_gate(case, policy),
        _public_safe_gate(case, policy),
        _research_footer_gate(case, policy),
    )


def _required_fields_gate(case: BacktestResultQualityCase) -> BacktestResultQualityGate:
    missing = [name for name in ("run_id", "strategy_id", "contract_version") if not getattr(case, name)]
    return _gate("required_fields_complete", [] if not missing else [f"{case.run_id or '<missing-run-id>'}: missing {', '.join(missing)}"], "Required identity fields are present.")


def _threshold_gate(name: str, passed: bool, failure: str) -> BacktestResultQualityGate:
    return _gate(name, [] if passed else [failure], "Threshold is satisfied.")


def _regime_split_gate(case: BacktestResultQualityCase, policy: BacktestResultQualityConfig) -> BacktestResultQualityGate:
    regimes = {item.regime for item in case.regime_slices if item.regime}
    failures = [] if len(regimes) >= policy.min_regime_count else [f"{case.run_id}: regime count {len(regimes)} < {policy.min_regime_count}"]
    return _gate("regime_split_available", failures, "Regime split is available.")


def _single_regime_share_gate(case: BacktestResultQualityCase, policy: BacktestResultQualityConfig) -> BacktestResultQualityGate:
    if case.trade_count <= 0 or not case.regime_slices:
        return _gate("no_single_regime_overfit", [f"{case.run_id}: missing trade/regime data"], "No single-regime concentration detected.")
    largest = max(item.trade_count for item in case.regime_slices)
    share = largest / case.trade_count * 100.0
    failures = [] if share <= policy.max_single_regime_trade_share_pct else [f"{case.run_id}: largest regime share {share:.2f}% > {policy.max_single_regime_trade_share_pct}%"]
    return _gate("no_single_regime_overfit", failures, "No single-regime concentration detected.")


def _public_safe_gate(case: BacktestResultQualityCase, policy: BacktestResultQualityConfig) -> BacktestResultQualityGate:
    if not policy.require_public_safe_tags:
        return BacktestResultQualityGate("public_safe_demo_tags", True, "Public-safe tags are optional by policy.")
    tags = set(case.tags)
    failures = [] if {"demo", "public_safe"}.issubset(tags) else [f"{case.run_id}: requires demo and public_safe tags"]
    return _gate("public_safe_demo_tags", failures, "Case is explicitly demo/public-safe.")


def _research_footer_gate(case: BacktestResultQualityCase, policy: BacktestResultQualityConfig) -> BacktestResultQualityGate:
    if not policy.require_research_footer:
        return BacktestResultQualityGate("research_footer_present", True, "Research footer is optional by policy.")
    failures = [] if case.footer == RESEARCH_ONLY_FOOTER else [f"{case.run_id}: missing research-only footer"]
    return _gate("research_footer_present", failures, "Research-only footer is present.")


def _aggregate_gates(cases: Sequence[BacktestResultQualityCase], case_gate_results: Sequence[Sequence[BacktestResultQualityGate]]) -> tuple[BacktestResultQualityGate, ...]:
    if not cases:
        return (BacktestResultQualityGate("non_empty_quality_case_set", False, "Gate failed.", ("no quality cases supplied",)),)
    failing = [cases[index].run_id for index, gates in enumerate(case_gate_results) if not all(gate.passed for gate in gates)]
    return (
        _gate("non_empty_quality_case_set", [], "At least one quality case is present."),
        _gate("all_cases_pass_quality", [f"failing cases: {', '.join(failing)}"] if failing else [], "All cases passed quality gates."),
    )


def _build_metrics(cases: Sequence[BacktestResultQualityCase], passing_cases: int) -> BacktestResultQualityMetrics:
    count = len(cases)
    if count == 0:
        return BacktestResultQualityMetrics(0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0)
    return BacktestResultQualityMetrics(
        case_count=count,
        passing_case_count=passing_cases,
        failing_case_count=count - passing_cases,
        average_trade_count=sum(item.trade_count for item in cases) / count,
        average_expectancy_r=sum(item.expectancy_r for item in cases) / count,
        average_profit_factor=sum(item.profit_factor for item in cases) / count,
        average_sharpe=sum(item.sharpe for item in cases) / count,
        worst_drawdown_pct=min(item.max_drawdown_pct for item in cases),
    )


def _gate(name: str, failures: Sequence[str], success_message: str) -> BacktestResultQualityGate:
    return BacktestResultQualityGate(name=name, passed=not failures, message=success_message if not failures else "Gate failed.", failures=tuple(failures))


def _demo_payloads() -> tuple[dict[str, Any], ...]:
    return (
        {
            "run_id": "bt4-demo-trend-quality-001",
            "strategy_id": "trend_demo",
            "contract_version": "BT3-demo-v1",
            "trade_count": 64,
            "max_drawdown_pct": -8.2,
            "expectancy_r": 0.18,
            "profit_factor": 1.42,
            "sharpe": 1.12,
            "win_rate_pct": 53.5,
            "loss_rate_pct": 46.5,
            "total_return_pct": 14.7,
            "regime_slices": [
                {"regime": "risk_on", "trade_count": 28, "expectancy_r": 0.22, "max_drawdown_pct": -4.1, "profit_factor": 1.55},
                {"regime": "neutral", "trade_count": 24, "expectancy_r": 0.15, "max_drawdown_pct": -5.4, "profit_factor": 1.32},
                {"regime": "risk_off", "trade_count": 12, "expectancy_r": 0.08, "max_drawdown_pct": -8.2, "profit_factor": 1.18}
            ],
            "tags": ["demo", "public_safe", "research_only"],
            "notes": "Demo quality case for continued research observation.",
            "footer": RESEARCH_ONLY_FOOTER,
        },
        {
            "run_id": "bt4-demo-reversion-quality-001",
            "strategy_id": "mean_reversion_demo",
            "contract_version": "BT3-demo-v1",
            "trade_count": 42,
            "max_drawdown_pct": -6.5,
            "expectancy_r": 0.11,
            "profit_factor": 1.23,
            "sharpe": 0.88,
            "win_rate_pct": 51.2,
            "loss_rate_pct": 48.8,
            "total_return_pct": 7.9,
            "regime_slices": [
                {"regime": "neutral", "trade_count": 22, "expectancy_r": 0.13, "max_drawdown_pct": -3.9, "profit_factor": 1.28},
                {"regime": "risk_off", "trade_count": 20, "expectancy_r": 0.09, "max_drawdown_pct": -6.5, "profit_factor": 1.18}
            ],
            "tags": ["demo", "public_safe", "research_only"],
            "notes": "Demo quality case for paper-observation continuation.",
            "footer": RESEARCH_ONLY_FOOTER,
        },
    )
