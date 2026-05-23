from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.backtesting.historical_entry_exit_backtest import (
    load_historical_bars,
    load_trade_plans,
    run_backtest,
    simulate_plan,
)
from src.backtesting.historical_models import (
    OUTCOME_ENTRY_NOT_HIT,
    OUTCOME_EXPIRED,
    OUTCOME_STOP_HIT,
    OUTCOME_TARGET_1_HIT,
    OUTCOME_TARGET_2_HIT,
    HistoricalTradePlan,
)
from src.backtesting.historical_report import render_markdown, write_report


def _bars(rows: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(rows)


def _base_plan(**overrides) -> HistoricalTradePlan:
    values = {
        "signal_id": "sig_1",
        "symbol": "TEST",
        "signal_date": "2026-01-01",
        "entry_trigger": 100.0,
        "stop_loss": 95.0,
        "target_1": 110.0,
        "target_2": 120.0,
    }
    values.update(overrides)
    return HistoricalTradePlan(**values)


def test_simulate_plan_entry_not_hit() -> None:
    result = simulate_plan(
        _base_plan(),
        _bars([
            {"date": "2026-01-02", "open": 90, "high": 99, "low": 89, "close": 95, "volume": 1},
            {"date": "2026-01-03", "open": 95, "high": 98, "low": 94, "close": 96, "volume": 1},
        ]),
    )

    assert result.outcome == OUTCOME_ENTRY_NOT_HIT
    assert not result.entry_hit
    assert result.reason == "entry_not_hit"


def test_simulate_plan_expires_with_valid_until_when_entry_not_hit() -> None:
    result = simulate_plan(
        _base_plan(valid_until="2026-01-03"),
        _bars([
            {"date": "2026-01-02", "open": 90, "high": 99, "low": 89, "close": 95, "volume": 1},
            {"date": "2026-01-03", "open": 95, "high": 98, "low": 94, "close": 96, "volume": 1},
        ]),
    )

    assert result.outcome == OUTCOME_EXPIRED
    assert not result.entry_hit


def test_simulate_plan_stop_hit_conservatively_on_entry_bar() -> None:
    result = simulate_plan(
        _base_plan(),
        _bars([
            {"date": "2026-01-02", "open": 99, "high": 111, "low": 94, "close": 105, "volume": 1},
        ]),
    )

    assert result.outcome == OUTCOME_STOP_HIT
    assert result.entry_hit
    assert result.stop_hit
    assert result.false_breakout
    assert result.r_multiple == -1.0
    assert result.reason == "same_bar_stop_first"


def test_simulate_plan_target_2_hit() -> None:
    result = simulate_plan(
        _base_plan(),
        _bars([
            {"date": "2026-01-02", "open": 99, "high": 105, "low": 99, "close": 104, "volume": 1},
            {"date": "2026-01-03", "open": 104, "high": 121, "low": 103, "close": 120, "volume": 1},
        ]),
    )

    assert result.outcome == OUTCOME_TARGET_2_HIT
    assert result.target_1_hit
    assert result.target_2_hit
    assert result.r_multiple == 4.0


def test_simulate_plan_target_1_only() -> None:
    result = simulate_plan(
        _base_plan(),
        _bars([
            {"date": "2026-01-02", "open": 99, "high": 105, "low": 99, "close": 104, "volume": 1},
            {"date": "2026-01-03", "open": 104, "high": 111, "low": 103, "close": 110, "volume": 1},
            {"date": "2026-01-04", "open": 110, "high": 115, "low": 108, "close": 112, "volume": 1},
        ]),
    )

    assert result.outcome == OUTCOME_TARGET_1_HIT
    assert result.target_1_hit
    assert not result.target_2_hit
    assert result.r_multiple == 2.0


def test_run_backtest_loads_symbol_csv_and_calculates_metrics(tmp_path: Path) -> None:
    bars_root = tmp_path / "bars"
    bars_root.mkdir()
    (bars_root / "TEST.csv").write_text(
        "date,open,high,low,close,volume\n"
        "2026-01-02,99,105,99,104,1\n"
        "2026-01-03,104,121,103,120,1\n",
        encoding="utf-8",
    )

    report = run_backtest([_base_plan()], bars_root=bars_root)

    assert report.metrics.total == 1
    assert report.metrics.entry_hit_rate == 1.0
    assert report.metrics.target_2_hit_rate == 1.0
    assert report.metrics.expectancy_r == 4.0


def test_load_trade_plans_accepts_signals_payload_and_filters_invalid(tmp_path: Path) -> None:
    path = tmp_path / "plans.json"
    path.write_text(
        json.dumps(
            {
                "signals": [
                    {
                        "signal_id": "ok",
                        "symbol": "test",
                        "signal_date": "2026-01-01",
                        "action": "BUY_WATCH",
                        "entry_trigger": 100,
                        "stop_loss": 95,
                        "target_1": 110,
                    },
                    {"symbol": "BAD", "action": "NO_TRADE"},
                    {"symbol": "BAD", "action": "BUY_WATCH", "entry_trigger": 100},
                ]
            }
        ),
        encoding="utf-8",
    )

    plans = load_trade_plans(path)

    assert len(plans) == 1
    assert plans[0].signal_id == "ok"
    assert plans[0].symbol == "TEST"


def test_load_historical_bars_requires_columns(tmp_path: Path) -> None:
    path = tmp_path / "bad.csv"
    path.write_text("date,open,high\n2026-01-01,1,2\n", encoding="utf-8")

    try:
        load_historical_bars(path)
    except ValueError as exc:
        assert "missing columns" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_write_report_outputs_json_and_markdown(tmp_path: Path) -> None:
    report = run_backtest(
        [_base_plan()],
        bars_root=_write_test_bars(tmp_path),
    )
    json_path = tmp_path / "report.json"
    markdown_path = tmp_path / "report.md"

    write_report(report, json_path=json_path, markdown_path=markdown_path)

    assert json.loads(json_path.read_text(encoding="utf-8"))["metrics"]["total"] == 1
    assert "Historical Entry / Stop / Exit Backtest" in markdown_path.read_text(encoding="utf-8")
    assert "TARGET_2_HIT" in render_markdown(report)


def _write_test_bars(tmp_path: Path) -> Path:
    bars_root = tmp_path / "bars2"
    bars_root.mkdir()
    (bars_root / "TEST.csv").write_text(
        "date,open,high,low,close,volume\n"
        "2026-01-02,99,105,99,104,1\n"
        "2026-01-03,104,121,103,120,1\n",
        encoding="utf-8",
    )
    return bars_root
