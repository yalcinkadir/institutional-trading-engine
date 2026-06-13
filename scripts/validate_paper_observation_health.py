#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
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
    parser.add_argument(
        "--scheduled-liveness-file",
        default=None,
        help="Optional scheduled-report liveness JSON to couple into the readiness decision.",
    )
    parser.add_argument(
        "--watcher-lifecycle-file",
        default=None,
        help="Optional watcher lifecycle JSON to couple into the readiness decision.",
    )
    parser.add_argument(
        "--run-timestamp",
        default=os.environ.get("GITHUB_RUN_ATTEMPT_TIMESTAMP") or os.environ.get("RUN_TIMESTAMP"),
        help="UTC timestamp identifying this observation run.",
    )
    parser.add_argument(
        "--workflow-name",
        default=os.environ.get("GITHUB_WORKFLOW"),
        help="GitHub Actions workflow name for this observation run.",
    )
    parser.add_argument(
        "--commit-sha",
        default=os.environ.get("GITHUB_SHA"),
        help="Commit SHA that produced this observation run.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    signals_file = Path(args.signals_file)
    report_dir = Path(args.report_dir)
    scheduled_liveness_file = Path(args.scheduled_liveness_file) if args.scheduled_liveness_file else None
    watcher_lifecycle_file = Path(args.watcher_lifecycle_file) if args.watcher_lifecycle_file else None

    report = validate_paper_observation_health_file(
        signals_file,
        run_timestamp=args.run_timestamp,
        workflow_name=args.workflow_name,
        commit_sha=args.commit_sha,
        scheduled_liveness_file=scheduled_liveness_file,
        watcher_lifecycle_file=watcher_lifecycle_file,
    )

    write_paper_observation_health_report(
        report,
        json_path=report_dir / "paper_observation_health.json",
        markdown_path=report_dir / "paper_observation_health.md",
        latest_json_path=report_dir / "latest-paper-observation-health.json",
    )

    status = "PASS" if report.passed else "FAIL"
    print(f"Paper observation health gate status: {status}")
    print(f"Observation health status: {report.observation_health_status}")
    print(f"Run timestamp: {report.run_timestamp}")
    print(f"Workflow name: {report.workflow_name}")
    print(f"Commit SHA: {report.commit_sha}")
    print(f"Signals file: {signals_file}")
    print(f"Market regime: {report.market_regime}")
    print(f"Data quality status: {report.data_quality_status}")
    print(f"Valid close values: {report.valid_close_count}/{report.total_signals}")
    print(f"Actionable signals: {report.actionable_count}")

    if scheduled_liveness_file is not None:
        print(f"Scheduled liveness file: {scheduled_liveness_file}")
    if watcher_lifecycle_file is not None:
        print(f"Watcher lifecycle file: {watcher_lifecycle_file}")

    if report.degradation_reasons:
        print("Degradation reasons:")
        for reason in report.degradation_reasons:
            print(f"- {reason}")

    if report.issues:
        print("Issues:")
        for issue in report.issues:
            print(f"- {issue.code}: {issue.message}")

    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())