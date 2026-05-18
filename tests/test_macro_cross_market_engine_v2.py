from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.macro_cross_market_engine_v2 import (  # noqa: E402
    MacroCrossMarketInput,
    evaluate_macro_cross_market,
)


def test_macro_risk_off_detected_under_credit_and_rate_stress():
    result = evaluate_macro_cross_market(
        MacroCrossMarketInput(
            ten_year_yield_change_20d_bps=48,
            two_year_yield_change_20d_bps=39,
            real_yield_change_20d_bps=31,
            credit_spread_change_20d_bps=52,
            dxy_return_20d=0.05,
            oil_return_20d=0.15,
            gold_return_20d=0.12,
            spy_return_20d=-0.04,
            fx_stress_score=81,
            yield_curve_slope_bps=-92,
        )
    )

    assert result.macro_regime == "macro_risk_off_stress"
    assert result.macro_risk_score < 30
    assert "credit_spread_stress" in result.warnings
    assert "dollar_shock" in result.warnings


def test_macro_supportive_environment_detected_when_conditions_ease():
    result = evaluate_macro_cross_market(
        MacroCrossMarketInput(
            ten_year_yield_change_20d_bps=-28,
            two_year_yield_change_20d_bps=-12,
            real_yield_change_20d_bps=-22,
            credit_spread_change_20d_bps=-18,
            dxy_return_20d=-0.03,
            oil_return_20d=-0.09,
            gold_return_20d=0.01,
            spy_return_20d=0.08,
            fx_stress_score=24,
            yield_curve_slope_bps=35,
        )
    )

    assert result.macro_regime in {
        "macro_constructive",
        "macro_risk_supportive",
    }
    assert result.macro_risk_score >= 60
    assert "credit_spreads_easing" in result.confirmations
