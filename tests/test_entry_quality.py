from __future__ import annotations

from src.signals.entry_quality import derive_entry_quality


def test_breakout_entry_prefers_scanner_high_trigger() -> None:
    result = derive_entry_quality(
        setup_type="momentum_breakout",
        close=100.0,
        atr=4.0,
        scanner_metrics={"high": 101.0},
    )

    assert result.is_valid
    assert result.entry_trigger == 101.1
    assert result.entry_type == "breakout"
    assert "scanner high" in result.entry_reason


def test_breakout_entry_falls_back_to_atr_when_high_missing() -> None:
    result = derive_entry_quality(
        setup_type="momentum_breakout",
        close=100.0,
        atr=4.0,
    )

    assert result.is_valid
    assert result.entry_trigger == 102.0
    assert result.entry_type == "breakout"
    assert "0.5 ATR" in result.entry_reason


def test_breakout_entry_passes_with_sufficient_rvol() -> None:
    result = derive_entry_quality(
        setup_type="momentum_breakout",
        close=100.0,
        atr=4.0,
        scanner_metrics={"high": 101.0, "rvol": 1.2},
    )

    assert result.is_valid
    assert result.entry_trigger == 101.1


def test_breakout_entry_rejects_low_rvol_when_available() -> None:
    result = derive_entry_quality(
        setup_type="momentum_breakout",
        close=100.0,
        atr=4.0,
        scanner_metrics={"high": 101.0, "rvol": 0.7},
    )

    assert not result.is_valid
    assert result.entry_type == "breakout"
    assert result.reasons == ["insufficient_volume_for_breakout"]


def test_breakout_entry_rejects_close_below_vwap_when_available() -> None:
    result = derive_entry_quality(
        setup_type="momentum_breakout",
        close=99.0,
        atr=4.0,
        scanner_metrics={"high": 101.0, "vwap": 100.0},
    )

    assert not result.is_valid
    assert result.reasons == ["breakout_entry_below_vwap"]


def test_breakout_entry_allows_missing_vwap() -> None:
    result = derive_entry_quality(
        setup_type="momentum_breakout",
        close=100.0,
        atr=4.0,
        scanner_metrics={"high": 101.0},
    )

    assert result.is_valid
    assert result.entry_trigger == 101.1


def test_breakout_entry_reports_multiple_context_failures() -> None:
    result = derive_entry_quality(
        setup_type="momentum_breakout",
        close=99.0,
        atr=4.0,
        scanner_metrics={"high": 101.0, "rvol": 0.7, "vwap": 100.0},
    )

    assert not result.is_valid
    assert result.reasons == [
        "insufficient_volume_for_breakout",
        "breakout_entry_below_vwap",
    ]


def test_pullback_entry_for_pullback_continuation() -> None:
    result = derive_entry_quality(
        setup_type="pullback_continuation",
        close=100.0,
        atr=4.0,
    )

    assert result.is_valid
    assert result.entry_trigger == 96.0
    assert result.entry_type == "pullback"
    assert "1 ATR below" in result.entry_reason


def test_pullback_entry_rejects_non_positive_computed_entry() -> None:
    result = derive_entry_quality(
        setup_type="pullback_continuation",
        close=2.5,
        atr=3.0,
    )

    assert not result.is_valid
    assert result.entry_trigger is None
    assert result.entry_type == "pullback"
    assert result.reasons == ["computed_entry_non_positive"]


def test_retest_entry_for_retest_continuation() -> None:
    result = derive_entry_quality(
        setup_type="retest_continuation",
        close=100.0,
        atr=4.0,
    )

    assert result.is_valid
    assert result.entry_trigger == 98.0
    assert result.entry_type == "retest"
    assert "0.5 ATR below" in result.entry_reason


def test_gap_fill_entry_for_gap_fill_setup() -> None:
    result = derive_entry_quality(
        setup_type="gap_fill",
        close=100.0,
        atr=4.0,
    )

    assert result.is_valid
    assert result.entry_trigger == 97.0
    assert result.entry_type == "gap_fill"
    assert "0.75 ATR below" in result.entry_reason


def test_at_market_entry_rejected_unless_explicitly_allowed() -> None:
    result = derive_entry_quality(
        setup_type="mean_reversion",
        close=100.0,
        atr=4.0,
        allow_at_market=False,
    )

    assert not result.is_valid
    assert result.entry_type == "at_market"
    assert result.reasons == ["at_market_entry_not_allowed"]


def test_at_market_entry_allowed_when_explicit() -> None:
    result = derive_entry_quality(
        setup_type="mean_reversion",
        close=100.0,
        atr=4.0,
        allow_at_market=True,
    )

    assert result.is_valid
    assert result.entry_trigger == 100.0
    assert result.entry_type == "at_market"


def test_scanner_provided_entry_is_used() -> None:
    result = derive_entry_quality(
        setup_type="momentum_breakout",
        close=100.0,
        atr=4.0,
        scanner_metrics={"entry": 103.0, "entry_type": "breakout"},
    )

    assert result.is_valid
    assert result.entry_trigger == 103.0
    assert result.entry_type == "breakout"
    assert result.entry_reason == "scanner provided executable entry level"


def test_scanner_provided_entry_rejects_low_breakout_rvol() -> None:
    result = derive_entry_quality(
        setup_type="momentum_breakout",
        close=100.0,
        atr=4.0,
        scanner_metrics={"entry": 103.0, "entry_type": "breakout", "rvol": 0.7},
    )

    assert not result.is_valid
    assert result.entry_trigger == 103.0
    assert result.reasons == ["insufficient_volume_for_breakout"]


def test_late_breakout_entry_is_rejected() -> None:
    result = derive_entry_quality(
        setup_type="momentum_breakout",
        close=110.0,
        atr=4.0,
        scanner_metrics={"entry": 100.0, "entry_type": "breakout"},
        max_breakout_extension_atr=1.5,
    )

    assert not result.is_valid
    assert result.entry_trigger == 100.0
    assert result.reasons == ["late_entry_price_extended_beyond_trigger"]


def test_missing_close_rejected() -> None:
    result = derive_entry_quality(
        setup_type="momentum_breakout",
        close=None,
        atr=4.0,
    )

    assert not result.is_valid
    assert result.reasons == ["missing_close"]


def test_non_positive_close_rejected() -> None:
    result = derive_entry_quality(
        setup_type="momentum_breakout",
        close=0.0,
        atr=4.0,
    )

    assert not result.is_valid
    assert result.reasons == ["missing_or_invalid_close"]


def test_missing_atr_rejected() -> None:
    result = derive_entry_quality(
        setup_type="momentum_breakout",
        close=100.0,
        atr=None,
    )

    assert not result.is_valid
    assert result.reasons == ["missing_or_invalid_atr"]
