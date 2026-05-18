"""
Portfolio Construction Optimizer.

This module converts ranked opportunities into constrained target weights.
It is not a mean-variance optimizer. It is a transparent risk-first allocator.

It considers:
- expected edge score
- risk tier
- volatility
- sector caps
- factor caps
- max single-position weight
- autonomous risk-reduction multiplier

The goal is robust portfolio construction without black-box optimization.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PortfolioOpportunity:
    symbol: str
    sector: str
    factor_tags: tuple[str, ...]
    expected_edge_score: float
    risk_tier: str
    volatility_20d: float
    liquidity_score: float


@dataclass(frozen=True)
class PortfolioConstructionConstraints:
    max_position_weight: float = 0.15
    max_sector_weight: float = 0.35
    max_factor_weight: float = 0.40
    min_liquidity_score: float = 40
    risk_reduction_multiplier: float = 1.0
    total_target_exposure: float = 1.0


@dataclass(frozen=True)
class PortfolioAllocation:
    symbol: str
    target_weight: float
    reason: str


@dataclass(frozen=True)
class PortfolioConstructionResult:
    portfolio_state: str
    total_allocated_weight: float
    allocations: tuple[PortfolioAllocation, ...]
    warnings: tuple[str, ...]


RISK_TIER_MULTIPLIER = {
    "tier_1": 1.0,
    "tier_2": 0.55,
    "tier_3": 0.25,
    "no_trade": 0.0,
}


def _raw_score(opportunity: PortfolioOpportunity) -> float:
    risk_multiplier = RISK_TIER_MULTIPLIER.get(opportunity.risk_tier, 0.0)
    volatility_penalty = max(opportunity.volatility_20d, 0.01)
    liquidity_multiplier = min(1.0, opportunity.liquidity_score / 80)
    return max(0.0, opportunity.expected_edge_score * risk_multiplier * liquidity_multiplier / volatility_penalty)


def construct_portfolio(
    opportunities: list[PortfolioOpportunity],
    constraints: PortfolioConstructionConstraints | None = None,
) -> PortfolioConstructionResult:
    constraints = constraints or PortfolioConstructionConstraints()
    warnings: list[str] = []

    eligible = []
    for opportunity in opportunities:
        if opportunity.risk_tier == "no_trade":
            warnings.append(f"excluded_no_trade:{opportunity.symbol}")
            continue
        if opportunity.liquidity_score < constraints.min_liquidity_score:
            warnings.append(f"excluded_low_liquidity:{opportunity.symbol}")
            continue
        score = _raw_score(opportunity)
        if score <= 0:
            warnings.append(f"excluded_zero_score:{opportunity.symbol}")
            continue
        eligible.append((opportunity, score))

    if not eligible:
        return PortfolioConstructionResult(
            portfolio_state="no_allocatable_opportunities",
            total_allocated_weight=0.0,
            allocations=(),
            warnings=tuple(dict.fromkeys(warnings)),
        )

    total_score = sum(score for _, score in eligible)
    target_exposure = constraints.total_target_exposure * constraints.risk_reduction_multiplier

    sector_weights: dict[str, float] = {}
    factor_weights: dict[str, float] = {}
    allocations: list[PortfolioAllocation] = []

    for opportunity, score in sorted(eligible, key=lambda item: item[1], reverse=True):
        desired_weight = (score / total_score) * target_exposure
        capped_weight = min(desired_weight, constraints.max_position_weight)

        sector_remaining = constraints.max_sector_weight - sector_weights.get(opportunity.sector, 0.0)
        capped_weight = min(capped_weight, max(0.0, sector_remaining))

        for factor in opportunity.factor_tags:
            factor_remaining = constraints.max_factor_weight - factor_weights.get(factor, 0.0)
            capped_weight = min(capped_weight, max(0.0, factor_remaining))

        if capped_weight <= 0:
            warnings.append(f"excluded_by_concentration_caps:{opportunity.symbol}")
            continue

        sector_weights[opportunity.sector] = sector_weights.get(opportunity.sector, 0.0) + capped_weight
        for factor in opportunity.factor_tags:
            factor_weights[factor] = factor_weights.get(factor, 0.0) + capped_weight

        reason = "allocated_by_edge_risk_volatility_constraints"
        if capped_weight < desired_weight:
            reason = "capped_by_risk_constraints"

        allocations.append(
            PortfolioAllocation(
                symbol=opportunity.symbol,
                target_weight=round(capped_weight, 4),
                reason=reason,
            )
        )

    total_allocated = round(sum(item.target_weight for item in allocations), 4)

    if total_allocated <= target_exposure * 0.5:
        state = "portfolio_underallocated_due_to_constraints"
    elif total_allocated < target_exposure * 0.9:
        state = "portfolio_selectively_allocated"
    else:
        state = "portfolio_constructed"

    return PortfolioConstructionResult(
        portfolio_state=state,
        total_allocated_weight=total_allocated,
        allocations=tuple(allocations),
        warnings=tuple(dict.fromkeys(warnings)),
    )
