from __future__ import annotations

from src.quality.liquidity_filter import (
    LiquidityFilterConfig,
    evaluate_liquidity,
    filter_universe,
    render_liquidity_markdown,
)


def _bar(close: float, volume: float, spread_pct: float = 0.01) -> dict:
    return {
        "o": close,
        "h": close * (1 + spread_pct / 2),
        "l": close * (1 - spread_pct / 2),
        "c": close,
        "v": volume,
    }


def test_liquid_symbol_passes() -> None:
    verdict = evaluate_liquidity("AAPL", [_bar(200.0, 50_000_000) for _ in range(80)])

    assert verdict.tradeable is True
    assert verdict.reasons == ()
    assert verdict.metrics is not None
    assert verdict.metrics.avg_dollar_volume > 9_000_000_000


def test_low_price_and_low_volume_are_rejected() -> None:
    verdict = evaluate_liquidity("PNNY", [_bar(2.5, 10_000) for _ in range(80)])

    assert verdict.tradeable is False
    assert "price_below_minimum" in verdict.reasons
    assert "dollar_volume_below_minimum" in verdict.reasons


def test_invalid_bars_are_skipped_for_metrics() -> None:
    bars = [_bar(100.0, 5_000_000) for _ in range(60)]
    bars.append({"close": "bad"})
    bars.append({})

    verdict = evaluate_liquidity("ROBUST", bars)

    assert verdict.metrics is not None
    assert verdict.metrics.bar_count == 60


def test_filter_universe_and_markdown() -> None:
    report = filter_universe(
        {
            "AAPL": [_bar(200.0, 50_000_000) for _ in range(80)],
            "PNNY": [_bar(2.0, 10_000) for _ in range(80)],
        }
    )

    assert report.tradeable_symbols == ["AAPL"]
    assert report.rejected_symbols == ["PNNY"]
    markdown = render_liquidity_markdown(report)
    assert "Liquidity Filter Report" in markdown
    assert "PNNY" in markdown


def test_custom_config_overrides_defaults() -> None:
    config = LiquidityFilterConfig(min_avg_daily_dollar_volume=1_000_000_000)
    verdict = evaluate_liquidity("MID", [_bar(100.0, 5_000_000) for _ in range(80)], config=config)

    assert verdict.tradeable is False
    assert "dollar_volume_below_minimum" in verdict.reasons
