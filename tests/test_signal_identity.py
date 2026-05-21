from __future__ import annotations

from src.signals.signal_identity import (
    build_signal_id,
    ensure_signal_identity,
    signal_date_from_payload,
)


def _payload(**overrides):
    payload = {
        "symbol": "NVDA",
        "action": "BUY_WATCH",
        "generated_at": "2026-05-21T08:00:00+00:00",
        "entry_trigger": 101.0,
        "stop_loss": 95.0,
        "target_1": 110.0,
        "target_2": 120.0,
        "valid_until": "2026-05-24",
    }
    payload.update(overrides)
    return payload


def test_signal_date_prefers_generated_at_date() -> None:
    assert signal_date_from_payload(_payload()) == "2026-05-21"


def test_signal_date_falls_back_to_signal_date() -> None:
    assert signal_date_from_payload({"signal_date": "2026-05-20"}) == "2026-05-20"


def test_build_signal_id_is_deterministic() -> None:
    signal = _payload()

    assert build_signal_id(signal) == build_signal_id(dict(signal))


def test_build_signal_id_changes_when_material_field_changes() -> None:
    assert build_signal_id(_payload(entry_trigger=101.0)) != build_signal_id(_payload(entry_trigger=102.0))


def test_ensure_signal_identity_preserves_existing_id() -> None:
    result = ensure_signal_identity(_payload(signal_id="existing-id"))

    assert result["signal_id"] == "existing-id"


def test_ensure_signal_identity_generates_missing_id() -> None:
    result = ensure_signal_identity(_payload())

    assert result["signal_id"].startswith("sig_NVDA_")
