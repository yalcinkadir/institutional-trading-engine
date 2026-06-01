from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

REVIEW_GATE_PASSED = "PASSED"
REVIEW_GATE_BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class PaperObservationReviewGateResult:
    valid: bool
    approved_for_review: bool
    blockers: tuple[str, ...]
    gate: dict[str, Any]


def _as_int(value: Any) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def evaluate_paper_observation_review_gate(
    summary: Mapping[str, Any],
    *,
    minimum_records: int = 1,
) -> PaperObservationReviewGateResult:
    """Evaluate whether Paper Observation evidence is ready for human review.

    PO9 consumes the deterministic PO8 Daily Observation Review Summary.

    This gate only approves paper-observation evidence for human review.
    It never authorizes live trading, broker execution or production deployment.
    """

    blockers: list[str] = []

    total_records = _as_int(summary.get("total_records"))
    accepted_count = _as_int(summary.get("accepted_count"))
    rejected_count = _as_int(summary.get("rejected_count"))
    needs_review_count = _as_int(summary.get("needs_review_count"))

    review_required_dates = _as_list(summary.get("review_required_dates"))
    rejected_dates = _as_list(summary.get("rejected_dates"))
    needs_review_dates = _as_list(summary.get("needs_review_dates"))

    if minimum_records < 1:
        blockers.append("minimum_records_must_be_positive")

    if total_records < max(minimum_records, 1):
        blockers.append("insufficient_observation_records")

    if summary.get("review_ready") is not True:
        blockers.append("summary_not_review_ready")

    if rejected_count != 0 or rejected_dates:
        blockers.append("rejected_observation_days_present")

    if needs_review_count != 0 or needs_review_dates:
        blockers.append("needs_review_observation_days_present")

    if review_required_dates:
        blockers.append("manual_review_required_dates_present")

    if accepted_count != total_records:
        blockers.append("accepted_count_must_equal_total_records")

    if summary.get("live_trading_authorized") is not False:
        blockers.append("live_trading_must_remain_false")

    if summary.get("broker_execution_mode") != "paper_only":
        blockers.append("broker_execution_mode_must_be_paper_only")

    approved_for_review = not blockers

    gate = {
        "gate_status": REVIEW_GATE_PASSED if approved_for_review else REVIEW_GATE_BLOCKED,
        "approved_for_review": approved_for_review,
        "minimum_records": minimum_records,
        "total_records": total_records,
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,
        "needs_review_count": needs_review_count,
        "review_required_dates": sorted(str(date) for date in review_required_dates),
        "rejected_dates": sorted(str(date) for date in rejected_dates),
        "needs_review_dates": sorted(str(date) for date in needs_review_dates),
        "blockers": tuple(blockers),
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }

    return PaperObservationReviewGateResult(
        valid=approved_for_review,
        approved_for_review=approved_for_review,
        blockers=tuple(blockers),
        gate=gate,
    )