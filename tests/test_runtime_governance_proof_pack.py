from __future__ import annotations

from datetime import UTC, datetime, timedelta

from src.governance.kill_switch import (
    INVALID_PORTFOLIO_GOVERNANCE_REASON,
    evaluate_kill_switch_for_portfolio_state,
)
from src.runtime.governance_approval_gate import (
    DATA_PROVIDER_FETCH_FAILURE_REASON,
    INVALID_GOVERNANCE_APPROVAL_REASON,
    KILL_SWITCH_APPROVAL_REASON,
    STALE_PORTFOLIO_STATE_REASON,
    evaluate_runtime_governance_approval,
    is_portfolio_state_stale,
)
from src.runtime.portfolio_state import PortfolioState


REFERENCE_TIME = datetime(2026, 5, 31, 12, 0, tzinfo=UTC)


def _valid_portfolio_state() -> PortfolioState:
    return PortfolioState(
        equity_start=100_000.0,
        equity_current=100_000.0,
        drawdown_percent=0.0,
        daily_loss_percent=0.0,
        governance_valid=True,
        source="trusted_test_snapshot",
        updated_at=REFERENCE_TIME.isoformat(),
    )


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
        updated_at=REFERENCE_TIME.isoformat(),
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
        updated_at=REFERENCE_TIME.isoformat(),
    )

    result = evaluate_kill_switch_for_portfolio_state(
        portfolio_state=state,
        vix=None,
        severe_anomaly_count=0,
    )

    assert result["kill_switch"] is True
    assert result["reasons"][0] == INVALID_PORTFOLIO_GOVERNANCE_REASON
    assert "portfolio_drawdown_limit" in result["reasons"]


def test_runtime_governance_approval_blocks_invalid_portfolio_state() -> None:
    state = PortfolioState.conservative_default("portfolio_state.json missing")

    approval = evaluate_runtime_governance_approval(
        portfolio_state=state,
        vix=None,
        severe_anomaly_count=0,
        now=REFERENCE_TIME,
    )

    assert approval.approved is False
    assert approval.blocked is True
    assert INVALID_GOVERNANCE_APPROVAL_REASON in approval.reasons
    assert KILL_SWITCH_APPROVAL_REASON in approval.reasons
    assert INVALID_PORTFOLIO_GOVERNANCE_REASON in approval.reasons
    assert approval.kill_switch["portfolio_governance_valid"] is False


def test_runtime_governance_approval_allows_valid_state_without_breach() -> None:
    state = _valid_portfolio_state()

    approval = evaluate_runtime_governance_approval(
        portfolio_state=state,
        vix=None,
        severe_anomaly_count=0,
        now=REFERENCE_TIME,
    )

    assert approval.approved is True
    assert approval.blocked is False
    assert approval.reasons == []
    assert approval.kill_switch["kill_switch"] is False


def test_runtime_governance_approval_blocks_valid_state_when_kill_switch_fires() -> None:
    state = PortfolioState(
        equity_start=100_000.0,
        equity_current=80_000.0,
        drawdown_percent=20.0,
        daily_loss_percent=0.0,
        governance_valid=True,
        source="trusted_test_snapshot",
        updated_at=REFERENCE_TIME.isoformat(),
    )

    approval = evaluate_runtime_governance_approval(
        portfolio_state=state,
        vix=None,
        severe_anomaly_count=0,
        now=REFERENCE_TIME,
    )

    assert approval.approved is False
    assert approval.blocked is True
    assert KILL_SWITCH_APPROVAL_REASON in approval.reasons
    assert "portfolio_drawdown_limit" in approval.reasons


def test_stale_portfolio_state_blocks_runtime_governance_approval() -> None:
    state = PortfolioState(
        equity_start=100_000.0,
        equity_current=100_000.0,
        drawdown_percent=0.0,
        daily_loss_percent=0.0,
        governance_valid=True,
        source="trusted_but_stale_snapshot",
        updated_at=(REFERENCE_TIME - timedelta(days=2)).isoformat(),
    )

    approval = evaluate_runtime_governance_approval(
        portfolio_state=state,
        vix=None,
        severe_anomaly_count=0,
        now=REFERENCE_TIME,
    )

    assert is_portfolio_state_stale(portfolio_state=state, now=REFERENCE_TIME) is True
    assert approval.approved is False
    assert approval.blocked is True
    assert STALE_PORTFOLIO_STATE_REASON in approval.reasons


def test_recent_portfolio_state_is_not_stale() -> None:
    state = PortfolioState(
        equity_start=100_000.0,
        equity_current=100_000.0,
        drawdown_percent=0.0,
        daily_loss_percent=0.0,
        governance_valid=True,
        source="trusted_recent_snapshot",
        updated_at=(REFERENCE_TIME - timedelta(hours=6)).isoformat(),
    )

    assert is_portfolio_state_stale(portfolio_state=state, now=REFERENCE_TIME) is False


def test_invalid_portfolio_state_timestamp_is_stale() -> None:
    state = PortfolioState(
        equity_start=100_000.0,
        equity_current=100_000.0,
        drawdown_percent=0.0,
        daily_loss_percent=0.0,
        governance_valid=True,
        source="trusted_snapshot_with_bad_timestamp",
        updated_at="not-a-valid-iso-timestamp",
    )

    approval = evaluate_runtime_governance_approval(
        portfolio_state=state,
        vix=None,
        severe_anomaly_count=0,
        now=REFERENCE_TIME,
    )

    assert is_portfolio_state_stale(portfolio_state=state, now=REFERENCE_TIME) is True
    assert approval.approved is False
    assert STALE_PORTFOLIO_STATE_REASON in approval.reasons


def test_actionable_signal_provider_fetch_failure_blocks_runtime_approval() -> None:
    approval = evaluate_runtime_governance_approval(
        portfolio_state=_valid_portfolio_state(),
        vix=None,
        severe_anomaly_count=0,
        now=REFERENCE_TIME,
        actionable_signal=True,
        provider_fetch_errors=["Polygon latest bars fetch failed for AAPL"],
    )

    assert approval.approved is False
    assert approval.blocked is True
    assert DATA_PROVIDER_FETCH_FAILURE_REASON in approval.reasons
    assert approval.provider_fetch_errors == ["Polygon latest bars fetch failed for AAPL"]
    assert approval.actionable_signal is True
    assert approval.to_dict()["provider_fetch_errors"] == ["Polygon latest bars fetch failed for AAPL"]


def test_non_actionable_provider_fetch_failure_is_recorded_but_does_not_block() -> None:
    approval = evaluate_runtime_governance_approval(
        portfolio_state=_valid_portfolio_state(),
        vix=None,
        severe_anomaly_count=0,
        now=REFERENCE_TIME,
        actionable_signal=False,
        provider_fetch_errors=["Polygon latest bars fetch failed for inactive symbol"],
    )

    assert approval.approved is True
    assert approval.blocked is False
    assert DATA_PROVIDER_FETCH_FAILURE_REASON not in approval.reasons
    assert approval.provider_fetch_errors == ["Polygon latest bars fetch failed for inactive symbol"]
