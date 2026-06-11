from __future__ import annotations

import hashlib
import json
from pathlib import Path

from scripts import run_historical_entry_exit_backtest as runner


PIPELINE_METADATA = {
    "pipeline_coupled": True,
    "pipeline_generation_source": "scanner_signal_quality_validator",
    "generated_signal_count": 1,
    "validated_trade_plan_count": 1,
    "blocked_signal_count": 0,
    "runtime_gates_applied": [
        "scanner",
        "signal_generator",
        "quality_fusion",
        "trade_plan_validator",
    ],
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_universe(path: Path, symbol: str = "AAPL") -> None:
    path.write_text(
        "symbol,effective_from,effective_to,active,asset_class,exchange,source,status,reason\n"
        f"{symbol},2020-01-01,,true,equity,NASDAQ,initial_universe,active,issue 159 test universe\n",
        encoding="utf-8",
    )


def _write_bars(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "date,open,high,low,close,volume\n2026-01-03,100,102,99,101,1000\n",
        encoding="utf-8",
    )


def _write_coverage_manifest(path: Path, *, bars_path: Path, symbol: str = "AAPL") -> None:
    path.write_text(
        json.dumps(
            {
                "vendor": "polygon",
                "generated_at": "2026-06-11T00:00:00Z",
                "multiplier": 1,
                "timespan": "day",
                "requested_start_date": "2026-01-02",
                "requested_end_date": "2026-01-03",
                "symbol_count": 1,
                "ok_symbol_count": 1,
                "status": "ok",
                "missing_data_summary": [],
                "symbols": [
                    {
                        "symbol": symbol,
                        "start_date": "2026-01-02",
                        "end_date": "2026-01-03",
                        "bar_count": 1,
                        "rows_fetched": 1,
                        "status": "ok",
                        "output_path": bars_path.as_posix(),
                        "output_sha256": _sha256(bars_path),
                        "missing_data_summary": [],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )


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
                "metadata": PIPELINE_METADATA,
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
                ],
            }
        ),
        encoding="utf-8",
    )
    _write_bars(bars_root / "AAPL.csv")
    _write_universe(universe)

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
    assert payload["input_pack_gate_status"] == "FAILED"
    assert payload["input_completeness_status"] == "BLOCKED_INPUT_PACK"
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
    flat_reasons = [reason for item in payload["rejection_reasons"] for reason in item["reasons"]]
    assert "missing_coverage_manifest" in flat_reasons


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
                "metadata": PIPELINE_METADATA,
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
                ],
            }
        ),
        encoding="utf-8",
    )
    bars_path = bars_root / "AAPL.csv"
    _write_bars(bars_path)
    _write_universe(universe)
    _write_coverage_manifest(coverage_manifest, bars_path=bars_path)

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
    assert payload["input_checksums"] == {bars_path.as_posix(): _sha256(bars_path)}
    assert payload["input_plan_count"] == 1
    assert payload["accepted_plan_count"] == 0
    assert payload["rejected_plan_count"] == 1
    assert payload["rejection_reasons"][0]["reasons"] == ["invalid_entry_stop_target_order"]
    assert payload["metrics"]["total"] == 0
    assert payload["results"] == []
