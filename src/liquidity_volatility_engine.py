"""
Liquidity & Volatility Engine v2.

Institutional systems do not only measure trend.
They evaluate whether market conditions are stable enough to support risk.

This engine evaluates:
- volatility expansion/contraction
- volatility instability
- liquidity deterioration
- gap risk
- ATR acceleration
- stress clustering

The goal is not prediction.
The goal is avoiding structurally unstable environments.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LiquidityVolatilityInput:
    vix: float
    previous_vix: float
    vvix: float
    atr_percent: float
    previous_atr_percent: float
    average_gap_percent: float
    liquidity_score: float
    spread_stress_score: float
    failed_breakout_rate: float
    volatility_of_volatility: float


@dataclass(frozen=True)
class LiquidityVolatilityAssessment:
    environment: str
    stability_score: int
    risk_posture: str
    warnings: tuple[str, ...]
    confirmations: tuple[str, ...]


def evaluate_liquidity_volatility_environment(
    data: LiquidityVolatilityInput,
) -> LiquidityVolatilityAssessment:
    warnings: list[str] = []
    confirmations: list[str] = []

    score = 50

    vix_delta = data.vix - data.previous_vix
    atr_delta = data.atr_percent - data.previous_atr_percent

    if data.vix <= 15:
        score += 15
        confirmations.append("low_volatility_environment")
    elif data.vix >= 28:
        score -= 20
        warnings.append("high_volatility_environment")

    if vix_delta >= 4:
        score -= 15
        warnings.append("volatility_expansion")
    elif vix_delta <= -3:
        score += 10
        confirmations.append("volatility_compression")

    if data.vvix >= 120:
        score -= 15
        warnings.append("volatility_instability")
    elif data.vvix <= 90:
        score += 8
        confirmations.append("volatility_structure_stable")

    if atr_delta >= 0.015:
        score -= 10
        warnings.append("atr_acceleration")

    if data.average_gap_percent >= 2.5:
        score -= 12
        warnings.append("gap_risk_expanding")
    elif data.average_gap_percent <= 1:
        score += 5
        confirmations.append("gap_risk_stable")

    if data.liquidity_score >= 75:
        score += 12
        confirmations.append("liquidity_supportive")
    elif data.liquidity_score <= 40:
        score -= 18
        warnings.append("liquidity_deterioration")

    if data.spread_stress_score >= 70:
        score -= 12
        warnings.append("spread_stress")

    if data.failed_breakout_rate >= 0.50:
        score -= 10
        warnings.append("failed_breakout_cluster")

    if data.volatility_of_volatility >= 0.7:
        score -= 10
        warnings.append("volatility_clustering")

    score = max(0, min(100, score))

    if score >= 75:
        environment = "stable_liquidity_risk_supportive"
        risk_posture = "allow_normal_or_aggressive_risk"
    elif score >= 60:
        environment = "constructive_but_selective"
        risk_posture = "favor_high_quality_setups"
    elif score >= 45:
        environment = "fragile_transition"
        risk_posture = "reduce_position_size"
    elif score >= 30:
        environment = "liquidity_stress_building"
        risk_posture = "prioritize_defense_and_capital_preservation"
    else:
        environment = "volatility_liquidity_crisis"
        risk_posture = "block_aggressive_exposure"

    return LiquidityVolatilityAssessment(
        environment=environment,
        stability_score=score,
        risk_posture=risk_posture,
        warnings=tuple(warnings),
        confirmations=tuple(confirmations),
    )
