from __future__ import annotations

from datetime import date, datetime, timezone

from src.watchers.entry_exit_watcher import (
    PriceBar,
    build_price_bar_from_polygon,
    evaluate_signal_against_bar,
    evaluate_signals,
)


def _signal(status: str = "PENDING") -> dict:
    return {
        "symbol": "NVDA",
        "action": "BUY_WATCH",
        "status": status,
        "signal_date": "2026-05-21",
        "entry_trigger": 101.0,
        "stop_loss": 95.0,
        "target_1": 110.0,
        "target_2": 120.0,
        "valid_until": "2026-05-25",
    }


def test_incomplete_bar_does_not_trigger_pending_entry() -> None:
    bar = PriceBar(
        symbol="NVDA",
        timestamp="2026-05-21T15:00:00Z",
        high=102.0,
        low=99.0,
        close=101.5,
        is_complete=False,
        completion_source="intraday_partial",
    )

    alert, update = evaluate_signal_against_bar(
        _signal(),
        bar,
        today=date(2026, 5, 21),
    )

    assert alert is None
    assert update is None


def test_incomplete_bar_does_not_trigger_stop_or_target() -> None:
    bar = PriceBar(
        symbol="NVDA",
        timestamp="2026-05-21T15:00:00Z",
        high=111.0,
        low=94.0,
        close=100.0,
        is_complete=False,
        completion_source="intraday_partial",
    )

    alert, update = evaluate_signal_against_bar(
        _signal(status="TRIGGERED"),
        bar,
        today=date(2026, 5, 21),
    )

    assert alert is None
    assert update is None


def test_completed_bar_preserves_existing_entry_behavior() -> None:
    bar = PriceBar(
        symbol="NVDA",
        timestamp="2026-05-21T21:00:00Z",
        high=102.0,
        low=99.0,
        close=101.5,
        is_complete=True,
        completed_at="2026-05-21T21:00:00Z",
        completion_source="test_completed_bar",
    )

    alert, update = evaluate_signal_against_bar(
        _signal(),
        bar,
        today=date(2026, 5, 21),
    )

    assert alert is not None
    assert update is not None
    assert alert.alert_type == "ENTRY_TRIGGERED"
    assert update.signal["status"] == "TRIGGERED"


def test_evaluate_signals_preserves_signal_when_bar_is_incomplete() -> None:
    signals = [_signal()]
    bars = {
        "NVDA": PriceBar(
            symbol="NVDA",
            timestamp="2026-05-21T15:00:00Z",
            high=102.0,
            low=99.0,
            close=101.5,
            is_complete=False,
        )
    }

    alerts, updates, updated = evaluate_signals(
        signals,
        bars,
        today=date(2026, 5, 21),
    )

    assert alerts == []
    assert updates == []
    assert updated[0]["status"] == "PENDING"


def test_polygon_daily_bar_without_provider_flag_gets_completion_metadata() -> None:
    historical_day_ms = int(
        datetime(2026, 5, 21, tzinfo=timezone.utc).timestamp() * 1000
    )

    bar = build_price_bar_from_polygon(
        "NVDA",
        {"t": historical_day_ms, "o": 100.0, "h": 102.0, "l": 99.0, "c": 101.0},
    )

    assert bar.completion_source == "daily_bar_timestamp"
    assert bar.completed_at is not None


def test_polygon_provider_complete_flag_is_respected() -> None:
    current_day_ms = int(
        datetime(2026, 5, 21, tzinfo=timezone.utc).timestamp() * 1000
    )

    incomplete = build_price_bar_from_polygon(
        "NVDA",
        {
            "t": current_day_ms,
            "o": 100.0,
            "h": 102.0,
            "l": 99.0,
            "c": 101.0,
            "is_complete": False,
        },
    )
    complete = build_price_bar_from_polygon(
        "NVDA",
        {
            "t": current_day_ms,
            "o": 100.0,
            "h": 102.0,
            "l": 99.0,
            "c": 101.0,
            "is_complete": True,
        },
    )

    assert incomplete.is_complete is False
    assert incomplete.completion_source == "provider_flag"
    assert complete.is_complete is True
    assert complete.completion_source == "provider_flag"