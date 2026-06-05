from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts.validate_bt9_real_historical_input_pack import validate_bt9_input_pack

VALIDATOR_SCRIPT = Path("scripts/validate_bt9_real_historical_input_pack.py")


def _write_universe(path: Path, *, demo_marker: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    source = "demo_vendor" if demo_marker else "polygon"
    path.write_text(
        "symbol,effective_from,effective_to,asset_class,exchange,source,status\n"
        f"SPY,2024-01-01,,ETF,NYSEARCA,{source},active\n",
        encoding="utf-8",
    )


def _write_bars(root: Path, *, demo_marker: bool = False) -> None:
    root.mkdir(parents=True, exist_ok=True)
    source = "demo" if demo_marker else "real"
    (root / "SPY.csv").write_text(
        "date,open,high,low,close,volume,source\n"
        f"2026-06-01,100,101,99,100,1000000,{source}\n"
        f"2026-06-02,101,105,100,104,1100000,{source}\n",
        encoding="utf-8",
    )


def _write_trade_plans(path: Path, *, demo_marker: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "plans": [
            {
                "signal_id": "sig_SPY_001",
                "symbol": "SPY",
                "signal_date": "2026-06-01",
                "entry_trigger": 101.0,
                "stop_loss": 99.0,
                "target_1": 104.0,
                "target_2": 106.0,
                "source": "demo" if demo_marker else "paper_observation_validated",
            }
        ]
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_bt9_valid_real_historical_input_pack_passes(tmp_path: Path) -> None:
    universe = tmp_path / "data/universe/survivorship_universe.csv"
    bars_root = tmp_path / "data/historical/bars/1day"
    trade_plans = tmp_path / "data/trade_plans/historical_trade_plans.json"
    _write_universe(universe)
    _write_bars(bars_root)
    _write_trade_plans(trade_plans)

    report = validate_bt9_input_pack(universe_path=universe, bars_root=bars_root, trade_plans_path=trade_plans)

    assert report.passed is True
    assert report.failures == []
    assert report.symbols == ["SPY"]
    assert report.date_range == {"start": "2026-06-01", "end": "2026-06-02"}


def test_bt9_missing_universe_blocks_real_backtest(tmp_path: Path) -> None:
    bars_root = tmp_path / "data/historical/bars/1day"
    trade_plans = tmp_path / "data/trade_plans/historical_trade_plans.json"
    _write_bars(bars_root)
    _write_trade_plans(trade_plans)

    report = validate_bt9_input_pack(
        universe_path=tmp_path / "data/universe/missing.csv",
        bars_root=bars_root,
        trade_plans_path=trade_plans,
    )

    assert report.passed is False
    assert "missing_universe_file" in report.failures


def test_bt9_missing_bars_block_real_backtest(tmp_path: Path) -> None:
    universe = tmp_path / "data/universe/survivorship_universe.csv"
    trade_plans = tmp_path / "data/trade_plans/historical_trade_plans.json"
    _write_universe(universe)
    _write_trade_plans(trade_plans)

    report = validate_bt9_input_pack(
        universe_path=universe,
        bars_root=tmp_path / "data/historical/bars/1day",
        trade_plans_path=trade_plans,
    )

    assert report.passed is False
    assert "missing_bars_root" in report.failures


def test_bt9_missing_trade_plans_block_real_backtest(tmp_path: Path) -> None:
    universe = tmp_path / "data/universe/survivorship_universe.csv"
    bars_root = tmp_path / "data/historical/bars/1day"
    _write_universe(universe)
    _write_bars(bars_root)

    report = validate_bt9_input_pack(
        universe_path=universe,
        bars_root=bars_root,
        trade_plans_path=tmp_path / "data/trade_plans/missing.json",
    )

    assert report.passed is False
    assert "missing_trade_plans_file" in report.failures


def test_bt9_rejects_demo_markers_in_input_pack(tmp_path: Path) -> None:
    universe = tmp_path / "data/universe/survivorship_universe.csv"
    bars_root = tmp_path / "data/historical/bars/1day"
    trade_plans = tmp_path / "data/trade_plans/historical_trade_plans.json"
    _write_universe(universe, demo_marker=True)
    _write_bars(bars_root, demo_marker=True)
    _write_trade_plans(trade_plans, demo_marker=True)

    report = validate_bt9_input_pack(universe_path=universe, bars_root=bars_root, trade_plans_path=trade_plans)

    assert report.passed is False
    assert any("demo_marker" in failure for failure in report.failures)


def test_bt9_cli_fails_closed_when_pack_is_missing(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR_SCRIPT),
            "--universe",
            str(tmp_path / "missing-universe.csv"),
            "--bars-root",
            str(tmp_path / "missing-bars"),
            "--trade-plans",
            str(tmp_path / "missing-plans.json"),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "BT9 real historical input pack gate status: FAIL" in result.stdout
    assert "missing_universe_file" in result.stdout
    assert "missing_trade_plans_file" in result.stdout
