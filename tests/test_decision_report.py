from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from reporting.decision_report import build_decision_report  # noqa: E402
from src.runtime.portfolio_state import PortfolioState  # noqa: E402


class _PortfolioStateStore:
    def __init__(self, *, governance_valid: bool = True, drawdown_percent: float = 0.0):
        self.state = PortfolioState(
            equity_start=100000.0,
            equity_current=100000.0,
            drawdown_percent=drawdown_percent,
            daily_loss_percent=0.0,
            open_positions=[],
            source="test_portfolio_state_store",
            warnings=[] if governance_valid else ["invalid_test_state"],
            governance_valid=governance_valid,
        )

    def load(self) -> PortfolioState:
        return self.state


def _live_bullish_market_regime():
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


def test_decision_report_contains_ranked_opportunities_and_market_state():
    market_regime = _live_bullish_market_regime()

    screener = {
        "watchlist": ["QQQ", "MSFT", "NVDA", "GLD"],
    }

    report = build_decision_report(
        market_regime,
        screener,
        portfolio_state_store=_PortfolioStateStore(),
    )

    assert report["market_state"] == "low_vol_bull"
    assert report["report_governance"]["status"] == "PASSED"
    assert report["approved_count"] >= 1
    assert len(report["allowed_setups"]) >= 1
    assert len(report["decisions"]) >= 1

    top = report["decisions"][0]

    assert "symbol" in top
    assert "decision" in top
    assert "risk_tier" in top
    assert "asymmetry_score" in top


def test_decision_report_detects_panic_dislocation_environment():
    market_regime = {
        "regime": "Neutral",
        "market_health_score": 42,
        "data_status": "LIVE",
        "breadth": {
            "breadth_percent": 28,
            "above_sma50": 4,
            "universe_size": 16,
        },
        "symbols": {
            "VIX": {
                "close": 41,
            }
        },
    }

    screener = {
        "watchlist": ["QQQ", "NVDA"],
    }

    report = build_decision_report(
        market_regime,
        screener,
        portfolio_state_store=_PortfolioStateStore(),
    )

    assert report["market_state"] == "panic_dislocation"
    assert report["report_governance"]["status"] == "BLOCKED"
    assert "extreme_volatility" in report["hard_overrides"]
    assert "reversal_asymmetry" in report["allowed_setups"]


def test_decision_report_reduces_confidence_when_fallback_active():
    market_regime = {
        "regime": "Bullish",
        "market_health_score": "DATA_UNAVAILABLE",
        "data_status": "FALLBACK",
        "breadth": {},
        "symbols": {},
    }

    screener = {
        "watchlist": ["SPY"],
    }

    report = build_decision_report(
        market_regime,
        screener,
        portfolio_state_store=_PortfolioStateStore(),
    )

    assert len(report["decisions"]) == 1
    assert report["decisions"][0]["data_confidence"] == 0.65
    assert report["data_quality_note"]


def test_decision_report_blocks_all_risk_when_portfolio_governance_invalid():
    report = build_decision_report(
        _live_bullish_market_regime(),
        {"watchlist": ["QQQ", "MSFT"]},
        portfolio_state_store=_PortfolioStateStore(governance_valid=False),
    )

    assert report["report_governance"]["status"] == "BLOCKED"
    assert report["report_governance"]["portfolio_governance_valid"] is False
    assert "invalid_portfolio_governance_state" in report["hard_overrides"]
    assert report["approved_count"] == 0
    assert report["portfolio_heat_limit"] == 0.0
    assert all(item["decision"] == "blocked" for item in report["decisions"])
    assert all(item["position_size_multiplier"] == 0.0 for item in report["decisions"])
