"""Canonical data path governance policy used by tests.

The repository must preserve auditability without committing raw/private/live data.
This test-support module is the single source of truth for tests that validate
`.gitignore` semantics around `data/`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

DATA_PATH_POLICY_VERSION = "data-path-policy-v1"

PROHIBITED_GLOBAL_DATA_IGNORE_PATTERNS = frozenset(
    {
        "data/",
        "/data/",
    }
)

REQUIRED_IGNORED_DATA_PATTERNS = frozenset(
    {
        "data/raw/",
        "data/live/",
        "data/private/",
        "data/vendor/",
    }
)

TRACKABLE_AUDIT_DATA_PATHS = frozenset(
    {
        "data/.gitkeep",
        "data/decision_log/",
        "data/evidence/",
        "data/contracts/",
    }
)


def normalize_gitignore_lines(content: str) -> set[str]:
    lines: set[str] = set()
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        lines.add(line)
    return lines


def missing_required_ignored_data_patterns(content: str) -> list[str]:
    lines = normalize_gitignore_lines(content)
    return sorted(pattern for pattern in REQUIRED_IGNORED_DATA_PATTERNS if pattern not in lines)


def prohibited_global_data_ignore_patterns(content: str) -> list[str]:
    lines = normalize_gitignore_lines(content)
    return sorted(pattern for pattern in PROHIBITED_GLOBAL_DATA_IGNORE_PATTERNS if pattern in lines)


def is_path_explicitly_ignored(path: str | Path, gitignore_entries: Iterable[str]) -> bool:
    normalized_path = Path(path).as_posix().lstrip("./")
    for entry in gitignore_entries:
        normalized_entry = Path(entry).as_posix().lstrip("./")
        if normalized_entry.endswith("/"):
            if normalized_path == normalized_entry.rstrip("/") or normalized_path.startswith(normalized_entry):
                return True
        elif normalized_path == normalized_entry:
            return True
    return False
