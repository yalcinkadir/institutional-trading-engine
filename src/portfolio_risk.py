"""
Portfolio Risk Layer for Decision Engine v3.

This layer prevents the classic screener mistake: treating highly correlated
opportunities as independent trades. Five bullish semiconductor/growth trades
can effectively be one single risk exposure.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from statistics import mean


@dataclass(frozen=True)
class PortfolioCandidate:
    symbol: str
    sector: str
    risk_tier: str
    position_size_multiplier: float
    returns_20d: tuple[float, ...]


@dataclass(frozen=True)
class PortfolioRiskResult:
    portfolio_heat: float
    concentration_warnings: tuple[str, ...]
    correlation_warnings: tuple[str, ...]
    approved_symbols: tuple[str, ...]
    reduced_symbols: tuple[str, ...]
    symbol_risk_multipliers: tuple[tuple[str, float], ...] = ()


RISK_TIER_HEAT = {
    "tier_1": 1.0,
    "tier_2": 0.5,
    "tier_3": 0.25,
    "no_trade": 0.0,
}

SECTOR_CONCENTRATION_MULTIPLIER = 0.75
CORRELATION_MULTIPLIER = 0.80
PORTFOLIO_HEAT_MULTIPLIER = 0.90


def calculate_correlation(a: tuple[float, ...], b: tuple[float, ...]) -> float:
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


def _tradable_symbols(candidates: list[PortfolioCandidate]) -> set[str]:
    return {candidate.symbol for candidate in candidates if candidate.risk_tier != "no_trade"}


def _candidate_by_symbol(candidates: list[PortfolioCandidate]) -> dict[str, PortfolioCandidate]:
    return {candidate.symbol: candidate for candidate in candidates}


def evaluate_portfolio_risk(
    candidates: list[PortfolioCandidate],
    *,
    max_portfolio_heat: float = 3.0,
    max_sector_heat: float = 1.5,
    correlation_threshold: float = 0.80,
) -> PortfolioRiskResult:
    concentration_warnings: list[str] = []
    correlation_warnings: list[str] = []
    approved: list[str] = []
    reduced: list[str] = []

    sector_heat: dict[str, float] = {}
    portfolio_heat = 0.0
    affected_symbols: set[str] = set()
    symbol_multipliers: dict[str, float] = {symbol: 1.0 for symbol in _tradable_symbols(candidates)}
    by_symbol = _candidate_by_symbol(candidates)

    for candidate in candidates:
        base_heat = RISK_TIER_HEAT.get(candidate.risk_tier, 0.0)
        heat = base_heat * candidate.position_size_multiplier
        portfolio_heat += heat
        sector_heat[candidate.sector] = sector_heat.get(candidate.sector, 0.0) + heat

    for sector, heat in sector_heat.items():
        if heat > max_sector_heat:
            concentration_warnings.append(f"sector_heat_exceeded:{sector}:{round(heat, 2)}")
            for candidate in candidates:
                if candidate.risk_tier != "no_trade" and candidate.sector == sector:
                    affected_symbols.add(candidate.symbol)
                    symbol_multipliers[candidate.symbol] = min(
                        symbol_multipliers[candidate.symbol], SECTOR_CONCENTRATION_MULTIPLIER
                    )

    if portfolio_heat > max_portfolio_heat:
        concentration_warnings.append(f"portfolio_heat_exceeded:{round(portfolio_heat, 2)}")
        for candidate in candidates:
            if candidate.risk_tier != "no_trade":
                affected_symbols.add(candidate.symbol)
                symbol_multipliers[candidate.symbol] = min(
                    symbol_multipliers[candidate.symbol], PORTFOLIO_HEAT_MULTIPLIER
                )

    for index, first in enumerate(candidates):
        if first.risk_tier == "no_trade":
            continue
        for second in candidates[index + 1 :]:
            if second.risk_tier == "no_trade":
                continue
            corr = calculate_correlation(first.returns_20d, second.returns_20d)
            if corr >= correlation_threshold:
                correlation_warnings.append(
                    f"high_correlation:{first.symbol}-{second.symbol}:{corr}"
                )
                for symbol in (first.symbol, second.symbol):
                    affected_symbols.add(symbol)
                    symbol_multipliers[symbol] = min(
                        symbol_multipliers[symbol], CORRELATION_MULTIPLIER
                    )

    for candidate in candidates:
        if candidate.risk_tier == "no_trade":
            continue

        if candidate.symbol in affected_symbols:
            reduced.append(candidate.symbol)
        else:
            approved.append(candidate.symbol)

    ordered_multipliers = tuple(
        (symbol, round(symbol_multipliers[symbol], 4))
        for symbol in sorted(symbol_multipliers)
        if symbol in by_symbol
    )

    return PortfolioRiskResult(
        portfolio_heat=round(portfolio_heat, 4),
        concentration_warnings=tuple(concentration_warnings),
        correlation_warnings=tuple(correlation_warnings),
        approved_symbols=tuple(approved),
        reduced_symbols=tuple(reduced),
        symbol_risk_multipliers=ordered_multipliers,
    )
