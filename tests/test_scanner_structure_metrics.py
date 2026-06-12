from __future__ import annotations

from datetime import date, timedelta

import pandas as pd

from src import scanner


def _daily_bars(rows: int = 230) -> pd.DataFrame:
    base_date = date(2025, 1, 1)
    data = []
    for idx in range(rows):
        close = 100.0 + idx * 0.1
        low = close - 1.0
        high = close + 1.0
        if idx == rows - 2:
            low = 90.0
        if idx == rows - 1:
            low = 95.0
        data.append(
            {
                "date": base_date + timedelta(days=idx),
                "open": close - 0.5,
                "high": high,
                "low": low,
                "close": close,
                "volume": 1_000_000 + idx,
            }
        )
    return pd.DataFrame(data)


def test_build_symbol_metrics_emits_native_swing_low_metric(monkeypatch) -> None:
    monkeypatch.setattr(scanner, "get_daily_bars", lambda symbol, **_kwargs: _daily_bars())

    metrics = scanner.build_symbol_metrics("NVDA", {"SPY": 1.0})

    assert metrics is not None
    assert metrics["symbol"] == "NVDA"
    assert metrics["swing_low_3bar"] == 90.0


def test_build_symbol_metrics_returns_na_when_no_confirmed_swing_low(monkeypatch) -> None:
    df = _daily_bars()
    df["low"] = range(len(df), 0, -1)
    monkeypatch.setattr(scanner, "get_daily_bars", lambda symbol, **_kwargs: df)

    metrics = scanner.build_symbol_metrics("NVDA", {"SPY": 1.0})

    assert metrics is not None
    assert pd.isna(metrics["swing_low_3bar"])
