from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.liquidity_volatility_engine import (  # noqa: E402
    LiquidityVolatilityInput,
    evaluate_liquidity_volatility_environment,
)


def test_stable_liquidity_environment_detected_when_conditions_are_supportive():
    result = evaluate_liquidity_volatility_environment(
        LiquidityVolatilityInput(
            vix=13,
            previous_vix=17,
            vvix=82,
            atr_percent=0.018,
            previous_atr_percent=0.021,
            average_gap_percent=0.7,
            liquidity_score=84,
            spread_stress_score=18,
            failed_breakout_rate=0.16,
            volatility_of_volatility=0.25,
        )
    )

    assert result.environment == "stable_liquidity_risk_supportive"
    assert result.stability_score >= 75
    assert "low_volatility_environment" in result.confirmations
    assert "liquidity_supportive" in result.confirmations


def test_volatility_liquidity_crisis_detected_when_stress_clusters_expand():
    result = evaluate_liquidity_volatility_environment(
        LiquidityVolatilityInput(
            vix=36,
            previous_vix=21,
            vvix=148,
            atr_percent=0.062,
            previous_atr_percent=0.031,
            average_gap_percent=4.2,
            liquidity_score=28,
            spread_stress_score=81,
            failed_breakout_rate=0.73,
            volatility_of_volatility=0.88,
        )
    )

    assert result.environment == "volatility_liquidity_crisis"
    assert result.stability_score < 30
    assert "volatility_expansion" in result.warnings
    assert "liquidity_deterioration" in result.warnings
