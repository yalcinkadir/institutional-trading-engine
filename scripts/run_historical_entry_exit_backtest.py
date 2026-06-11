#!/usr/bin/env python3
"""Run historical Entry / Stop / Exit backtest from JSON trade plans."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.validate_bt9_real_historical_input_pack import validate_bt9_input_pack
from src.backtesting.historical_entry_exit_backtest import load_trade_plans_with_report, run_backtest
from src.backtesting.historical_models import HistoricalBacktestMetrics, HistoricalBacktestReport
from src.backtesting.historical_report import write_report

DEFAULT_COVERAGE_MANIFEST = "data/historical/metadata/coverage_manifest.json"
PIPELINE_GATE_NAMES = [
    "scanner",
    "signal_generator",
    "quality_fusion",
    "trade_plan_validator",
]
ACCEPTED_PIPELINE_GENERATION_SOURCES = {
    "runtime_pipeline_adapter",
    "scanner_signal_quality_validator",
}
FORBIDDEN_REAL_DATA_GENERATION_SOURCES = {
    "validated_paper_observation_export",
    "deterministic_historical_generator",
    "historical_demo_generator",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run historical Entry / Stop / Exit backtest.")
    parser.add_argument("--plans-file", required=True, help="JSON list, plans[] or signals[] with trade plans.")
    parser.add_argument("--bars-root", default="data/historical/bars/1day")
    parser.add_argument("--universe", default="data/universe/survivorship_universe.csv")
    parser.add_argument("--coverage-manifest", default=DEFAULT_COVERAGE_MANIFEST)
    parser.add_argument("--max-bars", type=int, default=20)
    parser.add_argument("--run-id", default="historical-demo-run")
    parser.add_argument("--data-source", default="historical_demo", choices=["historical_demo", "real_data"])
    parser.add_argument("--strategy-version", default="historical-entry-exit-v1")
    parser.add_argument("--real-data", action="store_true", help="Mark output as real historical-data evidence.")
    parser.add_argument("--json-output", default="reports/backtests/historical-entry-exit-backtest.json")
    parser.add_argument("--markdown-output", default="reports/backtests/historical-entry-exit-backtest.md")
    return parser.parse_args()


def _real_data_requested(args: argparse.Namespace) -> bool:
    return bool(args.real_data or args.data_source == "real_data")


def _empty_metrics() -> HistoricalBacktestMetrics:
    return HistoricalBacktestMetrics(
        total=0,
        entry_hit_rate=0.0,
        expired_without_entry_rate=0.0,
        stop_hit_rate=0.0,
        target_1_hit_rate=0.0,
        target_2_hit_rate=0.0,
        false_breakout_rate=0.0,
        average_r=0.0,
        expectancy_r=0.0,
    )


def _read_trade_plan_payload(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return {
            "metadata": {},
            "plans": payload,
        }
    if isinstance(payload, dict):
        return payload
    return {
        "metadata": {},
        "plans": [],
    }


def _plan_count(payload: dict[str, Any]) -> int:
    raw = payload.get("plans") or payload.get("signals") or []
    return len(raw) if isinstance(raw, list) else 0


def _metadata(payload: dict[str, Any]) -> dict[str, Any]:
    metadata = payload.get("metadata") or {}
    return metadata if isinstance(metadata, dict) else {}


def _metadata_int(metadata: dict[str, Any], key: str, default: int) -> int:
    try:
        return int(metadata.get(key, default))
    except (TypeError, ValueError):
        return default


def _runtime_gates(metadata: dict[str, Any]) -> list[str]:
    raw = metadata.get("runtime_gates_applied") or []
    if isinstance(raw, list):
        return [str(item) for item in raw]
    return []


def _write_blocked_real_data_evidence(
    args: argparse.Namespace,
    *,
    input_pack_gate_status: str,
    input_completeness_status: str,
    run_health_status: str,
    rejection_reasons: list[dict],
    input_plan_count: int = 0,
    accepted_plan_count: int = 0,
    rejected_plan_count: int = 0,
    pipeline_coupled: bool = False,
    pipeline_generation_source: str = "UNKNOWN",
    generated_signal_count: int = 0,
    validated_trade_plan_count: int = 0,
    blocked_signal_count: int = 0,
    runtime_gates_applied: list[str] | None = None,
    input_checksums: dict[str, str] | None = None,
) -> None:
    report = HistoricalBacktestReport(
        metrics=_empty_metrics(),
        results=[],
        run_id=args.run_id,
        data_source="real_data",
        is_demo=False,
        symbol_universe=[],
        date_range={},
        strategy_version=args.strategy_version,
        tags=["real_data", "research_only", "blocked"],
        input_pack_gate_status=input_pack_gate_status,
        input_completeness_status=input_completeness_status,
        run_health_status=run_health_status,
        coverage_manifest_path=str(Path(args.coverage_manifest)),
        survivorship_universe_path=str(Path(args.universe)),
        trade_plans_path=str(Path(args.plans_file)),
        input_checksums=input_checksums or {},
        input_plan_count=input_plan_count,
        accepted_plan_count=accepted_plan_count,
        rejected_plan_count=rejected_plan_count,
        rejection_reasons=rejection_reasons,
        pipeline_coupled=pipeline_coupled,
        pipeline_generation_source=pipeline_generation_source,
        generated_signal_count=generated_signal_count,
        validated_trade_plan_count=validated_trade_plan_count,
        blocked_signal_count=blocked_signal_count,
        runtime_gates_applied=runtime_gates_applied or [],
        live_trading_authorized=False,
        broker_execution_mode="paper_only",
    )
    write_report(report, json_path=Path(args.json_output), markdown_path=Path(args.markdown_output))


def _fail_closed_if_real_data_requested(args: argparse.Namespace) -> tuple[int | None, str, dict[str, str]]:
    if not _real_data_requested(args):
        return None, "NOT_RUN", {}

    gate = validate_bt9_input_pack(
        universe_path=Path(args.universe),
        bars_root=Path(args.bars_root),
        trade_plans_path=Path(args.plans_file),
        coverage_manifest_path=Path(args.coverage_manifest),
    )
    if not gate.passed:
        print("BT9 real historical input pack gate status: FAIL")
        for failure in gate.failures:
            print(f"- {failure}")
        _write_blocked_real_data_evidence(
            args,
            input_pack_gate_status="FAILED",
            input_completeness_status="BLOCKED_INPUT_PACK",
            run_health_status="BLOCKED",
            rejection_reasons=[
                {
                    "plan_index": None,
                    "signal_id": None,
                    "symbol": None,
                    "reasons": list(gate.failures),
                }
            ],
            input_checksums=gate.input_checksums,
        )
        return 1, "FAILED", gate.input_checksums

    if not Path(args.coverage_manifest).exists():
        print("Real-data backtest blocked: missing_coverage_manifest")
        _write_blocked_real_data_evidence(
            args,
            input_pack_gate_status="PASSED",
            input_completeness_status="BLOCKED_MISSING_COVERAGE_MANIFEST",
            run_health_status="BLOCKED",
            rejection_reasons=[
                {
                    "plan_index": None,
                    "signal_id": None,
                    "symbol": None,
                    "reasons": ["missing_coverage_manifest"],
                }
            ],
            input_checksums=gate.input_checksums,
        )
        return 1, "FAILED", gate.input_checksums

    return None, "PASSED", gate.input_checksums


def _fail_closed_if_real_data_not_pipeline_coupled(
    args: argparse.Namespace,
    *,
    input_pack_gate_status: str,
    input_checksums: dict[str, str],
) -> int | None:
    if not _real_data_requested(args):
        return None

    payload = _read_trade_plan_payload(Path(args.plans_file))
    metadata = _metadata(payload)
    pipeline_coupled = metadata.get("pipeline_coupled") is True
    generation_source = str(metadata.get("pipeline_generation_source") or "UNKNOWN")
    runtime_gates_applied = _runtime_gates(metadata)
    missing_gates = sorted(set(PIPELINE_GATE_NAMES) - set(runtime_gates_applied))
    input_count = _plan_count(payload)

    generation_source_allowed = generation_source in ACCEPTED_PIPELINE_GENERATION_SOURCES
    generation_source_forbidden = generation_source in FORBIDDEN_REAL_DATA_GENERATION_SOURCES

    if pipeline_coupled and not missing_gates and generation_source_allowed:
        return None

    reasons = []
    if not pipeline_coupled:
        reasons.append("real_data_backtest_requires_pipeline_coupled_trade_plans")
    if missing_gates:
        reasons.append("missing_runtime_gates:" + ",".join(missing_gates))
    if generation_source_forbidden:
        reasons.append(f"forbidden_pipeline_generation_source:{generation_source}")
    elif not generation_source_allowed:
        reasons.append(f"unsupported_pipeline_generation_source:{generation_source}")

    print("Real-data backtest blocked: non_canonical_pipeline_trade_plans")
    _write_blocked_real_data_evidence(
        args,
        input_pack_gate_status=input_pack_gate_status,
        input_completeness_status="BLOCKED_NON_PIPELINE_COUPLED_PLANS",
        run_health_status="BLOCKED",
        rejection_reasons=[
            {
                "plan_index": None,
                "signal_id": None,
                "symbol": None,
                "reasons": reasons,
            }
        ],
        input_plan_count=input_count,
        accepted_plan_count=0,
        rejected_plan_count=input_count,
        pipeline_coupled=pipeline_coupled,
        pipeline_generation_source=generation_source,
        generated_signal_count=_metadata_int(metadata, "generated_signal_count", input_count),
        validated_trade_plan_count=_metadata_int(metadata, "validated_trade_plan_count", 0),
        blocked_signal_count=_metadata_int(metadata, "blocked_signal_count", input_count),
        runtime_gates_applied=runtime_gates_applied,
        input_checksums=input_checksums,
    )
    return 1


def main() -> int:
    args = parse_args()
    gate_exit, input_pack_gate_status, input_checksums = _fail_closed_if_real_data_requested(args)
    if gate_exit is not None:
        return gate_exit

    pipeline_exit = _fail_closed_if_real_data_not_pipeline_coupled(
        args,
        input_pack_gate_status=input_pack_gate_status,
        input_checksums=input_checksums,
    )
    if pipeline_exit is not None:
        return pipeline_exit

    payload = _read_trade_plan_payload(Path(args.plans_file))
    metadata = _metadata(payload)
    runtime_gates_applied = _runtime_gates(metadata)

    plan_load = load_trade_plans_with_report(Path(args.plans_file))
    if _real_data_requested(args) and plan_load.report.accepted_plan_count == 0:
        print("Real-data backtest blocked: accepted_plan_count=0")
        _write_blocked_real_data_evidence(
            args,
            input_pack_gate_status=input_pack_gate_status,
            input_completeness_status="EMPTY_INPUT",
            run_health_status="BLOCKED",
            rejection_reasons=[rejection.to_dict() for rejection in plan_load.report.rejection_reasons],
            input_plan_count=plan_load.report.input_plan_count,
            accepted_plan_count=plan_load.report.accepted_plan_count,
            rejected_plan_count=plan_load.report.rejected_plan_count,
            pipeline_coupled=metadata.get("pipeline_coupled") is True,
            pipeline_generation_source=str(metadata.get("pipeline_generation_source") or "UNKNOWN"),
            generated_signal_count=_metadata_int(metadata, "generated_signal_count", plan_load.report.input_plan_count),
            validated_trade_plan_count=_metadata_int(metadata, "validated_trade_plan_count", plan_load.report.accepted_plan_count),
            blocked_signal_count=_metadata_int(metadata, "blocked_signal_count", plan_load.report.rejected_plan_count),
            runtime_gates_applied=runtime_gates_applied,
            input_checksums=input_checksums,
        )
        return 1

    data_source = "real_data" if args.real_data else args.data_source
    is_demo = data_source != "real_data"
    report = run_backtest(
        plan_load.plans,
        bars_root=Path(args.bars_root),
        max_bars=args.max_bars,
        run_id=args.run_id,
        data_source=data_source,
        is_demo=is_demo,
        strategy_version=args.strategy_version,
        input_pack_gate_status=input_pack_gate_status,
        coverage_manifest_path=str(Path(args.coverage_manifest)),
        survivorship_universe_path=str(Path(args.universe)),
        trade_plans_path=str(Path(args.plans_file)),
        input_checksums=input_checksums,
        plan_load_report=plan_load.report,
        pipeline_coupled=metadata.get("pipeline_coupled") is True,
        pipeline_generation_source=str(metadata.get("pipeline_generation_source") or "UNKNOWN"),
        generated_signal_count=_metadata_int(metadata, "generated_signal_count", plan_load.report.input_plan_count),
        validated_trade_plan_count=_metadata_int(metadata, "validated_trade_plan_count", plan_load.report.accepted_plan_count),
        blocked_signal_count=_metadata_int(metadata, "blocked_signal_count", plan_load.report.rejected_plan_count),
        runtime_gates_applied=runtime_gates_applied,
    )
    write_report(report, json_path=Path(args.json_output), markdown_path=Path(args.markdown_output))

    print("Historical Entry / Stop / Exit backtest complete")
    print(f"Data source: {report.data_source}")
    print(f"Is demo: {report.is_demo}")
    print(f"Input pack gate: {report.input_pack_gate_status}")
    print(f"Pipeline coupled: {report.pipeline_coupled}")
    print(f"Input checksums: {len(report.input_checksums)}")
    print(f"Input plans: {report.input_plan_count}")
    print(f"Accepted plans: {report.accepted_plan_count}")
    print(f"Rejected plans: {report.rejected_plan_count}")
    print(f"Plans: {report.metrics.total}")
    print(f"Entry hit rate: {report.metrics.entry_hit_rate:.2%}")
    print(f"Stop hit rate: {report.metrics.stop_hit_rate:.2%}")
    print(f"Target 1 hit rate: {report.metrics.target_1_hit_rate:.2%}")
    print(f"Average R: {report.metrics.average_r:.2f}")
    print(f"Expectancy R: {report.metrics.expectancy_r:.2f}")
    print(f"JSON report: {args.json_output}")
    print(f"Markdown report: {args.markdown_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
