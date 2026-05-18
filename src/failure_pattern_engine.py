"""
Failure Pattern Engine.

This engine identifies combinations of conditions that frequently lead to
failed trades, weak follow-through or unstable market behavior.

The goal is not prediction.
The goal is reducing exposure to structurally poor conditions.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FailurePatternInput:
    setup_score: float
    asymmetry_score: float
    breadth_score: float
    liquidity_stability_score: float
    transition_score: float
    vix: float
    failed_breakout_rate: float
    mega_cap_dependency_percent: float
    semiconductor_leadership: bool
    equal_weight_confirming: bool
    volatility_expansion: bool
    event_risk_active: bool
    asset_extended_from_sma50_percent: float


@dataclass(frozen=True)
class FailurePatternAssessment:
    failure_risk_state: str
    failure_probability_score: int
    risk_action: str
    detected_patterns: tuple[str, ...]
    warnings: tuple[str, ...]


def evaluate_failure_patterns(
    data: FailurePatternInput,
) -> FailurePatternAssessment:
    patterns: list[str] = []
    warnings: list[str] = []

    score = 0

    if (
        data.asset_extended_from_sma50_percent >= 12
        and data.failed_breakout_rate >= 0.45
        and data.volatility_expansion
    ):
        score += 30
        patterns.append("extended_breakout_trap")

    if (
        data.breadth_score <= 45
        and data.mega_cap_dependency_percent >= 55
        and not data.equal_weight_confirming
    ):
        score += 25
        patterns.append("narrow_leadership_fragility")

    if (
        not data.semiconductor_leadership
        and data.transition_score <= 45
        and data.vix >= 22
    ):
        score += 20
        patterns.append("semiconductor_leadership_breakdown")

    if (
        data.liquidity_stability_score <= 40
        and data.volatility_expansion
    ):
        score += 20
        patterns.append("liquidity_volatility_instability")

    if (
        data.event_risk_active
        and data.vix >= 20
        and data.failed_breakout_rate >= 0.35
    ):
        score += 18
        patterns.append("event_risk_instability")

    if (
        data.asymmetry_score <= 0.35
        and data.setup_score >= 75
    ):
        score += 12
        patterns.append("high_score_poor_asymmetry")

    score = max(0, min(100, score))

    if score >= 70:
        failure_state = "extreme_failure_risk"
        risk_action = "block_aggressive_entries"
        warnings.append("multiple_failure_clusters_detected")

    elif score >= 50:
        failure_state = "high_failure_risk"
        risk_action = "reduce_position_size_and_raise_thresholds"
        warnings.append("conditions_fragile")

    elif score >= 30:
        failure_state = "moderate_failure_risk"
        risk_action = "favor_only_high_quality_setups"

    else:
        failure_state = "contained_failure_risk"
        risk_action = "normal_risk_protocol"

    return FailurePatternAssessment(
        failure_risk_state=failure_state,
        failure_probability_score=score,
        risk_action=risk_action,
        detected_patterns=tuple(patterns),
        warnings=tuple(warnings),
    )
