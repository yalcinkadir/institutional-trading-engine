#!/usr/bin/env python3
"""Generate a visible B1.1 paper observation asset timeline artifact."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.validation.paper_observation_asset_timeline import (  # noqa: E402
    build_asset_timeline_template,
    write_asset_timeline,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a B1.1 paper observation asset timeline.")
    parser.add_argument("--report-date", required=True, help="Observation date YYYY-MM-DD.")
    parser.add_argument("--output-dir", type=Path, default=Path("reports/paper_observation"))
    parser.add_argument("--event-time-utc", default=None, help="Optional fixed UTC timestamp for deterministic runs.")
    parser.add_argument("--exclude-macro-cfd", action="store_true", default=False)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    timeline = build_asset_timeline_template(
        report_date=args.report_date,
        event_time_utc=args.event_time_utc,
        include_macro_cfd=not args.exclude_macro_cfd,
    )
    issues = write_asset_timeline(
        timeline,
        json_path=args.output_dir / "paper_observation_asset_timeline.json",
        markdown_path=args.output_dir / "paper_observation_asset_timeline.md",
    )
    print(f"Paper observation asset timeline status: {'PASS' if not issues else 'FAIL'}")
    print(f"Assets logged: {len(timeline.events)}")
    for issue in issues:
        print(f"ISSUE: {issue}")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
