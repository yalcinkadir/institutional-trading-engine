"""
Meta-Learning Engine.

This module evaluates whether the Decision Engine's own confidence, factors and
risk tiers are reliable based on historical outcomes.

It answers:
- Which factors currently work?
- Which factors are deteriorating?
- Was high confidence justified?
- Should risk weights be increased or reduced?

The implementation is deterministic and explainable. It is not black-box ML.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from statistics import mean


@dataclass(frozen=True)
class MetaLearningRecord:
    setup_type: str
    market_state: str
    factor_tags: tuple[str, ...]
    confidence: float
    risk_tier: str
    result_5d: float


@dataclass(frozen=True)
class FactorReliabilityProfile:
    factor: str
    samples: int
    win_rate: float
    average_result: float
    reliability_score: int
    recommendation: str


@dataclass(frozen=True)
class ConfidenceCalibrationProfile:
    bucket: str
    samples: int
    average_confidence: float
    win_rate: float
    average_result: float
    calibration_state: str


@dataclass(frozen=True)
class MetaLearningAssessment:
    factor_profiles: tuple[FactorReliabilityProfile, ...]
    confidence_profiles: tuple[ConfidenceCalibrationProfile, ...]
    strongest_factors: tuple[str, ...]
    weakest_factors: tuple[str, ...]
    recommended_weight_adjustments: tuple[str, ...]


MIN_FACTOR_SAMPLES = 5


def _confidence_bucket(confidence: float) -> str:
    if confidence >= 0.8:
        return "high_confidence"
    if confidence >= 0.6:
        return "medium_confidence"
    return "low_confidence"


def _profile_factor(factor: str, results: list[float]) -> FactorReliabilityProfile:
    samples = len(results)
    if samples == 0:
        return FactorReliabilityProfile(factor, 0, 0.0, 0.0, 0, "insufficient_data")

    wins = [value for value in results if value > 0]
    win_rate = len(wins) / samples
    avg = mean(results)

    reliability = int(max(0, min(100, (win_rate * 55) + ((avg + 5) / 10 * 45))))

    if samples < MIN_FACTOR_SAMPLES:
        recommendation = "insufficient_data"
    elif reliability >= 70:
        recommendation = "increase_weight"
    elif reliability >= 55:
        recommendation = "maintain_weight"
    elif reliability >= 40:
        recommendation = "reduce_weight"
    else:
        recommendation = "deprioritize_or_block"

    return FactorReliabilityProfile(
        factor=factor,
        samples=samples,
        win_rate=round(win_rate, 4),
        average_result=round(avg, 4),
        reliability_score=reliability,
        recommendation=recommendation,
    )


def _profile_confidence(bucket: str, rows: list[MetaLearningRecord]) -> ConfidenceCalibrationProfile:
    if not rows:
        return ConfidenceCalibrationProfile(bucket, 0, 0.0, 0.0, 0.0, "insufficient_data")

    results = [row.result_5d for row in rows]
    wins = [value for value in results if value > 0]
    avg_conf = mean([row.confidence for row in rows])
    win_rate = len(wins) / len(rows)
    avg_result = mean(results)

    if len(rows) < 5:
        state = "insufficient_data"
    elif bucket == "high_confidence" and (win_rate < 0.5 or avg_result <= 0):
        state = "overconfident"
    elif bucket == "low_confidence" and avg_result > 1.0:
        state = "underconfident"
    else:
        state = "reasonably_calibrated"

    return ConfidenceCalibrationProfile(
        bucket=bucket,
        samples=len(rows),
        average_confidence=round(avg_conf, 4),
        win_rate=round(win_rate, 4),
        average_result=round(avg_result, 4),
        calibration_state=state,
    )


def build_meta_learning_assessment(records: list[MetaLearningRecord]) -> MetaLearningAssessment:
    by_factor: dict[str, list[float]] = defaultdict(list)
    by_confidence: dict[str, list[MetaLearningRecord]] = defaultdict(list)

    for record in records:
        for factor in record.factor_tags:
            by_factor[factor].append(record.result_5d)
        by_confidence[_confidence_bucket(record.confidence)].append(record)

    factor_profiles = tuple(
        sorted(
            (_profile_factor(factor, results) for factor, results in by_factor.items()),
            key=lambda profile: profile.reliability_score,
            reverse=True,
        )
    )

    confidence_profiles = tuple(
        _profile_confidence(bucket, by_confidence.get(bucket, []))
        for bucket in ("high_confidence", "medium_confidence", "low_confidence")
    )

    strongest = tuple(
        profile.factor
        for profile in factor_profiles
        if profile.samples >= MIN_FACTOR_SAMPLES and profile.reliability_score >= 70
    )[:5]

    weakest = tuple(
        profile.factor
        for profile in factor_profiles
        if profile.samples >= MIN_FACTOR_SAMPLES and profile.reliability_score < 40
    )[:5]

    adjustments: list[str] = []
    for profile in factor_profiles:
        if profile.recommendation in {"increase_weight", "reduce_weight", "deprioritize_or_block"}:
            adjustments.append(f"{profile.recommendation}:{profile.factor}")

    for profile in confidence_profiles:
        if profile.calibration_state == "overconfident":
            adjustments.append(f"lower_confidence_mapping:{profile.bucket}")
        elif profile.calibration_state == "underconfident":
            adjustments.append(f"raise_confidence_mapping:{profile.bucket}")

    return MetaLearningAssessment(
        factor_profiles=factor_profiles,
        confidence_profiles=confidence_profiles,
        strongest_factors=strongest,
        weakest_factors=weakest,
        recommended_weight_adjustments=tuple(dict.fromkeys(adjustments)),
    )
