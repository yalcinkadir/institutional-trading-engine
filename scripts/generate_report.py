#!/usr/bin/env python3
"""Generate Institutional Trading Engine reports.

Usage:
    python scripts/generate_report.py --type premarket --output reports/premarket-report.md
    python scripts/generate_report.py --type postmarket --output reports/postmarket-report.md
    python scripts/generate_report.py --type weekly --output reports/weekly-report.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.reporting.decision_report import build_decision_report
from src.reporting.market_regime import build_market_regime_summary
from src.reporting.report_formatter import format_report
from src.reporting.screener_engine import build_screener_snapshot
from src.reporting.weekly_summary import build_weekly_summary

VALID_REPORT_TYPES = {"premarket", "postmarket", "weekly"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a market report.")
    parser.add_argument(
        "--type",
        required=True,
        choices=sorted(VALID_REPORT_TYPES),
        help="Report type to generate.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional output markdown path. If omitted, the report is printed to stdout.",
    )
    return parser.parse_args()


def build_report(report_type: str) -> str:
    if report_type == "weekly":
        payload = {
            "report_type": report_type,
            "weekly_summary": build_weekly_summary(),
        }
    else:
        market_regime = build_market_regime_summary(report_type)
        screener = build_screener_snapshot(report_type)

        payload = {
            "report_type": report_type,
            "market_regime": market_regime,
            "screener": screener,
            "decision_report": build_decision_report(
                market_regime=market_regime,
                screener=screener,
            ),
        }

    return format_report(payload)


def main() -> int:
    args = parse_args()
    report = build_report(args.type)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        print(f"Report written to {output_path}")
    else:
        print(report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
