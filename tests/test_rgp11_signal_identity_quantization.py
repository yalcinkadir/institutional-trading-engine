from __future__ import annotations

from src.signals.signal_identity import build_signal_id, ensure_signal_identity


def _signal(**overrides):
    payload = {
        "symbol": "NVDA",
        "action": "BUY_WATCH",
        "entry_trigger": 101.0,
        "stop_loss": 95.0,
        "target_1": 110.0,
        "target_2": 120.0,
        "valid_until": "2026-05-25",
        "generated_at": "2026-05-20T21:00:00Z",
    }
    payload.update(overrides)
    return payload


def test_signal_id_quantizes_equivalent_price_representations() -> None:
    base = _signal(
        entry_trigger=101,
        stop_loss=95,
        target_1=110,
        target_2=120,
    )
    equivalent = _signal(
        entry_trigger="101.0",
        stop_loss="95.0000",
        target_1=110.00000001,
        target_2="120.00000001",
    )

    assert build_signal_id(base) == build_signal_id(equivalent)


def test_signal_id_still_changes_for_material_price_difference() -> None:
    base = _signal(entry_trigger=101.0)
    changed = _signal(entry_trigger=101.01)

    assert build_signal_id(base) != build_signal_id(changed)


def test_signal_id_quantization_does_not_mutate_source_signal_values() -> None:
    signal = _signal(entry_trigger="101.00000001", stop_loss="95.00000001")

    result = ensure_signal_identity(signal)

    assert signal["entry_trigger"] == "101.00000001"
    assert signal["stop_loss"] == "95.00000001"
    assert result["entry_trigger"] == "101.00000001"
    assert result["stop_loss"] == "95.00000001"
    assert result["signal_id"].startswith("sig_NVDA_")


def test_signal_id_normalizes_symbol_and_action_case() -> None:
    base = _signal(symbol="nvda", action="buy_watch")
    equivalent = _signal(symbol="NVDA", action="BUY_WATCH")

    assert build_signal_id(base) == build_signal_id(equivalent)
