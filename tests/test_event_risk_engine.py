from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.event_risk_engine import (  # noqa: E402
    EventRiskInput,
    EventSeverity,
    EventType,
    MarketEvent,
    evaluate_event_risk,
)


def test_critical_event_risk_detected_before_fomc_and_cpi():
    result = evaluate_event_risk(
        EventRiskInput(
            now_utc="2026-05-18T12:00:00+00:00",
            events=(
                MarketEvent(
                    event_type=EventType.FOMC,
                    timestamp_utc="2026-05-18T20:00:00+00:00",
                    severity=EventSeverity.CRITICAL,
                ),
                MarketEvent(
                    event_type=EventType.CPI,
                    timestamp_utc="2026-05-19T12:00:00+00:00",
                    severity=EventSeverity.HIGH,
                ),
            ),
            vix=28,
            volatility_expansion=True,
        )
    )

    assert result.event_risk_state == "critical_event_risk"
    assert result.event_risk_score >= 75
    assert "pre_event_risk:fomc" in result.warnings


def test_contained_event_risk_when_no_major_events_are_near():
    result = evaluate_event_risk(
        EventRiskInput(
            now_utc="2026-05-18T12:00:00+00:00",
            events=(
                MarketEvent(
                    event_type=EventType.OTHER,
                    timestamp_utc="2026-05-28T12:00:00+00:00",
                    severity=EventSeverity.LOW,
                ),
            ),
            vix=14,
            volatility_expansion=False,
        )
    )

    assert result.event_risk_state == "contained_event_risk"
    assert result.event_risk_score < 30
    assert "no_major_near_term_event_pressure" in result.confirmations
