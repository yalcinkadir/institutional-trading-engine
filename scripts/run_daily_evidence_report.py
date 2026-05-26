#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.validation.daily_evidence_report import (  # noqa: E402
    DailyEvidenceConfig,
    build_daily_evidence_report,
    load_component_reports,
    write_daily_evidence_report,
)


DEFAULT_COMPONENT_FILES = (
    "paper_observation_reconciliation.json",
    "performance_drift_detection.json",
    "sequential_edge_decay.json",
    "regime_change_detection.json",
    "position_risk_attribution.json",
    "monte_carlo_robustness.json",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a daily Phase B evidence report from component JSON reports.")
    parser.add_argument(
        "--input-dir",
        type=Path,
        required=True,
        help="Directory containing Phase B component JSON reports.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory where daily evidence JSON and Markdown reports will be written.",
    )
    parser.add_argument(
        "--report-date",
        required=True,
        help="Report date in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--allow-missing-risk-attribution",
        action="store_true",
        help="Allow risk-attribution component to be skipped for days with no open paper positions.",
    )
    parser.add_argument(
        "--allow-missing-monte-carlo",
        action="store_true",
        help="Allow Monte Carlo component to be skipped for days with insufficient observation history.",
    )
    parser.add_argument(
        "--max-failed-components",
        type=int,
        default=0,
        help="Maximum number of failed present components allowed before the daily report fails.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_dir: Path = args.input_dir
    output_dir: Path = args.output_dir

    component_paths = [input_dir / file_name for file_name in DEFAULT_COMPONENT_FILES if (input_dir / file_name).exists()]
    component_reports = load_component_reports(component_paths)
    config = DailyEvidenceConfig(
        require_risk_attribution=not args.allow_missing_risk_attribution,
        require_monte_carlo=not args.allow_missing_monte_carlo,
        max_failed_components=args.max_failed_components,
    )
    report = build_daily_evidence_report(component_reports, report_date=args.report_date, config=config)

    json_path = output_dir / f"daily_evidence_report_{args.report_date}.json"
    markdown_path = output_dir / f"daily_evidence_report_{args.report_date}.md"
    write_daily_evidence_report(report, json_path=json_path, markdown_path=markdown_path)

    print(f"Daily evidence report written: {json_path}")
    print(f"Daily evidence report written: {markdown_path}")
    print(f"Daily evidence status: {report.metrics.overall_status}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
