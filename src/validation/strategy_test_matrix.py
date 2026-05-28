from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable


RESEARCH_ONLY_FOOTER = "Research / Paper Observation Only. No live trading authorization."
FORBIDDEN_LIVE_TERMS = (
    "live_approved",
    "live_authorized",
    "real_money",
    "broker_execute",
    "place_order",
    "execute_order",
)
FORBIDDEN_PRIVATE_EDGE_TERMS = (
    "private_edge",
    "proprietary_edge",
    "real_threshold",
    "production_weight",
    "secret_setup_rank",
)


@dataclass(frozen=True)
class StrategyTestMatrixConfig:
    required_regimes: tuple[str, ...] = ("risk_on", "neutral", "risk_off")
    required_setup_families: tuple[str, ...] = ("breakout", "pullback", "mean_reversion_demo")
    required_validation_stages: tuple[str, ...] = ("backtest", "paper_observation", "execution_quality")
    required_data_modes: tuple[str, ...] = ("synthetic", "paper_observation")
    min_cases_per_strategy: int = 3
    public_demo_only: bool = True
    require_research_footer: bool = True


@dataclass(frozen=True)
class StrategyMatrixCase:
    case_id: str
    strategy_id: str
    sleeve: str
    regime: str
    setup_family: str
    asset_class: str
    data_mode: str
    validation_stage: str
    expected_gate: str
    risk_state: str = "paper_only"
    evidence_source: str = "synthetic_demo"
    notes: str = ""
    tags: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "StrategyMatrixCase":
        return cls(
            case_id=str(raw.get("case_id", "")).strip(),
            strategy_id=str(raw.get("strategy_id", "")).strip(),
            sleeve=str(raw.get("sleeve", "")).strip(),
            regime=str(raw.get("regime", "")).strip(),
            setup_family=str(raw.get("setup_family", "")).strip(),
            asset_class=str(raw.get("asset_class", "")).strip(),
            data_mode=str(raw.get("data_mode", "")).strip(),
            validation_stage=str(raw.get("validation_stage", "")).strip(),
            expected_gate=str(raw.get("expected_gate", "")).strip(),
            risk_state=str(raw.get("risk_state", "paper_only")).strip(),
            evidence_source=str(raw.get("evidence_source", "synthetic_demo")).strip(),
            notes=str(raw.get("notes", "")).strip(),
            tags=tuple(str(tag).strip() for tag in raw.get("tags", ()) if str(tag).strip()),
        )

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["tags"] = list(self.tags)
        return payload


@dataclass(frozen=True)
class StrategyTestMatrixMetrics:
    total_cases: int
    strategy_count: int
    regimes: tuple[str, ...]
    setup_families: tuple[str, ...]
    validation_stages: tuple[str, ...]
    data_modes: tuple[str, ...]
    cases_per_strategy: dict[str, int]

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_cases": self.total_cases,
            "strategy_count": self.strategy_count,
            "regimes": list(self.regimes),
            "setup_families": list(self.setup_families),
            "validation_stages": list(self.validation_stages),
            "data_modes": list(self.data_modes),
            "cases_per_strategy": dict(self.cases_per_strategy),
        }


@dataclass(frozen=True)
class StrategyTestMatrixGate:
    name: str
    passed: bool
    value: Any
    threshold: Any
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class StrategyTestMatrixReport:
    passed: bool
    metrics: StrategyTestMatrixMetrics
    gates: list[StrategyTestMatrixGate]
    cases: list[StrategyMatrixCase]
    footer: str = RESEARCH_ONLY_FOOTER

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "metrics": self.metrics.to_dict(),
            "gates": [gate.to_dict() for gate in self.gates],
            "cases": [case.to_dict() for case in self.cases],
            "footer": self.footer,
        }


def build_strategy_test_matrix(
    cases: Iterable[StrategyMatrixCase | dict[str, Any]],
    *,
    config: StrategyTestMatrixConfig = StrategyTestMatrixConfig(),
) -> StrategyTestMatrixReport:
    parsed_cases = [case if isinstance(case, StrategyMatrixCase) else StrategyMatrixCase.from_dict(case) for case in cases]
    metrics = _build_metrics(parsed_cases)
    gates = _build_gates(parsed_cases, metrics=metrics, config=config)
    return StrategyTestMatrixReport(
        passed=all(gate.passed for gate in gates),
        metrics=metrics,
        gates=gates,
        cases=parsed_cases,
    )


def load_strategy_test_matrix_json(path: Path) -> list[StrategyMatrixCase]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        raw_cases = payload
    elif isinstance(payload, dict):
        raw_cases = payload.get("cases", [])
    else:
        raise ValueError("strategy test matrix JSON must contain a list or an object with a 'cases' list")
    if not isinstance(raw_cases, list):
        raise ValueError("strategy test matrix JSON must contain a list or a 'cases' list")
    return [StrategyMatrixCase.from_dict(raw) for raw in raw_cases]


