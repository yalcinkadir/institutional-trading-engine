#!/usr/bin/env python3
"""Archive selected validation and operations reports."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.operations.report_archive import DEFAULT_REPORT_PATHS, archive_reports


def _parse_paths(value: str | None) -> list[Path] | None:
    if not value:
        return None
    return [Path(item.strip()) for item in value.split(",") if item.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Archive selected local reports into a timestamped archive directory.")
    parser.add_argument("--archive-root", default="reports/archive")
    parser.add_argument("--archive-id", default=None)
    parser.add_argument(
        "--report-paths",
        default=None,
        help="Optional comma-separated report paths. Defaults to the standard validation/report set.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report_paths = _parse_paths(args.report_paths) or DEFAULT_REPORT_PATHS
    manifest = archive_reports(
        report_paths=report_paths,
        archive_root=Path(args.archive_root),
        archive_id=args.archive_id,
    )

    print("Report archive completed")
    print(f"Archive ID: {manifest.archive_id}")
    print(f"Archive directory: {manifest.archive_dir}")
    print(f"Copied files: {len(manifest.copied_files)}")
    print(f"Missing files: {len(manifest.missing_files)}")
    print(f"Manifest JSON: {manifest.archive_dir}/manifest.json")
    print(f"Manifest Markdown: {manifest.archive_dir}/manifest.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
