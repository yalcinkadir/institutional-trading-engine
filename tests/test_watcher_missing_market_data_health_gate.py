import json
from pathlib import Path

from src.watchers.market_data_health import (
    BLOCKED,
    DEGRADED,
    PASSED,
    build_watcher_market_data_health,
    market_data_health_to_dict,
    write_watcher_market_data_health_artifact,
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


def test_watcher_market_data_health_passes_when_all_actionable_symbols_have_bars():
    health = build_watcher_market_data_health(
        [_signal(symbol="NVDA"), _signal(symbol="MSFT", status="STOP_HIT")],
        evaluated_symbols={"NVDA"},
        generated_at="2026-06-07T09:00:00+00:00",
        cycle_id="cycle-1",
    )

    assert health.status == PASSED
    assert health.checked_signal_count == 1
    assert health.evaluated_symbol_count == 1
    assert health.missing_market_data_count == 0
    assert health.missing_market_data == []


def test_watcher_market_data_health_degrades_for_pending_actionable_signal_without_bar():
    health = build_watcher_market_data_health(
        [_signal(symbol="NVDA", signal_id="pending-id", status="PENDING")],
        evaluated_symbols=set(),
        generated_at="2026-06-07T09:00:00+00:00",
    )

    payload = market_data_health_to_dict(health)

    assert payload["status"] == DEGRADED
    assert payload["missing_market_data_count"] == 1
    assert payload["missing_market_data"][0]["signal_id"] == "pending-id"
    assert payload["missing_market_data"][0]["symbol"] == "NVDA"
    assert payload["missing_market_data"][0]["severity"] == DEGRADED
    assert payload["missing_market_data"][0]["reason"] == "missing_bar_for_actionable_signal"


def test_watcher_market_data_health_blocks_for_triggered_signal_without_bar():
    health = build_watcher_market_data_health(
        [_signal(symbol="NVDA", signal_id="triggered-id", status="TRIGGERED")],
        evaluated_symbols=set(),
        generated_at="2026-06-07T09:00:00+00:00",
    )

    payload = market_data_health_to_dict(health)

    assert payload["status"] == BLOCKED
    assert payload["missing_market_data_count"] == 1
    assert payload["missing_market_data"][0]["severity"] == BLOCKED
    assert payload["missing_market_data"][0]["reason"] == "missing_bar_for_active_stop_or_exit_risk"


def test_watcher_market_data_health_artifact_is_written(tmp_path: Path):
    health = build_watcher_market_data_health(
        [_signal(symbol="NVDA", signal_id="runner-id", status="TARGET_1_HIT")],
        evaluated_symbols=set(),
        generated_at="2026-06-07T09:00:00+00:00",
        cycle_id="cycle-2",
    )
    artifact_path = tmp_path / "watcher-health.json"

    result = write_watcher_market_data_health_artifact(health, artifact_path=artifact_path)

    assert result == artifact_path
    payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert payload["status"] == BLOCKED
    assert payload["cycle_id"] == "cycle-2"
    assert payload["artifact_path"] == str(artifact_path)
    assert payload["missing_market_data"][0]["status"] == "TARGET_1_HIT"
