from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from pathlib import Path

from scripts.generate_historical_trade_plans import generate_plans, load_bars, write_output
from src.backtesting.historical_entry_exit_backtest import load_trade_plans


def _write_bars(path: Path, *, days: int = 100, close_start: float = 100.0) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = ["date,open,high,low,close,volume"]
    close = close_start
    start = date(2024, 1, 1)
    for index in range(days):
        current_date = start + timedelta(days=index)
        if index % 15 == 0:
            close *= 0.97
        else:
            close *= 1.003
        open_price = close * 0.995
        high = close * 1.02
        low = close * 0.985
        rows.append(f"{current_date},{open_price:.2f},{high:.2f},{low:.2f},{close:.2f},100000")
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def _args(tmp_path: Path) -> argparse.Namespace:
    return argparse.Namespace(
        bars_root=tmp_path / "bars",
        output=tmp_path / "historical_trade_plans.json",
        min_history=60,
        lookahead_days=20,
        max_plans=10,
        max_plans_per_symbol=2,
        min_dollar_volume=1_000_000.0,
    )


def test_load_bars_parses_valid_csv_rows(tmp_path: Path) -> None:
    bars = tmp_path / "bars" / "TEST.csv"
    _write_bars(bars, days=3)

    rows = load_bars(bars)

    assert len(rows) == 3
    assert rows[0]["date"] == "2024-01-01"
    assert isinstance(rows[0]["close"], float)


def test_generate_historical_trade_plans_writes_loadable_json(tmp_path: Path) -> None:
    args = _args(tmp_path)
    _write_bars(args.bars_root / "TEST.csv", days=110)

    plans, summary = generate_plans(args)
    write_output(plans, summary, args.output)
    loaded = load_trade_plans(args.output)

    assert summary.scanned_symbols == 1
    assert summary.generated_plans == len(plans)
    assert len(loaded) == len(plans)
    assert loaded
    assert loaded[0].symbol == "TEST"
    assert loaded[0].stop_loss < loaded[0].entry_trigger < loaded[0].target_1


def test_generate_historical_trade_plans_is_deterministic(tmp_path: Path) -> None:
    args = _args(tmp_path)
    _write_bars(args.bars_root / "TEST.csv", days=110)

    first, _ = generate_plans(args)
    second, _ = generate_plans(args)

    assert [plan.signal_id for plan in first] == [plan.signal_id for plan in second]


def test_generate_historical_trade_plans_empty_when_not_enough_history(tmp_path: Path) -> None:
    args = _args(tmp_path)
    _write_bars(args.bars_root / "TEST.csv", days=20)

    plans, summary = generate_plans(args)
    write_output(plans, summary, args.output)
    payload = json.loads(args.output.read_text(encoding="utf-8"))

    assert plans == []
    assert payload["metadata"]["generated_plans"] == 0
    assert payload["plans"] == []
