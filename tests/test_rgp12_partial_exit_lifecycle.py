from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from src.watchers.entry_exit_watcher import (
    PriceBar,
    append_lifecycle_updates,
    evaluate_signal_against_bar,
)


def _triggered_signal(**overrides):
    payload = {
        "symbol": "NVDA",
        "action": "BUY_WATCH",
        "status": "TRIGGERED",
        "entry_trigger": 101.0,
        "entry_price": 101.0,
        "stop_loss": 95.0,
        "target_1": 110.0,
        "target_2": 120.0,
        "atr14": 4.0,
        "valid_until": "2026-05-25",
        "generated_at": "2026-05-20T21:00:00Z",
        "signal_id": "stable-id",
    }
    payload.update(overrides)
    return payload


def test_target_1_hit_carries_partial_exit_lifecycle_supplemental_event() -> None:
    signal = _triggered_signal()
    bar = PriceBar(
        symbol="NVDA",
        timestamp="2026-05-21T17:30:00Z",
        high=110.5,
        low=100.0,
        close=110.0,
    )

    alert, update = evaluate_signal_against_bar(signal, bar, today=date(2026, 5, 21))

    assert alert is not None
    assert update is not None
    assert update.event_type == "TARGET_1_HIT"
    assert update.signal["partial_exit_completed"] is True
    assert update.supplemental_events == [
        {
            "signal_id": "stable-id",
            "symbol": "NVDA",
            "signal_date": "2026-05-20",
            "timestamp": "2026-05-21T17:30:00Z",
            "previous_status": "TRIGGERED",
            "new_status": "TARGET_1_HIT",
            "event_type": "PARTIAL_EXIT_FILLED",
            "price": 110.0,
            "signal": update.signal,
            "reasons": ["target_1_hit_runner_activated"],
        }
    ]


def test_append_lifecycle_updates_persists_target_1_and_partial_exit_events(tmp_path: Path) -> None:
    signal = _triggered_signal()
    bar = PriceBar(
        symbol="NVDA",
        timestamp="2026-05-21T17:30:00Z",
        high=110.5,
        low=100.0,
        close=110.0,
    )
    _, update = evaluate_signal_against_bar(signal, bar, today=date(2026, 5, 21))
    assert update is not None

    lifecycle_path = append_lifecycle_updates([update], log_path=tmp_path / "signal_lifecycle.jsonl")

    events = [json.loads(line)["event_type"] for line in lifecycle_path.read_text().splitlines()]
    assert events == ["TARGET_1_HIT", "PARTIAL_EXIT_FILLED"]


def test_append_lifecycle_updates_deduplicates_partial_exit_event(tmp_path: Path) -> None:
    signal = _triggered_signal()
    bar = PriceBar(
        symbol="NVDA",
        timestamp="2026-05-21T17:30:00Z",
        high=110.5,
        low=100.0,
        close=110.0,
    )
    _, update = evaluate_signal_against_bar(signal, bar, today=date(2026, 5, 21))
    assert update is not None

    lifecycle_path = tmp_path / "signal_lifecycle.jsonl"
    append_lifecycle_updates([update], log_path=lifecycle_path)
    append_lifecycle_updates([update], log_path=lifecycle_path)

    events = [json.loads(line)["event_type"] for line in lifecycle_path.read_text().splitlines()]
    assert events == ["TARGET_1_HIT", "PARTIAL_EXIT_FILLED"]
