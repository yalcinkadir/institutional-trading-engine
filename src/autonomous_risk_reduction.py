"""
Autonomous Risk Reduction Engine.

This module acts as a risk governor. It aggregates stress signals from multiple
independent layers and converts them into an explicit exposure policy.

The purpose is not to place trades automatically. The purpose is to prevent the
Decision Engine from increasing risk when multiple quality layers deteriorate.

Inputs can come from:
- Regime Transition Engine
- Liquidity & Volatility Engine
- Event Risk Engine
- Scenario Engine
- Failure Pattern Engine
- Breadth Engine v2
- Portfolio Intelligence v2
- Macro Cross-Market Engine v2
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskReductionInput:
    transition_score: float
    liquidity_stability_score: float
    event_risk_score: float
    scenario_impact_score: float
    failure_probability_score: float
    breadth_score: float
    portfolio_risk_score: float
    macro_risk_score: float
    current_portfolio_heat: float
    max_portfolio_heat: float


@dataclass(frozen=True)
class RiskReductionPolicy:
    risk_state: str
    exposure_multiplier: float
    max_new_position_size: float
    allow_new_aggressive_entries: bool
    allow_add_to_winners: bool
    require_manual_review: bool
    triggered_controls: tuple[str, ...]
    recommended_actions: tuple[str, ...]


def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def calculate_stress_score(data: RiskReductionInput) -> int:
    stress = 0.0

    stress += max(0, 60 - data.transition_score) * 0.22
    stress += max(0, 60 - data.liquidity_stability_score) * 0.24
    stress += data.event_risk_score * 0.16
    stress += data.scenario_impact_score * 0.18
    stress += data.failure_probability_score * 0.22
    stress += max(0, 60 - data.breadth_score) * 0.18
    stress += data.portfolio_risk_score * 0.20
    stress += max(0, 60 - data.macro_risk_score) * 0.18

    if data.current_portfolio_heat > data.max_portfolio_heat:
        stress += 18

    return int(max(0, min(100, round(stress))))


def build_risk_reduction_policy(data: RiskReductionInput) -> RiskReductionPolicy:
    stress_score = calculate_stress_score(data)
    controls: list[str] = []
    actions: list[str] = []

    if data.current_portfolio_heat > data.max_portfolio_heat:
        controls.append("portfolio_heat_exceeded")
        actions.append("reduce_existing_exposure_to_heat_limit")

    if data.liquidity_stability_score <= 40:
        controls.append("liquidity_stress")
        actions.append("avoid_illiquid_or_wide_spread_entries")

    if data.failure_probability_score >= 60:
        controls.append("failure_pattern_pressure")
        actions.append("raise_setup_quality_thresholds")

    if data.event_risk_score >= 55:
        controls.append("event_risk_pressure")
        actions.append("reduce_risk_before_or_after_major_event")

    if data.scenario_impact_score >= 60:
        controls.append("scenario_stress_pressure")
        actions.append("reduce_exposure_to_scenario_sensitive_assets")

    if data.breadth_score <= 40:
        controls.append("breadth_deterioration")
        actions.append("avoid_broad_beta_expansion")

    if data.macro_risk_score <= 40:
        controls.append("macro_pressure")
        actions.append("reduce_cyclical_and_high_beta_exposure")

    if stress_score >= 80:
        risk_state = "risk_reduction_extreme"
        exposure_multiplier = 0.0
        max_new_position_size = 0.0
        allow_new_aggressive_entries = False
        allow_add_to_winners = False
        require_manual_review = True
        actions.append("block_new_risk")
        actions.append("prioritize_capital_preservation")

    elif stress_score >= 60:
        risk_state = "risk_reduction_high"
        exposure_multiplier = 0.25
        max_new_position_size = 0.25
        allow_new_aggressive_entries = False
        allow_add_to_winners = False
        require_manual_review = True
        actions.append("cut_position_size_aggressively")

    elif stress_score >= 40:
        risk_state = "risk_reduction_moderate"
        exposure_multiplier = 0.50
        max_new_position_size = 0.50
        allow_new_aggressive_entries = False
        allow_add_to_winners = True
        require_manual_review = False
        actions.append("only_take_high_quality_asymmetric_setups")

    elif stress_score >= 25:
        risk_state = "risk_reduction_light"
        exposure_multiplier = 0.75
        max_new_position_size = 0.75
        allow_new_aggressive_entries = True
        allow_add_to_winners = True
        require_manual_review = False
        actions.append("maintain_selectivity")

    else:
        risk_state = "normal_risk_allowed"
        exposure_multiplier = 1.0
        max_new_position_size = 1.0
        allow_new_aggressive_entries = True
        allow_add_to_winners = True
        require_manual_review = False
        actions.append("normal_risk_protocol")

    return RiskReductionPolicy(
        risk_state=risk_state,
        exposure_multiplier=round(_clamp(exposure_multiplier), 4),
        max_new_position_size=round(_clamp(max_new_position_size), 4),
        allow_new_aggressive_entries=allow_new_aggressive_entries,
        allow_add_to_winners=allow_add_to_winners,
        require_manual_review=require_manual_review,
        triggered_controls=tuple(dict.fromkeys(controls)),
        recommended_actions=tuple(dict.fromkeys(actions)),
    )
