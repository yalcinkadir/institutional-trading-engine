"""
Exposure Correlation Engine.

This module evaluates hidden portfolio exposure overlap across:
- pairwise return correlation
- factor exposure overlap
- sector concentration
- beta-weighted exposure
- volatility-weighted exposure

The goal is to detect when a portfolio looks diversified by ticker count but is
actually concentrated in the same risk factor.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from statistics import mean


@dataclass(frozen=True)
class ExposurePosition:
    symbol: str
    sector: str
    factor_tags: tuple[str, ...]
    weight: float
    beta: float
    volatility_20d: float
    returns_20d: tuple[float, ...]


@dataclass(frozen=True)
class ExposureCluster:
    cluster_type: str
    name: str
    exposure_weight: float
    members: tuple[str, ...]
    risk_level: str


@dataclass(frozen=True)
class ExposureCorrelationAssessment:
    exposure_state: str
    exposure_risk_score: int
    pairwise_correlation_warnings: tuple[str, ...]
    clusters: tuple[ExposureCluster, ...]
    recommended_actions: tuple[str, ...]


def _correlation(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    if len(a) != len(b) or len(a) < 3:
        return 0.0

    mean_a = mean(a)
    mean_b = mean(b)
    numerator = sum((x - mean_a) * (y - mean_b) for x, y in zip(a, b))
    denominator_a = sqrt(sum((x - mean_a) ** 2 for x in a))
    denominator_b = sqrt(sum((y - mean_b) ** 2 for y in b))

    if denominator_a == 0 or denominator_b == 0:
        return 0.0

    return round(numerator / (denominator_a * denominator_b), 4)


def _risk_level(weight: float) -> str:
    if weight >= 0.60:
        return "extreme"
    if weight >= 0.45:
        return "high"
    if weight >= 0.30:
        return "moderate"
    return "contained"


def evaluate_exposure_correlation(
    positions: list[ExposurePosition],
    *,
    correlation_threshold: float = 0.80,
    concentration_threshold: float = 0.35,
) -> ExposureCorrelationAssessment:
    pairwise_warnings: list[str] = []
    clusters: list[ExposureCluster] = []
    actions: list[str] = []
    risk_score = 0

    for index, first in enumerate(positions):
        for second in positions[index + 1 :]:
            corr = _correlation(first.returns_20d, second.returns_20d)
            if corr >= correlation_threshold:
                shared = sorted(set(first.factor_tags).intersection(second.factor_tags))
                label = ",".join(shared) if shared else "return_correlation"
                pairwise_warnings.append(f"high_pairwise_correlation:{first.symbol}-{second.symbol}:{corr}:{label}")
                risk_score += 8

    sector_weights: dict[str, float] = {}
    sector_members: dict[str, list[str]] = {}
    factor_weights: dict[str, float] = {}
    factor_members: dict[str, list[str]] = {}

    beta_weighted_exposure = 0.0
    volatility_weighted_exposure = 0.0

    for position in positions:
        sector_weights[position.sector] = sector_weights.get(position.sector, 0.0) + position.weight
        sector_members.setdefault(position.sector, []).append(position.symbol)

        for factor in position.factor_tags:
            factor_weights[factor] = factor_weights.get(factor, 0.0) + position.weight
            factor_members.setdefault(factor, []).append(position.symbol)

        beta_weighted_exposure += position.weight * position.beta
        volatility_weighted_exposure += position.weight * position.volatility_20d

    for sector, weight in sector_weights.items():
        if weight >= concentration_threshold:
            level = _risk_level(weight)
            clusters.append(
                ExposureCluster(
                    cluster_type="sector",
                    name=sector,
                    exposure_weight=round(weight, 4),
                    members=tuple(sorted(sector_members[sector])),
                    risk_level=level,
                )
            )
            risk_score += 12 if level in {"high", "extreme"} else 6
            actions.append(f"cap_sector_exposure:{sector}")

    for factor, weight in factor_weights.items():
        if weight >= concentration_threshold:
            level = _risk_level(weight)
            clusters.append(
                ExposureCluster(
                    cluster_type="factor",
                    name=factor,
                    exposure_weight=round(weight, 4),
                    members=tuple(sorted(factor_members[factor])),
                    risk_level=level,
                )
            )
            risk_score += 15 if level in {"high", "extreme"} else 7
            actions.append(f"cap_factor_exposure:{factor}")

    if beta_weighted_exposure >= 1.25:
        risk_score += 15
        actions.append("reduce_beta_weighted_exposure")
        clusters.append(
            ExposureCluster(
                cluster_type="beta",
                name="high_beta_exposure",
                exposure_weight=round(beta_weighted_exposure, 4),
                members=tuple(sorted(position.symbol for position in positions if position.beta >= 1.2)),
                risk_level=_risk_level(min(1.0, beta_weighted_exposure / 2)),
            )
        )

    if volatility_weighted_exposure >= 0.08:
        risk_score += 10
        actions.append("reduce_volatility_weighted_exposure")
        clusters.append(
            ExposureCluster(
                cluster_type="volatility",
                name="high_volatility_budget",
                exposure_weight=round(volatility_weighted_exposure, 4),
                members=tuple(sorted(position.symbol for position in positions if position.volatility_20d >= 0.08)),
                risk_level="high",
            )
        )

    risk_score = max(0, min(100, risk_score))

    if risk_score >= 70:
        state = "exposure_correlation_extreme"
        actions.append("block_new_overlapping_risk")
    elif risk_score >= 50:
        state = "exposure_correlation_high"
        actions.append("reduce_or_hedge_clustered_exposure")
    elif risk_score >= 30:
        state = "exposure_correlation_moderate"
        actions.append("monitor_clustered_exposure")
    else:
        state = "exposure_correlation_contained"

    return ExposureCorrelationAssessment(
        exposure_state=state,
        exposure_risk_score=risk_score,
        pairwise_correlation_warnings=tuple(dict.fromkeys(pairwise_warnings)),
        clusters=tuple(clusters),
        recommended_actions=tuple(dict.fromkeys(actions)),
    )
