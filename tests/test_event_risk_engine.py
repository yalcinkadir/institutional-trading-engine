from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.event_risk_engine import (  # noqa: E402
    EVENT_RISK_LIVE_SOURCE,
    EVENT_RISK_PLACEHOLDER_SOURCE,
    EVENT_RISK_PLACEHOLDER_WARNING,
    EventRiskInput,
    EventSeverity,
    EventType,
    MarketEvent,
    evaluate_event_risk,
    placeholder_event_risk_assessment,
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
            event_risk_available=True,
            event_risk_source=EVENT_RISK_LIVE_SOURCE,
            event_risk_confidence="high",
        )
    )

    assert result.event_risk_state == "critical_event_risk"
    assert result.event_risk_score >= 75
    assert "pre_event_risk:fomc" in result.warnings
    assert result.event_risk_available is True
    assert result.event_risk_source == EVENT_RISK_LIVE_SOURCE
    assert result.event_risk_confidence == "high"
    assert result.event_risk_is_placeholder is False
    assert EVENT_RISK_PLACEHOLDER_WARNING not in result.warnings


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
            event_risk_available=True,
            event_risk_source=EVENT_RISK_LIVE_SOURCE,
            event_risk_confidence="medium",
        )
    )

    assert result.event_risk_state == "contained_event_risk"
    assert result.event_risk_score < 30
    assert "no_major_near_term_event_pressure" in result.confirmations
    assert result.event_risk_is_placeholder is False


def test_default_event_risk_input_is_marked_as_placeholder():
    result = evaluate_event_risk(
        EventRiskInput(
            now_utc="2026-05-18T12:00:00+00:00",
            events=(),
            vix=14,
            volatility_expansion=False,
        )
    )

    assert result.event_risk_available is False
    assert result.event_risk_source == EVENT_RISK_PLACEHOLDER_SOURCE
    assert result.event_risk_confidence == "low"
    assert result.event_risk_is_placeholder is True
    assert EVENT_RISK_PLACEHOLDER_WARNING in result.warnings
    assert result.risk_action.endswith("_with_unverified_event_calendar")


def test_placeholder_event_risk_assessment_factory_is_explicit():
    result = placeholder_event_risk_assessment(score=20)

    assert result.event_risk_state == "event_risk_placeholder"
    assert result.event_risk_score == 20
    assert result.event_risk_available is False
    assert result.event_risk_source == EVENT_RISK_PLACEHOLDER_SOURCE
    assert result.event_risk_confidence == "low"
    assert result.event_risk_is_placeholder is True
    assert result.active_events == ()
    assert result.warnings == (EVENT_RISK_PLACEHOLDER_WARNING,)
    assert result.risk_action == "do_not_treat_event_risk_as_live_calendar_verified"


def test_placeholder_event_risk_assessment_score_is_clamped():
    assert placeholder_event_risk_assessment(score=-5).event_risk_score == 0
    assert placeholder_event_risk_assessment(score=150).event_risk_score == 100
