from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from market_internal_quality import (  # noqa: E402
    MarketInternalSnapshot,
    evaluate_market_internal_quality,
)


def test_aggressive_environment_detected_when_breadth_and_followthrough_are_strong():
    snapshot = MarketInternalSnapshot(
        breadth_percent=78,
        breakout_success_rate=0.71,
        failed_breakout_rate=0.18,
        new_highs=180,
        new_lows=32,
        leaders_above_sma50_percent=82,
        opportunities_detected=15,
    )

    result = evaluate_market_internal_quality(snapshot)

    assert result.environment == "aggressive_risk_allowed"
    assert result.quality_score >= 75
    assert result.opportunity_density == "high"
    assert "strong_breadth" in result.confirmations


def test_capital_preservation_environment_detected_when_failures_expand():
    snapshot = MarketInternalSnapshot(
        breadth_percent=32,
        breakout_success_rate=0.28,
        failed_breakout_rate=0.66,
        new_highs=25,
        new_lows=160,
        leaders_above_sma50_percent=33,
        opportunities_detected=2,
    )

    result = evaluate_market_internal_quality(snapshot)

    assert result.environment == "capital_preservation"
    assert result.quality_score <= 40
    assert result.opportunity_density == "low"
    assert "failed_breakout_cluster" in result.warnings
