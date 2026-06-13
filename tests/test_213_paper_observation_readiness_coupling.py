from __future__ import annotations

from src.validation.paper_observation_health_gate import (
    HEALTH_STATUS_BLOCKED,
    validate_paper_observation_health,
)


def _healthy_no_trade_payload() -> dict:
    return {
        "market_regime": "Neutral",
        "total_signals": 2,
        "actionable_count": 0,
        "data_quality": {"data_quality_status": "OK"},
        "governance_state": {
            "governance_status": "PASSED",
            "live_trading_authorized": False,
            "broker_execution_mode": "paper_only",
        },
        "signals": [
            {
                "signal_id": "sig_spy",
                "symbol": "SPY",
                "action": "NO_TRADE",
                "decision": "blocked",
                "close": 530.0,
                "entry_reason": "n/a",
                "stop_reason": "n/a",
                "exit_reason": "n/a",
                "market_regime": "Neutral",
                "notes": "regime or quality filter",
                "source": "polygon",
                "source_timestamp": "2026-06-13T12:30:00Z",
                "fallback_level": "primary",
                "data_status": "OK",
            },
            {
                "signal_id": "sig_qqq",
                "symbol": "QQQ",
                "action": "NO_TRADE",
                "decision": "blocked",
                "close": 460.0,
                "entry_reason": "n/a",
                "stop_reason": "n/a",
                "exit_reason": "n/a",
                "market_regime": "Neutral",
                "notes": "regime or quality filter",
                "source": "polygon",
                "source_timestamp": "2026-06-13T12:30:00Z",
                "fallback_level": "primary",
                "data_status": "OK",
            },
        ],
    }


def test_213_health_gate_blocks_when_scheduled_liveness_is_blocked() -> None:
    report = validate_paper_observation_health(
        _healthy_no_trade_payload(),
        scheduled_liveness={
            "scheduled_report_status": "BLOCKED",
            "report_liveness_status": "REPORT_LIVENESS_BLOCKED",
            "productive_report_cycle": False,
            "errors": ["daily_evidence_stale_or_missing:2"],
        },
    )

    assert report.passed is False
    assert report.observation_health_status == HEALTH_STATUS_BLOCKED
    assert "scheduled_report_liveness_not_ready" in {issue.code for issue in report.issues}
    assert report.readiness_evidence["scheduled_liveness"]["scheduled_report_status"] == "BLOCKED"


def test_213_health_gate_blocks_when_watcher_lifecycle_evidence_is_empty() -> None:
    report = validate_paper_observation_health(
        _healthy_no_trade_payload(),
        watcher_lifecycle={
            "schema_version": "watcher_lifecycle.v1",
            "evaluated_plan_count": 0,
            "lifecycle_event_count": 0,
            "terminal_signal_count": 0,
            "live_trading_authorized": False,
            "broker_execution_mode": "paper_only",
        },
    )

    assert report.passed is False
    assert report.observation_health_status == HEALTH_STATUS_BLOCKED
    assert "watcher_lifecycle_evidence_missing" in {issue.code for issue in report.issues}
    assert report.readiness_evidence["watcher_lifecycle"]["lifecycle_event_count"] == 0
