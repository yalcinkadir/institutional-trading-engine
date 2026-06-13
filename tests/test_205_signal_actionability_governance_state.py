from __future__ import annotations

from src.reporting.decision_report import build_decision_report
from src.runtime.portfolio_state import PortfolioState
from src.signals.signal_generator import build_signals


class _PortfolioStateStore:
    def __init__(self, state: PortfolioState) -> None:
        self._state = state

    def load(self) -> PortfolioState:
        return self._state


def _bullish_market_regime() -> dict:
    return {
        "regime": "Bullish",
        "market_health_score": 82,
        "data_status": "LIVE",
        "breadth": {
            "breadth_percent": 71,
            "above_sma50": 11,
            "universe_size": 16,
        },
        "symbols": {
            "VIX": {
                "close": 14,
            }
        },
    }


def _screener() -> dict:
    return {
        "watchlist": ["QQQ", "MSFT", "NVDA", "GLD"],
    }


def _scanner_metrics_for(report: dict) -> dict[str, dict]:
    metrics: dict[str, dict] = {}
    for index, item in enumerate(report["decisions"]):
        symbol = item["symbol"]
        close = 100.0 + (index * 10.0)
        metrics[symbol] = {
            "close": close,
            "atr14": 2.0,
            "atr_pct": 2.0,
            "source": "unit_test_primary_feed",
            "source_timestamp": "2026-06-13T00:00:00+00:00",
            "fallback_level": "primary",
            "data_status": "OK",
        }
    return metrics


def test_205_default_repo_portfolio_state_allows_paper_observation_actionable_candidates() -> None:
    report = build_decision_report(_bullish_market_regime(), _screener())

    assert report["report_governance"]["status"] == "PASSED"
    assert report["report_governance"]["portfolio_governance_valid"] is True
    assert report["report_governance"]["live_trading_authorized"] is False
    assert report["report_governance"]["broker_execution_mode"] == "paper_only"
    assert "invalid_portfolio_governance_state" not in report["hard_overrides"]
    assert report["approved_count"] > 0

    signals = build_signals(
        decision_report=report,
        scanner_metrics_map=_scanner_metrics_for(report),
        market_regime="Bullish",
    )

    actionable = [signal for signal in signals if signal.action == "BUY_WATCH"]
    assert actionable, "valid paper-observation governance must allow executable BUY_WATCH signals"
    assert all(signal.entry_trigger is not None for signal in actionable)
    assert all(signal.stop_loss is not None for signal in actionable)
    assert all(signal.target_1 is not None for signal in actionable)


def test_205_invalid_portfolio_governance_still_fails_closed() -> None:
    invalid_state = PortfolioState(
        equity_start=100000.0,
        equity_current=100000.0,
        drawdown_percent=0.0,
        daily_loss_percent=0.0,
        open_positions=[],
        source="invalid_test_portfolio_state",
        warnings=["invalid test state"],
        governance_valid=False,
    )

    report = build_decision_report(
        _bullish_market_regime(),
        _screener(),
        portfolio_state_store=_PortfolioStateStore(invalid_state),
    )

    assert report["report_governance"]["status"] == "BLOCKED"
    assert report["report_governance"]["portfolio_governance_valid"] is False
    assert "invalid_portfolio_governance_state" in report["hard_overrides"]
    assert report["approved_count"] == 0
    assert all(item["decision"] == "blocked" for item in report["decisions"])
    assert all(item["position_size_multiplier"] == 0.0 for item in report["decisions"])
