from __future__ import annotations

from src.validation.production_readiness_gate import evaluate_production_readiness


def _paper_health(*, passed: bool = True) -> dict:
    return {
        "passed": passed,
        "observation_health_status": "OK" if passed else "BLOCKED",
        "issues": [] if passed else [{"code": "paper_blocked", "message": "blocked"}],
        "readiness_evidence": {},
        "governance_state": {
            "live_trading_authorized": False,
            "broker_execution_mode": "paper_only",
        },
    }


def _scheduled_liveness(*, passed: bool = True) -> dict:
    return {
        "scheduled_report_status": "PASSED" if passed else "BLOCKED",
        "report_liveness_status": "REPORT_LIVENESS_OK" if passed else "REPORT_LIVENESS_BLOCKED",
        "productive_report_cycle": passed,
        "current_run_state": "WORKFLOW_RAN_VALIDATED",
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
        "errors": [] if passed else ["signals_stale_or_missing:2"],
    }


def _signals(*, actionable_count: int = 1, portfolio_status: str = "PASSED") -> dict:
    return {
        "actionable_count": actionable_count,
        "total_signals": max(1, actionable_count),
        "governance_state": {
            "live_trading_authorized": False,
            "broker_execution_mode": "paper_only",
        },
        "signals": [
            {
                "symbol": "QQQ",
                "action": "BUY_WATCH" if actionable_count else "NO_TRADE",
                "portfolio_risk_status": portfolio_status,
                "portfolio_risk_multiplier": 1.0 if portfolio_status == "PASSED" else None,
            }
        ],
    }


def _watcher_lifecycle(*, evaluated_plan_count: int = 1) -> dict:
    return {
        "evaluated_plan_count": evaluated_plan_count,
        "lifecycle_event_count": evaluated_plan_count,
        "terminal_signal_count": evaluated_plan_count,
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }


def _backtest(*, input_plan_count: int = 30) -> dict:
    return {
        "input_plan_count": input_plan_count,
        "evaluated_plan_count": input_plan_count,
        "lifecycle_event_count": input_plan_count,
        "terminal_signal_count": input_plan_count,
        "production_rule_promotion_authorized": False,
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }


def test_214_unified_gate_passes_when_all_evidence_is_green_and_paper_only() -> None:
    report = evaluate_production_readiness(
        paper_health=_paper_health(),
        scheduled_liveness=_scheduled_liveness(),
        signals=_signals(),
        watcher_lifecycle=_watcher_lifecycle(),
        backtest=_backtest(),
        commit_sha="abc123",
        workflow_name="CI",
    )

    assert report["production_ready"] is True
    assert report["paper_observation_ready"] is True
    assert report["backtesting_ready"] is True
    assert report["live_trading_authorized"] is False
    assert report["capital_allocation_authorized"] is False
    assert report["blockers"] == []


def test_214_unified_gate_blocks_when_scheduled_liveness_is_blocked() -> None:
    report = evaluate_production_readiness(
        paper_health=_paper_health(),
        scheduled_liveness=_scheduled_liveness(passed=False),
        signals=_signals(),
        watcher_lifecycle=_watcher_lifecycle(),
        backtest=_backtest(),
    )

    assert report["production_ready"] is False
    assert report["paper_observation_ready"] is False
    assert "scheduled_report_liveness_not_ready" in report["blockers"]


def test_214_unified_gate_blocks_when_backtest_sample_is_too_small() -> None:
    report = evaluate_production_readiness(
        paper_health=_paper_health(),
        scheduled_liveness=_scheduled_liveness(),
        signals=_signals(),
        watcher_lifecycle=_watcher_lifecycle(),
        backtest=_backtest(input_plan_count=1),
    )

    assert report["production_ready"] is False
    assert report["backtesting_ready"] is False
    assert "backtest_sample_below_threshold" in report["blockers"]


def test_214_unified_gate_blocks_live_trading_authorization_anywhere() -> None:
    watcher = _watcher_lifecycle()
    watcher["live_trading_authorized"] = True

    report = evaluate_production_readiness(
        paper_health=_paper_health(),
        scheduled_liveness=_scheduled_liveness(),
        signals=_signals(),
        watcher_lifecycle=watcher,
        backtest=_backtest(),
    )

    assert report["production_ready"] is False
    assert report["live_trading_authorized"] is False
    assert "live_trading_authorized_in_evidence" in report["blockers"]


def test_214_unified_gate_blocks_when_portfolio_risk_path_is_not_passed_for_actionable_signals() -> None:
    report = evaluate_production_readiness(
        paper_health=_paper_health(),
        scheduled_liveness=_scheduled_liveness(),
        signals=_signals(actionable_count=1, portfolio_status="NOT_REQUIRED"),
        watcher_lifecycle=_watcher_lifecycle(),
        backtest=_backtest(),
    )

    assert report["production_ready"] is False
    assert report["paper_observation_ready"] is False
    assert "portfolio_risk_not_passed_for_actionable_signals" in report["blockers"]
