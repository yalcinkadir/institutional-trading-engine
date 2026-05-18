from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.scenario_engine import ScenarioContext, ScenarioShock, ScenarioType, evaluate_scenarios  # noqa: E402


def test_high_scenario_risk_detected_under_fragile_conditions():
    result = evaluate_scenarios(
        ScenarioContext(28, 31, 36, 24, 78, 1.8, 82, 74),
        (
            ScenarioShock(ScenarioType.HOT_CPI, 1.0),
            ScenarioShock(ScenarioType.VIX_SPIKE, 0.9),
            ScenarioShock(ScenarioType.CREDIT_STRESS, 0.9),
        ),
    )

    assert result.scenario_risk_state == "scenario_risk_high"
    assert result.aggregate_impact_score >= 50


def test_contained_scenario_risk_under_supportive_conditions():
    result = evaluate_scenarios(
        ScenarioContext(78, 81, 76, 72, 18, 0.9, 34, 16),
        (
            ScenarioShock(ScenarioType.HOT_CPI, 0.3),
            ScenarioShock(ScenarioType.VIX_SPIKE, 0.2),
        ),
    )

    assert result.scenario_risk_state == "scenario_risk_contained"
    assert result.aggregate_impact_score < 30
