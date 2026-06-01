from __future__ import annotations

from src.operations.daily_observation_record_index import build_daily_observation_record_index
from src.operations.daily_observation_record_writer import build_daily_observation_record
from src.operations.daily_observation_review_summary import build_daily_observation_review_summary
from src.operations.paper_observation_review_gate import evaluate_paper_observation_review_gate


def _record(day: str, **kwargs: object) -> dict[str, object]:
    return build_daily_observation_record(
        observation_date=day,
        created_at=f"{day}T00:00:00Z",
        **kwargs,
    )


def _summary(*records: dict[str, object]) -> dict[str, object]:
    index_result = build_daily_observation_record_index(records)
    assert index_result.valid is True
    summary_result = build_daily_observation_review_summary(index_result.index)
    assert summary_result.valid is True
    return summary_result.summary


def test_po9_passes_clean_review_ready_summary() -> None:
    summary = _summary(_record("2026-06-01"), _record("2026-06-02"))

    result = evaluate_paper_observation_review_gate(summary, minimum_records=2)

    assert result.valid is True
    assert result.approved_for_review is True
    assert result.blockers == ()
    assert result.gate["gate_status"] == "PASSED"
    assert result.gate["approved_for_review"] is True
    assert result.gate["live_trading_authorized"] is False
    assert result.gate["broker_execution_mode"] == "paper_only"


def test_po9_blocks_insufficient_observation_records() -> None:
    summary = _summary(_record("2026-06-01"))

    result = evaluate_paper_observation_review_gate(summary, minimum_records=2)

    assert result.valid is False
    assert result.approved_for_review is False
    assert result.gate["gate_status"] == "BLOCKED"
    assert "insufficient_observation_records" in result.blockers


def test_po9_blocks_rejected_observation_days() -> None:
    summary = _summary(_record("2026-06-01"), _record("2026-06-02", missing_evidence=["report"]))

    result = evaluate_paper_observation_review_gate(summary)

    assert result.valid is False
    assert "summary_not_review_ready" in result.blockers
    assert "rejected_observation_days_present" in result.blockers
    assert result.gate["rejected_dates"] == ["2026-06-02"]


def test_po9_blocks_needs_review_observation_days() -> None:
    summary = _summary(_record("2026-06-01", incidents=["manual review"]))

    result = evaluate_paper_observation_review_gate(summary)

    assert result.valid is False
    assert "summary_not_review_ready" in result.blockers
    assert "needs_review_observation_days_present" in result.blockers
    assert "manual_review_required_dates_present" in result.blockers
    assert result.gate["needs_review_dates"] == ["2026-06-01"]
    assert result.gate["review_required_dates"] == ["2026-06-01"]


def test_po9_blocks_summary_that_implies_live_trading() -> None:
    summary = _summary(_record("2026-06-01"))
    summary["live_trading_authorized"] = True

    result = evaluate_paper_observation_review_gate(summary)

    assert result.valid is False
    assert "live_trading_must_remain_false" in result.blockers
    assert result.gate["live_trading_authorized"] is False


def test_po9_blocks_summary_that_implies_non_paper_execution() -> None:
    summary = _summary(_record("2026-06-01"))
    summary["broker_execution_mode"] = "live"

    result = evaluate_paper_observation_review_gate(summary)

    assert result.valid is False
    assert "broker_execution_mode_must_be_paper_only" in result.blockers
    assert result.gate["broker_execution_mode"] == "paper_only"


def test_po9_blocks_empty_summary() -> None:
    summary = _summary()

    result = evaluate_paper_observation_review_gate(summary)

    assert result.valid is False
    assert "insufficient_observation_records" in result.blockers
    assert "summary_not_review_ready" in result.blockers


def test_po9_blocks_invalid_minimum_record_requirement() -> None:
    summary = _summary(_record("2026-06-01"))

    result = evaluate_paper_observation_review_gate(summary, minimum_records=0)

    assert result.valid is False
    assert "minimum_records_must_be_positive" in result.blockers
