from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

MIN_PAPER_OBSERVATION_MONTHS = 3
PREFERRED_PAPER_OBSERVATION_MONTHS = 6
MIN_LIVE_VS_PAPER_RATIO = 0.85
MAX_LIVE_DRAWDOWN_MULTIPLE = 1.5

READINESS_NOT_READY = "NOT_READY"
READINESS_OBSERVATION_ONLY = "OBSERVATION_ONLY"
READINESS_REVIEW_READY = "REVIEW_READY"


@dataclass(frozen=True)
class FinalReadinessEvidence:
    historical_edge_passed: bool = False
    regime_phase_passed: bool = False
    walk_forward_passed: bool = False
    execution_realism_passed: bool = False
    out_of_sample_passed: bool = False
    paper_observation_passed: bool = False
    paper_observation_months: float = 0.0
    paper_vs_backtest_ratio: float = 0.0
    manual_review_completed: bool = False
    risk_limits_defined: bool = False
    kill_switch_defined: bool = False
    live_drawdown_limit_multiple: float = MAX_LIVE_DRAWDOWN_MULTIPLE
    notes: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FinalReadinessGate:
    name: str
    passed: bool
    message: str
    severity: str = "blocker"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CapitalRiskPhase:
    phase: str
    max_size_fraction: float
    minimum_duration_months: int
    condition: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FinalLiveReadinessReport:
    ready: bool
    readiness_level: str
    evidence: FinalReadinessEvidence
    gates: list[FinalReadinessGate] = field(default_factory=list)
    capital_risk_phases: list[CapitalRiskPhase] = field(default_factory=list)
    kill_switch_rules: list[str] = field(default_factory=list)
    guardrails: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ready": self.ready,
            "readiness_level": self.readiness_level,
            "evidence": self.evidence.to_dict(),
            "gates": [gate.to_dict() for gate in self.gates],
            "capital_risk_phases": [phase.to_dict() for phase in self.capital_risk_phases],
            "kill_switch_rules": self.kill_switch_rules,
            "guardrails": self.guardrails,
        }


def evaluate_final_live_readiness(evidence: FinalReadinessEvidence) -> FinalLiveReadinessReport:
    gates = build_final_readiness_gates(evidence)
    ready = all(gate.passed for gate in gates)
    readiness_level = determine_readiness_level(evidence=evidence, gates=gates)

    return FinalLiveReadinessReport(
        ready=ready,
        readiness_level=readiness_level,
        evidence=evidence,
        gates=gates,
        capital_risk_phases=default_capital_risk_phases(),
        kill_switch_rules=default_kill_switch_rules(evidence),
        guardrails=default_guardrails(),
    )


def build_final_readiness_gates(evidence: FinalReadinessEvidence) -> list[FinalReadinessGate]:
    return [
        FinalReadinessGate(
            name="historical_edge_validation",
            passed=evidence.historical_edge_passed,
            message="P41 historical edge validation must pass.",
        ),
        FinalReadinessGate(
            name="regime_phase_matrix",
            passed=evidence.regime_phase_passed,
            message="P42 regime-phase matrix must pass.",
        ),
        FinalReadinessGate(
            name="walk_forward_validation",
            passed=evidence.walk_forward_passed,
            message="P43 walk-forward validation must pass.",
        ),
        FinalReadinessGate(
            name="execution_realism",
            passed=evidence.execution_realism_passed,
            message="P44 execution realism validation must pass.",
        ),
        FinalReadinessGate(
            name="out_of_sample_lockbox",
            passed=evidence.out_of_sample_passed,
            message="P45 out-of-sample lockbox must pass.",
        ),
        FinalReadinessGate(
            name="paper_observation_quality",
            passed=evidence.paper_observation_passed,
            message="P46 paper observation evidence must pass.",
        ),
        FinalReadinessGate(
            name="minimum_paper_observation_duration",
            passed=evidence.paper_observation_months >= MIN_PAPER_OBSERVATION_MONTHS,
            message=f"Paper observation months: {evidence.paper_observation_months:.2f}; minimum required: {MIN_PAPER_OBSERVATION_MONTHS}.",
        ),
        FinalReadinessGate(
            name="paper_vs_backtest_stability",
            passed=evidence.paper_vs_backtest_ratio >= MIN_LIVE_VS_PAPER_RATIO,
            message=f"Paper/live observation must retain at least {MIN_LIVE_VS_PAPER_RATIO:.0%} of expected backtest quality.",
        ),
        FinalReadinessGate(
            name="manual_review_completed",
            passed=evidence.manual_review_completed,
            message="Manual review must be completed before any capital-risk decision.",
        ),
        FinalReadinessGate(
            name="risk_limits_defined",
            passed=evidence.risk_limits_defined,
            message="Capital-at-risk limits must be explicitly defined.",
        ),
        FinalReadinessGate(
            name="kill_switch_defined",
            passed=evidence.kill_switch_defined,
            message="Kill-switch rules must be defined before any capital-risk decision.",
        ),
        FinalReadinessGate(
            name="drawdown_kill_switch_limit",
            passed=evidence.live_drawdown_limit_multiple <= MAX_LIVE_DRAWDOWN_MULTIPLE,
            message=f"Live drawdown kill switch must be <= {MAX_LIVE_DRAWDOWN_MULTIPLE:.1f}x backtest max drawdown.",
        ),
    ]


