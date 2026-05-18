from src.portfolio.correlation_engine import calculate_portfolio_correlation
from src.portfolio.exposure_manager import (
    calculate_exposure,
    classify_exposure_risk,
)
from src.portfolio.position_optimizer import optimize_position_sizes
from src.portfolio.sector_risk import (
    analyze_sector_risk,
    classify_sector_risk,
)


def test_exposure_manager():
    positions = [
        {"ticker": "NVDA", "market_value": 6000},
        {"ticker": "MSFT", "market_value": 4000},
    ]

    result = calculate_exposure(positions)

    assert result["total_value"] == 10000
    assert result["largest_position_percent"] == 60
    assert classify_exposure_risk(60) == "High Concentration Risk"


def test_correlation_engine():
    positions = [
        {"ticker": "NVDA", "correlation": 0.9},
        {"ticker": "MSFT", "correlation": 0.8},
    ]

    result = calculate_portfolio_correlation(positions)

    assert result["average_correlation"] >= 0.8
    assert result["classification"] == "Highly Correlated"


def test_sector_risk():
    positions = [
        {"ticker": "NVDA", "market_value": 7000, "sector": "Technology"},
        {"ticker": "XOM", "market_value": 3000, "sector": "Energy"},
    ]

    result = analyze_sector_risk(positions)

    assert result["highest_sector_exposure"] == 70
    assert classify_sector_risk(70) == "Extreme Sector Concentration"


def test_position_optimizer():
    positions = [
        {"ticker": "NVDA", "exposure_percent": 35},
        {"ticker": "GLD", "exposure_percent": 8},
    ]

    optimized = optimize_position_sizes(positions, max_position_percent=20)

    assert optimized[0]["position_recommendation"] == "REDUCE"
    assert optimized[1]["position_recommendation"] == "CAN_INCREASE"
