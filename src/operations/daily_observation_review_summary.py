from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

VALID_SUMMARY_STATUSES = ("ACCEPTED", "REJECTED", "NEEDS_REVIEW")


@dataclass(frozen=True)
class DailyObservationReviewSummaryResult:
    valid: bool
    errors: tuple[str, ...]
    summary: dict[str, Any]


def build_daily_observation_review_summary(index: Mapping[str, Any]) -> DailyObservationReviewSummaryResult:
    errors: list[str] = []
    records = list(index.get("records", []))

    if index.get("live_trading_authorized") is not False:
        errors.append("index_live_trading_must_remain_false")

    if index.get("broker_execution_mode") != "paper_only":
        errors.append("index_broker_execution_mode_must_be_paper_only")

    total_records = int(index.get("total_records", 0))
    if total_records != len(records):
        errors.append("total_records_must_match_record_count")

    status_counts = dict(index.get("status_counts", {}))
    accepted_count = int(status_counts.get("ACCEPTED", 0))
    rejected_count = int(status_counts.get("REJECTED", 0))
    needs_review_count = int(status_counts.get("NEEDS_REVIEW", 0))

    computed_counts = {status: 0 for status in VALID_SUMMARY_STATUSES}
    review_required_dates: list[str] = []
    rejected_dates: list[str] = []
    needs_review_dates: list[str] = []

    for record in records:
        date_value = str(record.get("date", ""))
        status = str(record.get("status", ""))

        if record.get("live_trading_authorized") is not False:
            errors.append(f"record:{date_value}:live_trading_must_remain_false")

        if record.get("broker_execution_mode") != "paper_only":
            errors.append(f"record:{date_value}:broker_execution_mode_must_be_paper_only")

        if status not in VALID_SUMMARY_STATUSES:
            errors.append(f"record:{date_value}:invalid_status")
        else:
            computed_counts[status] += 1

        if record.get("review_required") is True:
            review_required_dates.append(date_value)
        if status == "REJECTED":
            rejected_dates.append(date_value)
        if status == "NEEDS_REVIEW":
            needs_review_dates.append(date_value)

    if computed_counts["ACCEPTED"] != accepted_count:
        errors.append("accepted_count_mismatch")
    if computed_counts["REJECTED"] != rejected_count:
        errors.append("rejected_count_mismatch")
    if computed_counts["NEEDS_REVIEW"] != needs_review_count:
        errors.append("needs_review_count_mismatch")

    review_ready = (
        total_records > 0
        and rejected_count == 0
        and needs_review_count == 0
        and not review_required_dates
        and not errors
    )

    summary = {
        "total_records": total_records,
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,
        "needs_review_count": needs_review_count,
        "review_required_dates": sorted(review_required_dates),
        "rejected_dates": sorted(rejected_dates),
        "needs_review_dates": sorted(needs_review_dates),
        "review_ready": review_ready,
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }

    return DailyObservationReviewSummaryResult(valid=not errors, errors=tuple(errors), summary=summary)
