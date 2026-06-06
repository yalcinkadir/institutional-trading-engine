from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

DATA_STATUS_OK = "ok"
DATA_STATUS_BLOCKED = "blocked"
DATA_STATUS_DEGRADED = "degraded"


def evaluate_signal_quality(signals: list[dict]) -> dict:
    if not signals:
        return {
            "signals": 0,
            "quality_score": 0,
            "classification": "Unknown",
        }

    profitable = [signal for signal in signals if signal.get("pnl_percent", 0) > 0]
    avg_pnl = sum(signal.get("pnl_percent", 0) for signal in signals) / len(signals)

    quality_score = round(
        ((len(profitable) / len(signals)) * 60) + max(avg_pnl, 0) * 4,
        2,
    )

    quality_score = min(quality_score, 100)

    if quality_score >= 80:
        classification = "Institutional Grade"
    elif quality_score >= 65:
        classification = "High Quality"
    elif quality_score >= 50:
        classification = "Moderate"
    else:
        classification = "Weak"

    return {
        "signals": len(signals),
        "quality_score": quality_score,
        "classification": classification,
    }


@dataclass(frozen=True)
class MarketDataPoint:
    symbol: str
    close: float | None
    atr: float | None
    source: str | None
    source_timestamp: str | None
    fallback_level: str | None = None
    fallback_status: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class MarketDataQualityEvent:
    symbol: str
    status: str
    reason: str
    source: str | None
    source_timestamp: str | None
    fallback_level: str | None
    fallback_status: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MarketDataQualityReport:
    status: str
    events: list[MarketDataQualityEvent]
    provenance: dict[str, dict[str, Any]]

    @property
    def passed(self) -> bool:
        return self.status == DATA_STATUS_OK

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "passed": self.passed,
            "events": [event.to_dict() for event in self.events],
            "provenance": self.provenance,
        }


def _parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    text = str(value).replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _is_number(value: Any) -> bool:
    if value in (None, ""):
        return False
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def evaluate_market_data_quality(
    points: list[MarketDataPoint],
    *,
    as_of: datetime,
    max_staleness_minutes: int,
) -> MarketDataQualityReport:
    events: list[MarketDataQualityEvent] = []
    provenance: dict[str, dict[str, Any]] = {}
    as_of_utc = as_of.astimezone(timezone.utc) if as_of.tzinfo else as_of.replace(tzinfo=timezone.utc)

    for point in points:
        symbol = point.symbol.upper()
        source_ts = _parse_timestamp(point.source_timestamp)
        provenance[symbol] = {
            "source": point.source,
            "source_timestamp": point.source_timestamp,
            "fallback_level": point.fallback_level,
            "fallback_status": point.fallback_status,
        }
        base = {
            "symbol": symbol,
            "source": point.source,
            "source_timestamp": point.source_timestamp,
            "fallback_level": point.fallback_level,
            "fallback_status": point.fallback_status,
        }
        if not point.source:
            events.append(MarketDataQualityEvent(status=DATA_STATUS_BLOCKED, reason="missing_source", **base))
        if source_ts is None:
            events.append(MarketDataQualityEvent(status=DATA_STATUS_BLOCKED, reason="missing_or_invalid_source_timestamp", **base))
        else:
            age_minutes = (as_of_utc - source_ts).total_seconds() / 60
            if age_minutes > max_staleness_minutes:
                events.append(MarketDataQualityEvent(status=DATA_STATUS_BLOCKED, reason="stale_source_timestamp", **base))
        if not point.fallback_level:
            events.append(MarketDataQualityEvent(status=DATA_STATUS_DEGRADED, reason="fallback_level_not_recorded", **base))
        if not point.fallback_status:
            events.append(MarketDataQualityEvent(status=DATA_STATUS_DEGRADED, reason="fallback_status_not_recorded", **base))
        if not _is_number(point.close):
            events.append(MarketDataQualityEvent(status=DATA_STATUS_BLOCKED, reason="missing_close", **base))
        if not _is_number(point.atr):
            events.append(MarketDataQualityEvent(status=DATA_STATUS_BLOCKED, reason="missing_atr", **base))

    if any(event.status == DATA_STATUS_BLOCKED for event in events):
        status = DATA_STATUS_BLOCKED
    elif events:
        status = DATA_STATUS_DEGRADED
    else:
        status = DATA_STATUS_OK
    return MarketDataQualityReport(status=status, events=events, provenance=provenance)


def attach_data_quality_to_signal(signal: dict[str, Any], report: MarketDataQualityReport) -> dict[str, Any]:
    symbol = str(signal.get("symbol") or "").upper()
    matching_events = [event.to_dict() for event in report.events if event.symbol == symbol]
    updated = dict(signal)
    updated["data_status"] = report.status if matching_events else DATA_STATUS_OK
    updated["data_quality_events"] = matching_events
    updated["provenance"] = report.provenance.get(symbol, {})
    return updated
