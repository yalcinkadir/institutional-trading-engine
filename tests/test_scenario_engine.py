from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.scenario_engine import (  # noqa: E402
    ScenarioAssessment,
    ScenarioContext,
    ScenarioShock,
    ScenarioType,
    evaluate_scenarios,
)


def test_extreme_scenario_risk_detected_under_fragile_conditions():
    result: ScenarioAssessment = evaluate_scenarios(
        ScenarioContext(
            current_macro_risk_score=28,
            liquidity_stability_score=31,
            breadth_score=36,
            sector_rotation_offensive_score=24,
            failure_risk_score=78,
            portfolio_beta=1.8,
            portfolio_correlation_score=82,
            event_risk_score=74,
        ),
        shocks=(
            ScenarioShock(ScenarioType.HOT_CPI, 1.0),
            ScenarioShock(ScenarioType.VIX_SPIKE, 0.9),
            ScenarioShock(ScenarioType.CREDIT_STRESS, 0.9),
        ),
    )

    assert result.scenario_risk_state == "scenario_risk_extreme"
    assert result.aggregate_impact_score >= 70
    assert any("scenario_pressure" in item for item in result.warnings)


def test_contained_scenario_risk_under_supportive_conditions():
    result: ScenarioAssessment = evaluate_scenarios(
        ScenarioContext(
            current_macro_risk_score=78,
            liquidity_stability_score=81,
            breadth_score=76,
            sector_rotation_offensive_score=72,
            failure_risk_score=18,
            portfolio_beta=0.9,
            portfolio_correlation_score=34,
            event_risk_score=16,
        ),
        shocks=(
            ScenarioShock(ScenarioType.HOT_CPI, 0.3),
            ScenarioShock(ScenarioType.VIX_SPIKE, 0.2),
        ),
    )

    assert result.scenario_risk_state == "scenario_risk_contained"
    assert result.aggregate_impact_score < 30
