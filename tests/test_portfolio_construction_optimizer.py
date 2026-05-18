from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.portfolio_construction_optimizer import (  # noqa: E402
    PortfolioConstructionConstraints,
    PortfolioOpportunity,
    construct_portfolio,
)


def test_portfolio_optimizer_caps_concentrated_ai_exposure():
    result = construct_portfolio(
        [
            PortfolioOpportunity(
                symbol="NVDA",
                sector="Technology",
                factor_tags=("ai", "growth"),
                expected_edge_score=92,
                risk_tier="tier_1",
                volatility_20d=0.08,
                liquidity_score=90,
            ),
            PortfolioOpportunity(
                symbol="AMD",
                sector="Technology",
                factor_tags=("ai", "growth"),
                expected_edge_score=88,
                risk_tier="tier_1",
                volatility_20d=0.085,
                liquidity_score=88,
            ),
            PortfolioOpportunity(
                symbol="MU",
                sector="Technology",
                factor_tags=("ai", "memory"),
                expected_edge_score=79,
                risk_tier="tier_1",
                volatility_20d=0.075,
                liquidity_score=82,
            ),
        ],
        PortfolioConstructionConstraints(
            max_position_weight=0.20,
            max_sector_weight=0.35,
            max_factor_weight=0.40,
        ),
    )

    assert result.total_allocated_weight <= 0.40
    assert len(result.allocations) > 0


def test_portfolio_optimizer_respects_risk_reduction_multiplier():
    result = construct_portfolio(
        [
            PortfolioOpportunity(
                symbol="AAPL",
                sector="Technology",
                factor_tags=("quality",),
                expected_edge_score=80,
                risk_tier="tier_1",
                volatility_20d=0.03,
                liquidity_score=95,
            )
        ],
        PortfolioConstructionConstraints(
            total_target_exposure=1.0,
            risk_reduction_multiplier=0.25,
        ),
    )

    assert result.total_allocated_weight <= 0.25
