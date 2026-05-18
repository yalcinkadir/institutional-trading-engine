"""
Real-Time Monitoring Layer.

This module provides snapshot-based monitoring for institutional risk changes.
It is intentionally not tick-by-tick. The first robust version should monitor
meaningful state changes on 5m/15m/scheduled snapshots.

It detects:
- regime deterioration
- volatility spikes
- breadth deterioration
- leadership breakdown
- liquidity stress
- macro/event risk escalation
- autonomous risk reduction triggers
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass(frozen=True)
class MonitoringSnapshot:
    timestamp_utc: str
    market_state: str
    transition_score: float
    previous_transition_score: float
    volatility_stability_score: float
    previous_volatility_stability_score: float
    breadth_score: float
    previous_breadth_score: float
    sector_rotation_state: str
    previous_sector_rotation_state: str
    liquidity_score: float
    previous_liquidity_score: float
    event_risk_score: float
    previous_event_risk_score: float
    macro_risk_score: float
    previous_macro_risk_score: float
    risk_reduction_state: str
    previous_risk_reduction_state: str


@dataclass(frozen=True)
class MonitoringAlert:
    severity: AlertSeverity
    code: str
    message: str
    recommended_action: str


@dataclass(frozen=True)
class MonitoringAssessment:
    monitoring_state: str
    alerts: tuple[MonitoringAlert, ...]
    critical_count: int
    warning_count: int


def evaluate_realtime_monitoring(snapshot: MonitoringSnapshot) -> MonitoringAssessment:
    alerts: list[MonitoringAlert] = []

    transition_delta = snapshot.transition_score - snapshot.previous_transition_score
    volatility_delta = snapshot.volatility_stability_score - snapshot.previous_volatility_stability_score
    breadth_delta = snapshot.breadth_score - snapshot.previous_breadth_score
    liquidity_delta = snapshot.liquidity_score - snapshot.previous_liquidity_score
    event_delta = snapshot.event_risk_score - snapshot.previous_event_risk_score
    macro_delta = snapshot.macro_risk_score - snapshot.previous_macro_risk_score

    if transition_delta <= -15:
        alerts.append(
            MonitoringAlert(
                severity=AlertSeverity.CRITICAL,
                code="regime_transition_deterioration",
                message="Regime transition quality deteriorated sharply.",
                recommended_action="reduce_new_risk_and_review_market_state",
            )
        )
    elif transition_delta <= -8:
        alerts.append(
            MonitoringAlert(
                severity=AlertSeverity.WARNING,
                code="regime_transition_softening",
                message="Regime transition quality is weakening.",
                recommended_action="raise_entry_thresholds",
            )
        )

    if volatility_delta <= -15 or snapshot.volatility_stability_score <= 35:
        alerts.append(
            MonitoringAlert(
                severity=AlertSeverity.CRITICAL,
                code="volatility_instability_spike",
                message="Volatility stability deteriorated into a fragile zone.",
                recommended_action="cut_position_size_and_avoid_breakout_chasing",
            )
        )

    if breadth_delta <= -15 or snapshot.breadth_score <= 35:
        alerts.append(
            MonitoringAlert(
                severity=AlertSeverity.CRITICAL,
                code="breadth_deterioration",
                message="Market breadth deteriorated materially.",
                recommended_action="avoid_broad_beta_expansion",
            )
        )
    elif breadth_delta <= -8:
        alerts.append(
            MonitoringAlert(
                severity=AlertSeverity.WARNING,
                code="breadth_softening",
                message="Breadth is weakening versus the previous snapshot.",
                recommended_action="favor_only_strong_relative_strength_leaders",
            )
        )

    if (
        snapshot.previous_sector_rotation_state == "risk_on_offensive_leadership"
        and snapshot.sector_rotation_state in {"defensive_rotation", "mixed_rotation_transition"}
    ):
        alerts.append(
            MonitoringAlert(
                severity=AlertSeverity.WARNING,
                code="leadership_rotation_warning",
                message="Sector leadership rotated away from offensive risk-on leadership.",
                recommended_action="reduce_high_beta_and_monitor_defensive_rotation",
            )
        )

    if liquidity_delta <= -15 or snapshot.liquidity_score <= 35:
        alerts.append(
            MonitoringAlert(
                severity=AlertSeverity.CRITICAL,
                code="liquidity_stress_escalation",
                message="Liquidity conditions deteriorated sharply.",
                recommended_action="avoid_illiquid_entries_and_reduce_slippage_sensitive_exposure",
            )
        )

    if event_delta >= 20 or snapshot.event_risk_score >= 70:
        alerts.append(
            MonitoringAlert(
                severity=AlertSeverity.WARNING,
                code="event_risk_escalation",
                message="Event risk increased materially.",
                recommended_action="avoid_marginal_setups_until_event_risk_normalizes",
            )
        )

    if macro_delta <= -15 or snapshot.macro_risk_score <= 35:
        alerts.append(
            MonitoringAlert(
                severity=AlertSeverity.WARNING,
                code="macro_pressure_escalation",
                message="Macro risk backdrop deteriorated.",
                recommended_action="reduce_cyclical_high_beta_and_macro_sensitive_exposure",
            )
        )

    if (
        snapshot.previous_risk_reduction_state != snapshot.risk_reduction_state
        and snapshot.risk_reduction_state in {"risk_reduction_high", "risk_reduction_extreme"}
    ):
        alerts.append(
            MonitoringAlert(
                severity=AlertSeverity.CRITICAL,
                code="risk_governor_escalation",
                message="Autonomous risk governor escalated risk reduction state.",
                recommended_action="follow_risk_reduction_policy_before_new_entries",
            )
        )

    critical_count = sum(1 for alert in alerts if alert.severity == AlertSeverity.CRITICAL)
    warning_count = sum(1 for alert in alerts if alert.severity == AlertSeverity.WARNING)

    if critical_count >= 2:
        state = "critical_monitoring_alert"
    elif critical_count == 1:
        state = "elevated_monitoring_alert"
    elif warning_count >= 2:
        state = "monitoring_warning_cluster"
    elif warning_count == 1:
        state = "single_monitoring_warning"
    else:
        state = "monitoring_stable"

    return MonitoringAssessment(
        monitoring_state=state,
        alerts=tuple(alerts),
        critical_count=critical_count,
        warning_count=warning_count,
    )
