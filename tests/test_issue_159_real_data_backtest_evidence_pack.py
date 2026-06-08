from __future__ import annotations

import json
from pathlib import Path

from scripts import run_historical_entry_exit_backtest as runner


def test_real_data_backtest_writes_blocked_evidence_when_coverage_manifest_missing(monkeypatch, tmp_path: Path) -> None:
    plans_file = tmp_path / "plans.json"
    bars_root = tmp_path / "bars"
    universe = tmp_path / "survivorship_universe.csv"
    coverage_manifest = tmp_path / "missing_coverage_manifest.json"
    json_output = tmp_path / "reports" / "backtests" / "real-data-backtest-evidence.json"
    markdown_output = tmp_path / "reports" / "backtests" / "real-data-backtest-evidence.md"

    plans_file.write_text(
        json.dumps(
            {
                "plans": [
                    {
                        "signal_id": "real-plan-1",
                        "symbol": "AAPL",
                        "signal_date": "2026-01-02",
                        "entry_trigger": 101.0,
                        "stop_loss": 99.0,
                        "target_1": 105.0,
                        "action": "BUY_WATCH",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    bars_root.mkdir(parents=True)
    (bars_root / "AAPL.csv").write_text(
        "date,open,high,low,close,volume\n2026-01-03,100,102,99,101,1000\n",
        encoding="utf-8",
    )
    universe.write_text("symbol,start_date,end_date\nAAPL,2020-01-01,\n", encoding="utf-8")

    monkeypatch.setattr(
        runner,
        "parse_args",
        lambda: type(
            "Args",
            (),
            {
                "plans_file": str(plans_file),
                "bars_root": str(bars_root),
                "universe": str(universe),
                "coverage_manifest": str(coverage_manifest),
                "max_bars": 20,
                "run_id": "issue-159-missing-coverage",
                "data_source": "real_data",
                "strategy_version": "historical-entry-exit-v1",
                "real_data": True,
                "json_output": str(json_output),
                "markdown_output": str(markdown_output),
            },
        )(),
    )

    assert runner.main() == 1
    assert json_output.exists()
    assert markdown_output.exists()

    payload = json.loads(json_output.read_text(encoding="utf-8"))
    assert payload["run_id"] == "issue-159-missing-coverage"
    assert payload["data_source"] == "real_data"
    assert payload["is_demo"] is False
    assert payload["input_pack_gate_status"] == "PASSED"
    assert payload["input_completeness_status"] == "BLOCKED_MISSING_COVERAGE_MANIFEST"
    assert payload["run_health_status"] == "BLOCKED"
    assert payload["coverage_manifest_path"] == str(coverage_manifest)
    assert payload["survivorship_universe_path"] == str(universe)
    assert payload["trade_plans_path"] == str(plans_file)
    assert payload["input_plan_count"] == 0
    assert payload["accepted_plan_count"] == 0
    assert payload["rejected_plan_count"] == 0
    assert payload["live_trading_authorized"] is False
    assert payload["broker_execution_mode"] == "paper_only"
    assert payload["metrics"]["total"] == 0
    assert payload["results"] == []
    assert payload["rejection_reasons"][0]["reasons"] == ["missing_coverage_manifest"]


def test_real_data_backtest_writes_blocked_evidence_when_all_plans_are_rejected(monkeypatch, tmp_path: Path) -> None:
    plans_file = tmp_path / "plans.json"
    bars_root = tmp_path / "bars"
    universe = tmp_path / "survivorship_universe.csv"
    coverage_manifest = tmp_path / "coverage_manifest.json"
    json_output = tmp_path / "reports" / "backtests" / "real-data-backtest-evidence.json"
    markdown_output = tmp_path / "reports" / "backtests" / "real-data-backtest-evidence.md"

    plans_file.write_text(
        json.dumps(
            {
                "plans": [
                    {
                        "signal_id": "rejected-plan-1",
                        "symbol": "AAPL",
                        "signal_date": "2026-01-02",
                        "entry_trigger": 101.0,
                        "stop_loss": 103.0,
                        "target_1": 105.0,
                        "action": "BUY_WATCH",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    bars_root.mkdir(parents=True)
    (bars_root / "AAPL.csv").write_text(
        "date,open,high,low,close,volume\n2026-01-03,100,102,99,101,1000\n",
        encoding="utf-8",
    )
    universe.write_text("symbol,start_date,end_date\nAAPL,2020-01-01,\n", encoding="utf-8")
    coverage_manifest.write_text(json.dumps({"symbols": ["AAPL"]}), encoding="utf-8")

    monkeypatch.setattr(
        runner,
        "parse_args",
        lambda: type(
            "Args",
            (),
            {
                "plans_file": str(plans_file),
                "bars_root": str(bars_root),
                "universe": str(universe),
                "coverage_manifest": str(coverage_manifest),
                "max_bars": 20,
                "run_id": "issue-159-all-rejected",
                "data_source": "real_data",
                "strategy_version": "historical-entry-exit-v1",
                "real_data": True,
                "json_output": str(json_output),
                "markdown_output": str(markdown_output),
            },
        )(),
    )

    assert runner.main() == 1
    payload = json.loads(json_output.read_text(encoding="utf-8"))
    assert payload["run_id"] == "issue-159-all-rejected"
    assert payload["data_source"] == "real_data"
    assert payload["is_demo"] is False
    assert payload["input_pack_gate_status"] == "PASSED"
    assert payload["input_completeness_status"] == "EMPTY_INPUT"
    assert payload["run_health_status"] == "BLOCKED"
    assert payload["input_plan_count"] == 1
    assert payload["accepted_plan_count"] == 0
    assert payload["rejected_plan_count"] == 1
    assert payload["rejection_reasons"][0]["reasons"] == ["invalid_entry_stop_target_order"]
    assert payload["metrics"]["total"] == 0
    assert payload["results"] == []
