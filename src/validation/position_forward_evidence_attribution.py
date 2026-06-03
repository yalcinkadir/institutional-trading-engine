from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from src.validation.position_risk_attribution import PositionRiskAttributionReport

POSITION_FORWARD_REVIEW_READY = "REVIEW_READY"
POSITION_FORWARD_BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class PositionForwardEvidenceAttributionResult:
    valid: bool
    errors: tuple[str, ...]
    summary: dict[str, Any]


def _safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _safe_str(value: Any) -> str:
    return str(value or "").strip()


def _symbol(value: Any) -> str:
    return _safe_str(value).upper()


def _decision_index(records: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    indexed: dict[str, Mapping[str, Any]] = {}
    for record in records:
        symbol = _symbol(record.get("symbol") or record.get("ticker"))
        if symbol and symbol not in indexed:
            indexed[symbol] = record
    return indexed


def build_position_forward_evidence_attribution(
    *,
    risk_report: PositionRiskAttributionReport,
    decision_records: Sequence[Mapping[str, Any]],
    observation_window: str,
    evidence_manifest_path: str,
    live_trading_authorized: bool = False,
    broker_execution_mode: str = "paper_only",
) -> PositionForwardEvidenceAttributionResult:
    """Build a position-level forward-evidence attribution summary.

    PFA1 joins position risk attribution with forward outcome records. It is a
    review/evidence layer only and does not authorize live trading, broker
    execution, capital allocation or production deployment.
    """

    errors: list[str] = []
    window = _safe_str(observation_window)
    manifest = _safe_str(evidence_manifest_path)

    if not window:
        errors.append("missing_observation_window")
    if not manifest:
        errors.append("missing_evidence_manifest_path")
    if not risk_report.passed:
        errors.append("risk_attribution_report_failed")
    if live_trading_authorized is not False:
        errors.append("live_trading_must_remain_false")
    if broker_execution_mode != "paper_only":
        errors.append("broker_execution_mode_must_be_paper_only")

    decisions = _decision_index(decision_records)
    position_attributions: list[dict[str, Any]] = []
    unmatched: list[str] = []

    for position in risk_report.metrics.position_attributions:
        record = decisions.get(position.symbol)
        if record is None:
            unmatched.append(position.symbol)
            continue

        position_attributions.append(
            {
                "symbol": position.symbol,
                "sector": position.sector,
                "risk_contribution_r": position.total_contribution_r,
                "beta_contribution_r": position.beta_contribution_r,
                "factor_contribution_r": position.factor_contribution_r,
                "specific_contribution_r": position.specific_contribution_r,
                "market_state": _safe_str(record.get("market_state")),
                "setup_type": _safe_str(record.get("setup_type")),
                "decision": _safe_str(record.get("decision")),
                "risk_tier": _safe_str(record.get("risk_tier")),
                "setup_score": _safe_float(record.get("setup_score")),
                "regime_alignment": _safe_float(record.get("regime_alignment")),
                "asymmetry_score": _safe_float(record.get("asymmetry_score")),
                "data_confidence": _safe_float(record.get("data_confidence")),
                "result_1d": _safe_float(record.get("result_1d")),
                "result_5d": _safe_float(record.get("result_5d")),
                "result_20d": _safe_float(record.get("result_20d")),
                "mfe": _safe_float(record.get("mfe")),
                "mae": _safe_float(record.get("mae")),
            }
        )

    if unmatched:
        errors.append("unmatched_position_symbols")

    total_1d = round(sum(item["result_1d"] for item in position_attributions), 6)
    total_5d = round(sum(item["result_5d"] for item in position_attributions), 6)
    total_20d = round(sum(item["result_20d"] for item in position_attributions), 6)

    status = POSITION_FORWARD_BLOCKED if errors else POSITION_FORWARD_REVIEW_READY
    summary = {
        "position_forward_attribution_status": status,
        "approved_for_forward_review": not errors,
        "observation_window": window,
        "evidence_manifest_path": manifest,
        "risk_report_passed": risk_report.passed,
        "position_count": risk_report.metrics.positions,
        "matched_position_count": len(position_attributions),
        "unmatched_symbols": unmatched,
        "portfolio_risk": {
            "portfolio_r": risk_report.metrics.portfolio_r,
            "beta_contribution_r": risk_report.metrics.beta_contribution_r,
            "factor_contribution_r": risk_report.metrics.factor_contribution_r,
            "specific_contribution_r": risk_report.metrics.specific_contribution_r,
            "unattributed_r": risk_report.metrics.unattributed_r,
        },
        "portfolio_outcome": {
            "total_result_1d": total_1d,
            "total_result_5d": total_5d,
            "total_result_20d": total_20d,
        },
        "position_attributions": position_attributions,
        "errors": tuple(errors),
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }

    return PositionForwardEvidenceAttributionResult(valid=not errors, errors=tuple(errors), summary=summary)
