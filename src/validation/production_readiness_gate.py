from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

DEFAULT_BACKTEST_MIN_SAMPLE = 30


def evaluate_production_readiness(
    *,
    paper_health: dict[str, Any] | None = None,
    scheduled_liveness: dict[str, Any] | None = None,
    signals: dict[str, Any] | None = None,
    watcher_lifecycle: dict[str, Any] | None = None,
    backtest: dict[str, Any] | None = None,
    commit_sha: str | None = None,
    workflow_name: str | None = None,
    backtest_min_sample: int = DEFAULT_BACKTEST_MIN_SAMPLE,
) -> dict[str, Any]:
    paper_health = paper_health if isinstance(paper_health, dict) else {}
    scheduled_liveness = scheduled_liveness if isinstance(scheduled_liveness, dict) else {}
    signals = signals if isinstance(signals, dict) else {}
    watcher_lifecycle = watcher_lifecycle if isinstance(watcher_lifecycle, dict) else {}
    backtest = backtest if isinstance(backtest, dict) else {}

    blockers: list[str] = []

    if not paper_health.get("passed"):
        blockers.append("paper_observation_health_not_passed")

    if str(scheduled_liveness.get("scheduled_report_status") or "UNKNOWN") != "PASSED":
        blockers.append("scheduled_report_liveness_not_ready")
    if str(scheduled_liveness.get("report_liveness_status") or scheduled_liveness.get("liveness_status") or "UNKNOWN") != "REPORT_LIVENESS_OK":
        blockers.append("report_liveness_not_ok")
    if scheduled_liveness.get("productive_report_cycle") is not True:
        blockers.append("productive_report_cycle_not_validated")

    watcher_evaluated_plan_count = _as_int(watcher_lifecycle.get("evaluated_plan_count"), 0)
    watcher_lifecycle_event_count = _as_int(watcher_lifecycle.get("lifecycle_event_count"), 0)
    watcher_terminal_signal_count = _as_int(watcher_lifecycle.get("terminal_signal_count"), 0)
    if watcher_evaluated_plan_count <= 0 or watcher_lifecycle_event_count <= 0 or watcher_terminal_signal_count <= 0:
        blockers.append("watcher_lifecycle_evidence_missing")

    actionable_count = _as_int(signals.get("actionable_count"), 0)
    signal_items = signals.get("signals") if isinstance(signals.get("signals"), list) else []
    if actionable_count > 0:
        actionable_signals = [item for item in signal_items if isinstance(item, dict) and item.get("action") == "BUY_WATCH"]
        if not actionable_signals:
            blockers.append("actionable_count_without_actionable_signal_records")
        elif any(str(item.get("portfolio_risk_status") or "UNKNOWN") != "PASSED" for item in actionable_signals):
            blockers.append("portfolio_risk_not_passed_for_actionable_signals")

    backtest_input_plan_count = _as_int(backtest.get("input_plan_count"), 0)
    backtest_evaluated_plan_count = _as_int(backtest.get("evaluated_plan_count"), 0)
    backtest_lifecycle_event_count = _as_int(backtest.get("lifecycle_event_count"), 0)
    backtest_terminal_signal_count = _as_int(backtest.get("terminal_signal_count"), 0)
    if backtest_input_plan_count < backtest_min_sample or backtest_evaluated_plan_count < backtest_min_sample:
        blockers.append("backtest_sample_below_threshold")
    if backtest_lifecycle_event_count <= 0 or backtest_terminal_signal_count <= 0:
        blockers.append("backtest_lifecycle_evidence_missing")
    if backtest.get("production_rule_promotion_authorized") is True:
        blockers.append("backtest_production_rule_promotion_authorized")

    if _any_live_trading_authorized(
        paper_health,
        scheduled_liveness,
        signals,
        watcher_lifecycle,
        backtest,
    ):
        blockers.append("live_trading_authorized_in_evidence")

    blockers = sorted(set(blockers))
    paper_blockers = {
        "paper_observation_health_not_passed",
        "scheduled_report_liveness_not_ready",
        "report_liveness_not_ok",
        "productive_report_cycle_not_validated",
        "watcher_lifecycle_evidence_missing",
        "portfolio_risk_not_passed_for_actionable_signals",
        "actionable_count_without_actionable_signal_records",
        "live_trading_authorized_in_evidence",
    }
    backtest_blockers = {
        "backtest_sample_below_threshold",
        "backtest_lifecycle_evidence_missing",
        "backtest_production_rule_promotion_authorized",
        "live_trading_authorized_in_evidence",
    }

    paper_observation_ready = not any(blocker in paper_blockers for blocker in blockers)
    backtesting_ready = not any(blocker in backtest_blockers for blocker in blockers)
    production_ready = paper_observation_ready and backtesting_ready and not blockers

    return {
        "schema_version": "production_readiness.v1",
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "issue": "#214",
        "workflow_name": workflow_name or "UNKNOWN",
        "commit_sha": commit_sha or "UNKNOWN",
        "production_ready": production_ready,
        "paper_observation_ready": paper_observation_ready,
        "backtesting_ready": backtesting_ready,
        "live_trading_authorized": False,
        "capital_allocation_authorized": False,
        "broker_execution_mode": "paper_only",
        "blockers": blockers,
        "thresholds": {
            "backtest_min_sample": backtest_min_sample,
        },
        "evidence_summary": {
            "paper_health_passed": paper_health.get("passed"),
            "observation_health_status": paper_health.get("observation_health_status"),
            "scheduled_report_status": scheduled_liveness.get("scheduled_report_status"),
            "report_liveness_status": scheduled_liveness.get("report_liveness_status") or scheduled_liveness.get("liveness_status"),
            "productive_report_cycle": scheduled_liveness.get("productive_report_cycle"),
            "actionable_count": actionable_count,
            "watcher_evaluated_plan_count": watcher_evaluated_plan_count,
            "watcher_lifecycle_event_count": watcher_lifecycle_event_count,
            "watcher_terminal_signal_count": watcher_terminal_signal_count,
            "backtest_input_plan_count": backtest_input_plan_count,
            "backtest_evaluated_plan_count": backtest_evaluated_plan_count,
            "backtest_lifecycle_event_count": backtest_lifecycle_event_count,
            "backtest_terminal_signal_count": backtest_terminal_signal_count,
        },
    }


def _any_live_trading_authorized(*payloads: dict[str, Any]) -> bool:
    for payload in payloads:
        if payload.get("live_trading_authorized") is True:
            return True
        governance = payload.get("governance_state")
        if isinstance(governance, dict) and governance.get("live_trading_authorized") is True:
            return True
    return False


def _as_int(value: Any, fallback: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback
