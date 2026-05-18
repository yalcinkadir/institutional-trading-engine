from src.relative_strength.relative_strength import (
    calculate_relative_strength,
    classify_relative_strength,
)
from src.scoring.asset_score import calculate_asset_score
from src.screening.asset_ranker import rank_assets
from src.screening.leader_detector import detect_leaders
from src.screening.weak_name_detector import detect_weak_names
from src.reporting.trade_summary import build_trade_summary


def test_relative_strength_classification():
    assert calculate_relative_strength(12, 10) == 1.2
    assert classify_relative_strength(1.25) == "Leader"
    assert classify_relative_strength(1.0) == "Neutral"
    assert classify_relative_strength(0.7) == "Weak"


def test_asset_score_status_bands():
    strong = calculate_asset_score(25, 25, 20, 10, 10)
    ready = calculate_asset_score(20, 20, 15, 10, 10)
    weak = calculate_asset_score(10, 10, 5, 5, 5)

    assert strong["score"] == 90
    assert strong["status"] == "Strong Ready"
    assert ready["status"] == "Ready"
    assert weak["status"] == "Weak"


def test_rank_assets_orders_by_score_descending():
    assets = [
        {"ticker": "AAPL", "score": 70},
        {"ticker": "NVDA", "score": 91},
        {"ticker": "MSFT", "score": 84},
    ]

    ranked = rank_assets(assets)

    assert [asset["ticker"] for asset in ranked] == ["NVDA", "MSFT", "AAPL"]


def test_leader_and_weak_name_detection():
    assets = [
        {"ticker": "NVDA", "score": 91},
        {"ticker": "MSFT", "score": 80},
        {"ticker": "INTC", "score": 40},
    ]

    leaders = detect_leaders(assets)
    weak_names = detect_weak_names(assets)

    assert [asset["ticker"] for asset in leaders] == ["NVDA", "MSFT"]
    assert [asset["ticker"] for asset in weak_names] == ["INTC"]


def test_trade_summary_contains_required_sections():
    leaders = [
        {"ticker": "NVDA", "score": 91, "status": "Strong Ready"},
        {"ticker": "MSFT", "score": 80, "status": "Ready"},
    ]
    weak_names = [{"ticker": "INTC", "score": 40, "status": "Weak"}]

    summary = build_trade_summary("Bullish", 82, leaders, weak_names)

    assert "TRADE SUMMARY" in summary
    assert "Market Regime: Bullish" in summary
    assert "Market Health Score: 82" in summary
    assert "Top Leaders:" in summary
    assert "Weak Names:" in summary
    assert "NVDA" in summary
    assert "INTC" in summary
