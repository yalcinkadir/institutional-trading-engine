from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

RUNTIME_PROOF_REVIEW_READY = "REVIEW_READY"
RUNTIME_PROOF_BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class RuntimeProofPackSummaryResult:
    valid: bool
    errors: tuple[str, ...]
    summary: dict[str, Any]


def _as_mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return []


def build_runtime_proof_pack_summary(runtime_pack: Mapping[str, Any]) -> RuntimeProofPackSummaryResult:
    """Build a deterministic runtime proof-pack summary for review.

    RGP13 summarizes existing runtime/governance evidence. It does not approve
    live trading, broker execution, capital allocation or production deployment.
    """

    errors: list[str] = []

    portfolio_state = _as_mapping(runtime_pack.get("portfolio_state"))
    approval_gate = _as_mapping(runtime_pack.get("approval_gate"))
    signal_lifecycle = _as_mapping(runtime_pack.get("signal_lifecycle"))
    runtime_evidence = _as_mapping(runtime_pack.get("runtime_evidence"))

    if not portfolio_state:
        errors.append("missing_portfolio_state")
    if not approval_gate:
        errors.append("missing_approval_gate")
    if not signal_lifecycle:
        errors.append("missing_signal_lifecycle")
    if not runtime_evidence:
        errors.append("missing_runtime_evidence")

    if runtime_pack.get("live_trading_authorized") is not False:
        errors.append("live_trading_must_remain_false")

    if runtime_pack.get("broker_execution_mode") != "paper_only":
        errors.append("broker_execution_mode_must_be_paper_only")

    portfolio_warnings = [str(item) for item in _as_list(portfolio_state.get("warnings")) if item]

    if portfolio_state and portfolio_state.get("governance_valid") is not True:
        errors.append("portfolio_state_governance_invalid")

    if approval_gate and approval_gate.get("approved") is not True:
        errors.append("approval_gate_not_approved")

    evidence_paths: list[str] = []
    manifest_path = runtime_evidence.get("manifest_path")
    if manifest_path:
        evidence_paths.append(str(manifest_path))

    status = RUNTIME_PROOF_BLOCKED if errors else RUNTIME_PROOF_REVIEW_READY
    summary = {
        "observation_date": str(runtime_pack.get("observation_date", "")),
        "runtime_proof_status": status,
        "approved_for_runtime_review": not errors,
        "portfolio_governance_valid": portfolio_state.get("governance_valid") is True,
        "portfolio_warnings": portfolio_warnings,
        "approval_decision": str(approval_gate.get("decision", "")),
        "approval_reason": str(approval_gate.get("reason", "")),
        "signal_id": str(signal_lifecycle.get("signal_id", "")),
        "signal_status": str(signal_lifecycle.get("status", "")),
        "evidence_paths": evidence_paths,
        "errors": tuple(errors),
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }

    return RuntimeProofPackSummaryResult(valid=not errors, errors=tuple(errors), summary=summary)
