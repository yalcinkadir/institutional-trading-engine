#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.operations.scheduled_report_liveness import (  # noqa: E402
    build_scheduled_report_liveness_artifact,
    write_scheduled_report_liveness_artifact,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate scheduled report liveness evidence for #192.")
    parser.add_argument("--report-type", required=True, help="Report type: premarket, intraday, postmarket or weekly.")
    parser.add_argument("--report-file", required=True, help="Expected dated report file produced by the scheduled run.")
    parser.add_argument("--latest-file", required=True, help="Expected latest report file copied by the scheduled run.")
    parser.add_argument("--signals-file", default="reports/signals/latest-signals.json", help="Latest signals JSON required for market reports.")
    parser.add_argument(
        "--paper-health-file",
        default="reports/validation/latest-paper-observation-health.json",
        help="Latest paper observation health JSON required for market reports.",
    )
    parser.add_argument("--report-root", default=".", help="Repository/report root used for family freshness scanning.")
    parser.add_argument("--report-dir", default="reports/scheduled_report_liveness", help="Reserved for workflow clarity; output path remains canonical.")
    parser.add_argument("--run-timestamp", default=os.environ.get("HEALTH_RUN_TIMESTAMP") or os.environ.get("RUN_TIMESTAMP"))
    parser.add_argument("--workflow-name", default=os.environ.get("GITHUB_WORKFLOW"))
    parser.add_argument("--commit-sha", default=os.environ.get("GITHUB_SHA"))
    parser.add_argument("--run-date", default=os.environ.get("RUN_DATE"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = build_scheduled_report_liveness_artifact(
        report_type=args.report_type,
        report_file=args.report_file,
        latest_file=args.latest_file,
        signals_file=args.signals_file,
        paper_health_file=args.paper_health_file,
        run_timestamp=args.run_timestamp,
        workflow_name=args.workflow_name,
        commit_sha=args.commit_sha,
        run_date=args.run_date,
        report_root=args.report_root,
    )
    write_scheduled_report_liveness_artifact(result=result)

    print(f"Scheduled report liveness status: {result.artifact['scheduled_report_status']}")
    print(f"Report liveness status: {result.artifact['report_liveness_status']}")
    print(f"Current run state: {result.artifact['current_run_state']}")
    print(f"Report type: {result.artifact['report_type']}")
    print(f"Artifact: {result.artifact_path}")
    print(f"Latest artifact: {result.latest_artifact_path}")
    if result.errors:
        print("Errors:")
        for error in result.errors:
            print(f"- {error}")
    return 0 if result.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
