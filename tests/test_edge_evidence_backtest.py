from __future__ import annotations

import json
from pathlib import Path

from src.backtesting.edge_evidence_backtest import (
    EdgeEvidenceBacktestConfig,
    run_edge_evidence_backtest,
)


def _write_universe(path: Path, *, symbols: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = ["symbol,active_from,active_to,delisting_reason,successor_symbol,final_close_price,notes"]
    for symbol in symbols:
        rows.append(f"{symbol},2020-01-01,,,,,test")
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def _write_plans(path: Path, symbols: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "plans": [
                    {
                        "signal_id": f"sig-{symbol}",
                        "symbol": symbol,
                        "signal_date": "2026-01-01",
                        "entry_trigger": 100,
                        "stop_loss": 95,
                        "target_1": 110,
                        "target_2": 120,
                    }
                    for symbol in symbols
                ]
            }
        ),
        encoding="utf-8",
    )


def _write_bars(root: Path, symbol: str) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / f"{symbol}.csv").write_text(
        "date,open,high,low,close,volume\n"
        "2026-01-02,99,105,99,104,1000000\n"
        "2026-01-03,104,121,103,120,1000000\n",
        encoding="utf-8",
    )


def test_edge_backtest_fails_closed_when_universe_too_small(tmp_path: Path) -> None:
    universe_path = tmp_path / "universe.csv"
    plans_path = tmp_path / "plans.json"
    bars_root = tmp_path / "bars"
    _write_universe(universe_path, symbols=["TEST"])
    _write_plans(plans_path, ["TEST"])
    _write_bars(bars_root, "TEST")

    report = run_edge_evidence_backtest(
        EdgeEvidenceBacktestConfig(
            universe_path=universe_path,
            trade_plans_path=plans_path,
            bars_root=bars_root,
            output_dir=tmp_path / "reports",
            minimum_tradeable_count=500,
        )
    )

    assert report.passed is False
    assert "universe_coverage_below_minimum" in report.reasons
    assert (tmp_path / "reports" / "edge-evidence-summary.json").exists()


def test_edge_backtest_fails_closed_when_trade_plans_file_is_missing(tmp_path: Path) -> None:
    universe_path = tmp_path / "universe.csv"
    bars_root = tmp_path / "bars"
    _write_universe(universe_path, symbols=["TEST"])
    _write_bars(bars_root, "TEST")

    report = run_edge_evidence_backtest(
        EdgeEvidenceBacktestConfig(
            universe_path=universe_path,
            trade_plans_path=tmp_path / "missing-plans.json",
            bars_root=bars_root,
            output_dir=tmp_path / "reports",
            minimum_tradeable_count=1,
        )
    )

    assert report.passed is False
    assert report.trade_plan_count == 0
    assert "no_trade_plans_loaded" in report.reasons
    assert (tmp_path / "reports" / "edge-evidence-summary.md").exists()


def test_edge_backtest_runs_when_gates_pass_with_relaxed_minimum(tmp_path: Path) -> None:
    universe_path = tmp_path / "universe.csv"
    plans_path = tmp_path / "plans.json"
    bars_root = tmp_path / "bars"
    _write_universe(universe_path, symbols=["TEST"])
    _write_plans(plans_path, ["TEST"])
    _write_bars(bars_root, "TEST")

    report = run_edge_evidence_backtest(
        EdgeEvidenceBacktestConfig(
            universe_path=universe_path,
            trade_plans_path=plans_path,
            bars_root=bars_root,
            output_dir=tmp_path / "reports",
            minimum_tradeable_count=1,
        )
    )

    assert report.trade_plan_count == 1
    assert report.historical_result_count == 1
    assert (tmp_path / "reports" / "historical-entry-exit-backtest.json").exists()
    assert (tmp_path / "reports" / "walk-forward-validation.json").exists()
    assert (tmp_path / "reports" / "out-of-sample-lockbox.json").exists()


def test_edge_backtest_fails_survivorship_audit_for_out_of_window_plan(tmp_path: Path) -> None:
    universe_path = tmp_path / "universe.csv"
    plans_path = tmp_path / "plans.json"
    bars_root = tmp_path / "bars"
    universe_path.parent.mkdir(parents=True, exist_ok=True)
    universe_path.write_text(
        "symbol,active_from,active_to,delisting_reason,successor_symbol,final_close_price,notes\n"
        "TEST,2020-01-01,2025-01-01,bankruptcy,,,,\n",
        encoding="utf-8",
    )
    _write_plans(plans_path, ["TEST"])
    _write_bars(bars_root, "TEST")

    report = run_edge_evidence_backtest(
        EdgeEvidenceBacktestConfig(
            universe_path=universe_path,
            trade_plans_path=plans_path,
            bars_root=bars_root,
            output_dir=tmp_path / "reports",
            minimum_tradeable_count=1,
        )
    )

    assert report.passed is False
    assert "survivorship_audit_failed" in report.reasons
