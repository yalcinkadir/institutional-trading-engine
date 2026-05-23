#!/usr/bin/env python3
"""Build the static dashboard."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.operations.static_dashboard import build_dashboard_payload, build_static_dashboard  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build static HTML dashboard")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--output-html", default="reports/dashboard/index.html")
    parser.add_argument("--output-json", default="reports/dashboard/dashboard.json")
    parser.add_argument("--json", action="store_true", help="Print dashboard summary JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = build_static_dashboard(
        root=Path(args.root),
        output_html=Path(args.output_html),
        output_json=Path(args.output_json),
    )
    payload = build_dashboard_payload(result)

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"Static dashboard status: {result.status}")
        print(f"HTML: {result.output_html}")
        print(f"JSON: {result.output_json}")
        if result.warnings:
            print("Warnings:")
            for warning in result.warnings:
                print(f"- {warning}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
