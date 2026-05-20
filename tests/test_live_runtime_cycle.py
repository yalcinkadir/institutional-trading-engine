from src.runtime.live_runtime_cycle import live_runtime_cycle


def test_live_runtime_cycle_runs():
    metrics_map = {
        "SPY": {
            "rsi14": 62,
        },
        "QQQ": {
            "rsi14": 66,
        },
        "VIX": {
            "close": 18,
        },
    }

    result = live_runtime_cycle.run_cycle(metrics_map)

    assert result["decision"]["market_regime_score"] == 64.0
    assert result["decision"]["volatility_level"] == 18
