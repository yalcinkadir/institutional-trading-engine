"""
Dynamic Outcome-Based Weighting Engine.

This module converts meta-learning and expectancy evidence into controlled
factor-weight adjustments.

It is intentionally conservative:
- no black-box optimization
- no unlimited factor swings
- caps per update
- minimum sample safeguards
- explicit recommendations

The purpose is adaptive weighting without overfitting.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FactorWeightInput:
    factor: str
    current_weight: float
    reliability_score: int
    samples: int
    expectancy: float
    confidence: float


@dataclass(frozen=True)
class FactorWeightAdjustment:
    factor: str
    old_weight: float
    new_weight: float
    delta: float
    action: str
    reason: str


@dataclass(frozen=True)
class DynamicWeightingPolicy:
    adjustments: tuple[FactorWeightAdjustment, ...]
    total_weight: float
    warnings: tuple[str, ...]


MIN_SAMPLES = 10
WEIGHT_PRECISION = 4
TARGET_WEIGHT_SUM = 1.0


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def _with_new_weight(item: FactorWeightAdjustment, new_weight: float) -> FactorWeightAdjustment:
    rounded_weight = round(new_weight, WEIGHT_PRECISION)
    return FactorWeightAdjustment(
        factor=item.factor,
        old_weight=round(item.old_weight, WEIGHT_PRECISION),
        new_weight=rounded_weight,
        delta=round(rounded_weight - item.old_weight, WEIGHT_PRECISION),
        action=item.action,
        reason=item.reason,
    )


def _force_exact_weight_sum(
    adjustments: list[FactorWeightAdjustment],
    *,
    target_sum: float = TARGET_WEIGHT_SUM,
) -> tuple[FactorWeightAdjustment, ...]:
    """Correct rounding remainder so rounded weights sum exactly to target_sum."""

    if not adjustments:
        return ()

    rounded_total = round(sum(item.new_weight for item in adjustments), WEIGHT_PRECISION)
    remainder = round(target_sum - rounded_total, WEIGHT_PRECISION)
    if remainder == 0:
        return tuple(adjustments)

    anchor_index = max(
        range(len(adjustments)),
        key=lambda index: (adjustments[index].new_weight, adjustments[index].factor),
    )
    anchor = adjustments[anchor_index]
    adjusted_anchor = _with_new_weight(anchor, anchor.new_weight + remainder)
    corrected = list(adjustments)
    corrected[anchor_index] = adjusted_anchor
    corrected_total = round(sum(item.new_weight for item in corrected), WEIGHT_PRECISION)
    if corrected_total != round(target_sum, WEIGHT_PRECISION):
        raise ValueError(
            f"normalized dynamic weights do not sum to {target_sum}: {corrected_total}"
        )
    return tuple(corrected)


def _normalize_weights(adjustments: list[FactorWeightAdjustment]) -> tuple[FactorWeightAdjustment, ...]:
    total = sum(item.new_weight for item in adjustments)
    if total <= 0:
        return tuple(adjustments)

    normalized = []
    for item in adjustments:
        normalized_weight = item.new_weight / total
        normalized.append(_with_new_weight(item, normalized_weight))
    return _force_exact_weight_sum(normalized)


def build_dynamic_weighting_policy(
    factors: list[FactorWeightInput],
    *,
    max_delta_per_update: float = 0.08,
    min_weight: float = 0.02,
    max_weight: float = 0.35,
) -> DynamicWeightingPolicy:
    warnings: list[str] = []
    adjustments: list[FactorWeightAdjustment] = []

    if not factors:
        return DynamicWeightingPolicy(
            adjustments=(),
            total_weight=0.0,
            warnings=("no_factors_provided",),
        )

    for factor in factors:
        delta = 0.0
        action = "maintain_weight"
        reason = "neutral_or_insufficient_evidence"

        if factor.samples < MIN_SAMPLES:
            warnings.append(f"insufficient_samples:{factor.factor}:{factor.samples}")
        else:
            if factor.reliability_score >= 75 and factor.expectancy > 1.0 and factor.confidence >= 0.6:
                delta = max_delta_per_update
                action = "increase_weight"
                reason = "high_reliability_positive_expectancy"
            elif factor.reliability_score >= 60 and factor.expectancy > 0:
                delta = max_delta_per_update / 2
                action = "slightly_increase_weight"
                reason = "constructive_reliability"
            elif factor.reliability_score <= 35 or factor.expectancy < -1.0:
                delta = -max_delta_per_update
                action = "decrease_weight"
                reason = "poor_reliability_or_negative_expectancy"
            elif factor.reliability_score <= 50 or factor.expectancy <= 0:
                delta = -(max_delta_per_update / 2)
                action = "slightly_decrease_weight"
                reason = "weak_or_flat_edge"

        new_weight = _clamp(factor.current_weight + delta, min_weight, max_weight)

        adjustments.append(
            FactorWeightAdjustment(
                factor=factor.factor,
                old_weight=round(factor.current_weight, WEIGHT_PRECISION),
                new_weight=round(new_weight, WEIGHT_PRECISION),
                delta=round(new_weight - factor.current_weight, WEIGHT_PRECISION),
                action=action,
                reason=reason,
            )
        )

    normalized = _normalize_weights(adjustments)
    total_weight = round(sum(item.new_weight for item in normalized), WEIGHT_PRECISION)

    return DynamicWeightingPolicy(
        adjustments=normalized,
        total_weight=total_weight,
        warnings=tuple(dict.fromkeys(warnings)),
    )
