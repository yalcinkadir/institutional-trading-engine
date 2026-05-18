from src.core.conflict_resolution import resolve_signal_conflicts
from src.core.conviction_engine import calculate_conviction
from src.core.decision_fusion import fuse_decision_signals
from src.core.final_recommendation import generate_final_recommendation


def test_decision_fusion():
    result = fuse_decision_signals(
        {
            "market": {"score": 80, "weight": 0.4},
            "research": {"score": 70, "weight": 0.3},
            "technical": {"score": 90, "weight": 0.3},
        }
    )

    assert result["fusion_score"] >= 75
    assert result["classification"] in {
        "Strong Bullish Bias",
        "Bullish Bias",
    }


def test_conviction_engine():
    result = calculate_conviction(
        fusion_score=82,
        confidence_score=80,
        signal_quality_score=78,
        macro_score=75,
    )

    assert result["conviction_score"] >= 75
    assert result["level"] in {
        "Institutional High Conviction",
        "High Conviction",
    }


def test_conflict_resolution():
    result = resolve_signal_conflicts(
        {
            "market": "bullish",
            "macro": "bullish",
            "research": "bearish",
        }
    )

    assert result["resolution"] == "Bullish Consensus"


def test_final_recommendation():
    result = generate_final_recommendation(
        conviction_score=88,
        conflict_resolution="Bullish Consensus",
        setup_status="READY",
    )

    assert result["recommendation"] == "STRONG BUY"
