from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from portfolio_risk import (  # noqa: E402
    PortfolioCandidate,
    calculate_correlation,
    evaluate_portfolio_risk,
)


def test_correlation_detects_highly_correlated_assets():
    a = (0.01, 0.02, 0.03, 0.01, 0.04)
    b = (0.011, 0.019, 0.031, 0.012, 0.041)

    corr = calculate_correlation(a, b)

    assert corr > 0.95


def test_portfolio_heat_and_sector_concentration_are_detected():
    candidates = [
        PortfolioCandidate(
            symbol="NVDA",
            sector="Semiconductors",
            risk_tier="tier_1",
            position_size_multiplier=1.0,
            returns_20d=(0.01, 0.02, 0.03, 0.02, 0.04),
        ),
        PortfolioCandidate(
            symbol="AMD",
            sector="Semiconductors",
            risk_tier="tier_1",
            position_size_multiplier=1.0,
            returns_20d=(0.011, 0.019, 0.031, 0.022, 0.041),
        ),
        PortfolioCandidate(
            symbol="MU",
            sector="Semiconductors",
            risk_tier="tier_1",
            position_size_multiplier=1.0,
            returns_20d=(0.009, 0.018, 0.032, 0.021, 0.039),
        ),
    ]

    result = evaluate_portfolio_risk(candidates)

    assert result.portfolio_heat > 2.5
    assert len(result.concentration_warnings) >= 1
    assert len(result.correlation_warnings) >= 1
    assert "NVDA" in result.reduced_symbols


def test_diversified_portfolio_has_lower_risk_pressure():
    candidates = [
        PortfolioCandidate(
            symbol="AAPL",
            sector="Technology",
            risk_tier="tier_2",
            position_size_multiplier=0.5,
            returns_20d=(0.01, 0.02, 0.00, 0.01, 0.03),
        ),
        PortfolioCandidate(
            symbol="GLD",
            sector="Metals",
            risk_tier="tier_2",
            position_size_multiplier=0.5,
            returns_20d=(-0.01, 0.00, 0.01, -0.01, 0.00),
        ),
    ]

    result = evaluate_portfolio_risk(candidates)

    assert result.portfolio_heat < 2
    assert len(result.correlation_warnings) == 0
    assert "AAPL" in result.approved_symbols
