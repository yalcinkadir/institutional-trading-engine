from __future__ import annotations

from src.operations.daily_observation_record_index import build_daily_observation_record_index
from src.operations.daily_observation_record_writer import build_daily_observation_record
from src.operations.daily_observation_review_summary import build_daily_observation_review_summary


def _record(day: str, **kwargs: object) -> dict[str, object]:
    return build_daily_observation_record(
        observation_date=day,
        created_at=f"{day}T00:00:00Z",
        **kwargs,
    )


def _index(*records: dict[str, object]) -> dict[str, object]:
    result = build_daily_observation_record_index(records)
    assert result.valid is True
    return result.index


def test_po8_marks_clean_accepted_index_as_review_ready() -> None:
    index = _index(_record("2026-06-01"), _record("2026-06-02"))

    result = build_daily_observation_review_summary(index)

    assert result.valid is True
    assert result.errors == ()
    assert result.summary["total_records"] == 2
    assert result.summary["accepted_count"] == 2
    assert result.summary["rejected_count"] == 0
    assert result.summary["needs_review_count"] == 0
    assert result.summary["review_required_dates"] == []
    assert result.summary["review_ready"] is True
    assert result.summary["live_trading_authorized"] is False
    assert result.summary["broker_execution_mode"] == "paper_only"


def test_po8_collects_rejected_dates_and_blocks_review_ready() -> None:
    index = _index(_record("2026-06-01"), _record("2026-06-02", missing_evidence=["report"]))

    result = build_daily_observation_review_summary(index)

    assert result.valid is True
    assert result.summary["accepted_count"] == 1
    assert result.summary["rejected_count"] == 1
    assert result.summary["rejected_dates"] == ["2026-06-02"]
    assert result.summary["review_ready"] is False


def test_po8_collects_needs_review_dates_and_review_required_dates() -> None:
    index = _index(_record("2026-06-01", incidents=["manual review"]))

    result = build_daily_observation_review_summary(index)

    assert result.valid is True
    assert result.summary["needs_review_count"] == 1
    assert result.summary["needs_review_dates"] == ["2026-06-01"]
    assert result.summary["review_required_dates"] == ["2026-06-01"]
    assert result.summary["review_ready"] is False


def test_po8_rejects_status_count_mismatch() -> None:
    index = _index(_record("2026-06-01"))
    index["status_counts"] = {"ACCEPTED": 0, "REJECTED": 0, "NEEDS_REVIEW": 0}

    result = build_daily_observation_review_summary(index)

    assert result.valid is False
    assert "accepted_count_mismatch" in result.errors
    assert result.summary["review_ready"] is False


def test_po8_rejects_total_record_mismatch() -> None:
    index = _index(_record("2026-06-01"))
    index["total_records"] = 2

    result = build_daily_observation_review_summary(index)

    assert result.valid is False
    assert "total_records_must_match_record_count" in result.errors
    assert result.summary["review_ready"] is False


def test_po8_rejects_index_live_trading_flag() -> None:
    index = _index(_record("2026-06-01"))
    index["live_trading_authorized"] = True

    result = build_daily_observation_review_summary(index)

    assert result.valid is False
    assert "index_live_trading_must_remain_false" in result.errors
    assert result.summary["live_trading_authorized"] is False


def test_po8_rejects_record_live_trading_flag() -> None:
    index = _index(_record("2026-06-01"))
    index["records"][0]["live_trading_authorized"] = True

    result = build_daily_observation_review_summary(index)

    assert result.valid is False
    assert "record:2026-06-01:live_trading_must_remain_false" in result.errors
    assert result.summary["live_trading_authorized"] is False


def test_po8_empty_index_is_not_review_ready() -> None:
    index = _index()

    result = build_daily_observation_review_summary(index)

    assert result.valid is True
    assert result.summary["total_records"] == 0
    assert result.summary["review_ready"] is False
