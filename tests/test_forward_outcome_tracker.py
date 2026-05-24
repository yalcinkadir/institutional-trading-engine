from __future__ import annotations

from datetime import date

from src.outcomes.forward_outcome_tracker import (
    OutcomeExitReason,
    SignalReference,
    append_outcome,
    compute_forward_outcome,
    load_outcomes,
)


def _signal() -> SignalReference:
    return SignalReference(
        signal_id="sig-1",
        symbol="AAPL",
        signal_date=date(2024, 1, 1),
        entry_trigger=100.0,
        stop_loss=95.0,
        target_1=110.0,
        target_2=120.0,
        setup_type="momentum_breakout",
        market_regime="low_vol_bull",
        risk_tier="tier_1",
    )


def _bar(open_: float, high: float, low: float, close: float) -> dict:
    return {"o": open_, "h": high, "l": low, "c": close}


def test_target_1_hit_computes_realized_r() -> None:
    outcome = compute_forward_outcome(
        _signal(),
        [
            _bar(99, 101, 98, 100),
            _bar(101, 110, 100, 109),
        ],
        horizons_days=(1, 2),
    )

    assert outcome.exit_reason == OutcomeExitReason.TARGET_1_HIT.value
    assert outcome.realized_entry == 100.0
    assert outcome.realized_r == 2.0
    assert outcome.mfe_r == 2.0
    assert outcome.horizons[1].r_multiple_at_horizon == 1.8


def test_stop_hit_before_target_is_conservative() -> None:
    outcome = compute_forward_outcome(_signal(), [_bar(101, 120, 94, 110)])

    assert outcome.exit_reason == OutcomeExitReason.STOP_HIT.value
    assert outcome.realized_r == -1.2


def test_no_fill_when_entry_never_triggers() -> None:
    outcome = compute_forward_outcome(_signal(), [_bar(90, 99, 88, 92)])

    assert outcome.exit_reason == OutcomeExitReason.NO_FILL.value
    assert "no_entry_fill_within_window" in outcome.warnings


def test_append_and_load_outcomes(tmp_path) -> None:
    path = tmp_path / "outcomes.jsonl"
    outcome = compute_forward_outcome(_signal(), [_bar(100, 110, 99, 108)])

    append_outcome(outcome, journal_path=path)
    path.write_text(path.read_text(encoding="utf-8") + "{bad-json\n", encoding="utf-8")

    loaded = load_outcomes(path)
    assert len(loaded) == 1
    assert loaded[0]["signal_id"] == "sig-1"
