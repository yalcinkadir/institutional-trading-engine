from __future__ import annotations

from src.operations.forward_evidence_quality_gate import evaluate_forward_evidence_quality_gate


def _pack(**overrides: object) -> dict[str, object]:
    pack: dict[str, object] = {
        "month": "2026-06",
        "monthly_review_status": "REVIEW_READY",
        "total_days": 5,
        "passed_days": ["2026-06-01", "2026-06-02", "2026-06-03", "2026-06-04", "2026-06-05"],
        "blocked_days": [],
        "review_ready_days": ["2026-06-01", "2026-06-02", "2026-06-03", "2026-06-04", "2026-06-05"],
        "gate_failure_days": [],
        "blocker_count": 0,
        "error_count": 0,
        "rejected_record_count": 0,
        "needs_review_record_count": 0,
        "errors": (),
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }
    pack.update(overrides)
    return pack


def test_po14_accepts_review_ready_forward_evidence() -> None:
    result = evaluate_forward_evidence_quality_gate(_pack(), minimum_total_days=5, minimum_review_ready_ratio=0.8)

    assert result.valid is True
    assert result.errors == ()
    assert result.gate["forward_evidence_quality_status"] == "PASSED"
    assert result.gate["approved_for_forward_review"] is True
    assert result.gate["review_ready_ratio"] == 1.0
    assert result.gate["live_trading_authorized"] is False
    assert result.gate["broker_execution_mode"] == "paper_only"


def test_po14_blocks_insufficient_review_ready_ratio_and_sample_size() -> None:
    result = evaluate_forward_evidence_quality_gate(
        _pack(total_days=2, review_ready_days=["2026-06-01"]),
        minimum_total_days=5,
        minimum_review_ready_ratio=0.8,
    )

    assert result.valid is False
    assert result.gate["forward_evidence_quality_status"] == "BLOCKED"
    assert result.gate["approved_for_forward_review"] is False
    assert result.gate["review_ready_ratio"] == 0.5
    assert "insufficient_total_forward_days" in result.errors
    assert "insufficient_review_ready_ratio" in result.errors


def test_po14_blocks_quality_defects_and_boundary_breaks() -> None:
    result = evaluate_forward_evidence_quality_gate(
        _pack(
            blocked_days=["2026-06-04"],
            gate_failure_days=["2026-06-04"],
            blocker_count=1,
            error_count=1,
            rejected_record_count=1,
            needs_review_record_count=1,
            live_trading_authorized=True,
            broker_execution_mode="live",
        )
    )

    assert result.valid is False
    assert {
        "blocked_forward_days_present",
        "gate_failures_present",
        "forward_blockers_present",
        "forward_errors_present",
        "rejected_records_present",
        "needs_review_records_present",
        "live_trading_must_remain_false",
        "broker_execution_mode_must_be_paper_only",
    }.issubset(set(result.errors))
    assert result.gate["live_trading_authorized"] is False
    assert result.gate["broker_execution_mode"] == "paper_only"
