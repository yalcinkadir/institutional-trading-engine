from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.regime_transition import (  # noqa: E402
    RegimeTransitionInput,
    evaluate_regime_transition,
)


def test_risk_on_strengthening_detected_when_market_conditions_improve():
    result = evaluate_regime_transition(
        RegimeTransitionInput(
            current_market_health_score=82,
            previous_market_health_score=68,
            current_breadth_percent=78,
            previous_breadth_percent=61,
            current_vix=13,
            previous_vix=18,
            current_cross_asset_risk_score=85,
            previous_cross_asset_risk_score=66,
            failed_breakout_rate=0.14,
            opportunity_density="high",
        )
    )

    assert result.transition_state == "risk_on_strengthening"
    assert result.transition_score >= 75
    assert "breadth_expansion" in result.confirmations
    assert "volatility_compression" in result.confirmations


def test_risk_off_acceleration_detected_when_conditions_break_down():
    result = evaluate_regime_transition(
        RegimeTransitionInput(
            current_market_health_score=28,
            previous_market_health_score=55,
            current_breadth_percent=31,
            previous_breadth_percent=62,
            current_vix=31,
            previous_vix=18,
            current_cross_asset_risk_score=24,
            previous_cross_asset_risk_score=58,
            failed_breakout_rate=0.67,
            opportunity_density="low",
        )
    )

    assert result.transition_state == "risk_off_acceleration"
    assert result.transition_score < 30
    assert "failed_breakout_transition_pressure" in result.warnings
    assert "volatility_expansion" in result.warnings
