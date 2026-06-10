#!/usr/bin/env python3
"""Run historical Entry / Stop / Exit backtest from JSON trade plans."""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path
from statistics import median

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.validate_bt9_real_historical_input_pack import validate_bt9_input_pack
from src.backtesting.historical_entry_exit_backtest import load_trade_plans_with_report, run_backtest
from src.backtesting.historical_models import (
    HistoricalBacktestMetrics,
    HistoricalBacktestReport,
    HistoricalBacktestResult,
    derive_sample_quality_status,
)
from src.backtesting.historical_report import write_report
from src.validation.capacity_turnover_realism_gate import RESEARCH_ONLY_FOOTER

DEFAULT_COVERAGE_MANIFEST = "data/historical/metadata/coverage_manifest.json"
DEFAULT_PROPOSED_CAPITAL_USD = 100000.0
DEFAULT_ROUND_TRIP_COST_BPS = 7.5
TRADING_DAYS_PER_YEAR = 252


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
    parser.add_argument(
        "--proposed-capital-usd",
        type=float,
        default=DEFAULT_PROPOSED_CAPITAL_USD,
        help="Research-only proposed capital used for capacity/turnover realism metrics.",
    )
    parser.add_argument(
        "--round-trip-cost-bps",
        type=float,
        default=DEFAULT_ROUND_TRIP_COST_BPS,
        help="Research-only round-trip cost assumption used for net expectancy bps.",
    )
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


def _safe_positive_float(value: object) -> float | None:
    try:
        converted = float(value)
    except (TypeError, ValueError):
        return None
    return converted if converted > 0 else None


def _load_symbol_adv_usd(bars_root: Path, symbol: str) -> float:
    """Return median dollar ADV from real historical bars.

    The calculation intentionally uses the same bar contract as the backtest
    input gate: close * volume from the symbol CSV. Missing, non-positive or
    malformed values yield 0.0 and therefore fail the downstream BT7 positive
    scale / liquidity gates instead of silently using a fallback.
    """

    path = bars_root / f"{symbol}.csv"
    values: list[float] = []
    if not path.exists():
        return 0.0
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            close = _safe_positive_float(row.get("close"))
            volume = _safe_positive_float(row.get("volume"))
            if close is None or volume is None:
                continue
            values.append(close * volume)
    return round(float(median(values)), 4) if values else 0.0


def _parse_iso_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def _calendar_span_days(report: HistoricalBacktestReport) -> int:
    start = _parse_iso_date(report.date_range.get("start"))
    end = _parse_iso_date(report.date_range.get("end"))
    if start is None or end is None or end < start:
        return 1
    return max((end - start).days + 1, 1)


def _holding_days(results: list[HistoricalBacktestResult]) -> list[int]:
    days: list[int] = []
    for result in results:
        entry = _parse_iso_date(result.entry_date)
        exit_ = _parse_iso_date(result.exit_date)
        if entry is None or exit_ is None or exit_ < entry:
            continue
        days.append(max((exit_ - entry).days, 1))
    return days


def _average_holding_days(results: list[HistoricalBacktestResult]) -> float:
    values = _holding_days(results)
    return round(sum(values) / len(values), 4) if values else 0.0


def _gross_expectancy_bps(report: HistoricalBacktestReport) -> float:
    """Convert average R into approximate gross bps using observed entry risk.

    For each entered trade, one R is approximated as initial risk divided by the
    observed entry price. If a trade lacks those fields, it is excluded. If no
    entered trade has enough data, return 0.0 and let BT7 fail closed.
    """

    bps_values: list[float] = []
    for result in report.results:
        entry_price = _safe_positive_float(result.entry_price)
        initial_stop = _safe_positive_float(result.initial_stop_loss)
        if entry_price is None or initial_stop is None or initial_stop >= entry_price:
            continue
        one_r_bps = ((entry_price - initial_stop) / entry_price) * 10000.0
        bps_values.append(result.r_multiple * one_r_bps)
    return round(sum(bps_values) / len(bps_values), 4) if bps_values else 0.0


