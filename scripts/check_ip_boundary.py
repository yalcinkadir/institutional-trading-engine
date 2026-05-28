#!/usr/bin/env python3
"""Run IP1 public/private edge boundary scan."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.validation.ip_boundary import (
    load_ip_boundary_policy,
    scan_ip_boundary,
    write_ip_boundary_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check public/private edge boundary")
    parser.add_argument("--root", default=".", help="Repository root to scan")
    parser.add_argument("--policy", default=".ip-boundary.yml", help="Policy file path")
    parser.add_argument("--json-output", default="reports/ip-boundary-report.json")
    parser.add_argument("--markdown-output", default="reports/ip-boundary-report.md")
    parser.add_argument("--no-write", action="store_true", help="Do not write report files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root)
    policy_path = Path(args.policy)
    if not policy_path.is_absolute():
        policy_path = root / policy_path

    policy = load_ip_boundary_policy(policy_path)
    report = scan_ip_boundary(root, policy=policy)

    if not args.no_write:
        write_ip_boundary_report(
            report,
            json_path=Path(args.json_output),
            markdown_path=Path(args.markdown_output),
        )

    print(f"IP boundary status: {report.status.value}")
    print(f"Scanned files: {report.scanned_file_count}")
    print(f"Findings: {report.finding_count}")
    for finding in report.findings:
        print(
            f"{finding.severity.value.upper()} {finding.code} "
            f"{finding.path}:{finding.line} {finding.match}"
        )

    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
