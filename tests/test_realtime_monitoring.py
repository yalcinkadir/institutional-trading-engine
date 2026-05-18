from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.realtime_monitoring import (  # noqa: E402
    MonitoringSnapshot,
    evaluate_realtime_monitoring,
)


def test_critical_monitoring_alert_detected_under_multi_layer_deterioration():
    result = evaluate_realtime_monitoring(
        MonitoringSnapshot(
            timestamp_utc="2026-05-18T18:00:00+00:00",
            market_state="transition_fragile",
            transition_score=34,
            previous_transition_score=61,
            volatility_stability_score=31,
            previous_volatility_stability_score=57,
            breadth_score=29,
            previous_breadth_score=55,
            sector_rotation_state="defensive_rotation",
            previous_sector_rotation_state="risk_on_offensive_leadership",
            liquidity_score=27,
            previous_liquidity_score=51,
            event_risk_score=78,
            previous_event_risk_score=42,
            macro_risk_score=33,
            previous_macro_risk_score=58,
            risk_reduction_state="risk_reduction_extreme",
            previous_risk_reduction_state="risk_reduction_light",
        )
    )

    assert result.monitoring_state == "critical_monitoring_alert"
    assert result.critical_count >= 2


def test_monitoring_stable_when_conditions_remain_constructive():
    result = evaluate_realtime_monitoring(
        MonitoringSnapshot(
            timestamp_utc="2026-05-18T18:00:00+00:00",
            market_state="risk_on",
            transition_score=82,
            previous_transition_score=79,
            volatility_stability_score=80,
            previous_volatility_stability_score=78,
            breadth_score=77,
            previous_breadth_score=74,
            sector_rotation_state="risk_on_offensive_leadership",
            previous_sector_rotation_state="risk_on_offensive_leadership",
            liquidity_score=79,
            previous_liquidity_score=76,
            event_risk_score=18,
            previous_event_risk_score=16,
            macro_risk_score=76,
            previous_macro_risk_score=74,
            risk_reduction_state="normal_risk_allowed",
            previous_risk_reduction_state="normal_risk_allowed",
        )
    )

    assert result.monitoring_state == "monitoring_stable"
    assert result.critical_count == 0
