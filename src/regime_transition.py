"""
Regime Transition Engine.

A strong market screener must not only classify the current regime. It must also
identify whether the regime is improving, deteriorating or becoming unstable.

This module detects transition pressure between:
- risk-on strengthening
- bullish but fragile
- neutral transition
- defensive deterioration
- risk-off acceleration

The goal is early warning, not prediction.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RegimeTransitionInput:
    current_market_health_score: float
    previous_market_health_score: float
    current_breadth_percent: float
    previous_breadth_percent: float
    current_vix: float
    previous_vix: float
    current_cross_asset_risk_score: float
    previous_cross_asset_risk_score: float
    failed_breakout_rate: float
    opportunity_density: str


@dataclass(frozen=True)
class RegimeTransitionAssessment:
    transition_state: str
    transition_score: int
    risk_action: str
    warnings: tuple[str, ...]
    confirmations: tuple[str, ...]


def evaluate_regime_transition(data: RegimeTransitionInput) -> RegimeTransitionAssessment:
    warnings: list[str] = []
    confirmations: list[str] = []
    score = 50

    mhs_delta = data.current_market_health_score - data.previous_market_health_score
    breadth_delta = data.current_breadth_percent - data.previous_breadth_percent
    vix_delta = data.current_vix - data.previous_vix
    cross_asset_delta = data.current_cross_asset_risk_score - data.previous_cross_asset_risk_score

    if mhs_delta >= 8:
        score += 15
        confirmations.append("market_health_improving")
    elif mhs_delta <= -8:
        score -= 15
        warnings.append("market_health_deteriorating")

    if breadth_delta >= 8:
        score += 15
        confirmations.append("breadth_expansion")
    elif breadth_delta <= -8:
        score -= 15
        warnings.append("breadth_deterioration")

    if vix_delta <= -3:
        score += 10
        confirmations.append("volatility_compression")
    elif vix_delta >= 3:
        score -= 15
        warnings.append("volatility_expansion")

    if cross_asset_delta >= 8:
        score += 15
        confirmations.append("cross_asset_risk_appetite_improving")
    elif cross_asset_delta <= -8:
        score -= 15
        warnings.append("cross_asset_risk_appetite_deteriorating")

    if data.failed_breakout_rate >= 0.50:
        score -= 20
        warnings.append("failed_breakout_transition_pressure")
    elif data.failed_breakout_rate <= 0.20:
        score += 8
        confirmations.append("breakout_followthrough_stable")

    if data.opportunity_density == "high":
        score += 10
        confirmations.append("opportunity_density_expanding")
    elif data.opportunity_density == "low":
        score -= 10
        warnings.append("opportunity_density_contracting")

    score = max(0, min(100, score))

    if score >= 75:
        transition_state = "risk_on_strengthening"
        risk_action = "allow_selective_risk_expansion"
    elif score >= 60:
        transition_state = "constructive_transition"
        risk_action = "maintain_risk_with_confirmation"
    elif score >= 45:
        transition_state = "neutral_transition"
        risk_action = "avoid_aggressive_expansion"
    elif score >= 30:
        transition_state = "defensive_deterioration"
        risk_action = "reduce_size_and_raise_quality_thresholds"
    else:
        transition_state = "risk_off_acceleration"
        risk_action = "block_aggressive_risk_and_prioritize_capital_preservation"

    return RegimeTransitionAssessment(
        transition_state=transition_state,
        transition_score=score,
        risk_action=risk_action,
        warnings=tuple(warnings),
        confirmations=tuple(confirmations),
    )
