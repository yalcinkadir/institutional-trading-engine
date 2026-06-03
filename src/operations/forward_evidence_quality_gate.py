from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

FORWARD_EVIDENCE_QUALITY_PASSED = "PASSED"
FORWARD_EVIDENCE_QUALITY_BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class ForwardEvidenceQualityGateResult:
    valid: bool
    errors: tuple[str, ...]
    gate: dict[str, Any]


def _as_int(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return []


def _review_ready_ratio(review_ready_days: list[Any], total_days: int) -> float:
    if total_days <= 0:
        return 0.0
    return round(len(review_ready_days) / total_days, 6)


def evaluate_forward_evidence_quality_gate(
    monthly_pack: Mapping[str, Any],
    *,
    minimum_total_days: int = 5,
    minimum_review_ready_ratio: float = 0.8,
) -> ForwardEvidenceQualityGateResult:
    """Evaluate whether a monthly Paper Observation pack is usable forward evidence.

    PO14 is a review-quality gate only. It does not authorize live trading,
    broker execution, capital allocation or production deployment.
    """

    errors: list[str] = []

    if minimum_total_days < 1:
        errors.append("minimum_total_days_must_be_positive")

    if not 0.0 <= minimum_review_ready_ratio <= 1.0:
        errors.append("minimum_review_ready_ratio_must_be_between_0_and_1")

    total_days = _as_int(monthly_pack.get("total_days"))
    review_ready_days = _as_list(monthly_pack.get("review_ready_days"))
    blocked_days = _as_list(monthly_pack.get("blocked_days"))
    gate_failure_days = _as_list(monthly_pack.get("gate_failure_days"))
    blocker_count = _as_int(monthly_pack.get("blocker_count"))
    error_count = _as_int(monthly_pack.get("error_count"))
    rejected_record_count = _as_int(monthly_pack.get("rejected_record_count"))
    needs_review_record_count = _as_int(monthly_pack.get("needs_review_record_count"))
    ratio = _review_ready_ratio(review_ready_days, total_days)

    if monthly_pack.get("live_trading_authorized") is not False:
        errors.append("live_trading_must_remain_false")

    if monthly_pack.get("broker_execution_mode") != "paper_only":
        errors.append("broker_execution_mode_must_be_paper_only")

    if str(monthly_pack.get("monthly_review_status", "")) != "REVIEW_READY":
        errors.append("monthly_review_status_must_be_review_ready")

    if total_days < max(minimum_total_days, 1):
        errors.append("insufficient_total_forward_days")

    if ratio < minimum_review_ready_ratio:
        errors.append("insufficient_review_ready_ratio")

    if blocked_days:
        errors.append("blocked_forward_days_present")

    if gate_failure_days:
        errors.append("gate_failures_present")

    if blocker_count > 0:
        errors.append("forward_blockers_present")

    if error_count > 0:
        errors.append("forward_errors_present")

    if rejected_record_count > 0:
        errors.append("rejected_records_present")

    if needs_review_record_count > 0:
        errors.append("needs_review_records_present")

    status = FORWARD_EVIDENCE_QUALITY_BLOCKED if errors else FORWARD_EVIDENCE_QUALITY_PASSED
    gate = {
        "month": str(monthly_pack.get("month", "")),
        "forward_evidence_quality_status": status,
        "approved_for_forward_review": not errors,
        "minimum_total_days": minimum_total_days,
        "minimum_review_ready_ratio": minimum_review_ready_ratio,
        "total_days": total_days,
        "review_ready_days": list(str(day) for day in review_ready_days),
        "review_ready_ratio": ratio,
        "blocked_days": list(str(day) for day in blocked_days),
        "gate_failure_days": list(str(day) for day in gate_failure_days),
        "blocker_count": blocker_count,
        "error_count": error_count,
        "rejected_record_count": rejected_record_count,
        "needs_review_record_count": needs_review_record_count,
        "errors": tuple(errors),
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }

    return ForwardEvidenceQualityGateResult(valid=not errors, errors=tuple(errors), gate=gate)
