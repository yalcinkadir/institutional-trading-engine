from __future__ import annotations

from datetime import datetime, timezone

from src.analytics.signal_quality import (
    DATA_STATUS_BLOCKED,
    DATA_STATUS_DEGRADED,
    DATA_STATUS_OK,
    MarketDataPoint,
    attach_data_quality_to_signal,
    evaluate_market_data_quality,
)


def _as_of() -> datetime:
    return datetime(2026, 6, 6, 12, 0, tzinfo=timezone.utc)


def test_data1_valid_market_data_passes_with_provenance_and_fallback_recorded() -> None:
    report = evaluate_market_data_quality(
        [
            MarketDataPoint(
                symbol="SPY",
                close=101.2,
                atr=1.4,
                source="polygon",
                source_timestamp="2026-06-06T11:59:00Z",
                fallback_level="primary",
                fallback_status="not_needed",
            )
        ],
        as_of=_as_of(),
        max_staleness_minutes=5,
    )

    assert report.status == DATA_STATUS_OK
    assert report.passed is True
    assert report.events == []
    assert report.provenance["SPY"]["source"] == "polygon"
    assert report.provenance["SPY"]["fallback_level"] == "primary"


def test_data1_missing_close_blocks_before_signals_or_reports() -> None:
    report = evaluate_market_data_quality(
        [
            MarketDataPoint(
                symbol="SPY",
                close=None,
                atr=1.4,
                source="polygon",
                source_timestamp="2026-06-06T11:59:00Z",
                fallback_level="primary",
                fallback_status="not_needed",
            )
        ],
        as_of=_as_of(),
        max_staleness_minutes=5,
    )

    assert report.status == DATA_STATUS_BLOCKED
    assert any(event.reason == "missing_close" for event in report.events)


def test_data1_missing_atr_blocks_before_signals_or_reports() -> None:
    report = evaluate_market_data_quality(
        [
            MarketDataPoint(
                symbol="SPY",
                close=101.2,
                atr=None,
                source="polygon",
                source_timestamp="2026-06-06T11:59:00Z",
                fallback_level="primary",
                fallback_status="not_needed",
            )
        ],
        as_of=_as_of(),
        max_staleness_minutes=5,
    )

    assert report.status == DATA_STATUS_BLOCKED
    assert any(event.reason == "missing_atr" for event in report.events)


def test_data1_stale_timestamp_blocks_market_data() -> None:
    report = evaluate_market_data_quality(
        [
            MarketDataPoint(
                symbol="SPY",
                close=101.2,
                atr=1.4,
                source="polygon",
                source_timestamp="2026-06-06T11:00:00Z",
                fallback_level="primary",
                fallback_status="not_needed",
            )
        ],
        as_of=_as_of(),
        max_staleness_minutes=5,
    )

    assert report.status == DATA_STATUS_BLOCKED
    assert any(event.reason == "stale_source_timestamp" for event in report.events)


def test_data1_fallback_unrecorded_is_degraded_not_silent() -> None:
    report = evaluate_market_data_quality(
        [
            MarketDataPoint(
                symbol="SPY",
                close=101.2,
                atr=1.4,
                source="polygon",
                source_timestamp="2026-06-06T11:59:00Z",
                fallback_level=None,
                fallback_status=None,
            )
        ],
        as_of=_as_of(),
        max_staleness_minutes=5,
    )

    assert report.status == DATA_STATUS_DEGRADED
    assert any(event.reason == "fallback_level_not_recorded" for event in report.events)
    assert any(event.reason == "fallback_status_not_recorded" for event in report.events)


def test_data1_signal_consumes_same_data_quality_status_and_provenance() -> None:
    report = evaluate_market_data_quality(
        [
            MarketDataPoint(
                symbol="SPY",
                close=None,
                atr=1.4,
                source="polygon",
                source_timestamp="2026-06-06T11:59:00Z",
                fallback_level="primary",
                fallback_status="not_needed",
            )
        ],
        as_of=_as_of(),
        max_staleness_minutes=5,
    )

    signal = attach_data_quality_to_signal({"symbol": "SPY", "action": "NO_TRADE"}, report)

    assert signal["data_status"] == DATA_STATUS_BLOCKED
    assert signal["provenance"]["source"] == "polygon"
    assert signal["data_quality_events"][0]["reason"] == "missing_close"
