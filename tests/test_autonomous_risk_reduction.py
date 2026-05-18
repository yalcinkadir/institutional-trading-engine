from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.autonomous_risk_reduction import (  # noqa: E402
    RiskReductionInput,
    build_risk_reduction_policy,
)


def test_extreme_risk_reduction_triggered_when_multiple_layers_break_down():
    result = build_risk_reduction_policy(
        RiskReductionInput(
            transition_score=24,
            liquidity_stability_score=28,
            event_risk_score=74,
            scenario_impact_score=81,
            failure_probability_score=79,
            breadth_score=33,
            portfolio_risk_score=72,
            macro_risk_score=29,
            current_portfolio_heat=1.35,
            max_portfolio_heat=1.0,
        )
    )

    assert result.risk_state == "risk_reduction_extreme"
    assert result.exposure_multiplier == 0.0
    assert result.allow_new_aggressive_entries is False
    assert "portfolio_heat_exceeded" in result.triggered_controls


def test_normal_risk_allowed_when_conditions_are_stable():
    result = build_risk_reduction_policy(
        RiskReductionInput(
            transition_score=82,
            liquidity_stability_score=84,
            event_risk_score=18,
            scenario_impact_score=16,
            failure_probability_score=14,
            breadth_score=79,
            portfolio_risk_score=22,
            macro_risk_score=77,
            current_portfolio_heat=0.45,
            max_portfolio_heat=1.0,
        )
    )

    assert result.risk_state == "normal_risk_allowed"
    assert result.exposure_multiplier == 1.0
    assert result.allow_new_aggressive_entries is True
