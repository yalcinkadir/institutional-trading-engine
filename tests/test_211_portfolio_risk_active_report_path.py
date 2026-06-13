from __future__ import annotations

from src.reporting.decision_report import build_decision_report
from src.runtime.portfolio_state import PortfolioState
from src.signals.signal_generator import build_signals


class _PortfolioStateStore:
    def load(self) -> PortfolioState:
        return PortfolioState(
            date="2026-06-13",
            daily_loss_percent=0.0,
            portfolio_heat=0.0,
            open_positions=0,
            consecutive_losses=0,
            data_quality="OK",
        )


def _market_regime() -> dict:
    return {
        "regime": "Bullish",
        "market_health_score": 82,
        "data_status": "LIVE",
        "breadth": {"breadth_percent": 72.0},
        "symbols": {
            "VIX": {"close": 18.0},
        },
    }


def _screener() -> dict:
    return {
        "watchlist": ["NVDA"],
        "scanner_metrics": {
            "NVDA": {
                "trend_score": 0.92,
                "volume_score": 0.88,
                "volatility_score": 0.74,
                "setup_quality_score": 0.91,
                "liquidity_score": 0.93,
            }
        },
    }


def _scanner_metrics(*, include_returns: bool) -> dict:
    metrics = {
        "close": 225.0,
        "high": 226.0,
        "low": 218.0,
        "atr14": 8.0,
        "atr_pct": 3.6,
        "sma20": 220.0,
        "sma50": 210.0,
        "source": "polygon",
        "source_timestamp": "2026-06-12T14:30:00+00:00",
        "fallback_level": "primary",
        "data_status": "OK",
        "sector": "semiconductors",
    }
    if include_returns:
        metrics["returns_20d"] = tuple(float(i) / 100 for i in range(1, 21))
    return {"NVDA": metrics}


def test_211_decision_report_marks_portfolio_risk_required_on_active_path() -> None:
    report = build_decision_report(
        _market_regime(),
        _screener(),
        portfolio_state_store=_PortfolioStateStore(),
    )

    assert report["portfolio_risk_required"] is True
    assert report["portfolio_risk_policy"] == "required_for_actionable_signals"
    assert report["live_trading_authorized"] is False
    assert report["broker_execution_mode"] == "paper_only"


def test_211_active_report_path_fails_closed_when_portfolio_context_missing() -> None:
    report = build_decision_report(
        _market_regime(),
        _screener(),
        portfolio_state_store=_PortfolioStateStore(),
    )

    signals = build_signals(report, _scanner_metrics(include_returns=False), "Bullish")

    signal = signals[0]
    assert signal.action == "NO_TRADE"
    assert signal.portfolio_risk_status == "BLOCKED"
    assert signal.portfolio_risk_block_reason == "portfolio_risk_context_missing"
    assert "portfolio_risk_context_missing" in signal.notes
