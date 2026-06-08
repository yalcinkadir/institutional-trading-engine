#!/usr/bin/env python3
"""Run historical Entry / Stop / Exit backtest from JSON trade plans."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.validate_bt9_real_historical_input_pack import validate_bt9_input_pack
from src.backtesting.historical_entry_exit_backtest import load_trade_plans_with_report, run_backtest
from src.backtesting.historical_models import HistoricalBacktestMetrics, HistoricalBacktestReport
from src.backtesting.historical_report import write_report

DEFAULT_COVERAGE_MANIFEST = "data/historical/metadata/coverage_manifest.json"


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
        input_plan_count=input_plan_count,
        accepted_plan_count=accepted_plan_count,
        rejected_plan_count=rejected_plan_count,
        rejection_reasons=rejection_reasons,
        live_trading_authorized=False,
        broker_execution_mode="paper_only",
    )
    write_report(report, json_path=Path(args.json_output), markdown_path=Path(args.markdown_output))


def _fail_closed_if_real_data_requested(args: argparse.Namespace) -> tuple[int | None, str]:
    if not _real_data_requested(args):
        return None, "NOT_RUN"

    gate = validate_bt9_input_pack(
        universe_path=Path(args.universe),
        bars_root=Path(args.bars_root),
        trade_plans_path=Path(args.plans_file),
    )
    if not gate.passed:
        print("BT9 real historical input pack gate status: FAIL")
        reasons: list[dict] = []
        for failure in gate.failures:
            print(f"- {failure}")
            reasons.append({"plan_index": None, "signal_id": None, "symbol": None, "reasons": [failure]})
        _write_blocked_real_data_evidence(
            args,
            input_pack_gate_status="FAILED",
            input_completeness_status="BLOCKED_INPUT_PACK",
            run_health_status="BLOCKED",
            rejection_reasons=reasons,
        )
        return 1, "FAILED"

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
        )
        return 1, "FAILED"

    return None, "PASSED"


def main() -> int:
    args = parse_args()
    gate_exit, input_pack_gate_status = _fail_closed_if_real_data_requested(args)
    if gate_exit is not None:
        return gate_exit

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
        plan_load_report=plan_load.report,
    )
    write_report(report, json_path=Path(args.json_output), markdown_path=Path(args.markdown_output))

    print("Historical Entry / Stop / Exit backtest completed")
    print(f"Run ID: {report.run_id}")
    print(f"Data source: {report.data_source}")
    print(f"Is demo: {report.is_demo}")
    print(f"Input pack gate: {report.input_pack_gate_status}")
    print(f"Input plans: {report.input_plan_count}")
    print(f"Accepted plans: {report.accepted_plan_count}")
    print(f"Rejected plans: {report.rejected_plan_count}")
    print(f"Plans: {report.metrics.total}")
    print(f"Entry hit rate: {report.metrics.entry_hit_rate:.2%}")
    print(f"Target 1 hit rate: {report.metrics.target_1_hit_rate:.2%}")
    print(f"Target 2 hit rate: {report.metrics.target_2_hit_rate:.2%}")
    print(f"Stop hit rate: {report.metrics.stop_hit_rate:.2%}")
    print(f"Expectancy R: {report.metrics.expectancy_r:.4f}")
    print(f"JSON: {args.json_output}")
    print(f"Markdown: {args.markdown_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