def demo_strategy_test_matrix_cases() -> list[StrategyMatrixCase]:
    return [
        StrategyMatrixCase(
            case_id="BT2-DEMO-001",
            strategy_id="trend_demo",
            sleeve="core_trend_demo",
            regime="risk_on",
            setup_family="breakout",
            asset_class="equity_index_demo",
            data_mode="synthetic",
            validation_stage="backtest",
            expected_gate="research_review",
            notes="Synthetic public demo case for trend breakout coverage.",
            tags=("demo", "public_safe"),
        ),
        StrategyMatrixCase(
            case_id="BT2-DEMO-002",
            strategy_id="trend_demo",
            sleeve="core_trend_demo",
            regime="neutral",
            setup_family="pullback",
            asset_class="large_cap_equity_demo",
            data_mode="paper_observation",
            validation_stage="paper_observation",
            expected_gate="continue_observation",
            notes="Paper-observation demo case without production thresholds.",
            tags=("demo", "public_safe"),
        ),
        StrategyMatrixCase(
            case_id="BT2-DEMO-003",
            strategy_id="trend_demo",
            sleeve="core_trend_demo",
            regime="risk_off",
            setup_family="mean_reversion_demo",
            asset_class="defensive_equity_demo",
            data_mode="synthetic",
            validation_stage="execution_quality",
            expected_gate="manual_review",
            notes="Execution-quality demo case for adverse regime handling.",
            tags=("demo", "public_safe"),
        ),
        StrategyMatrixCase(
            case_id="BT2-DEMO-004",
            strategy_id="mean_reversion_demo",
            sleeve="satellite_reversion_demo",
            regime="risk_on",
            setup_family="mean_reversion_demo",
            asset_class="sector_etf_demo",
            data_mode="synthetic",
            validation_stage="backtest",
            expected_gate="research_review",
            notes="Synthetic public demo case for future multi-strategy expansion.",
            tags=("demo", "public_safe"),
        ),
        StrategyMatrixCase(
            case_id="BT2-DEMO-005",
            strategy_id="mean_reversion_demo",
            sleeve="satellite_reversion_demo",
            regime="neutral",
            setup_family="pullback",
            asset_class="large_cap_equity_demo",
            data_mode="paper_observation",
            validation_stage="paper_observation",
            expected_gate="continue_observation",
            notes="Observation-only demo case for neutral regime behavior.",
            tags=("demo", "public_safe"),
        ),
        StrategyMatrixCase(
            case_id="BT2-DEMO-006",
            strategy_id="mean_reversion_demo",
            sleeve="satellite_reversion_demo",
            regime="risk_off",
            setup_family="breakout",
            asset_class="commodity_etf_demo",
            data_mode="synthetic",
            validation_stage="execution_quality",
            expected_gate="manual_review",
            notes="Public-safe stress case; no real execution authorization.",
            tags=("demo", "public_safe"),
        ),
    ]


