"""Evidence Quality Gate (#188).

The gate prevents roadmap, strategy, paper-confidence, production-grade evidence or
live-readiness promotion when evidence is incomplete, degraded, demo/stub based or
not tied to the real runtime path.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

GateStatus = Literal["PASS", "DEGRADED", "BLOCKED"]

PROMOTION_CLAIMS = {
    "roadmap_stable",
    "strategy_promotion",
    "production_grade_evidence",
    "paper_confidence_authorized",
    "backtesting_evidence_promotion",
    "live_ready",
    "decision_stack_validated",
}

UNSAFE_PROMOTION_DATA_MODES = {
    "demo",
    "stub",
    "synthetic",
    "placeholder",
    "degraded",
}

REQUIRED_PROMOTION_FIELDS = {
    "run_id",
    "data_mode",
    "provenance",
    "checksum_or_manifest",
    "runtime_trace",
    "promotion_claim",
}

EVIDENCE_CRITICAL_ISSUES = {
    "pipeline_coupled_real_backtest": "#177",
    "runtime_reachable_decision_modules": "#178",
    "durable_paper_observation_index": "#181",
    "persisted_historical_inputs": "#184",
    "report_validation_green": "#185",
    "empty_signal_state_classified": "#186",
    "regime_vix_provenance_or_block": "#187",
}


@dataclass(frozen=True)
class EvidenceQualityBlocker:
    code: str
    issue: str
    reason: str

    def as_dict(self) -> dict[str, str]:
        return {
            "code": self.code,
            "issue": self.issue,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class EvidenceQualityInput:
    run_id: str | None
    data_mode: str | None
    provenance: str | None
    checksum_or_manifest: str | None
    runtime_trace: str | None
    promotion_claim: bool = False
    claim_type: str | None = None
    pipeline_coupled_real_backtest: bool = False
    runtime_reachable_decision_modules: bool = False
    durable_paper_observation_index: bool = False
    persisted_historical_inputs: bool = False
    report_validation_green: bool = False
    empty_signal_state_classified: bool = False
    regime_vix_provenance_or_block: bool = False
    open_blockers: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> "EvidenceQualityInput":
        return cls(
            run_id=payload.get("run_id"),
            data_mode=payload.get("data_mode"),
            provenance=payload.get("provenance"),
            checksum_or_manifest=payload.get("checksum_or_manifest"),
            runtime_trace=payload.get("runtime_trace"),
            promotion_claim=bool(payload.get("promotion_claim", False)),
            claim_type=payload.get("claim_type"),
            pipeline_coupled_real_backtest=bool(payload.get("pipeline_coupled_real_backtest", False)),
            runtime_reachable_decision_modules=bool(payload.get("runtime_reachable_decision_modules", False)),
            durable_paper_observation_index=bool(payload.get("durable_paper_observation_index", False)),
            persisted_historical_inputs=bool(payload.get("persisted_historical_inputs", False)),
            report_validation_green=bool(payload.get("report_validation_green", False)),
            empty_signal_state_classified=bool(payload.get("empty_signal_state_classified", False)),
            regime_vix_provenance_or_block=bool(payload.get("regime_vix_provenance_or_block", False)),
            open_blockers=tuple(str(item) for item in payload.get("open_blockers", ())),
        )


def _is_missing(value: Any) -> bool:
    return value is None or str(value).strip() == ""


def _normalize_issue(issue: str) -> str:
    text = str(issue).strip()
    return text if text.startswith("#") else f"#{text}"


def _has_promotion_claim(evidence: EvidenceQualityInput) -> bool:
    if evidence.promotion_claim:
        return True
    if evidence.claim_type is None:
        return False
    return str(evidence.claim_type).strip().lower() in PROMOTION_CLAIMS


def evaluate_evidence_quality_gate(evidence: EvidenceQualityInput | dict[str, Any]) -> dict[str, Any]:
    if isinstance(evidence, dict):
        evidence = EvidenceQualityInput.from_mapping(evidence)

    blockers: list[EvidenceQualityBlocker] = []
    warnings: list[str] = []
    promotion_claim = _has_promotion_claim(evidence)
    data_mode = (evidence.data_mode or "").strip().lower()

    if promotion_claim:
        for field_name in sorted(REQUIRED_PROMOTION_FIELDS):
            if _is_missing(getattr(evidence, field_name)):
                blockers.append(
                    EvidenceQualityBlocker(
                        code="missing_required_promotion_field",
                        issue="#188",
                        reason=f"Promotion claim requires `{field_name}`.",
                    )
                )

    if promotion_claim and data_mode in UNSAFE_PROMOTION_DATA_MODES:
        blockers.append(
            EvidenceQualityBlocker(
                code="unsafe_data_mode_for_promotion",
                issue="#188",
                reason=(
                    f"`{data_mode}` evidence may be useful for research visibility, "
                    "but it cannot support production-grade, roadmap, strategy, "
                    "paper-confidence or live-readiness claims."
                ),
            )
        )

    evidence_checks = {
        "pipeline_coupled_real_backtest": evidence.pipeline_coupled_real_backtest,
        "runtime_reachable_decision_modules": evidence.runtime_reachable_decision_modules,
        "durable_paper_observation_index": evidence.durable_paper_observation_index,
        "persisted_historical_inputs": evidence.persisted_historical_inputs,
        "report_validation_green": evidence.report_validation_green,
        "empty_signal_state_classified": evidence.empty_signal_state_classified,
        "regime_vix_provenance_or_block": evidence.regime_vix_provenance_or_block,
    }

    for code, passed in evidence_checks.items():
        if passed:
            continue
        blockers.append(
            EvidenceQualityBlocker(
                code=code,
                issue=EVIDENCE_CRITICAL_ISSUES[code],
                reason=f"Evidence dimension `{code}` is not proven.",
            )
        )

    for issue in evidence.open_blockers:
        normalized_issue = _normalize_issue(issue)
        if normalized_issue in EVIDENCE_CRITICAL_ISSUES.values():
            blockers.append(
                EvidenceQualityBlocker(
                    code="evidence_critical_issue_open",
                    issue=normalized_issue,
                    reason=f"Evidence-critical blocker {normalized_issue} remains open.",
                )
            )

    if data_mode in UNSAFE_PROMOTION_DATA_MODES and not promotion_claim:
        warnings.append(
            f"Data mode `{data_mode}` is not production-grade; research visibility only."
        )

    status: GateStatus
    if blockers:
        status = "BLOCKED"
    elif warnings:
        status = "DEGRADED"
    else:
        status = "PASS"

    return {
        "schema_version": 1,
        "gate": "Evidence Quality Gate #188",
        "status": status,
        "blockers": [blocker.as_dict() for blocker in blockers],
        "warnings": warnings,
        "data_mode": data_mode or None,
        "promotion_claim": promotion_claim,
    }
