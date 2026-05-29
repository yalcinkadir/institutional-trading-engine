from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class ScoreConsumer(str, Enum):
    REPORTING = "reporting"
    DECISION_ENGINE = "decision_engine"
    BACKTEST_GATE = "backtest_gate"
    PAPER_EXECUTION_GATE = "paper_execution_gate"


class ScoreSystemKind(str, Enum):
    REPORT_ONLY = "report_only"
    DECISION_INPUT = "decision_input"
    VALIDATION_GATE = "validation_gate"


@dataclass(frozen=True)
class ScoreSystemDefinition:
    name: str
    module_path: str
    score_field: str
    kind: ScoreSystemKind
    scale: str
    consumers: tuple[ScoreConsumer, ...]
    decision_authoritative: bool
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["kind"] = self.kind.value
        payload["consumers"] = [consumer.value for consumer in self.consumers]
        payload["notes"] = list(self.notes)
        return payload


@dataclass(frozen=True)
class ScoreAuditIssue:
    code: str
    message: str
    severity: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ScoreAuditReport:
    definitions: tuple[ScoreSystemDefinition, ...]
    issues: tuple[ScoreAuditIssue, ...]
    notes: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return not any(issue.severity == "error" for issue in self.issues)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "definitions": [definition.to_dict() for definition in self.definitions],
            "issues": [issue.to_dict() for issue in self.issues],
            "notes": list(self.notes),
        }


PUBLIC_SCORE_SYSTEMS: tuple[ScoreSystemDefinition, ...] = (
    ScoreSystemDefinition(
        name="live_setup_scoring",
        module_path="src/setup_scoring.py",
        score_field="SetupScore.setup_score",
        kind=ScoreSystemKind.DECISION_INPUT,
        scale="0_to_100_public_demo_score",
        consumers=(ScoreConsumer.DECISION_ENGINE, ScoreConsumer.REPORTING),
        decision_authoritative=True,
        notes=(
            "Feeds SetupCandidate.setup_score for Decision Engine v3.",
            "Public constants remain demo defaults, not proprietary production edge.",
        ),
    ),
    ScoreSystemDefinition(
        name="decision_engine_tier_gate",
        module_path="src/decision_engine.py",
        score_field="DecisionResult.risk_tier",
        kind=ScoreSystemKind.DECISION_INPUT,
        scale="tier_1_tier_2_tier_3_no_trade",
        consumers=(ScoreConsumer.DECISION_ENGINE, ScoreConsumer.PAPER_EXECUTION_GATE),
        decision_authoritative=True,
        notes=(
            "Hierarchy-first gate combines setup_score, regime_alignment, asymmetry and data_confidence.",
            "This is the authoritative decision outcome, not a cosmetic report score.",
        ),
    ),
    ScoreSystemDefinition(
        name="report_ranking_score",
        module_path="reports/* and report builders",
        score_field="report_score/ranking_score",
        kind=ScoreSystemKind.REPORT_ONLY,
        scale="presentation_only",
        consumers=(ScoreConsumer.REPORTING,),
        decision_authoritative=False,
        notes=(
            "Report ranking scores are presentation aids only.",
            "They must not be treated as execution authorization or as equivalent to DecisionResult.",
        ),
    ),
)


def audit_score_systems(definitions: tuple[ScoreSystemDefinition, ...] = PUBLIC_SCORE_SYSTEMS) -> ScoreAuditReport:
    issues: list[ScoreAuditIssue] = []
    names = [definition.name for definition in definitions]
    if len(set(names)) != len(names):
        issues.append(ScoreAuditIssue("duplicate_score_system_name", "score-system names must be unique", "error"))

    authoritative = [definition for definition in definitions if definition.decision_authoritative]
    if not authoritative:
        issues.append(ScoreAuditIssue("missing_authoritative_decision_score", "at least one authoritative decision score/gate must be declared", "error"))

    for definition in definitions:
        if definition.kind == ScoreSystemKind.REPORT_ONLY and definition.decision_authoritative:
            issues.append(
                ScoreAuditIssue(
                    "report_score_marked_authoritative",
                    f"report-only score system {definition.name} must not be decision-authoritative",
                    "error",
                )
            )
        if ScoreConsumer.PAPER_EXECUTION_GATE in definition.consumers and not definition.decision_authoritative:
            issues.append(
                ScoreAuditIssue(
                    "non_authoritative_execution_gate_score",
                    f"{definition.name} feeds an execution gate but is not marked decision-authoritative",
                    "error",
                )
            )
        if not definition.module_path.strip() or not definition.score_field.strip():
            issues.append(
                ScoreAuditIssue(
                    "missing_score_system_reference",
                    f"{definition.name} must declare module_path and score_field",
                    "error",
                )
            )

    return ScoreAuditReport(
        definitions=definitions,
        issues=tuple(issues),
        notes=(
            "CL2 audit boundary: report-only scores and decision-authoritative scores are explicitly separated.",
            "Changing score semantics requires updating this registry and regression tests.",
        ),
    )


def render_score_audit_markdown(report: ScoreAuditReport) -> str:
    lines = [
        "# CL2 Scoring System Audit",
        "",
        f"Passed: **{str(report.passed).lower()}**",
        "",
        "## Registered Score Systems",
        "",
    ]
    for definition in report.definitions:
        lines.extend(
            [
                f"### {definition.name}",
                "",
                f"- Module: `{definition.module_path}`",
                f"- Field: `{definition.score_field}`",
                f"- Kind: `{definition.kind.value}`",
                f"- Scale: `{definition.scale}`",
                f"- Decision-authoritative: **{str(definition.decision_authoritative).lower()}**",
                f"- Consumers: {', '.join(consumer.value for consumer in definition.consumers)}",
                "",
            ]
        )
    lines.extend(["## Issues", ""])
    if report.issues:
        for issue in report.issues:
            lines.append(f"- **{issue.severity.upper()}** `{issue.code}` — {issue.message}")
    else:
        lines.append("- None")
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    return "\n".join(lines).rstrip() + "\n"
