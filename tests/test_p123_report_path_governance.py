from __future__ import annotations

from src.runtime.portfolio_state import PortfolioState


class _PortfolioStateStore:
    def __init__(self, state: PortfolioState) -> None:
        self._state = state

    def load(self) -> PortfolioState:
        return self._state


def _portfolio_state(
    *,
    drawdown_percent: float = 0.0,
    daily_loss_percent: float = 0.0,
    governance_valid: bool = True,
    source: str = "p123_test_portfolio_state",
) -> PortfolioState:
    return PortfolioState(
        equity_start=100000.0,
        equity_current=100000.0,
        drawdown_percent=drawdown_percent,
        daily_loss_percent=daily_loss_percent,
        open_positions=[],
        source=source,
        governance_valid=governance_valid,
    )


def _market_regime() -> dict:
    return {
        "regime": "Bullish",
        "market_health_score": 78,
        "data_status": "LIVE",
        "symbols": {
            "SPY": {
                "close": 500.0,
                "sma50": 490.0,
                "sma200": 460.0,
                "above_sma50": True,
                "above_sma200": True,
                "atr14": 5.5,
                "avg_volume_20": 70_000_000,
            },
            "QQQ": {
                "close": 420.0,
                "sma50": 410.0,
                "sma200": 380.0,
                "above_sma50": True,
                "above_sma200": True,
                "atr14": 6.2,
                "avg_volume_20": 55_000_000,
            },
            "VIX": {
                "close": 16.0,
                "sma50": None,
                "sma200": None,
                "above_sma50": False,
                "above_sma200": False,
                "atr14": None,
            },
        },
        "breadth": {
            "universe_size": 100,
            "above_sma50": 68,
            "breadth_percent": 68.0,
        },
        "focus_areas": [],
        "notes": [],
        "errors": [],
    }


def _screener() -> dict:
    return {
        "title": "P123 Test Watchlist",
        "watchlist": ["NVDA", "MSFT", "AAPL"],
        "objectives": [],
        "warnings": [],
    }


def _build_report_for_state(state: PortfolioState) -> dict:
    from src.reporting.decision_report import build_decision_report

    return build_decision_report(
        _market_regime(),
        _screener(),
        portfolio_state_store=_PortfolioStateStore(state),
    )


def _assert_all_decisions_blocked(report: dict) -> None:
    assert report["report_governance"]["blocked"] is True
    assert report["report_governance"]["status"] == "BLOCKED"
    assert report["portfolio_heat_limit"] == 0.0
    assert report["approved_count"] == 0
    assert report["decisions"], "test requires at least one decision candidate"

    for decision in report["decisions"]:
        assert decision["decision"] == "blocked"
        assert decision["risk_tier"] == "no_trade"
        assert decision["position_size_multiplier"] == 0.0
        assert "report_governance_blocked_before_risk_approval" in decision["notes"]


def test_p123_valid_portfolio_state_allows_report_path_risk_approval() -> None:
    report = _build_report_for_state(_portfolio_state())

    assert report["report_governance"]["blocked"] is False
    assert report["report_governance"]["status"] == "PASSED"
    assert report["approved_count"] > 0
    assert report["portfolio_heat_limit"] > 0.0


def test_p123_invalid_portfolio_state_fails_closed_on_report_path() -> None:
    report = _build_report_for_state(
        _portfolio_state(
            governance_valid=False,
            source="invalid_portfolio_state_fail_closed",
        )
    )

    _assert_all_decisions_blocked(report)
    assert "invalid_portfolio_governance_state" in report["hard_overrides"]
    assert report["report_governance"]["portfolio_governance_valid"] is False


def test_p123_drawdown_breach_blocks_scheduled_report_decisions() -> None:
    report = _build_report_for_state(_portfolio_state(drawdown_percent=20.0))

    _assert_all_decisions_blocked(report)
    assert "portfolio_drawdown_limit" in report["hard_overrides"]


def test_p123_daily_loss_breach_blocks_scheduled_report_decisions() -> None:
    report = _build_report_for_state(_portfolio_state(daily_loss_percent=5.0))

    _assert_all_decisions_blocked(report)
    assert "max_daily_loss_breached" in report["hard_overrides"]
