from __future__ import annotations

import pandas as pd

from scripts.generate_report import _enrich_metrics_with_structure


def test_enrich_metrics_with_structure_adds_latest_swing_low() -> None:
    metrics = {"symbol": "NVDA", "close": 100.0}
    bars_df = pd.DataFrame({"low": [105.0, 101.0, 104.0, 103.0, 98.0, 102.0]})

    enriched = _enrich_metrics_with_structure(metrics, bars_df)

    assert enriched is not None
    assert enriched["swing_low_3bar"] == 98.0
    assert metrics.get("swing_low_3bar") is None


def test_enrich_metrics_with_structure_handles_missing_bars() -> None:
    metrics = {"symbol": "NVDA", "close": 100.0}

    enriched = _enrich_metrics_with_structure(metrics, None)

    assert enriched == metrics


def test_enrich_metrics_with_structure_handles_missing_metrics() -> None:
    assert _enrich_metrics_with_structure(None, pd.DataFrame({"low": [1, 2, 3]})) is None
