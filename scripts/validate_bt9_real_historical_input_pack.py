#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.validate_survivorship_universe import validate_survivorship_universe

DEMO_MARKERS = {"demo", "synthetic", "public_safe", "historical_demo", "placeholder"}
REQUIRED_BAR_COLUMNS = {"date", "open", "high", "low", "close", "volume"}
REQUIRED_TRADE_PLAN_FIELDS = {"signal_id", "symbol", "signal_date", "entry_trigger", "stop_loss", "target_1"}


@dataclass(frozen=True)
class BT9RealHistoricalInputPackReport:
    passed: bool
    universe_path: str
    bars_root: str
    trade_plans_path: str
    symbols: list[str] = field(default_factory=list)
    date_range: dict[str, str] = field(default_factory=dict)
    failures: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _has_demo_marker(value: Any) -> bool:
    if isinstance(value, str):
        lower = value.lower()
        return any(marker in lower for marker in DEMO_MARKERS)
    if isinstance(value, list):
        return any(_has_demo_marker(item) for item in value)
    if isinstance(value, dict):
        return any(_has_demo_marker(item) for item in value.values())
    return False


def _read_trade_plans(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    if not path.exists():
        return [], ["missing_trade_plans_file"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [], [f"trade_plans_invalid_json:{exc}"]
    raw = payload if isinstance(payload, list) else payload.get("plans") or payload.get("signals") if isinstance(payload, dict) else None
    if not isinstance(raw, list) or not raw:
        return [], ["trade_plans_empty_or_invalid"]
    failures: list[str] = []
    plans: list[dict[str, Any]] = []
    for index, plan in enumerate(raw):
        if not isinstance(plan, dict):
            failures.append(f"trade_plan_{index}_not_object")
            continue
        missing = sorted(field_name for field_name in REQUIRED_TRADE_PLAN_FIELDS if plan.get(field_name) in (None, ""))
        if missing:
            failures.append(f"trade_plan_{index}_missing:{','.join(missing)}")
        if _has_demo_marker(plan):
            failures.append(f"trade_plan_{index}_demo_marker")
        plans.append(plan)
    return plans, failures


def _validate_bars(bars_root: Path, symbols: list[str]) -> tuple[dict[str, str], list[str]]:
    if not bars_root.exists():
        return {}, ["missing_bars_root"]
    failures: list[str] = []
    all_dates: list[str] = []
    for symbol in symbols:
        path = bars_root / f"{symbol}.csv"
        if not path.exists():
            failures.append(f"missing_bars:{symbol}")
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            failures.append(f"empty_bars:{symbol}")
            continue
        columns = set(rows[0].keys())
        missing_columns = sorted(REQUIRED_BAR_COLUMNS - columns)
        if missing_columns:
            failures.append(f"bars_missing_columns:{symbol}:{','.join(missing_columns)}")
            continue
        if any(_has_demo_marker(row) for row in rows):
            failures.append(f"bars_demo_marker:{symbol}")
        for row_index, row in enumerate(rows, start=2):
            if any(row.get(column) in (None, "") for column in REQUIRED_BAR_COLUMNS):
                failures.append(f"bars_incomplete_row:{symbol}:{row_index}")
            all_dates.append(str(row.get("date")))
    all_dates = sorted(date for date in all_dates if date)
    return ({"start": all_dates[0], "end": all_dates[-1]} if all_dates else {}), failures


def validate_bt9_input_pack(*, universe_path: Path, bars_root: Path, trade_plans_path: Path) -> BT9RealHistoricalInputPackReport:
    plans, trade_plan_failures = _read_trade_plans(trade_plans_path)
    plan_symbols = sorted({str(plan.get("symbol") or "").upper() for plan in plans if plan.get("symbol")})
    signal_dates = sorted(str(plan.get("signal_date")) for plan in plans if plan.get("signal_date"))
    requested_start = signal_dates[0] if signal_dates else None
    requested_end = signal_dates[-1] if signal_dates else None
    universe_report = validate_survivorship_universe(
        universe_path=universe_path,
        requested_symbols=plan_symbols,
        start_date=requested_start,
        end_date=requested_end,
    )
    requested_symbols = sorted(set(universe_report.active_symbols) | set(plan_symbols))
    date_range, bar_failures = _validate_bars(bars_root, requested_symbols)
    failures = universe_report.failures + trade_plan_failures + bar_failures
    return BT9RealHistoricalInputPackReport(
        passed=not failures,
        universe_path=universe_path.as_posix(),
        bars_root=bars_root.as_posix(),
        trade_plans_path=trade_plans_path.as_posix(),
        symbols=requested_symbols,
        date_range=date_range,
        failures=failures,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate BT9 real historical backtesting input pack.")
    parser.add_argument("--universe", default="data/universe/survivorship_universe.csv")
    parser.add_argument("--bars-root", default="data/historical/bars/1day")
    parser.add_argument("--trade-plans", default="data/trade_plans/historical_trade_plans.json")
    parser.add_argument("--report-output", default="reports/backtests/bt9-real-historical-input-pack-gate.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = validate_bt9_input_pack(
        universe_path=Path(args.universe),
        bars_root=Path(args.bars_root),
        trade_plans_path=Path(args.trade_plans),
    )
    output = Path(args.report_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    status = "PASS" if report.passed else "FAIL"
    print(f"BT9 real historical input pack gate status: {status}")
    if report.failures:
        print("Failures:")
        for failure in report.failures:
            print(f"- {failure}")
    print(f"Gate report: {args.report_output}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
