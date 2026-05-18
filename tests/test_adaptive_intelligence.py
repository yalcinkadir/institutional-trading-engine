from src.analytics.adaptive_weighting import adjust_factor_weights
from src.analytics.alpha_tracker import calculate_alpha, summarize_alpha
from src.analytics.regime_performance import analyze_regime_performance
from src.analytics.signal_quality import evaluate_signal_quality


def test_alpha_tracking():
    alpha = calculate_alpha(15, 10)

    assert alpha["alpha_percent"] == 5
    assert alpha["quality"] == "Strong Alpha"


def test_alpha_summary():
    summary = summarize_alpha(
        [
            {"alpha_percent": 5},
            {"alpha_percent": -2},
            {"alpha_percent": 3},
        ]
    )

    assert summary["signals"] == 3
    assert summary["positive_alpha_rate"] > 60


def test_regime_performance_analysis():
    trades = [
        {"market_regime": "Bullish", "pnl_percent": 10},
        {"market_regime": "Bullish", "pnl_percent": -5},
        {"market_regime": "Neutral", "pnl_percent": 2},
    ]

    analysis = analyze_regime_performance(trades)

    assert "Bullish" in analysis
    assert analysis["Bullish"]["trades"] == 2


def test_signal_quality():
    result = evaluate_signal_quality(
        [
            {"pnl_percent": 10},
            {"pnl_percent": 5},
            {"pnl_percent": -2},
        ]
    )

    assert result["signals"] == 3
    assert result["quality_score"] > 50


def test_adaptive_weighting():
    weights = {
        "trend": 0.3,
        "relative_strength": 0.3,
        "volume": 0.2,
        "risk": 0.2,
    }

    performance = {
        "trend": 10,
        "relative_strength": 15,
        "volume": -5,
        "risk": 5,
    }

    adjusted = adjust_factor_weights(weights, performance)

    assert round(sum(adjusted.values()), 2) == 1.0
    assert adjusted["relative_strength"] >= adjusted["volume"]