def _build_capacity_turnover_snapshot(
    report: HistoricalBacktestReport,
    *,
    bars_root: Path,
    proposed_capital_usd: float = DEFAULT_PROPOSED_CAPITAL_USD,
    round_trip_cost_bps: float = DEFAULT_ROUND_TRIP_COST_BPS,
) -> dict:
    """Build a data-derived real-data capacity/turnover snapshot.

    No ADV, turnover, holding-period or expectancy defaults are used. Missing
    or malformed real bar data produces zero-valued metrics that fail the BT7
    capacity/turnover realism gate instead of becoming reviewable evidence.
    """

    trade_count = report.metrics.total
    symbol_count = max(len(report.symbol_universe), 1)
    symbol_advs = {symbol: _load_symbol_adv_usd(bars_root, symbol) for symbol in report.symbol_universe}
    positive_advs = [value for value in symbol_advs.values() if value > 0]
    median_adv_usd = round(float(median(positive_advs)), 4) if positive_advs else 0.0
    total_adv_usd = sum(positive_advs)

    per_symbol_capital = proposed_capital_usd / symbol_count if symbol_count else proposed_capital_usd
    position_adv_pcts = [per_symbol_capital / adv * 100.0 for adv in positive_advs if adv > 0]
    max_position_adv_pct = round(max(position_adv_pcts), 4) if position_adv_pcts else 0.0
    portfolio_adv_pct = round(proposed_capital_usd / total_adv_usd * 100.0, 4) if total_adv_usd > 0 else 0.0

    span_days = _calendar_span_days(report)
    average_daily_turnover_pct = round((trade_count * per_symbol_capital / span_days) / proposed_capital_usd * 100.0, 4)
    annual_turnover_pct = round(average_daily_turnover_pct * TRADING_DAYS_PER_YEAR, 4)

    gross_expectancy_bps = _gross_expectancy_bps(report)
    net_expectancy_bps = round(gross_expectancy_bps - round_trip_cost_bps, 4)
    average_holding_days = _average_holding_days(report.results)

    return {
        "run_id": report.run_id,
        "strategy_id": report.strategy_version,
        "dataset_id": "real-data-historical-backtest",
        "parameter_version": report.strategy_version,
        "evidence_type": "capacity_turnover_realism",
        "proposed_capital_usd": proposed_capital_usd,
        "symbol_count": symbol_count,
        "metrics": {
            "median_adv_usd": median_adv_usd,
            "max_position_adv_pct": max_position_adv_pct,
            "portfolio_adv_pct": portfolio_adv_pct,
            "average_daily_turnover_pct": average_daily_turnover_pct,
            "annual_turnover_pct": annual_turnover_pct,
            "round_trip_cost_bps": round_trip_cost_bps,
            "gross_expectancy_bps": gross_expectancy_bps,
            "net_expectancy_bps": net_expectancy_bps,
            "average_holding_days": average_holding_days,
            "trade_count": trade_count,
            "slippage_model_coverage_pct": 100.0,
        },
        "artifact_hashes": {
            "coverage_manifest": report.coverage_manifest_path,
            "trade_plans": report.trade_plans_path,
            "survivorship_universe": report.survivorship_universe_path,
            "bars_root": str(bars_root),
        },
        "tags": ["real_data", "public_safe", "research_only"],
        "footer": RESEARCH_ONLY_FOOTER,
    }


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
        sample_quality_status=derive_sample_quality_status(0, is_demo=False),
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
    report = replace(report, sample_quality_status=derive_sample_quality_status(report.metrics.total, is_demo=is_demo))
    if not is_demo:
        report = replace(
            report,
            capacity_turnover_snapshot=_build_capacity_turnover_snapshot(
                report,
                bars_root=Path(args.bars_root),
                proposed_capital_usd=args.proposed_capital_usd,
                round_trip_cost_bps=args.round_trip_cost_bps,
            ),
        )
    write_report(report, json_path=Path(args.json_output), markdown_path=Path(args.markdown_output))

    print("Historical Entry / Stop / Exit backtest completed")
    print(f"Run ID: {report.run_id}")
    print(f"Data source: {report.data_source}")
    print(f"Is demo: {report.is_demo}")
    print(f"Input pack gate: {report.input_pack_gate_status}")
    print(f"Sample quality status: {report.sample_quality_status}")
    if report.capacity_turnover_snapshot is not None:
        print("Capacity/turnover snapshot: present")
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
