from __future__ import annotations

from src.watchers.regime_invalidation import (
    REGIME_INVALIDATION_EVENT,
    REGIME_INVALIDATION_STATUS,
    apply_regime_invalidation,
    is_risk_off_regime,
    normalize_regime_label,
)


def _signal(**overrides):
    payload = {
        "symbol": "NVDA",
        "signal_id": "sig_NVDA_test",
        "action": "BUY_WATCH",
        "status": "TRIGGERED",
        "entry_trigger": 100.0,
        "stop_loss": 96.0,
        "target_1": 110.0,
        "target_2": 120.0,
    }
    payload.update(overrides)
    return payload


def test_normalize_regime_label_supports_dict_inputs() -> None:
    assert normalize_regime_label({"risk_state": "Risk-Off"}) == "risk off"
    assert normalize_regime_label({"regime": "low_vol_bull"}) == "low vol bull"


def test_is_risk_off_regime_matches_defensive_labels() -> None:
    assert is_risk_off_regime("Risk-Off")
    assert is_risk_off_regime("risk_off")
    assert is_risk_off_regime("Bearish")
    assert is_risk_off_regime({"risk_state": "Capital Protection"})


def test_is_risk_off_regime_rejects_constructive_labels() -> None:
    assert not is_risk_off_regime("Bullish")
    assert not is_risk_off_regime("low_vol_bull")
    assert not is_risk_off_regime({"risk_state": "Risk-On"})


def test_apply_regime_invalidation_cancels_triggered_signal() -> None:
    result = apply_regime_invalidation(
        _signal(status="TRIGGERED"),
        regime="Risk-Off",
        timestamp="2026-05-21T20:00:00Z",
    )

    assert result.invalidated
    assert result.event_type == REGIME_INVALIDATION_EVENT
    assert result.previous_status == "TRIGGERED"
    assert result.new_status == REGIME_INVALIDATION_STATUS
    assert result.signal["status"] == REGIME_INVALIDATION_STATUS
    assert result.signal["regime_invalidation_at"] == "2026-05-21T20:00:00Z"
    assert result.signal["regime_invalidation_reason"] == "risk off"


def test_apply_regime_invalidation_cancels_runner_signal() -> None:
    result = apply_regime_invalidation(
        _signal(status="TARGET_1_HIT", runner_status="active"),
        regime={"risk_state": "Defensive"},
        timestamp="2026-05-21T20:00:00Z",
    )

    assert result.invalidated
    assert result.signal["status"] == REGIME_INVALIDATION_STATUS


def test_apply_regime_invalidation_noops_when_regime_not_risk_off() -> None:
    result = apply_regime_invalidation(
        _signal(status="TARGET_1_HIT"),
        regime="Bullish",
        timestamp="2026-05-21T20:00:00Z",
    )

    assert not result.invalidated
    assert result.reasons == ["regime_not_risk_off"]
    assert result.signal["status"] == "TARGET_1_HIT"


def test_apply_regime_invalidation_cancels_pending_signal() -> None:
    result = apply_regime_invalidation(
        _signal(status="PENDING"),
        regime="Risk-Off",
        timestamp="2026-05-21T20:00:00Z",
    )

    assert result.invalidated
    assert result.event_type == REGIME_INVALIDATION_EVENT
    assert result.previous_status == "PENDING"
    assert result.new_status == REGIME_INVALIDATION_STATUS
    assert result.signal["status"] == REGIME_INVALIDATION_STATUS


def test_apply_regime_invalidation_ignores_terminal_signal() -> None:
    result = apply_regime_invalidation(
        _signal(status="STOP_HIT"),
        regime="Risk-Off",
        timestamp="2026-05-21T20:00:00Z",
    )

    assert not result.invalidated
    assert result.reasons == ["terminal_signal"]


def test_apply_regime_invalidation_ignores_non_actionable_signal() -> None:
    result = apply_regime_invalidation(
        _signal(action="NO_TRADE", status="TRIGGERED"),
        regime="Risk-Off",
        timestamp="2026-05-21T20:00:00Z",
    )

    assert not result.invalidated
    assert result.reasons == ["non_actionable_signal"]


def test_apply_regime_invalidation_does_not_duplicate_already_cancelled_signal() -> None:
    result = apply_regime_invalidation(
        _signal(status=REGIME_INVALIDATION_STATUS),
        regime="Risk-Off",
        timestamp="2026-05-21T20:00:00Z",
    )

    assert not result.invalidated
    assert result.reasons == ["terminal_signal"]
