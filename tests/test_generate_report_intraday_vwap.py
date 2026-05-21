from __future__ import annotations

from scripts.generate_report import _enrich_metrics_with_intraday_context


def test_enrich_metrics_with_intraday_context_adds_vwap() -> None:
    metrics = {"symbol": "NVDA", "close": 100.0}
    bars = [
        {"h": 102.0, "l": 98.0, "c": 100.0, "v": 1000},
        {"h": 105.0, "l": 99.0, "c": 102.0, "v": 2000},
    ]

    enriched = _enrich_metrics_with_intraday_context(metrics, bars)

    assert enriched is not None
    assert enriched["vwap"] == 101.3333
    assert "vwap" not in metrics


def test_enrich_metrics_with_intraday_context_is_non_fatal_without_bars() -> None:
    metrics = {"symbol": "NVDA", "close": 100.0}

    assert _enrich_metrics_with_intraday_context(metrics, None) == metrics


def test_enrich_metrics_with_intraday_context_handles_missing_metrics() -> None:
    assert _enrich_metrics_with_intraday_context(None, [{"h": 1, "l": 1, "c": 1, "v": 1}]) is None
