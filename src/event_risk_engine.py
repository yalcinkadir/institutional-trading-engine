"""
Event Risk Engine.

Institutional systems must evaluate whether it is the right time to take risk.
A strong setup can still be a poor decision directly before CPI, FOMC, NFP,
OPEX or major earnings clusters.

This module evaluates:
- event severity
- time until event
- pre-event risk compression
- post-event stabilization window
- earnings cluster risk
- volatility interaction

It is deterministic, explainable and testable.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class EventType(str, Enum):
    CPI = "cpi"
    FOMC = "fomc"
    NFP = "nfp"
    PPI = "ppi"
    OPEX = "opex"
    TREASURY_AUCTION = "treasury_auction"
    EARNINGS = "earnings"
    EARNINGS_CLUSTER = "earnings_cluster"
    OTHER = "other"


class EventSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class MarketEvent:
    event_type: EventType
    timestamp_utc: str
    severity: EventSeverity
    description: str = ""
    affected_symbols: tuple[str, ...] = ()
    affected_sectors: tuple[str, ...] = ()


@dataclass(frozen=True)
class EventRiskInput:
    now_utc: str
    events: tuple[MarketEvent, ...]
    vix: float
    volatility_expansion: bool
    target_symbol: str | None = None
    target_sector: str | None = None


@dataclass(frozen=True)
class EventRiskAssessment:
    event_risk_state: str
    event_risk_score: int
    risk_action: str
    active_events: tuple[str, ...]
    warnings: tuple[str, ...]
    confirmations: tuple[str, ...]


SEVERITY_POINTS = {
    EventSeverity.LOW: 8,
    EventSeverity.MEDIUM: 18,
    EventSeverity.HIGH: 30,
    EventSeverity.CRITICAL: 45,
}


def _parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _hours_until(now: datetime, event_time: datetime) -> float:
    return (event_time - now).total_seconds() / 3600


def _event_relevance(event: MarketEvent, symbol: str | None, sector: str | None) -> float:
    if event.event_type in {
        EventType.CPI,
        EventType.FOMC,
        EventType.NFP,
        EventType.PPI,
        EventType.OPEX,
        EventType.TREASURY_AUCTION,
    }:
        return 1.0

    if symbol and symbol in event.affected_symbols:
        return 1.0

    if sector and sector in event.affected_sectors:
        return 0.75

    if event.event_type == EventType.EARNINGS_CLUSTER:
        return 0.70

    return 0.25


def evaluate_event_risk(data: EventRiskInput) -> EventRiskAssessment:
    now = _parse_utc(data.now_utc)
    score = 0
    warnings: list[str] = []
    confirmations: list[str] = []
    active_events: list[str] = []

    for event in data.events:
        event_time = _parse_utc(event.timestamp_utc)
        hours = _hours_until(now, event_time)
        abs_hours = abs(hours)

        relevance = _event_relevance(event, data.target_symbol, data.target_sector)
        base_points = SEVERITY_POINTS[event.severity] * relevance

        if 0 <= hours <= 24:
            multiplier = 1.25
            warnings.append(f"pre_event_risk:{event.event_type.value}")
        elif 24 < hours <= 72:
            multiplier = 0.75
            warnings.append(f"upcoming_event:{event.event_type.value}")
        elif -24 <= hours < 0:
            multiplier = 1.0
            warnings.append(f"post_event_stabilization_window:{event.event_type.value}")
        elif -72 <= hours < -24:
            multiplier = 0.35
        else:
            multiplier = 0.0

        event_score = int(base_points * multiplier)
        if event_score > 0:
            score += event_score
            active_events.append(event.event_type.value)

    if data.volatility_expansion:
        score += 15
        warnings.append("event_risk_amplified_by_volatility_expansion")

    if data.vix >= 25:
        score += 15
        warnings.append("event_risk_amplified_by_high_vix")
    elif data.vix <= 16:
        confirmations.append("low_vix_reduces_event_risk")

    score = max(0, min(100, score))

    if score >= 75:
        event_state = "critical_event_risk"
        risk_action = "block_aggressive_entries_and_reduce_existing_risk"
    elif score >= 55:
        event_state = "high_event_risk"
        risk_action = "reduce_position_size_and_raise_entry_thresholds"
    elif score >= 30:
        event_state = "moderate_event_risk"
        risk_action = "avoid_marginal_setups"
    else:
        event_state = "contained_event_risk"
        risk_action = "normal_event_protocol"
        confirmations.append("no_major_near_term_event_pressure")

    return EventRiskAssessment(
        event_risk_state=event_state,
        event_risk_score=score,
        risk_action=risk_action,
        active_events=tuple(sorted(set(active_events))),
        warnings=tuple(dict.fromkeys(warnings)),
        confirmations=tuple(dict.fromkeys(confirmations)),
    )
