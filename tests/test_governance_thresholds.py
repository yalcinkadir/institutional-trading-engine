from __future__ import annotations

import inspect

from src.governance.governance_thresholds import (
    DEFAULT_GOVERNANCE_THRESHOLDS,
    GovernanceThresholds,
)
from src.governance.kill_switch import evaluate_kill_switch
from src.runtime.live_runtime_cycle import LiveRuntimeCycle


def test_default_governance_thresholds_preserve_existing_public_defaults() -> None:
    thresholds = DEFAULT_GOVERNANCE_THRESHOLDS

    assert thresholds.vix_kill_level == 40.0
    assert thresholds.portfolio_drawdown_kill_percent == 20.0
    assert thresholds.severe_anomaly_kill_count == 5
    assert thresholds.max_drawdown_percent == 15.0
    assert thresholds.max_daily_loss_percent == 5.0


def test_kill_switch_uses_injected_thresholds_instead_of_magic_numbers() -> None:
    relaxed = GovernanceThresholds(
        vix_kill_level=50.0,
        portfolio_drawdown_kill_percent=30.0,
        severe_anomaly_kill_count=10,
        max_drawdown_percent=15.0,
        max_daily_loss_percent=5.0,
    )

    result = evaluate_kill_switch(
        vix=45.0,
        drawdown_percent=25.0,
        severe_anomaly_count=7,
        thresholds=relaxed,
    )

    assert result["kill_switch"] is False
    assert result["reasons"] == []


def test_kill_switch_triggers_from_shared_custom_thresholds() -> None:
    strict = GovernanceThresholds(
        vix_kill_level=18.0,
        portfolio_drawdown_kill_percent=4.0,
        severe_anomaly_kill_count=2,
        max_drawdown_percent=3.0,
        max_daily_loss_percent=1.0,
    )

    result = evaluate_kill_switch(
        vix=18.0,
        drawdown_percent=4.0,
        severe_anomaly_count=2,
        thresholds=strict,
    )

    assert result["kill_switch"] is True
    assert result["reasons"] == [
        "extreme_volatility",
        "portfolio_drawdown_limit",
        "market_instability",
    ]


def test_live_runtime_cycle_accepts_shared_threshold_source() -> None:
    thresholds = GovernanceThresholds(
        vix_kill_level=99.0,
        portfolio_drawdown_kill_percent=88.0,
        severe_anomaly_kill_count=77,
        max_drawdown_percent=66.0,
        max_daily_loss_percent=55.0,
    )

    cycle = LiveRuntimeCycle(governance_thresholds=thresholds)

    assert cycle.governance_thresholds is thresholds


def test_runtime_cycle_no_longer_defines_local_governance_threshold_constants() -> None:
    source = inspect.getsource(LiveRuntimeCycle)

    assert "_GOVERNANCE_VIX_KILL_THRESHOLD" not in source
    assert "_GOVERNANCE_DRAWDOWN_KILL_THRESHOLD" not in source
    assert "_GOVERNANCE_ANOMALY_KILL_THRESHOLD" not in source
    assert "_GOVERNANCE_MAX_DRAWDOWN_PCT" not in source
    assert "_GOVERNANCE_MAX_DAILY_LOSS_PCT" not in source


def test_thresholds_are_auditable_as_dict() -> None:
    payload = DEFAULT_GOVERNANCE_THRESHOLDS.to_dict()

    assert payload == {
        "vix_kill_level": 40.0,
        "portfolio_drawdown_kill_percent": 20.0,
        "severe_anomaly_kill_count": 5,
        "max_drawdown_percent": 15.0,
        "max_daily_loss_percent": 5.0,
    }