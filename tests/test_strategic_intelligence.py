from src.strategy.global_risk_monitor import evaluate_global_risk
from src.strategy.intermarket_analysis import analyze_intermarket_signals
from src.strategy.macro_regime import classify_macro_regime
from src.strategy.sector_rotation import detect_sector_rotation


def test_macro_regime():
    result = classify_macro_regime(
        dollar_trend="falling",
        yields_trend="falling",
        gold_trend="neutral",
        equity_regime="Bullish",
    )

    assert result["macro_score"] >= 60
    assert result["macro_regime"] == "Macro Risk-On"


def test_intermarket_analysis():
    result = analyze_intermarket_signals(
        spy_trend="bullish",
        bonds_trend="neutral",
        dollar_trend="bearish",
        gold_trend="neutral",
    )

    assert result["classification"] in {
        "Risk-On Alignment",
        "Mixed Alignment",
    }


def test_sector_rotation():
    result = detect_sector_rotation(
        {
            "Technology": 4.2,
            "Healthcare": 1.1,
            "Utilities": -0.4,
            "Energy": -1.2,
        }
    )

    assert result["rotation_type"] == "Growth Rotation"
    assert len(result["leaders"]) == 3


def test_global_risk_monitor():
    result = evaluate_global_risk(
        vix=28,
        credit_spreads="widening",
        geopolitical_risk="high",
    )

    assert result["global_risk_score"] < 75
    assert result["classification"] in {
        "Elevated Risk",
        "Global Stress",
    }
