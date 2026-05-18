from src.memory.anomaly_memory import detect_market_anomalies
from src.memory.pattern_memory import (
    classify_pattern_strength,
    detect_repeating_patterns,
)
from src.memory.regime_memory import (
    find_similar_regimes,
    summarize_regime_memory,
)
from src.memory.trade_memory import analyze_trade_memory


def test_regime_memory():
    matches = find_similar_regimes(
        current_regime={
            "market_health_score": 80,
            "regime": "Bullish",
        },
        historical_regimes=[
            {
                "market_health_score": 85,
                "regime": "Bullish",
                "forward_return_percent": 5,
            },
            {
                "market_health_score": 50,
                "regime": "Neutral",
                "forward_return_percent": -2,
            },
        ],
    )

    summary = summarize_regime_memory(matches)

    assert summary["matches"] >= 1
    assert summary["memory_signal"] == "Historically Positive"


def test_pattern_memory():
    result = detect_repeating_patterns(
        [
            {"pattern": "Breakout"},
            {"pattern": "Breakout"},
            {"pattern": "Pullback"},
        ]
    )

    assert result["pattern_count"] >= 2
    assert classify_pattern_strength(12) == "Strong Pattern"


def test_trade_memory():
    result = analyze_trade_memory(
        [
            {"setup": "Momentum", "pnl_percent": 10},
            {"setup": "Momentum", "pnl_percent": 5},
            {"setup": "Mean Reversion", "pnl_percent": -3},
        ]
    )

    assert result["best_setup"][0] == "Momentum"


def test_anomaly_memory():
    result = detect_market_anomalies(
        [
            {"anomaly": True, "severity": "critical"},
            {"anomaly": True, "severity": "high"},
            {"anomaly": False, "severity": "low"},
        ]
    )

    assert result["anomaly_count"] == 2
    assert result["classification"] in {
        "Watchlist Environment",
        "Elevated Instability",
    }
