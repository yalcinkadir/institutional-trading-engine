from __future__ import annotations

import math

from src.signals.scanner_metrics_pipeline import (
    normalize_scanner_metrics_map,
    normalize_symbol_metrics,
)


def test_normalize_symbol_metrics_preserves_required_signal_fields() -> None:
    row = normalize_symbol_metrics({
        "symbol": "NVDA",
        "close": "100.5",
        "atr14": "4.2",
        "atr_pct": "4.1",
        "entry": "102",
        "entry_type": "breakout",
        "stop_loss": "94",
        "exit_1": "114",
        "exit_2": "122",
        "warnings": ["test"],
    })

    assert row == {
        "close": 100.5,
        "atr14": 4.2,
        "atr_pct": 4.1,
        "entry": 102.0,
        "entry_type": "breakout",
        "stop_loss": 94.0,
        "exit_1": 114.0,
        "exit_2": 122.0,
        "symbol": "NVDA",
        "warnings": ["test"],
    }


def test_normalize_symbol_metrics_converts_nan_to_none() -> None:
    row = normalize_symbol_metrics({
        "symbol": "NVDA",
        "close": math.nan,
        "atr14": float("inf"),
        "atr_pct": None,
    })

    assert row["close"] is None
    assert row["atr14"] is None
    assert row["atr_pct"] is None


def test_normalize_scanner_metrics_map_reports_valid_and_missing_symbols() -> None:
    normalized, diagnostics = normalize_scanner_metrics_map(
        {
            "NVDA": {"close": 100.0, "atr14": 4.0, "atr_pct": 4.0},
            "MSFT": {"close": 200.0},
            "AAPL": None,
        },
        ["NVDA", "MSFT", "AAPL", "QQQ"],
    )

    assert normalized["NVDA"]["close"] == 100.0
    assert normalized["NVDA"]["atr14"] == 4.0
    assert diagnostics.total_symbols == 4
    assert diagnostics.valid_symbols == 1
    assert diagnostics.missing_symbols == ["AAPL", "QQQ"]
    assert diagnostics.missing_required_fields == {"MSFT": ["atr14"]}
    assert diagnostics.has_warnings
    assert "scanner_metrics_missing:AAPL" in diagnostics.warning_lines()
    assert "scanner_metrics_incomplete:MSFT:atr14" in diagnostics.warning_lines()


def test_normalize_scanner_metrics_map_handles_none_source() -> None:
    normalized, diagnostics = normalize_scanner_metrics_map(None, ["NVDA"])

    assert normalized == {}
    assert diagnostics.valid_symbols == 0
    assert diagnostics.missing_symbols == ["NVDA"]
