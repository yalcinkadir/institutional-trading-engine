from __future__ import annotations

import hashlib
import json
from pathlib import Path

from scripts.validate_bt9_real_historical_input_pack import validate_bt9_input_pack
from scripts.validate_real_data_backtest_evidence_gate import validate_real_data_backtest_evidence_artifact

AUDIT_CONTRACT_PATH = Path("docs/operations/bt184_historical_input_auditability.md")
BT131_WORKFLOW_PATH = Path(".github/workflows/bt131_real_data_backtest_evidence.yml")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_universe(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "symbol,effective_from,effective_to,active,asset_class,exchange,source,status,reason\n"
        "SPY,2020-01-01,,true,equity,NYSE,polygon,active,bt184_fixture\n",
        encoding="utf-8",
    )


def _write_bars(path: Path) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "date,timestamp,open,high,low,close,volume\n"
        "2026-06-10,2026-06-10T00:00:00+00:00,100,101,99,100.5,1000000\n"
        "2026-06-11,2026-06-11T00:00:00+00:00,101,103,100,102,1100000\n",
        encoding="utf-8",
    )
    return _sha256(path)


def _write_plans(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "metadata": {
            "pipeline_coupled": True,
            "pipeline_generation_source": "scanner_signal_quality_validator",
            "runtime_gates_applied": ["scanner", "signal_generator", "quality_fusion", "trade_plan_validator"],
            "generated_signal_count": 1,
            "validated_trade_plan_count": 1,
            "blocked_signal_count": 0,
        },
        "plans": [
            {
                "signal_id": "bt184-spy-001",
                "symbol": "SPY",
                "signal_date": "2026-06-10",
                "entry_trigger": 101.0,
                "stop_loss": 99.0,
                "target_1": 103.0,
                "source": "scanner_signal_quality_validator",
            }
        ],
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_manifest(path: Path, *, bars_path: Path, sha256: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "vendor": "polygon",
        "generated_at": "2026-06-11T00:00:00+00:00",
        "multiplier": 1,
        "timespan": "day",
        "requested_start_date": "2026-06-10",
        "requested_end_date": "2026-06-11",
        "symbol_count": 1,
        "ok_symbol_count": 1,
        "status": "ok",
        "missing_data_summary": [],
        "symbols": [
            {
                "symbol": "SPY",
                "start_date": "2026-06-10",
                "end_date": "2026-06-11",
                "bar_count": 2,
                "rows_fetched": 2,
                "status": "ok",
                "output_path": bars_path.as_posix(),
                "output_sha256": sha256,
                "missing_data_summary": [],
            }
        ],
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _valid_evidence_payload(input_checksums: dict[str, str]) -> dict:
    return {
        "run_id": "bt184-evidence-001",
        "data_source": "real_data",
        "is_demo": False,
        "symbol_universe": ["SPY"],
        "date_range": {"start": "2026-06-10", "end": "2026-06-11"},
        "strategy_version": "historical-entry-exit-v1",
        "tags": ["real_data", "research_only"],
        "input_pack_gate_status": "PASSED",
        "input_completeness_status": "OK",
        "run_health_status": "OK",
        "coverage_manifest_path": "data/historical/metadata/coverage_manifest.json",
        "survivorship_universe_path": "data/historical/metadata/bt131_runtime_universe.csv",
        "trade_plans_path": "data/trade_plans/historical_trade_plans.json",
        "input_checksums": input_checksums,
        "input_plan_count": 1,
        "accepted_plan_count": 1,
        "rejected_plan_count": 0,
        "rejection_reasons": [],
        "metrics": {"total": 1},
        "results": [{"signal_id": "bt184-spy-001", "symbol": "SPY"}],
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }


def test_184_bt9_passes_when_manifest_checksum_matches_source_bars(tmp_path: Path) -> None:
    universe = tmp_path / "data/historical/metadata/bt131_runtime_universe.csv"
    bars_root = tmp_path / "data/historical/bars/1day"
    bars = bars_root / "SPY.csv"
    plans = tmp_path / "data/trade_plans/historical_trade_plans.json"
    manifest = tmp_path / "data/historical/metadata/coverage_manifest.json"

    _write_universe(universe)
    digest = _write_bars(bars)
    _write_plans(plans)
    _write_manifest(manifest, bars_path=bars, sha256=digest)

    report = validate_bt9_input_pack(
        universe_path=universe,
        bars_root=bars_root,
        trade_plans_path=plans,
        coverage_manifest_path=manifest,
    )

    assert report.passed, report.failures
    assert report.input_checksums == {bars.as_posix(): digest}


def test_184_bt9_fails_when_coverage_manifest_is_missing(tmp_path: Path) -> None:
    universe = tmp_path / "data/historical/metadata/bt131_runtime_universe.csv"
    bars_root = tmp_path / "data/historical/bars/1day"
    bars = bars_root / "SPY.csv"
    plans = tmp_path / "data/trade_plans/historical_trade_plans.json"
    manifest = tmp_path / "data/historical/metadata/coverage_manifest.json"

    _write_universe(universe)
    _write_bars(bars)
    _write_plans(plans)

    report = validate_bt9_input_pack(
        universe_path=universe,
        bars_root=bars_root,
        trade_plans_path=plans,
        coverage_manifest_path=manifest,
    )

    assert not report.passed
    assert "missing_coverage_manifest" in report.failures


def test_184_bt9_fails_when_manifest_checksum_does_not_match_bars(tmp_path: Path) -> None:
    universe = tmp_path / "data/historical/metadata/bt131_runtime_universe.csv"
    bars_root = tmp_path / "data/historical/bars/1day"
    bars = bars_root / "SPY.csv"
    plans = tmp_path / "data/trade_plans/historical_trade_plans.json"
    manifest = tmp_path / "data/historical/metadata/coverage_manifest.json"

    _write_universe(universe)
    _write_bars(bars)
    _write_plans(plans)
    _write_manifest(manifest, bars_path=bars, sha256="0" * 64)

    report = validate_bt9_input_pack(
        universe_path=universe,
        bars_root=bars_root,
        trade_plans_path=plans,
        coverage_manifest_path=manifest,
    )

    assert not report.passed
    assert "coverage_manifest_checksum_mismatch:SPY" in report.failures


def test_184_real_data_evidence_gate_requires_input_checksums(tmp_path: Path) -> None:
    evidence = tmp_path / "real-data-backtest-evidence.json"
    payload = _valid_evidence_payload(input_checksums={})
    evidence.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    report = validate_real_data_backtest_evidence_artifact(evidence)

    assert not report.passed
    assert "input_checksums" in report.invalid_fields


def test_184_real_data_evidence_gate_accepts_valid_input_checksums(tmp_path: Path) -> None:
    evidence = tmp_path / "real-data-backtest-evidence.json"
    payload = _valid_evidence_payload(input_checksums={"data/historical/bars/1day/SPY.csv": "a" * 64})
    evidence.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    report = validate_real_data_backtest_evidence_artifact(evidence)

    assert report.passed, report.to_dict()


def test_184_audit_contract_documents_repository_as_source_of_truth() -> None:
    text = AUDIT_CONTRACT_PATH.read_text(encoding="utf-8")

    assert "GitHub Actions artifacts are review aids. They are not the durable audit source of truth." in text
    assert "The repository is the durable source of truth" in text
    assert "data/historical/bars/1day/*.csv" in text
    assert "data/historical/metadata/coverage_manifest.json" in text
    assert "data/trade_plans/historical_trade_plans.json" in text
    assert "reports/backtests/real_data/runs/<github_run_id>/real-data-backtest-evidence.json" in text
    assert "reports/backtests/real_data/index.json" in text


def test_184_bt131_workflow_persists_source_inputs_not_only_artifacts() -> None:
    text = BT131_WORKFLOW_PATH.read_text(encoding="utf-8")

    assert "Persist validated backtest reports and source inputs to repository" in text
    assert "git add data/historical/bars/1day/*.csv" in text
    assert "data/historical/metadata/*.json" in text
    assert "data/historical/metadata/*.csv" in text
    assert "data/trade_plans/*.json" in text
    assert "git push" in text
    assert "actions/upload-artifact@v4" in text
    assert text.index("Persist validated backtest reports and source inputs to repository") < text.index("Upload real-data backtest evidence artifacts")
