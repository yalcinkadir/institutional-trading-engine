from __future__ import annotations

from src.governance.kill_switch import (
    INVALID_PORTFOLIO_GOVERNANCE_REASON,
    evaluate_kill_switch_for_portfolio_state,
)
from src.runtime.portfolio_state import PortfolioState


def test_missing_portfolio_state_conservative_default_forces_kill_switch() -> None:
    state = PortfolioState.conservative_default("portfolio_state.json missing")

    result = evaluate_kill_switch_for_portfolio_state(
        portfolio_state=state,
        vix=None,
        severe_anomaly_count=0,
    )

    assert result["kill_switch"] is True
    assert result["portfolio_governance_valid"] is False
    assert result["portfolio_state_source"] == "missing_portfolio_state_fail_closed"
    assert result["vix_available"] is False
    assert INVALID_PORTFOLIO_GOVERNANCE_REASON in result["reasons"]


def test_valid_portfolio_state_does_not_force_kill_switch_without_breach() -> None:
    state = PortfolioState(
        equity_start=100_000.0,
        equity_current=99_500.0,
        drawdown_percent=0.5,
        daily_loss_percent=0.2,
        governance_valid=True,
        source="trusted_test_snapshot",
    )

    result = evaluate_kill_switch_for_portfolio_state(
        portfolio_state=state,
        vix=None,
        severe_anomaly_count=0,
    )

    assert result["kill_switch"] is False
    assert result["portfolio_governance_valid"] is True
    assert result["reasons"] == []


def test_invalid_portfolio_state_preserves_existing_kill_switch_reasons() -> None:
    state = PortfolioState(
        equity_start=100_000.0,
        equity_current=80_000.0,
        drawdown_percent=20.0,
        daily_loss_percent=0.0,
        governance_valid=False,
        source="invalid_test_snapshot",
    )

    result = evaluate_kill_switch_for_portfolio_state(
        portfolio_state=state,
        vix=None,
        severe_anomaly_count=0,
    )

    assert result["kill_switch"] is True
    assert result["reasons"][0] == INVALID_PORTFOLIO_GOVERNANCE_REASON
    assert "portfolio_drawdown_limit" in result["reasons"]
