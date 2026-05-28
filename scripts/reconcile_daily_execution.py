#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.validation.daily_execution_reconciliation import (  # noqa: E402
    DailyExecutionReconciliationConfig,
    load_expected_execution_records,
    load_observed_execution_records,
    reconcile_daily_execution,
    write_daily_execution_reconciliation_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reconcile expected/backtest executions against observed paper/live executions.")
    parser.add_argument("--expected-file", type=Path, required=True, help="JSON list or object with records[] expected executions.")
    parser.add_argument("--observed-file", type=Path, required=True, help="JSON list or object with records[] observed executions.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for JSON/Markdown reconciliation output.")
    parser.add_argument("--max-abs-quantity-drift", type=float, default=0.000001)
    parser.add_argument("--max-abs-price-drift-pct", type=float, default=0.01)
    parser.add_argument("--max-abs-r-drift", type=float, default=0.25)
    parser.add_argument("--max-abs-total-r-drift", type=float, default=0.5)
    parser.add_argument("--allow-missing-observed", action="store_true")
    parser.add_argument("--allow-unexpected-observed", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = DailyExecutionReconciliationConfig(
        max_abs_quantity_drift=args.max_abs_quantity_drift,
        max_abs_price_drift_pct=args.max_abs_price_drift_pct,
        max_abs_r_drift=args.max_abs_r_drift,
        max_abs_total_r_drift=args.max_abs_total_r_drift,
        require_observed_for_each_expected=not args.allow_missing_observed,
        fail_on_unexpected_observed=not args.allow_unexpected_observed,
    )
    report = reconcile_daily_execution(
        expected_records=load_expected_execution_records(args.expected_file),
        observed_records=load_observed_execution_records(args.observed_file),
        config=config,
    )
    write_daily_execution_reconciliation_report(
        report,
        json_path=args.output_dir / "daily_execution_reconciliation.json",
        markdown_path=args.output_dir / "daily_execution_reconciliation.md",
    )
    print(f"Daily execution reconciliation status: {report.status.value}")
    print(f"Matched records: {report.metrics.matched_count}")
    print(f"Missing observed records: {report.metrics.missing_count}")
    print(f"Unexpected observed records: {report.metrics.unexpected_count}")
    print(f"Total R drift: {report.metrics.total_r_drift:.4f}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
