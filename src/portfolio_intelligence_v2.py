"""
Portfolio Intelligence v2.

This module extends portfolio risk analysis beyond simple sector concentration.
It focuses on hidden correlation, beta clustering, risk stacking and volatility
budgeting.

Important design principle:
No static asset list is treated as permanent truth. Market leadership changes.
Therefore, clusters should be inferred from recent correlation, sector/factor
metadata and volatility rather than hard-coded ticker groups.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from statistics import mean


@dataclass(frozen=True)
class PortfolioPositionV2:
    symbol: str
    sector: str
    factor_tags: tuple[str, ...]
    weight: float
    beta: float
    volatility_20d: float
    returns_20d: tuple[float, ...]


@dataclass(frozen=True)
class PortfolioIntelligenceAssessment:
    portfolio_state: str
    risk_score: int
    hidden_correlation_clusters: tuple[str, ...]
    beta_cluster_warning: bool
    risk_stacking_warnings: tuple[str, ...]
    volatility_budget: tuple[str, ...]
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


def _shared_factor_count(first: PortfolioPositionV2, second: PortfolioPositionV2) -> int:
    return len(set(first.factor_tags).intersection(second.factor_tags))


def evaluate_portfolio_intelligence_v2(
    positions: list[PortfolioPositionV2],
    *,
    correlation_threshold: float = 0.78,
    high_beta_threshold: float = 1.25,
    max_single_factor_weight: float = 0.45,
) -> PortfolioIntelligenceAssessment:
    hidden_clusters: list[str] = []
    risk_stacking: list[str] = []
    recommended_actions: list[str] = []
    volatility_budget: list[str] = []

    risk_score = 0

    for index, first in enumerate(positions):
        for second in positions[index + 1 :]:
            corr = _correlation(first.returns_20d, second.returns_20d)
            shared_factors = _shared_factor_count(first, second)

            if corr >= correlation_threshold:
                hidden_clusters.append(f"correlation_cluster:{first.symbol}-{second.symbol}:{corr}")
                risk_score += 10

            if corr >= correlation_threshold and shared_factors >= 1:
                risk_stacking.append(
                    f"factor_stack:{first.symbol}-{second.symbol}:{','.join(sorted(set(first.factor_tags).intersection(second.factor_tags)))}"
                )
                risk_score += 8

    high_beta_weight = sum(position.weight for position in positions if position.beta >= high_beta_threshold)
    beta_cluster_warning = high_beta_weight >= 0.50

    if beta_cluster_warning:
        risk_score += 20
        risk_stacking.append(f"high_beta_cluster:{round(high_beta_weight, 4)}")
        recommended_actions.append("reduce_high_beta_exposure")

    factor_weights: dict[str, float] = {}
    for position in positions:
        for tag in position.factor_tags:
            factor_weights[tag] = factor_weights.get(tag, 0.0) + position.weight

    for factor, weight in sorted(factor_weights.items()):
        if weight >= max_single_factor_weight:
            risk_score += 15
            risk_stacking.append(f"single_factor_overweight:{factor}:{round(weight, 4)}")
            recommended_actions.append(f"cap_factor_exposure:{factor}")

    total_volatility_budget = sum(position.weight * position.volatility_20d for position in positions)
    for position in positions:
        contribution = position.weight * position.volatility_20d
        share = contribution / total_volatility_budget if total_volatility_budget else 0.0
        volatility_budget.append(f"{position.symbol}:{round(share, 4)}")
        if share >= 0.35:
            risk_score += 10
            risk_stacking.append(f"volatility_budget_concentration:{position.symbol}:{round(share, 4)}")
            recommended_actions.append(f"reduce_volatility_contribution:{position.symbol}")

    risk_score = max(0, min(100, risk_score))

    if risk_score >= 70:
        portfolio_state = "portfolio_risk_stacked"
        recommended_actions.append("block_new_correlated_risk")
    elif risk_score >= 45:
        portfolio_state = "portfolio_concentration_elevated"
        recommended_actions.append("reduce_or_hedge_overlapping_exposure")
    elif risk_score >= 25:
        portfolio_state = "portfolio_overlap_moderate"
        recommended_actions.append("monitor_hidden_correlation")
    else:
        portfolio_state = "portfolio_diversification_healthy"

    return PortfolioIntelligenceAssessment(
        portfolio_state=portfolio_state,
        risk_score=risk_score,
        hidden_correlation_clusters=tuple(hidden_clusters),
        beta_cluster_warning=beta_cluster_warning,
        risk_stacking_warnings=tuple(risk_stacking),
        volatility_budget=tuple(volatility_budget),
        recommended_actions=tuple(dict.fromkeys(recommended_actions)),
    )
