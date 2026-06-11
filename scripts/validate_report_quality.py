#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.reporting.report_quality import RISK_TIER_DECISION_LINE_RE, validate_report_quality


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate generated report quality.")
    parser.add_argument("--type", required=True, choices=["premarket", "postmarket", "weekly"])
    parser.add_argument("--file", required=True, help="Path to report markdown file")
    parser.add_argument("--min-score", type=int, default=75)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report_path = Path(args.file)

    print(f"Validation file: {report_path}")
    print("Risk Tier field check: markdown decision row `- Decision: **<decision>** | Risk Tier: <tier>`")
    print(f"Risk Tier pattern: {RISK_TIER_DECISION_LINE_RE.pattern}")

    if not report_path.exists():
        print(f"ERROR: Report file does not exist: {report_path}", file=sys.stderr)
        return 1

    report = report_path.read_text(encoding="utf-8")
    result = validate_report_quality(report, args.type)

    print(f"Report type: {result.report_type}")
    print(f"Quality score: {result.score}")
    print(f"Passed: {result.passed}")
    if result.risk_tier_evidence:
        print(f"Risk Tier validation status: {result.risk_tier_evidence.get('status')}")
        print(f"Risk Tier rows found: {result.risk_tier_evidence.get('decision_risk_tier_row_count')}")
        print(f"Explicit no-active-risk state: {result.risk_tier_evidence.get('explicit_no_active_risk')}")

    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"- {warning}")

    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"- {error}")

    if not result.passed or result.score < args.min_score:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
