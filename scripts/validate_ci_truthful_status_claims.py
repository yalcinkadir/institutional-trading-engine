#!/usr/bin/env python3
"""Validate audit-safe CI status claims in project documentation.

The guard is intentionally narrow: feature-level labels such as
`Done / CI-green` are allowed as scoped historical feature status, while
repository-wide claims such as `CI is green`, `full regression green`,
`main is green` or `all workflows green` require nearby evidence.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DOCS = ("README.md", "ROADMAP.md", "CHANGELOG.md")

DANGEROUS_CLAIM_RE = re.compile(
    r"(" 
    r"\bCI\s+is\s+green\b|"
    r"\bfull\s+regression(?:\s+suite)?\s+(?:is\s+)?green\b|"
    r"\bmain(?:\s+branch)?\s+(?:is\s+)?green\b|"
    r"\ball\s+workflows\s+(?:are\s+)?green\b|"
    r"\breport\s+pipeline\s+(?:is\s+)?green\b|"
    r"\bproduction\s+(?:is\s+)?green\b"
    r")",
    re.IGNORECASE,
)

EVIDENCE_RE = re.compile(
    r"(" 
    r"https://github\.com/[^\s)]+/(?:actions/runs/\d+(?:/job/\d+)?|commit/[0-9a-fA-F]{7,40})|"
    r"\b[a-f0-9]{7,40}\b|"
    r"\bevidence artifact\b|"
    r"\bartifact:\s*\S+|"
    r"\bCI green on main:\s*\S+"
    r")",
    re.IGNORECASE,
)

SCOPED_FEATURE_LABEL_RE = re.compile(
    r"\b(?:Done|Implemented|Closed)\s*/\s*CI-green\b|\bimplemented\s+and\s+CI-green\b",
    re.IGNORECASE,
)


def _nearby_lines(lines: list[str], index: int, radius: int = 2) -> str:
    start = max(0, index - radius)
    end = min(len(lines), index + radius + 1)
    return "\n".join(lines[start:end])


def validate_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    errors: list[str] = []

    for i, line in enumerate(lines):
        if not DANGEROUS_CLAIM_RE.search(line):
            continue
        nearby = _nearby_lines(lines, i)
        if EVIDENCE_RE.search(nearby):
            continue
        errors.append(
            f"{path.relative_to(REPO_ROOT)}:{i + 1}: unsupported repository-wide CI-green claim: {line.strip()}"
        )

    return errors


def validate_policy_present(root: Path) -> list[str]:
    policy = root / "docs" / "operations" / "ci_truthful_status_claims_policy.md"
    if not policy.is_file():
        return ["missing docs/operations/ci_truthful_status_claims_policy.md"]
    text = policy.read_text(encoding="utf-8")
    required = [
        "Single-test success is not full-regression success",
        "CI green on main:",
        "Feature-level historical labels",
    ]
    return [f"policy missing required phrase: {phrase}" for phrase in required if phrase not in text]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        default=list(DEFAULT_DOCS),
        help="Documentation paths to validate. Defaults to README.md ROADMAP.md CHANGELOG.md.",
    )
    args = parser.parse_args(argv)

    errors: list[str] = []
    errors.extend(validate_policy_present(REPO_ROOT))

    for raw in args.paths:
        path = (REPO_ROOT / raw).resolve()
        if not path.is_file():
            errors.append(f"missing documentation file: {raw}")
            continue
        errors.extend(validate_file(path))

    if errors:
        print("CI-truthful status claim validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("CI-truthful status claim validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
