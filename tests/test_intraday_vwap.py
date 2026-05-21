from __future__ import annotations

from src.signals.intraday_vwap import calculate_intraday_vwap, enrich_metrics_with_vwap


def test_calculate_intraday_vwap_with_normalized_keys() -> None:
    bars = [
        {"high": 102.0, "low": 98.0, "close": 100.0, "volume": 1000},
        {"high": 105.0, "low": 99.0, "close": 102.0, "volume": 2000},
    ]

    assert calculate_intraday_vwap(bars) == 101.3333


def test_calculate_intraday_vwap_with_polygon_keys() -> None:
    bars = [
        {"h": 102.0, "l": 98.0, "c": 100.0, "v": 1000},
        {"h": 105.0, "l": 99.0, "c": 102.0, "v": 2000},
    ]

    assert calculate_intraday_vwap(bars) == 101.3333


def test_calculate_intraday_vwap_ignores_invalid_bars() -> None:
    bars = [
        {"h": 102.0, "l": 98.0, "c": 100.0, "v": 1000},
        {"h": 999.0, "l": 1.0, "c": 2.0},
        {"h": 105.0, "l": 99.0, "c": 102.0, "v": 0},
        "invalid",
    ]

    assert calculate_intraday_vwap(bars) == 100.0


def test_calculate_intraday_vwap_returns_none_without_usable_volume() -> None:
    assert calculate_intraday_vwap([]) is None
    assert calculate_intraday_vwap([{"h": 102.0, "l": 98.0, "c": 100.0, "v": 0}]) is None
    assert calculate_intraday_vwap([{"h": 102.0, "l": 98.0, "c": 100.0}]) is None


def test_enrich_metrics_with_vwap_adds_value_when_available() -> None:
    metrics = {"symbol": "NVDA", "close": 100.0}
    bars = [{"h": 102.0, "l": 98.0, "c": 100.0, "v": 1000}]

    enriched = enrich_metrics_with_vwap(metrics, bars)

    assert enriched == {"symbol": "NVDA", "close": 100.0, "vwap": 100.0}
    assert "vwap" not in metrics


def test_enrich_metrics_with_vwap_is_non_fatal_without_intraday_data() -> None:
    metrics = {"symbol": "NVDA", "close": 100.0}

    assert enrich_metrics_with_vwap(metrics, None) == metrics


def test_enrich_metrics_with_vwap_handles_missing_metrics() -> None:
    assert enrich_metrics_with_vwap(None, [{"h": 1, "l": 1, "c": 1, "v": 1}]) is None