def determine_readiness_level(*, evidence: FinalReadinessEvidence, gates: list[FinalReadinessGate]) -> str:
    if all(gate.passed for gate in gates):
        return READINESS_REVIEW_READY
    validation_gates = {
        "historical_edge_validation",
        "regime_phase_matrix",
        "walk_forward_validation",
        "execution_realism",
        "out_of_sample_lockbox",
    }
    validation_ready = all(gate.passed for gate in gates if gate.name in validation_gates)
    if validation_ready and evidence.paper_observation_months > 0:
        return READINESS_OBSERVATION_ONLY
    return READINESS_NOT_READY


def default_capital_risk_phases() -> list[CapitalRiskPhase]:
    return [
        CapitalRiskPhase(
            phase="months_1_to_3",
            max_size_fraction=0.50,
            minimum_duration_months=3,
            condition="Only after all readiness gates pass and manual review approves observation evidence.",
        ),
        CapitalRiskPhase(
            phase="months_4_to_6",
            max_size_fraction=0.75,
            minimum_duration_months=3,
            condition="Allowed only if observed metrics remain at or above 85% of paper expectation.",
        ),
        CapitalRiskPhase(
            phase="month_7_plus",
            max_size_fraction=1.00,
            minimum_duration_months=1,
            condition="Allowed only if cumulatively profitable and drawdown remains below the configured kill-switch limit.",
        ),
    ]


def default_kill_switch_rules(evidence: FinalReadinessEvidence) -> list[str]:
    return [
        f"Stop and review if live drawdown exceeds {evidence.live_drawdown_limit_multiple:.2f}x backtest max drawdown.",
        "Stop and review if live/paper metrics fall below 85% of expected observation quality.",
        "Stop and review after any unexplained execution deviation cluster.",
        "Stop and review after any manual protocol breach cluster.",
    ]


def default_guardrails() -> list[str]:
    return [
        "Decision-support only.",
        "No broker integration.",
        "No order execution.",
        "No automatic live-trading authorization.",
        "Code quality is not trading edge.",
    ]


def render_final_live_readiness_markdown(report: FinalLiveReadinessReport) -> str:
    lines = [
        "# Final Live Readiness Gate",
        "",
        f"Ready: **{report.ready}**",
        f"Readiness level: **{report.readiness_level}**",
        "",
        "## Gates",
        "",
        "| Gate | Status | Message |",
        "|---|---:|---|",
    ]
    for gate in report.gates:
        lines.append(f"| {gate.name} | {'PASS' if gate.passed else 'FAIL'} | {gate.message} |")

    lines.extend(["", "## Capital Risk Phases", "", "| Phase | Max Size | Minimum Duration | Condition |", "|---|---:|---:|---|"])
    for phase in report.capital_risk_phases:
        lines.append(
            f"| {phase.phase} | {phase.max_size_fraction:.0%} | {phase.minimum_duration_months} months | {phase.condition} |"
        )

    lines.extend(["", "## Kill Switch Rules", ""])
    for rule in report.kill_switch_rules:
        lines.append(f"- {rule}")

    lines.extend(["", "## Guardrails", ""])
    for guardrail in report.guardrails:
        lines.append(f"- {guardrail}")

    return "\n".join(lines).rstrip() + "\n"


def write_final_live_readiness_report(
    report: FinalLiveReadinessReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_final_live_readiness_markdown(report), encoding="utf-8")
