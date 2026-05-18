"""
Macro Cross-Market Engine v2.

This module evaluates macro pressure across rates, credit, FX, commodities and
risk assets. It extends the simpler cross-asset layer by focusing on macro
transmission channels:

- yield curve pressure
- real yield pressure
- credit spread stress
- dollar shock
- oil/inflation pressure
- gold defensive demand
- FX stress

The goal is not macro forecasting. The goal is identifying when macro conditions
support risk-taking or demand defensive risk posture.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MacroCrossMarketInput:
    ten_year_yield_change_20d_bps: float
    two_year_yield_change_20d_bps: float
    real_yield_change_20d_bps: float
    credit_spread_change_20d_bps: float
    dxy_return_20d: float
    oil_return_20d: float
    gold_return_20d: float
    spy_return_20d: float
    fx_stress_score: float
    yield_curve_slope_bps: float


@dataclass(frozen=True)
class MacroCrossMarketAssessment:
    macro_regime: str
    macro_risk_score: int
    risk_action: str
    warnings: tuple[str, ...]
    confirmations: tuple[str, ...]


def evaluate_macro_cross_market(data: MacroCrossMarketInput) -> MacroCrossMarketAssessment:
    warnings: list[str] = []
    confirmations: list[str] = []
    score = 50

    if data.real_yield_change_20d_bps >= 25:
        score -= 18
        warnings.append("real_yield_pressure")
    elif data.real_yield_change_20d_bps <= -15:
        score += 12
        confirmations.append("real_yields_easing")

    if data.ten_year_yield_change_20d_bps >= 35:
        score -= 12
        warnings.append("long_rate_shock")
    elif data.ten_year_yield_change_20d_bps <= -25:
        score += 8
        confirmations.append("long_rates_easing")

    if data.two_year_yield_change_20d_bps >= 30:
        score -= 10
        warnings.append("front_end_rate_pressure")

    if data.yield_curve_slope_bps <= -75:
        score -= 8
        warnings.append("deep_curve_inversion")
    elif data.yield_curve_slope_bps >= 25:
        score += 6
        confirmations.append("curve_normalization_supportive")

    if data.credit_spread_change_20d_bps >= 35:
        score -= 22
        warnings.append("credit_spread_stress")
    elif data.credit_spread_change_20d_bps <= -15:
        score += 14
        confirmations.append("credit_spreads_easing")

    if data.dxy_return_20d >= 0.035:
        score -= 15
        warnings.append("dollar_shock")
    elif data.dxy_return_20d <= -0.02:
        score += 8
        confirmations.append("dollar_pressure_easing")

    if data.oil_return_20d >= 0.12:
        score -= 10
        warnings.append("oil_inflation_pressure")
    elif data.oil_return_20d <= -0.08:
        score += 5
        confirmations.append("oil_pressure_easing")

    gold_vs_spy = data.gold_return_20d - data.spy_return_20d
    if gold_vs_spy >= 0.06:
        score -= 10
        warnings.append("defensive_gold_demand")
    elif gold_vs_spy <= -0.04:
        score += 6
        confirmations.append("risk_assets_outperform_gold")

    if data.fx_stress_score >= 70:
        score -= 12
        warnings.append("fx_stress")
    elif data.fx_stress_score <= 30:
        score += 5
        confirmations.append("fx_stress_contained")

    score = max(0, min(100, score))

    if score >= 75:
        macro_regime = "macro_risk_supportive"
        risk_action = "allow_risk_expansion_if_market_internals_confirm"
    elif score >= 60:
        macro_regime = "macro_constructive"
        risk_action = "maintain_selective_risk"
    elif score >= 45:
        macro_regime = "macro_neutral_mixed"
        risk_action = "avoid_macro_dependent_overexposure"
    elif score >= 30:
        macro_regime = "macro_pressure_building"
        risk_action = "reduce_cyclical_and_high_beta_risk"
    else:
        macro_regime = "macro_risk_off_stress"
        risk_action = "prioritize_capital_preservation_and_defensive_exposure"

    return MacroCrossMarketAssessment(
        macro_regime=macro_regime,
        macro_risk_score=score,
        risk_action=risk_action,
        warnings=tuple(dict.fromkeys(warnings)),
        confirmations=tuple(dict.fromkeys(confirmations)),
    )
