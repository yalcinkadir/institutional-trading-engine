from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from portfolio_risk import PortfolioCandidate, evaluate_portfolio_risk  # noqa: E402


def test_er9_high_correlation_reduces_only_involved_symbols():
    candidates = [
        PortfolioCandidate(
            symbol="NVDA",
            sector="Semiconductors",
            risk_tier="tier_2",
            position_size_multiplier=0.5,
            returns_20d=(0.01, 0.02, 0.03, 0.02, 0.04),
        ),
        PortfolioCandidate(
            symbol="AMD",
            sector="Semiconductors",
            risk_tier="tier_2",
            position_size_multiplier=0.5,
            returns_20d=(0.011, 0.019, 0.031, 0.022, 0.041),
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
    multipliers = dict(result.symbol_risk_multipliers)

    assert set(result.reduced_symbols) == {"NVDA", "AMD"}
    assert "GLD" in result.approved_symbols
    assert multipliers["NVDA"] < 1.0
    assert multipliers["AMD"] < 1.0
    assert multipliers["GLD"] == 1.0


def test_er9_sector_concentration_reduces_only_involved_sector():
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
            returns_20d=(-0.01, 0.01, -0.02, 0.01, 0.00),
        ),
        PortfolioCandidate(
            symbol="GLD",
            sector="Metals",
            risk_tier="tier_2",
            position_size_multiplier=0.5,
            returns_20d=(0.00, -0.01, 0.01, 0.00, -0.01),
        ),
    ]

    result = evaluate_portfolio_risk(candidates)
    multipliers = dict(result.symbol_risk_multipliers)

    assert set(result.reduced_symbols) == {"NVDA", "AMD"}
    assert "GLD" in result.approved_symbols
    assert multipliers["NVDA"] < 1.0
    assert multipliers["AMD"] < 1.0
    assert multipliers["GLD"] == 1.0
