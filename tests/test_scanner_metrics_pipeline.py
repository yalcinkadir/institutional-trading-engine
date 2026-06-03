from __future__ import annotations

import math
from datetime import UTC, datetime

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
        "high": "101",
        "rvol": "1.25",
        "vwap": "99.8",
        "swing_low_3bar": "96.0",
        "source": "polygon",
        "source_timestamp": "2026-06-03T14:30:00+00:00",
        "fallback_level": "primary",
        "data_status": "OK",
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
        "high": 101.0,
        "rvol": 1.25,
        "vwap": 99.8,
        "swing_low_3bar": 96.0,
        "source": "polygon",
        "source_timestamp": "2026-06-03T14:30:00+00:00",
        "fallback_level": "primary",
        "data_status": "OK",
        "symbol": "NVDA",
        "warnings": ["test"],
    }


def test_normalize_symbol_metrics_converts_nan_to_none() -> None:
    row = normalize_symbol_metrics({
        "symbol": "NVDA",
        "close": math.nan,
        "atr14": float("inf"),
        "atr_pct": None,
        "rvol": math.nan,
        "vwap": float("inf"),
        "swing_low_3bar": math.nan,
    })

    assert row["close"] is None
    assert row["atr14"] is None
    assert row["atr_pct"] is None
    assert row["rvol"] is None
    assert row["vwap"] is None
    assert row["swing_low_3bar"] is None


def test_normalize_scanner_metrics_map_reports_valid_and_missing_symbols() -> None:
    normalized, diagnostics = normalize_scanner_metrics_map(
        {
            "NVDA": {
                "close": 100.0,
                "atr14": 4.0,
                "atr_pct": 4.0,
                "rvol": 1.2,
                "swing_low_3bar": 96.0,
                "source": "polygon",
                "source_timestamp": "2026-06-03T14:30:00+00:00",
                "fallback_level": "primary",
            },
            "MSFT": {"close": 200.0},
            "AAPL": None,
        },
        ["NVDA", "MSFT", "AAPL", "QQQ"],
        now_utc=datetime(2026, 6, 3, 15, 0, tzinfo=UTC),
    )

    assert normalized["NVDA"]["close"] == 100.0
    assert normalized["NVDA"]["atr14"] == 4.0
    assert normalized["NVDA"]["rvol"] == 1.2
    assert normalized["NVDA"]["swing_low_3bar"] == 96.0
    assert normalized["NVDA"]["data_status"] == "OK"
    assert diagnostics.total_symbols == 4
    assert diagnostics.valid_symbols == 1
    assert diagnostics.missing_symbols == ["AAPL", "QQQ"]
    assert diagnostics.missing_required_fields == {"MSFT": ["atr14"]}
    assert diagnostics.has_warnings
    assert diagnostics.data_quality_status == "BLOCKED"
    assert "scanner_metrics_missing:AAPL" in diagnostics.warning_lines()
    assert "scanner_metrics_incomplete:MSFT:atr14" in diagnostics.warning_lines()


def test_normalize_scanner_metrics_map_handles_none_source() -> None:
    normalized, diagnostics = normalize_scanner_metrics_map(None, ["NVDA"])

    assert normalized == {}
    assert diagnostics.valid_symbols == 0
    assert diagnostics.missing_symbols == ["NVDA"]
    assert diagnostics.data_quality_status == "BLOCKED"


def test_data1_reports_missing_provenance_as_degraded_not_silent_green() -> None:
    normalized, diagnostics = normalize_scanner_metrics_map(
        {
            "NVDA": {"close": 100.0, "atr14": 4.0},
        },
        ["NVDA"],
        now_utc=datetime(2026, 6, 3, 15, 0, tzinfo=UTC),
    )

    assert normalized["NVDA"]["data_status"] == "DEGRADED"
    assert diagnostics.data_quality_status == "DEGRADED"
    assert diagnostics.missing_required_fields == {}
    assert diagnostics.missing_provenance_fields == {
        "NVDA": ["source", "source_timestamp", "fallback_level"]
    }
    assert "scanner_metrics_missing_provenance:NVDA:source,source_timestamp,fallback_level" in diagnostics.warning_lines()


def test_data1_reports_stale_source_timestamp_as_degraded() -> None:
    normalized, diagnostics = normalize_scanner_metrics_map(
        {
            "NVDA": {
                "close": 100.0,
                "atr14": 4.0,
                "source": "polygon",
                "source_timestamp": "2026-06-01T14:30:00+00:00",
                "fallback_level": "primary",
            },
        },
        ["NVDA"],
        now_utc=datetime(2026, 6, 3, 15, 0, tzinfo=UTC),
        max_staleness_minutes=60,
    )

    assert normalized["NVDA"]["data_status"] == "DEGRADED"
    assert diagnostics.data_quality_status == "DEGRADED"
    assert diagnostics.stale_symbols == {"NVDA": "source_timestamp_too_old"}
    assert "scanner_metrics_stale:NVDA:source_timestamp_too_old" in diagnostics.warning_lines()


def test_data1_blocks_missing_close_or_atr_before_actionable_signals() -> None:
    normalized, diagnostics = normalize_scanner_metrics_map(
        {
            "NVDA": {
                "close": None,
                "atr14": 4.0,
                "source": "polygon",
                "source_timestamp": "2026-06-03T14:30:00+00:00",
                "fallback_level": "primary",
            },
            "MSFT": {
                "close": 200.0,
                "atr14": None,
                "source": "polygon",
                "source_timestamp": "2026-06-03T14:30:00+00:00",
                "fallback_level": "primary",
            },
        },
        ["NVDA", "MSFT"],
        now_utc=datetime(2026, 6, 3, 15, 0, tzinfo=UTC),
    )

    assert normalized["NVDA"]["data_status"] == "BLOCKED"
    assert normalized["MSFT"]["data_status"] == "BLOCKED"
    assert diagnostics.data_quality_status == "BLOCKED"
    assert diagnostics.valid_symbols == 0
    assert diagnostics.missing_required_fields == {
        "NVDA": ["close"],
        "MSFT": ["atr14"],
    }
