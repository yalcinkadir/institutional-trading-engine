from src.research.earnings_intelligence import analyze_earnings_risk
from src.research.event_risk import evaluate_event_risk
from src.research.narrative_engine import detect_market_narratives
from src.research.news_sentiment import analyze_news_sentiment


def test_news_sentiment():
    result = analyze_news_sentiment(
        [
            {"sentiment": "positive"},
            {"sentiment": "positive"},
            {"sentiment": "neutral"},
        ]
    )

    assert result["classification"] == "Positive News Flow"


def test_narrative_engine():
    result = detect_market_narratives(
        [
            {"narrative": "AI Growth"},
            {"narrative": "AI Growth"},
            {"narrative": "Defensive Rotation"},
        ]
    )

    assert result["dominant_narrative"] == "AI Growth"


def test_event_risk():
    result = evaluate_event_risk(
        [
            {"event": "FOMC", "severity": "high"},
            {"event": "CPI", "severity": "medium"},
        ]
    )

    assert result["classification"] in {
        "Moderate Event Risk",
        "High Event Risk",
    }


def test_earnings_risk():
    result = analyze_earnings_risk(
        days_until_earnings=2,
        implied_move_percent=12,
    )

    assert result["classification"] == "High Earnings Risk"
