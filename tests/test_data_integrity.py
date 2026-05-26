from datetime import date

from src.data_integrity import (
    DataIntegrityDecision,
    HistoricalSymbol,
    HistoricalUniverse,
    ListingStatus,
    OhlcvBar,
    ProviderComparisonTolerance,
    compare_provider_bars,
    has_missing_bars,
    require_survivorship_safe_universe,
)


def test_survivorship_safe_universe_requires_inactive_symbols():
    universe = HistoricalUniverse(
        symbols=(
            HistoricalSymbol(
                symbol="ACTIVE",
                name="Active Company",
                listing_status=ListingStatus.ACTIVE,
                listed_from=date(2010, 1, 1),
            ),
        )
    )

    assert require_survivorship_safe_universe(universe) == DataIntegrityDecision.FAIL_CLOSED


def test_survivorship_safe_universe_passes_with_delisted_symbol():
    universe = HistoricalUniverse(
        symbols=(
            HistoricalSymbol(
                symbol="WINNER",
                name="Winner Company",
                listing_status=ListingStatus.ACTIVE,
                listed_from=date(2010, 1, 1),
            ),
            HistoricalSymbol(
                symbol="FAILED",
                name="Failed Company",
                listing_status=ListingStatus.DELISTED,
                listed_from=date(2010, 1, 1),
                listed_to=date(2018, 6, 30),
            ),
        )
    )

    assert require_survivorship_safe_universe(universe) == DataIntegrityDecision.PASS
    assert universe.survivorship_sensitive_symbols()[0].symbol == "FAILED"


def test_historical_universe_active_on_includes_symbol_before_delisting():
    universe = HistoricalUniverse(
        symbols=(
            HistoricalSymbol(
                symbol="OLD",
                name="Old Listed Company",
                listing_status=ListingStatus.DELISTED,
                listed_from=date(2010, 1, 1),
                listed_to=date(2015, 12, 31),
            ),
        )
    )

    assert len(universe.active_on(date(2014, 1, 1))) == 1
    assert len(universe.active_on(date(2016, 1, 1))) == 0


def test_provider_comparison_passes_for_small_differences():
    primary = OhlcvBar(
        symbol="QQQ",
        as_of=date(2026, 5, 22),
        open=100.0,
        high=102.0,
        low=99.0,
        close=101.0,
        volume=1_000_000,
        provider="primary",
    )
    secondary = OhlcvBar(
        symbol="QQQ",
        as_of=date(2026, 5, 22),
        open=100.01,
        high=102.01,
        low=99.0,
        close=101.01,
        volume=1_001_000,
        provider="secondary",
    )

    result = compare_provider_bars(primary, secondary)

    assert result.decision == DataIntegrityDecision.PASS
    assert result.reasons == ()


def test_provider_comparison_warns_for_non_critical_volume_divergence():
    primary = OhlcvBar(
        symbol="QQQ",
        as_of=date(2026, 5, 22),
        open=100.0,
        high=102.0,
        low=99.0,
        close=101.0,
        volume=1_000_000,
        provider="primary",
    )
    secondary = OhlcvBar(
        symbol="QQQ",
        as_of=date(2026, 5, 22),
        open=100.0,
        high=102.0,
        low=99.0,
        close=101.0,
        volume=1_100_000,
        provider="secondary",
    )

    result = compare_provider_bars(primary, secondary)

    assert result.decision == DataIntegrityDecision.WARN
    assert "volume_divergence_warning" in result.reasons


def test_provider_comparison_fails_closed_for_critical_price_divergence():
    primary = OhlcvBar(
        symbol="QQQ",
        as_of=date(2026, 5, 22),
        open=100.0,
        high=102.0,
        low=99.0,
        close=101.0,
        volume=1_000_000,
        provider="primary",
    )
    secondary = OhlcvBar(
        symbol="QQQ",
        as_of=date(2026, 5, 22),
        open=100.0,
        high=105.0,
        low=99.0,
        close=101.0,
        volume=1_000_000,
        provider="secondary",
    )

    result = compare_provider_bars(primary, secondary)

    assert result.decision == DataIntegrityDecision.FAIL_CLOSED
    assert "critical_price_divergence" in result.reasons


def test_provider_comparison_fails_closed_for_adjustment_policy_mismatch():
    primary = OhlcvBar(
        symbol="QQQ",
        as_of=date(2026, 5, 22),
        open=100.0,
        high=102.0,
        low=99.0,
        close=101.0,
        volume=1_000_000,
        provider="primary",
        adjusted=True,
    )
    secondary = OhlcvBar(
        symbol="QQQ",
        as_of=date(2026, 5, 22),
        open=100.0,
        high=102.0,
        low=99.0,
        close=101.0,
        volume=1_000_000,
        provider="secondary",
        adjusted=False,
    )

    result = compare_provider_bars(primary, secondary)

    assert result.decision == DataIntegrityDecision.FAIL_CLOSED
    assert "adjustment_policy_mismatch" in result.reasons


def test_provider_comparison_allows_custom_tolerance():
    primary = OhlcvBar(
        symbol="QQQ",
        as_of=date(2026, 5, 22),
        open=100.0,
        high=102.0,
        low=99.0,
        close=101.0,
        volume=1_000_000,
        provider="primary",
    )
    secondary = OhlcvBar(
        symbol="QQQ",
        as_of=date(2026, 5, 22),
        open=100.0,
        high=102.4,
        low=99.0,
        close=101.0,
        volume=1_000_000,
        provider="secondary",
    )

    result = compare_provider_bars(
        primary,
        secondary,
        ProviderComparisonTolerance(max_price_pct_warn=0.01, max_price_pct_fail=0.02),
    )

    assert result.decision == DataIntegrityDecision.PASS


def test_missing_bars_are_detected():
    bars = [
        OhlcvBar(
            symbol="QQQ",
            as_of=date(2026, 5, 20),
            open=100.0,
            high=101.0,
            low=99.0,
            close=100.5,
            volume=1_000_000,
            provider="primary",
        )
    ]

    assert has_missing_bars([date(2026, 5, 20), date(2026, 5, 21)], bars) is True
