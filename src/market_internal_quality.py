"""
Market Internal Quality Layer.

This layer evaluates whether the market environment is healthy enough for
aggressive participation.

It focuses on:
- breadth quality
- breakout failure pressure
- opportunity density
- leadership expansion

The purpose is not prediction. The purpose is environment quality assessment.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MarketInternalSnapshot:
    breadth_percent: float
    breakout_success_rate: float
    failed_breakout_rate: float
    new_highs: int
    new_lows: int
    leaders_above_sma50_percent: float
    opportunities_detected: int


@dataclass(frozen=True)
class MarketInternalAssessment:
    environment: str
    quality_score: int
    opportunity_density: str
    warnings: tuple[str, ...]
    confirmations: tuple[str, ...]


def evaluate_market_internal_quality(snapshot: MarketInternalSnapshot) -> MarketInternalAssessment:
    score = 50
    warnings: list[str] = []
    confirmations: list[str] = []

    if snapshot.breadth_percent >= 70:
        score += 15
        confirmations.append("strong_breadth")
    elif snapshot.breadth_percent <= 40:
        score -= 20
        warnings.append("weak_breadth")

    if snapshot.breakout_success_rate >= 0.65:
        score += 15
        confirmations.append("healthy_breakout_followthrough")
    elif snapshot.breakout_success_rate <= 0.40:
        score -= 15
        warnings.append("poor_breakout_followthrough")

    if snapshot.failed_breakout_rate >= 0.50:
        score -= 20
        warnings.append("failed_breakout_cluster")
    elif snapshot.failed_breakout_rate <= 0.25:
        score += 10
        confirmations.append("limited_breakout_failure_pressure")

    if snapshot.new_highs > snapshot.new_lows * 2:
        score += 10
        confirmations.append("new_high_expansion")
    elif snapshot.new_lows > snapshot.new_highs:
        score -= 15
        warnings.append("new_low_expansion")

    if snapshot.leaders_above_sma50_percent >= 75:
        score += 10
        confirmations.append("leaders_confirm_trend")
    elif snapshot.leaders_above_sma50_percent <= 45:
        score -= 10
        warnings.append("leader_trend_deterioration")

    if snapshot.opportunities_detected >= 12:
        opportunity_density = "high"
        score += 10
        confirmations.append("high_opportunity_density")
    elif snapshot.opportunities_detected >= 6:
        opportunity_density = "medium"
    else:
        opportunity_density = "low"
        score -= 10
        warnings.append("low_opportunity_density")

    score = max(0, min(100, score))

    if score >= 75:
        environment = "aggressive_risk_allowed"
    elif score >= 55:
        environment = "selective_risk_allowed"
    elif score >= 40:
        environment = "defensive_selectivity"
    else:
        environment = "capital_preservation"

    return MarketInternalAssessment(
        environment=environment,
        quality_score=score,
        opportunity_density=opportunity_density,
        warnings=tuple(warnings),
        confirmations=tuple(confirmations),
    )
