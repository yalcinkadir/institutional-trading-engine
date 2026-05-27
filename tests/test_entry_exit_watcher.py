from datetime import date
import json
from pathlib import Path

from src.signals.signal_identity import build_signal_id, ensure_signal_identity
from src.watchers.entry_exit_watcher import (
    PriceBar,
    append_lifecycle_updates,
    evaluate_regime_invalidation,
    evaluate_regime_invalidations,
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


def test_build_signal_id_is_deterministic_for_same_signal():
    signal = _signal()

    assert build_signal_id(signal) == build_signal_id(dict(signal))


def test_build_signal_id_changes_for_material_signal_fields():
    signal = _signal()
    changed = _signal(entry_trigger=102.0)

    assert build_signal_id(signal) != build_signal_id(changed)


def test_ensure_signal_identity_preserves_existing_signal_id():
    signal = _signal(signal_id="existing-id")

    result = ensure_signal_identity(signal)

    assert result["signal_id"] == "existing-id"


def test_pending_signal_invalidates_before_entry_when_stop_is_breached():
    signal = _signal(signal_id="gap-risk-id")
    bar = PriceBar(symbol="NVDA", timestamp="2026-05-21T13:30:00Z", high=100.0, low=94.0, close=96.0)

    alert, update = evaluate_signal_against_bar(signal, bar, today=date(2026, 5, 21))

    assert alert is not None
    assert update is not None
    assert alert.alert_type == "INVALIDATED_BEFORE_ENTRY"
    assert alert.previous_status == "PENDING"
    assert alert.new_status == "INVALIDATED_BEFORE_ENTRY"
    assert alert.trigger_price == 95.0
    assert update.event_type == "INVALIDATED_BEFORE_ENTRY"
    assert update.signal["status"] == "INVALIDATED_BEFORE_ENTRY"
    assert update.signal["last_event_price"] == 95.0


def test_pending_signal_invalidates_before_entry_when_same_bar_touches_entry_and_stop():
    signal = _signal(signal_id="same-bar-risk-id")
    bar = PriceBar(symbol="NVDA", timestamp="2026-05-21T13:30:00Z", high=102.0, low=94.0, close=101.0)

    alert, update = evaluate_signal_against_bar(signal, bar, today=date(2026, 5, 21))

    assert alert is not None
    assert update is not None
    assert alert.alert_type == "INVALIDATED_BEFORE_ENTRY"
    assert update.signal["status"] == "INVALIDATED_BEFORE_ENTRY"
    assert "entry_triggered_at" not in update.signal
    assert "entry_price" not in update.signal


def test_invalidated_before_entry_is_terminal_and_never_retriggers():
    signal = _signal(status="INVALIDATED_BEFORE_ENTRY", signal_id="terminal-id")
    bar = PriceBar(symbol="NVDA", timestamp="2026-05-22T13:30:00Z", high=130.0, low=120.0, close=125.0)

    alert, update = evaluate_signal_against_bar(signal, bar, today=date(2026, 5, 22))

    assert alert is None
    assert update is None


def test_pending_signal_triggers_entry_when_high_crosses_entry():
    signal = _signal()
    bar = PriceBar(symbol="NVDA", timestamp="2026-05-21T15:00:00Z", high=102.0, low=99.0, close=101.5)

    alert, update = evaluate_signal_against_bar(signal, bar, today=date(2026, 5, 21))

    assert alert is not None
    assert update is not None
    assert alert.alert_type == "ENTRY_TRIGGERED"
    assert alert.previous_status == "PENDING"
    assert alert.new_status == "TRIGGERED"
    assert alert.signal_id.startswith("sig_NVDA_")
    assert update.signal_id == alert.signal_id
    assert update.signal["signal_id"] == alert.signal_id
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


def test_triggered_signal_hits_target_1_and_activates_runner():
    signal = _signal(status="TRIGGERED", atr14=4.0)
    bar = PriceBar(symbol="NVDA", timestamp="2026-05-21T17:30:00Z", high=110.5, low=100.0, close=110.0)

    alert, update = evaluate_signal_against_bar(signal, bar, today=date(2026, 5, 21))

    assert alert is not None
    assert update is not None
    assert alert.alert_type == "TARGET_1_HIT"
    assert alert.stop_loss == 104.5
    assert update.signal["status"] == "TARGET_1_HIT"
    assert update.signal["partial_exit_completed"] is True
    assert update.signal["partial_exit_ratio"] == 0.5
    assert update.signal["runner_status"] == "active"
    assert update.signal["stop_loss"] == 104.5
    assert update.signal["trail_stop"] == 104.5


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


def test_regime_invalidation_emits_alert_and_lifecycle_update():
    signal = _signal(status="TARGET_1_HIT", signal_id="stable-id", last_event_price=110.0)

    alert, update = evaluate_regime_invalidation(
        signal,
        regime={"risk_state": "Risk-Off"},
        timestamp="2026-05-21T20:00:00Z",
    )

    assert alert is not None
    assert update is not None
    assert alert.alert_type == "REGIME_INVALIDATION_EXIT"
    assert alert.previous_status == "TARGET_1_HIT"
    assert alert.new_status == "CANCELLED_BY_REGIME_CHANGE"
    assert alert.price == 110.0
    assert update.event_type == "REGIME_INVALIDATION_EXIT"
    assert update.signal["status"] == "CANCELLED_BY_REGIME_CHANGE"
    assert update.signal["regime_invalidation_reason"] == "risk off"


def test_regime_invalidation_cancels_pending_signal():
    signal = _signal(status="PENDING", signal_id="stable-id")

    alert, update = evaluate_regime_invalidation(
        signal,
        regime="Risk-Off",
        timestamp="2026-05-21T20:00:00Z",
    )

    assert alert is not None
    assert update is not None
    assert alert.alert_type == "REGIME_INVALIDATION_EXIT"
    assert alert.previous_status == "PENDING"
    assert alert.new_status == "CANCELLED_BY_REGIME_CHANGE"
    assert update.signal["status"] == "CANCELLED_BY_REGIME_CHANGE"


def test_regime_invalidation_ignores_non_risk_off_regime():
    signal = _signal(status="TARGET_1_HIT")

    alert, update = evaluate_regime_invalidation(
        signal,
        regime="Bullish",
        timestamp="2026-05-21T20:00:00Z",
    )

    assert alert is None
    assert update is None


def test_evaluate_regime_invalidations_updates_open_signals():
    signals = [
        _signal(symbol="NVDA", signal_id="nvda-id", status="TRIGGERED"),
        _signal(symbol="MSFT", signal_id="msft-id", status="TARGET_1_HIT"),
        _signal(symbol="AAPL", signal_id="aapl-id", status="PENDING"),
        _signal(symbol="TSLA", signal_id="tsla-id", status="STOP_HIT"),
    ]

    alerts, updates, updated_signals = evaluate_regime_invalidations(
        signals,
        regime="Defensive",
        timestamp="2026-05-21T20:00:00Z",
    )

    assert len(alerts) == 3
    assert len(updates) == 3
    statuses = {signal["signal_id"]: signal["status"] for signal in updated_signals}
    assert statuses["nvda-id"] == "CANCELLED_BY_REGIME_CHANGE"
    assert statuses["msft-id"] == "CANCELLED_BY_REGIME_CHANGE"
    assert statuses["aapl-id"] == "CANCELLED_BY_REGIME_CHANGE"
    assert statuses["tsla-id"] == "STOP_HIT"


def test_evaluate_signals_updates_only_matching_symbols_and_preserves_ids():
    signals = [_signal(symbol="NVDA"), _signal(symbol="AAPL", signal_id="aapl-id")]
    bars = {
        "NVDA": PriceBar(symbol="NVDA", timestamp="2026-05-21T15:00:00Z", high=102.0, low=100.0, close=101.0)
    }

    alerts, updates, updated_signals = evaluate_signals(signals, bars, today=date(2026, 5, 21))

    assert len(alerts) == 1
    assert len(updates) == 1
    assert updated_signals[0]["status"] == "TRIGGERED"
    assert updated_signals[0]["signal_id"].startswith("sig_NVDA_")
    assert updated_signals[1]["status"] == "PENDING"
    assert updated_signals[1]["signal_id"] == "aapl-id"


def test_append_lifecycle_updates_deduplicates_by_signal_id_and_event_type(tmp_path: Path):
    signal = _signal(signal_id="stable-id")
    bar = PriceBar(symbol="NVDA", timestamp="2026-05-21T15:00:00Z", high=102.0, low=100.0, close=101.5)
    _, update = evaluate_signal_against_bar(signal, bar, today=date(2026, 5, 21))

    assert update is not None
    lifecycle_path = tmp_path / "signal_lifecycle.jsonl"
    append_lifecycle_updates([update], log_path=lifecycle_path)
    append_lifecycle_updates([update], log_path=lifecycle_path)

    lines = lifecycle_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    payload = json.loads(lines[0])
    assert payload["signal_id"] == "stable-id"
    assert payload["event_type"] == "ENTRY_TRIGGERED"


def test_append_lifecycle_updates_deduplicates_regime_invalidation(tmp_path: Path):
    signal = _signal(signal_id="stable-id", status="TARGET_1_HIT")
    _, update = evaluate_regime_invalidation(
        signal,
        regime="Risk-Off",
        timestamp="2026-05-21T20:00:00Z",
    )
    assert update is not None

    lifecycle_path = tmp_path / "signal_lifecycle.jsonl"
    append_lifecycle_updates([update], log_path=lifecycle_path)
    append_lifecycle_updates([update], log_path=lifecycle_path)

    lines = lifecycle_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["event_type"] == "REGIME_INVALIDATION_EXIT"


def test_append_lifecycle_updates_allows_different_events_for_same_signal(tmp_path: Path):
    signal = _signal(signal_id="stable-id")
    entry_bar = PriceBar(symbol="NVDA", timestamp="2026-05-21T15:00:00Z", high=102.0, low=100.0, close=101.5)
    _, entry_update = evaluate_signal_against_bar(signal, entry_bar, today=date(2026, 5, 21))
    assert entry_update is not None

    stop_signal = dict(entry_update.signal)
    stop_bar = PriceBar(symbol="NVDA", timestamp="2026-05-22T15:00:00Z", high=102.0, low=94.0, close=95.0)
    _, stop_update = evaluate_signal_against_bar(stop_signal, stop_bar, today=date(2026, 5, 22))
    assert stop_update is not None

    lifecycle_path = tmp_path / "signal_lifecycle.jsonl"
    append_lifecycle_updates([entry_update, stop_update], log_path=lifecycle_path)

    lines = lifecycle_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert {json.loads(line)["event_type"] for line in lines} == {"ENTRY_TRIGGERED", "STOP_HIT"}


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
    assert "signal_id" in latest.read_text(encoding="utf-8")

    lifecycle_path = append_lifecycle_updates([update], log_path=tmp_path / "signal_lifecycle.jsonl")
    assert lifecycle_path.exists()
    assert "ENTRY_TRIGGERED" in lifecycle_path.read_text(encoding="utf-8")
    assert "signal_id" in lifecycle_path.read_text(encoding="utf-8")

    signal_file = tmp_path / "signals.json"
    signal_file.write_text('{"signals": []}', encoding="utf-8")
    save_updated_signal_file(signal_file, [update.signal])

    loaded = load_signal_file(signal_file)
    assert loaded[0]["status"] == "TRIGGERED"
    assert loaded[0]["signal_id"] == update.signal_id
    assert (tmp_path / "latest-signals.json").exists()
