from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from reporting.decision_report import build_decision_report  # noqa: E402


def test_decision_report_contains_ranked_opportunities_and_market_state():
    market_regime = {
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

    screener = {
        "watchlist": ["QQQ", "MSFT", "NVDA", "GLD"],
    }

    report = build_decision_report(market_regime, screener)

    assert report["market_state"] == "low_vol_bull"
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

    report = build_decision_report(market_regime, screener)

    assert report["market_state"] == "panic_dislocation"
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

    report = build_decision_report(market_regime, screener)

    assert len(report["decisions"]) == 1
    assert report["decisions"][0]["data_confidence"] == 0.65
    assert report["data_quality_note"]
