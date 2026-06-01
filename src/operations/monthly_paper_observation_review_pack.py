from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

MONTHLY_REVIEW_READY = "REVIEW_READY"
MONTHLY_REVIEW_BLOCKED = "BLOCKED"
MONTHLY_REVIEW_PACK_ROOT = Path("reports/monthly_paper_observation_review")


@dataclass(frozen=True)
class MonthlyPaperObservationReviewPackResult:
    valid: bool
    errors: tuple[str, ...]
    pack_path: str
    pack: dict[str, Any]


def build_monthly_paper_observation_review_pack_path(month: str) -> Path:
    return MONTHLY_REVIEW_PACK_ROOT / f"{month}.json"


def _as_int(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_entries(index: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    entries = index.get("artifacts", [])
    if isinstance(entries, list):
        return [entry for entry in entries if isinstance(entry, Mapping)]
    return []


def _entry_month(entry: Mapping[str, Any]) -> str:
    observation_date = str(entry.get("observation_date", ""))
    return observation_date[:7] if len(observation_date) >= 7 else ""


def _month_is_valid(month: str) -> bool:
    if len(month) != 7 or month[4] != "-":
        return False
    year, month_value = month.split("-", maxsplit=1)
    if not year.isdigit() or not month_value.isdigit():
        return False
    return 1 <= int(month_value) <= 12


def build_monthly_paper_observation_review_pack(
    review_index: Mapping[str, Any],
    *,
    month: str,
    minimum_review_ready_days: int = 1,
) -> MonthlyPaperObservationReviewPackResult:
    """Build a deterministic monthly review pack from the PO12 review index.

    PO13 prepares monthly Paper Observation evidence for human review only.
    It never authorizes live trading, broker execution or capital allocation.
    """

    errors: list[str] = []

    if not _month_is_valid(month):
        errors.append("month_must_use_yyyy_mm_format")

    if minimum_review_ready_days < 1:
        errors.append("minimum_review_ready_days_must_be_positive")

    if review_index.get("live_trading_authorized") is not False:
        errors.append("review_index_live_trading_must_remain_false")

    if review_index.get("broker_execution_mode") != "paper_only":
        errors.append("review_index_broker_execution_mode_must_be_paper_only")

    month_entries = [dict(entry) for entry in _as_entries(review_index) if _entry_month(entry) == month]
    month_entries.sort(key=lambda entry: str(entry.get("observation_date", "")))

    total_days = len(month_entries)
    review_ready_days = [str(entry.get("observation_date", "")) for entry in month_entries if entry.get("review_ready") is True]
    blocked_days = [str(entry.get("observation_date", "")) for entry in month_entries if entry.get("automation_status") == "BLOCKED"]
    passed_days = [str(entry.get("observation_date", "")) for entry in month_entries if entry.get("automation_status") == "PASSED"]
    gate_failure_days = [
        str(entry.get("observation_date", ""))
        for entry in month_entries
        if str(entry.get("gate_status", "")) == "BLOCKED"
    ]

    blocker_count = sum(_as_int(entry.get("blocker_count")) for entry in month_entries)
    error_count = sum(_as_int(entry.get("error_count")) for entry in month_entries)
    rejected_record_count = sum(_as_int(entry.get("rejected_count")) for entry in month_entries)
    needs_review_record_count = sum(_as_int(entry.get("needs_review_count")) for entry in month_entries)

    for entry in month_entries:
        observation_date = str(entry.get("observation_date", ""))
        if entry.get("live_trading_authorized") is not False:
            errors.append(f"artifact:{observation_date}:live_trading_must_remain_false")
        if entry.get("broker_execution_mode") != "paper_only":
            errors.append(f"artifact:{observation_date}:broker_execution_mode_must_be_paper_only")

    if total_days == 0:
        errors.append("no_monthly_observation_artifacts")

    if len(review_ready_days) < max(minimum_review_ready_days, 1):
        errors.append("insufficient_review_ready_days")

    if blocked_days:
        errors.append("blocked_observation_days_present")

    if gate_failure_days:
        errors.append("gate_failures_present")

    if blocker_count > 0:
        errors.append("monthly_blockers_present")

    if error_count > 0:
        errors.append("monthly_errors_present")

    if rejected_record_count > 0:
        errors.append("rejected_records_present")

    if needs_review_record_count > 0:
        errors.append("needs_review_records_present")

    monthly_review_status = MONTHLY_REVIEW_BLOCKED if errors else MONTHLY_REVIEW_READY
    pack_path = build_monthly_paper_observation_review_pack_path(month)

    pack = {
        "month": month,
        "monthly_review_status": monthly_review_status,
        "minimum_review_ready_days": minimum_review_ready_days,
        "total_days": total_days,
        "passed_days": passed_days,
        "blocked_days": blocked_days,
        "review_ready_days": review_ready_days,
        "gate_failure_days": gate_failure_days,
        "blocker_count": blocker_count,
        "error_count": error_count,
        "rejected_record_count": rejected_record_count,
        "needs_review_record_count": needs_review_record_count,
        "artifacts": month_entries,
        "errors": tuple(errors),
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }

    return MonthlyPaperObservationReviewPackResult(
        valid=not errors,
        errors=tuple(errors),
        pack_path=str(pack_path),
        pack=pack,
    )


def write_monthly_paper_observation_review_pack(
    *,
    result: MonthlyPaperObservationReviewPackResult,
    output_path: str | Path | None = None,
    indent: int = 2,
) -> MonthlyPaperObservationReviewPackResult:
    path = Path(output_path) if output_path is not None else Path(result.pack_path)
    expected_path = Path(result.pack_path)

    if path != expected_path:
        pack = dict(result.pack)
        errors = tuple(result.errors) + ("monthly_review_pack_path_must_be_canonical",)
        pack["errors"] = errors
        return MonthlyPaperObservationReviewPackResult(
            valid=False,
            errors=errors,
            pack_path=result.pack_path,
            pack=pack,
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result.pack, indent=indent, sort_keys=True) + "\n", encoding="utf-8")
    return result
