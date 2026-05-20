from datetime import date
from pathlib import Path

from src.watchers.entry_exit_watcher import (
    PriceBar,
    append_lifecycle_updates,
    evaluate_signal_against_bar,
    evaluate_signals,
    load_signal_file,
    save_alerts,
    save_updated_signal_file,
)


def _signal(**overrides):
    payload = {
        "symbol": "NVDA",
        "action": "BUY_WATCH",
        "status": "PENDING",
        "entry_trigger": 101.0,
        "stop_loss": 95.0,
        "target_1": 110.0,
        "target_2": 120.0,
        "valid_until": "2026-05-25",
        "generated_at": "2026-05-20T21:00:00Z",
    }
    payload.update(overrides)
    return payload


def test_pending_signal_triggers_entry_when_high_crosses_entry():
    signal = _signal()
    bar = PriceBar(symbol="NVDA", timestamp="2026-05-21T15:00:00Z", high=102.0, low=99.0, close=101.5)

    alert, update = evaluate_signal_against_bar(signal, bar, today=date(2026, 5, 21))

    assert alert is not None
    assert update is not None
    assert alert.alert_type == "ENTRY_TRIGGERED"
    assert alert.previous_status == "PENDING"
    assert alert.new_status == "TRIGGERED"
    assert update.signal["status"] == "TRIGGERED"
    assert update.signal["entry_price"] == 101.0


def test_triggered_signal_hits_stop_before_target_to_avoid_optimistic_bias():
    signal = _signal(status="TRIGGERED")
    bar = PriceBar(symbol="NVDA", timestamp="2026-05-21T17:30:00Z", high=111.0, low=94.0, close=100.0)

    alert, update = evaluate_signal_against_bar(signal, bar, today=date(2026, 5, 21))

    assert alert is not None
    assert update is not None
    assert alert.alert_type == "STOP_HIT"
    assert update.signal["status"] == "STOP_HIT"


def test_triggered_signal_hits_target_1():
    signal = _signal(status="TRIGGERED")
    bar = PriceBar(symbol="NVDA", timestamp="2026-05-21T17:30:00Z", high=110.5, low=100.0, close=110.0)

    alert, update = evaluate_signal_against_bar(signal, bar, today=date(2026, 5, 21))

    assert alert is not None
    assert update is not None
    assert alert.alert_type == "TARGET_1_HIT"
    assert update.signal["status"] == "TARGET_1_HIT"


def test_target_1_signal_hits_target_2():
    signal = _signal(status="TARGET_1_HIT")
    bar = PriceBar(symbol="NVDA", timestamp="2026-05-22T17:30:00Z", high=121.0, low=111.0, close=120.5)

    alert, update = evaluate_signal_against_bar(signal, bar, today=date(2026, 5, 22))

    assert alert is not None
    assert update is not None
    assert alert.alert_type == "TARGET_2_HIT"
    assert update.signal["status"] == "TARGET_2_HIT"


def test_pending_signal_expires_after_valid_until():
    signal = _signal(valid_until="2026-05-20")
    bar = PriceBar(symbol="NVDA", timestamp="2026-05-21T21:00:00Z", high=100.0, low=98.0, close=99.0)

    alert, update = evaluate_signal_against_bar(signal, bar, today=date(2026, 5, 21))

    assert alert is not None
    assert update is not None
    assert alert.alert_type == "EXPIRED"
    assert update.signal["status"] == "EXPIRED"


def test_terminal_signal_does_not_emit_new_alert():
    signal = _signal(status="STOP_HIT")
    bar = PriceBar(symbol="NVDA", timestamp="2026-05-22T17:30:00Z", high=130.0, low=90.0, close=120.0)

    alert, update = evaluate_signal_against_bar(signal, bar, today=date(2026, 5, 22))

    assert alert is None
    assert update is None


def test_evaluate_signals_updates_only_matching_symbols():
    signals = [_signal(symbol="NVDA"), _signal(symbol="AAPL")]
    bars = {
        "NVDA": PriceBar(symbol="NVDA", timestamp="2026-05-21T15:00:00Z", high=102.0, low=100.0, close=101.0)
    }

    alerts, updates, updated_signals = evaluate_signals(signals, bars, today=date(2026, 5, 21))

    assert len(alerts) == 1
    assert len(updates) == 1
    assert updated_signals[0]["status"] == "TRIGGERED"
    assert updated_signals[1]["status"] == "PENDING"


def test_persistence_helpers_write_alerts_lifecycle_and_updated_signals(tmp_path: Path):
    signal = _signal()
    bar = PriceBar(symbol="NVDA", timestamp="2026-05-21T15:00:00Z", high=102.0, low=100.0, close=101.5)
    alert, update = evaluate_signal_against_bar(signal, bar, today=date(2026, 5, 21))

    assert alert is not None
    assert update is not None

    alerts_dir = tmp_path / "alerts"
    dated, latest = save_alerts([alert], alerts_dir=alerts_dir, date_str="2026-05-21")
    assert dated.exists()
    assert latest.exists()

    lifecycle_path = append_lifecycle_updates([update], log_path=tmp_path / "signal_lifecycle.jsonl")
    assert lifecycle_path.exists()
    assert "ENTRY_TRIGGERED" in lifecycle_path.read_text(encoding="utf-8")

    signal_file = tmp_path / "signals.json"
    signal_file.write_text('{"signals": []}', encoding="utf-8")
    save_updated_signal_file(signal_file, [update.signal])

    loaded = load_signal_file(signal_file)
    assert loaded[0]["status"] == "TRIGGERED"
    assert (tmp_path / "latest-signals.json").exists()
