from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.execution_intelligence import (  # noqa: E402
    ExecutionInput,
    build_execution_plan,
)


def test_high_quality_execution_plan_generated_for_stable_conditions():
    result = build_execution_plan(
        ExecutionInput(
            symbol="NVDA",
            current_price=120.0,
            sma50=115.0,
            atr14=3.0,
            relative_volume=1.6,
            intraday_range_percent=1.8,
            liquidity_score=82,
            volatility_stability_score=79,
            failure_risk_score=18,
            event_risk_active=False,
            spread_percent=0.04,
            risk_tier="tier_1",
        )
    )

    assert result.execution_state == "execution_quality_high"
    assert result.entry_quality_score >= 75
    assert result.position_size_multiplier >= 0.75
    assert result.stop_distance_atr >= 1.0


def test_execution_avoided_when_conditions_are_fragile():
    result = build_execution_plan(
        ExecutionInput(
            symbol="SMCI",
            current_price=120.0,
            sma50=95.0,
            atr14=9.0,
            relative_volume=0.7,
            intraday_range_percent=6.1,
            liquidity_score=28,
            volatility_stability_score=31,
            failure_risk_score=81,
            event_risk_active=True,
            spread_percent=0.35,
            risk_tier="tier_2",
        )
    )

    assert result.execution_state in {
        "avoid_execution",
        "do_not_execute",
    }
    assert result.position_size_multiplier <= 0.25
    assert "event_risk_active" in result.warnings
