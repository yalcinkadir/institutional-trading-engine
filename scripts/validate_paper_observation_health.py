#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.validation.paper_observation_health_gate import (
    validate_paper_observation_health_file,
    write_paper_observation_health_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate paper observation health from latest signals payload.")
    parser.add_argument(
        "--signals-file",
        default="reports/signals/latest-signals.json",
        help="Path to latest signals JSON payload.",
    )
    parser.add_argument(
        "--report-dir",
        default="reports/validation",
        help="Directory for health gate JSON/Markdown reports.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    signals_file = Path(args.signals_file)
    report_dir = Path(args.report_dir)

    report = validate_paper_observation_health_file(signals_file)
    write_paper_observation_health_report(
        report,
        json_path=report_dir / "paper_observation_health.json",
        markdown_path=report_dir / "paper_observation_health.md",
    )

    status = "PASS" if report.passed else "FAIL"
    print(f"Paper observation health gate status: {status}")
    print(f"Signals file: {signals_file}")
    print(f"Market regime: {report.market_regime}")
    print(f"Valid close values: {report.valid_close_count}/{report.total_signals}")
    print(f"Actionable signals: {report.actionable_count}")

    if report.issues:
        print("Issues:")
        for issue in report.issues:
            print(f"- {issue.code}: {issue.message}")

    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
