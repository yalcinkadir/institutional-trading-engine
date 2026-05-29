#!/usr/bin/env python3
"""Validate IP2 public repository hygiene policy."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.validation.public_repo_policy import (  # noqa: E402
    validate_public_repo_policy,
    write_public_repo_policy_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate public repository hygiene policy")
    parser.add_argument(
        "--policy-file",
        default="docs/operations/public_repo_hygiene_policy.md",
        help="Policy document to validate",
    )
    parser.add_argument("--json-output", default="reports/public-repo-policy-report.json")
    parser.add_argument("--markdown-output", default="reports/public-repo-policy-report.md")
    parser.add_argument("--no-write", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = validate_public_repo_policy(Path(args.policy_file))

    if not args.no_write:
        write_public_repo_policy_report(
            report,
            json_path=Path(args.json_output),
            markdown_path=Path(args.markdown_output),
        )

    print(f"Public repo policy status: {report.status.value}")
    print(f"Findings: {report.finding_count}")
    for finding in report.findings:
        print(f"{finding.severity.value.upper()} {finding.code}: {finding.detail or finding.message}")

    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