def render_strategy_test_matrix_markdown(report: StrategyTestMatrixReport) -> str:
    lines = [
        "# BT2 Strategy Test Matrix",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        "",
        "## Metrics",
        "",
        f"- Total cases: {report.metrics.total_cases}",
        f"- Strategy count: {report.metrics.strategy_count}",
        f"- Regimes: {', '.join(report.metrics.regimes)}",
        f"- Setup families: {', '.join(report.metrics.setup_families)}",
        f"- Validation stages: {', '.join(report.metrics.validation_stages)}",
        f"- Data modes: {', '.join(report.metrics.data_modes)}",
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
    lines.extend([
        "",
        "## Cases",
        "",
        "| Case | Strategy | Regime | Setup | Data | Stage | Gate |",
        "|---|---|---|---|---|---|---|",
    ])
    for case in report.cases:
        lines.append(
            f"| {case.case_id} | {case.strategy_id} | {case.regime} | {case.setup_family} | "
            f"{case.data_mode} | {case.validation_stage} | {case.expected_gate} |"
        )
    lines.extend(["", report.footer])
    return "\n".join(lines).rstrip() + "\n"


def write_strategy_test_matrix_report(
    report: StrategyTestMatrixReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_strategy_test_matrix_markdown(report), encoding="utf-8")


def _build_metrics(cases: list[StrategyMatrixCase]) -> StrategyTestMatrixMetrics:
    strategy_counts: dict[str, int] = {}
    for case in cases:
        strategy_counts[case.strategy_id] = strategy_counts.get(case.strategy_id, 0) + 1
    return StrategyTestMatrixMetrics(
        total_cases=len(cases),
        strategy_count=len(strategy_counts),
        regimes=tuple(sorted({case.regime for case in cases if case.regime})),
        setup_families=tuple(sorted({case.setup_family for case in cases if case.setup_family})),
        validation_stages=tuple(sorted({case.validation_stage for case in cases if case.validation_stage})),
        data_modes=tuple(sorted({case.data_mode for case in cases if case.data_mode})),
        cases_per_strategy=dict(sorted(strategy_counts.items())),
    )


def _build_gates(
    cases: list[StrategyMatrixCase],
    *,
    metrics: StrategyTestMatrixMetrics,
    config: StrategyTestMatrixConfig,
) -> list[StrategyTestMatrixGate]:
    required_fields_complete = bool(cases) and all(
        case.case_id
        and case.strategy_id
        and case.sleeve
        and case.regime
        and case.setup_family
        and case.asset_class
        and case.data_mode
        and case.validation_stage
        and case.expected_gate
        for case in cases
    )
    minimum_cases_passed = bool(metrics.cases_per_strategy) and all(
        count >= config.min_cases_per_strategy for count in metrics.cases_per_strategy.values()
    )
    public_demo_passed = bool(cases) and ((not config.public_demo_only) or all(
        "demo" in case.tags and "public_safe" in case.tags for case in cases
    ))
    no_live_terms_passed = not _contains_forbidden_terms(cases, FORBIDDEN_LIVE_TERMS)
    no_private_edge_terms_passed = not _contains_forbidden_terms(cases, FORBIDDEN_PRIVATE_EDGE_TERMS)
    return [
        StrategyTestMatrixGate(
            name="required_fields_complete",
            passed=required_fields_complete,
            value=required_fields_complete,
            threshold=True,
            message="Every matrix case must carry deterministic classification fields.",
        ),
        StrategyTestMatrixGate(
            name="minimum_cases_per_strategy",
            passed=minimum_cases_passed,
            value=min(metrics.cases_per_strategy.values()) if metrics.cases_per_strategy else 0,
            threshold=config.min_cases_per_strategy,
            message="Each strategy sleeve needs enough cases before matrix coverage is trusted.",
        ),
        _coverage_gate("required_regime_coverage", metrics.regimes, config.required_regimes),
        _coverage_gate("required_setup_family_coverage", metrics.setup_families, config.required_setup_families),
        _coverage_gate("required_validation_stage_coverage", metrics.validation_stages, config.required_validation_stages),
        _coverage_gate("required_data_mode_coverage", metrics.data_modes, config.required_data_modes),
        StrategyTestMatrixGate(
            name="public_demo_only",
            passed=public_demo_passed,
            value=public_demo_passed,
            threshold=True,
            message="Public BT2 matrices must stay demo-only and public-safe.",
        ),
        StrategyTestMatrixGate(
            name="no_live_trading_authorization",
            passed=no_live_terms_passed,
            value=no_live_terms_passed,
            threshold=True,
            message="BT2 must not approve live trading or broker execution.",
        ),
        StrategyTestMatrixGate(
            name="no_private_edge_terms",
            passed=no_private_edge_terms_passed,
            value=no_private_edge_terms_passed,
            threshold=True,
            message="BT2 public matrix must not expose private edge terminology or production constants.",
        ),
        StrategyTestMatrixGate(
            name="research_footer_present",
            passed=(not config.require_research_footer) or bool(RESEARCH_ONLY_FOOTER.strip()),
            value=RESEARCH_ONLY_FOOTER,
            threshold="required",
            message="BT2 reports must remain research/paper-observation only.",
        ),
    ]


def _coverage_gate(name: str, observed: tuple[str, ...], required: tuple[str, ...]) -> StrategyTestMatrixGate:
    missing = [item for item in required if item not in observed]
    return StrategyTestMatrixGate(
        name=name,
        passed=not missing,
        value=list(observed),
        threshold=list(required),
        message=f"Missing required dimensions: {', '.join(missing) if missing else 'none'}.",
    )


def _contains_forbidden_terms(cases: list[StrategyMatrixCase], forbidden_terms: tuple[str, ...]) -> bool:
    for case in cases:
        haystack = " ".join(
            [
                case.case_id,
                case.strategy_id,
                case.sleeve,
                case.regime,
                case.setup_family,
                case.asset_class,
                case.data_mode,
                case.validation_stage,
                case.expected_gate,
                case.risk_state,
                case.evidence_source,
                case.notes,
                *case.tags,
            ]
        ).lower()
        if any(term in haystack for term in forbidden_terms):
            return True
    return False


def _format_value(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.4f}"
    if isinstance(value, (list, tuple)):
        return ", ".join(str(item) for item in value)
    return str(value)
