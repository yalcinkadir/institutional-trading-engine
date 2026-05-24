from __future__ import annotations

from datetime import date

from src.macro.vix_adapter import VixDataQuality, build_vix_snapshot


def _bar(close: float, day: str = "2024-01-15") -> dict:
    return {"c": close, "date": day}


def test_direct_quality_with_vix_and_vix9d() -> None:
    def fetcher(symbol: str) -> list[dict]:
        if symbol == "I:VIX":
            return [_bar(20.0, "2024-01-14"), _bar(22.0, "2024-01-15")]
        if symbol == "I:VIX9D":
            return [_bar(19.0, "2024-01-14"), _bar(24.0, "2024-01-15")]
        if symbol == "I:VIX3M":
            return [_bar(21.0, "2024-01-15")]
        return []

    snapshot = build_vix_snapshot(bar_fetcher=fetcher)
    assert snapshot.quality == VixDataQuality.DIRECT
    assert snapshot.spot_vix == 22.0
    assert snapshot.vix_9d == 24.0
    assert snapshot.inverted is True
    assert snapshot.as_of == date(2024, 1, 15)


def test_direct_quality_not_inverted() -> None:
    def fetcher(symbol: str) -> list[dict]:
        if symbol == "I:VIX":
            return [_bar(20.0)]
        if symbol == "I:VIX9D":
            return [_bar(18.0)]
        return []

    snapshot = build_vix_snapshot(bar_fetcher=fetcher)
    assert snapshot.quality == VixDataQuality.DIRECT
    assert snapshot.inverted is False
    assert snapshot.term_structure_ratio == 0.9


def test_falls_back_to_vix_vs_vix3m() -> None:
    def fetcher(symbol: str) -> list[dict]:
        if symbol == "I:VIX":
            return [_bar(25.0)]
        if symbol == "I:VIX3M":
            return [_bar(20.0)]
        return []

    snapshot = build_vix_snapshot(bar_fetcher=fetcher)
    assert snapshot.quality == VixDataQuality.PARTIAL
    assert snapshot.spot_vix == 25.0
    assert snapshot.vix_3m == 20.0
    assert snapshot.inverted is True


def test_partial_when_only_spot_vix_available() -> None:
    def fetcher(symbol: str) -> list[dict]:
        if symbol == "I:VIX":
            return [_bar(18.0)]
        return []

    snapshot = build_vix_snapshot(bar_fetcher=fetcher)
    assert snapshot.quality == VixDataQuality.PARTIAL
    assert snapshot.spot_vix == 18.0
    assert snapshot.term_structure_ratio is None
    assert snapshot.inverted is False
    assert "term_structure_unavailable" in snapshot.source_notes


def test_alternative_symbol_candidates_used() -> None:
    def fetcher(symbol: str) -> list[dict]:
        if symbol == "I:VIX":
            return []
        if symbol == "VIX":
            return [_bar(20.0)]
        if symbol == "VIX9D":
            return [_bar(22.0)]
        return []

    snapshot = build_vix_snapshot(bar_fetcher=fetcher)
    assert snapshot.quality == VixDataQuality.DIRECT
    assert snapshot.spot_vix == 20.0
    assert snapshot.vix_9d == 22.0
    assert "spot_vix_from:VIX" in snapshot.source_notes


def test_fetcher_exception_does_not_crash() -> None:
    def fetcher(symbol: str) -> list[dict]:
        if symbol == "I:VIX":
            raise RuntimeError("polygon 500")
        if symbol == "VIX":
            return [_bar(15.0)]
        return []

    snapshot = build_vix_snapshot(bar_fetcher=fetcher)
    assert snapshot.spot_vix == 15.0


def test_realized_volatility_fallback_when_no_vix_data() -> None:
    def vix_fetcher(symbol: str) -> list[dict]:
        return []

    spy_bars: list[dict] = []
    price = 400.0
    for index in range(17):
        spy_bars.append({"c": price, "date": f"2024-01-{index + 1:02d}"})
        price *= 1.001
    for index in range(5):
        delta = 0.04 if index % 2 == 0 else -0.04
        price *= 1 + delta
        spy_bars.append({"c": price, "date": f"2024-02-{index + 1:02d}"})

    def spy_fetcher(symbol: str) -> list[dict]:
        return spy_bars

    snapshot = build_vix_snapshot(bar_fetcher=vix_fetcher, spy_bar_fetcher=spy_fetcher)
    assert snapshot.quality == VixDataQuality.REALIZED_PROXY
    assert snapshot.term_structure_ratio is not None
    assert snapshot.inverted is True


def test_unavailable_when_no_data_at_all() -> None:
    snapshot = build_vix_snapshot(bar_fetcher=lambda symbol: [])
    assert snapshot.quality == VixDataQuality.UNAVAILABLE
    assert snapshot.spot_vix is None
    assert snapshot.inverted is False


def test_realized_proxy_skipped_when_insufficient_spy_history() -> None:
    snapshot = build_vix_snapshot(
        bar_fetcher=lambda symbol: [],
        spy_bar_fetcher=lambda symbol: [{"c": 400.0, "date": "2024-01-01"}],
    )
    assert snapshot.quality == VixDataQuality.UNAVAILABLE


def test_direct_vix_snapshot_activates_market_context_hard_override() -> None:
    from src.decision_engine import (
        MarketContext,
        MarketState,
        apply_vix_snapshot_to_context,
        detect_hard_overrides,
    )

    snapshot = build_vix_snapshot(
        bar_fetcher=lambda symbol: [_bar(24.0)] if symbol == "I:VIX9D" else [_bar(22.0)] if symbol == "I:VIX" else []
    )
    context = MarketContext(
        market_state=MarketState.HIGH_VOL_TRANSITION,
        credit_spreads_widening=True,
        breadth_collapse=True,
    )

    context = apply_vix_snapshot_to_context(context, snapshot)

    assert context.vix_term_structure_inverted is True
    assert "systemic_risk_cluster" in detect_hard_overrides(context)


def test_realized_proxy_does_not_activate_context_unless_explicitly_allowed() -> None:
    from src.decision_engine import MarketContext, MarketState, apply_vix_snapshot_to_context
    from src.macro.vix_adapter import VixSnapshot

    snapshot = VixSnapshot(
        as_of=date(2024, 1, 31),
        spot_vix=None,
        vix_9d=None,
        vix_3m=None,
        term_structure_ratio=1.5,
        inverted=True,
        quality=VixDataQuality.REALIZED_PROXY,
    )
    context = MarketContext(market_state=MarketState.HIGH_VOL_TRANSITION)

    unchanged = apply_vix_snapshot_to_context(context, snapshot)
    allowed = apply_vix_snapshot_to_context(context, snapshot, allow_realized_proxy=True)

    assert unchanged.vix_term_structure_inverted is False
    assert allowed.vix_term_structure_inverted is True
