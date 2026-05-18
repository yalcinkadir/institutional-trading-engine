from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.failure_pattern_engine import (  # noqa: E402
    FailurePatternInput,
    evaluate_failure_patterns,
)


def test_extreme_failure_risk_detected_when_multiple_fragile_conditions_align():
    result = evaluate_failure_patterns(
        FailurePatternInput(
            setup_score=84,
            asymmetry_score=0.28,
            breadth_score=38,
            liquidity_stability_score=31,
            transition_score=34,
            vix=29,
            failed_breakout_rate=0.58,
            mega_cap_dependency_percent=63,
            semiconductor_leadership=False,
            equal_weight_confirming=False,
            volatility_expansion=True,
            event_risk_active=True,
            asset_extended_from_sma50_percent=15,
        )
    )

    assert result.failure_risk_state == "extreme_failure_risk"
    assert result.failure_probability_score >= 70
    assert "extended_breakout_trap" in result.detected_patterns
    assert "narrow_leadership_fragility" in result.detected_patterns


def test_contained_failure_risk_detected_when_market_quality_is_healthy():
    result = evaluate_failure_patterns(
        FailurePatternInput(
            setup_score=82,
            asymmetry_score=0.74,
            breadth_score=79,
            liquidity_stability_score=81,
            transition_score=76,
            vix=14,
            failed_breakout_rate=0.14,
            mega_cap_dependency_percent=29,
            semiconductor_leadership=True,
            equal_weight_confirming=True,
            volatility_expansion=False,
            event_risk_active=False,
            asset_extended_from_sma50_percent=4,
        )
    )

    assert result.failure_risk_state == "contained_failure_risk"
    assert result.failure_probability_score < 30
