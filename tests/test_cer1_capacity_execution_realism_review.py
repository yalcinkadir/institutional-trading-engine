from __future__ import annotations

from src.validation.capacity_execution_realism_review import build_capacity_execution_realism_review
from src.validation.capacity_turnover_realism_gate import build_capacity_turnover_realism_report, demo_capacity_turnover_snapshot


def _report(**metric_overrides: float):
    snapshot = demo_capacity_turnover_snapshot()
    metrics = dict(snapshot.metrics)
    metrics.update(metric_overrides)
    snapshot = snapshot.__class__.from_mapping({**snapshot.to_dict(), "metrics": metrics})
    return build_capacity_turnover_realism_report(snapshot, generated_at="2026-06-03T00:00:00Z")


def test_cer1_builds_review_ready_summary_from_passing_bt7_report() -> None:
    review = build_capacity_execution_realism_review(_report())

    assert review.valid is True
    assert review.errors == ()
    assert review.summary["capacity_execution_review_status"] == "REVIEW_READY"
    assert review.summary["approved_for_execution_review"] is True
    assert review.summary["bt7_passed"] is True
    assert review.summary["liquidity_profile"]["max_position_adv_pct"] == 1.25
    assert review.summary["cost_profile"]["round_trip_cost_bps"] == 7.5
    assert review.summary["live_trading_authorized"] is False
    assert review.summary["broker_execution_mode"] == "paper_only"


def test_cer1_blocks_failed_bt7_report_and_surfaces_failed_gate_names() -> None:
    review = build_capacity_execution_realism_review(_report(max_position_adv_pct=9.0, round_trip_cost_bps=30.0))

    assert review.valid is False
    assert review.summary["capacity_execution_review_status"] == "BLOCKED"
    assert review.summary["approved_for_execution_review"] is False
    assert "bt7_report_failed" in review.errors
    assert "capacity_liquidity_limits" in review.summary["failed_gates"]
    assert "cost_drag_realism" in review.summary["failed_gates"]


def test_cer1_blocks_missing_artifact_hashes_and_public_safety_breaks() -> None:
    snapshot = demo_capacity_turnover_snapshot().__class__.from_mapping(
        {
            **demo_capacity_turnover_snapshot().to_dict(),
            "artifact_hashes": {},
            "tags": ["demo"],
            "footer": "Live trading approved",
        }
    )
    report = build_capacity_turnover_realism_report(snapshot)
    review = build_capacity_execution_realism_review(report)

    assert review.valid is False
    assert "artifact_hashes_present" in review.summary["failed_gates"]
    assert "public_safe_tags" in review.summary["failed_gates"]
    assert "research_only_footer" in review.summary["failed_gates"]


def test_cer1_keeps_live_and_broker_execution_blocked_even_for_good_report() -> None:
    review = build_capacity_execution_realism_review(
        _report(),
        live_trading_authorized=True,
        broker_execution_mode="live",
    )

    assert review.valid is False
    assert "live_trading_must_remain_false" in review.errors
    assert "broker_execution_mode_must_be_paper_only" in review.errors
    assert review.summary["live_trading_authorized"] is False
    assert review.summary["broker_execution_mode"] == "paper_only"
