#!/usr/bin/env python3
"""Create token-efficient Markdown exports for Claude project analysis.

The exporter is intentionally dependency-free and conservative:
- it excludes secrets, private edge modules, generated reports, caches and binaries
- it writes grouped Markdown files for lite, focused and full analysis modes
- it creates a ZIP artifact that can be downloaded from GitHub Actions

This tool is for code review / project analysis only. It does not change runtime
trading behavior and does not authorize broker execution.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
EXPORT_ROOT = ROOT / "exports" / "claude"
ZIP_PATH = ROOT / "exports" / "claude_project_import.zip"
DEFAULT_MAX_FILE_BYTES = 1_000_000

EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "htmlcov",
    "exports",
    "secrets",
    "private",
    "private_config",
    "local_config",
    "private_edge",
    "external_edge",
    "data",
    "evidence",
    "lockbox",
    "artifacts",
    "outputs",
    "generated",
    "logs",
}

EXCLUDE_FILE_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
    "secrets.json",
}

EXCLUDE_SUFFIXES = {
    ".pem",
    ".key",
    ".crt",
    ".p12",
    ".pfx",
    ".db",
    ".sqlite",
    ".sqlite3",
    ".duckdb",
    ".parquet",
    ".feather",
    ".xlsx",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".pdf",
    ".zip",
    ".gz",
    ".tar",
}

INCLUDE_SUFFIXES = {
    ".py",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".csv",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".sql",
    ".lock",
}

INCLUDE_FILE_NAMES = {
    "Dockerfile",
    "Makefile",
    "README",
    "README.md",
    "CHANGELOG.md",
    "ROADMAP.md",
    "DISCLAIMER.md",
    "LICENSE",
    "requirements.txt",
    "requirements.lock",
    "pyproject.toml",
}

AREA_PATTERNS: dict[str, list[str]] = {
    "entry_exit_watcher": [
        "src/watcher",
        "src/entry",
        "src/exit",
        "src/trade",
        "src/signals",
        "tests/test_watcher",
        "tests/test_entry",
        "tests/test_exit",
        "tests/test_trade",
    ],
    "risk_governance": [
        "src/governance",
        "src/risk",
        "src/validation",
        "tests/test_governance",
        "tests/test_risk",
        "tests/test_validation",
    ],
    "decision_engine": [
        "src/decision",
        "src/decision_engine",
        "src/scoring",
        "src/orchestrator",
        "tests/test_decision",
        "tests/test_scoring",
        "tests/test_orchestrator",
    ],
    "tests_ci": [
        "tests",
        ".github/workflows",
        "requirements",
        "pyproject.toml",
    ],
    "runtime_evidence": [
        "src/operations",
        "scripts/generate_runtime_evidence_manifest.py",
        "tests/test_psr1_runtime_evidence_manifest.py",
        "docs/operations",
    ],
}

LITE_PATTERNS = [
    "README.md",
    "ROADMAP.md",
    "CHANGELOG.md",
    "DISCLAIMER.md",
    "LICENSE",
    "pyproject.toml",
    "requirements.txt",
    "requirements.lock",
    ".github/pull_request_template.md",
]


@dataclass(frozen=True)
class ExportFile:
    path: Path
    rel: str
    size_bytes: int
    sha256: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export safe Markdown context for Claude analysis.")
    parser.add_argument(
        "--mode",
        choices=["lite", "focus", "full", "all"],
        default="all",
        help="Export scope. Default: all.",
    )
    parser.add_argument(
        "--area",
        choices=[*AREA_PATTERNS.keys(), "all"],
        default="all",
        help="Focused export area used when --mode focus or --mode all. Default: all.",
    )
    parser.add_argument(
        "--max-file-bytes",
        type=int,
        default=DEFAULT_MAX_FILE_BYTES,
        help="Skip individual files larger than this value. Default: 1000000.",
    )
    return parser.parse_args()


def safe_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def has_excluded_part(path: Path) -> bool:
    return bool(set(path.relative_to(ROOT).parts) & EXCLUDE_DIRS)


def looks_private_or_generated(path: Path) -> bool:
    rel = safe_relative(path)
    name = path.name
    lower_name = name.lower()

    if name in EXCLUDE_FILE_NAMES:
        return True

    if path.suffix.lower() in EXCLUDE_SUFFIXES:
        return True

    private_markers = (
        ".env.",
        ".local.",
        "secret",
        "credential",
        "private",
        "live",
        "raw",
        "generated",
    )
    return any(marker in rel.lower() or marker in lower_name for marker in private_markers)


def should_include(path: Path, max_file_bytes: int) -> bool:
    if not path.is_file():
        return False
    if has_excluded_part(path):
        return False
    if looks_private_or_generated(path):
        return False
    if path.stat().st_size > max_file_bytes:
        return False
    if path.name in INCLUDE_FILE_NAMES:
        return True
    return path.suffix.lower() in INCLUDE_SUFFIXES


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_files(max_file_bytes: int) -> list[ExportFile]:
    files: list[ExportFile] = []
    for path in sorted(ROOT.rglob("*")):
        if should_include(path, max_file_bytes=max_file_bytes):
            files.append(
                ExportFile(
                    path=path,
                    rel=safe_relative(path),
                    size_bytes=path.stat().st_size,
                    sha256=sha256_file(path),
                )
            )
    return files


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1", errors="ignore")


def language_for(path: Path) -> str:
    suffix = path.suffix.lower().lstrip(".")
    if path.name == "Dockerfile":
        return "dockerfile"
    if path.name == "Makefile":
        return "makefile"
    return suffix or "text"


def file_block(item: ExportFile) -> str:
    content = read_text(item.path).rstrip()
    return f"""

---

## File: `{item.rel}`

Metadata:

```text
size_bytes={item.size_bytes}
sha256={item.sha256}
```

````{language_for(item.path)}
{content}
````
"""


def rel_matches(rel: str, patterns: Iterable[str]) -> bool:
    return any(rel == pattern or rel.startswith(pattern.rstrip("/") + "/") or rel.startswith(pattern) for pattern in patterns)


def select_by_patterns(files: list[ExportFile], patterns: Iterable[str]) -> list[ExportFile]:
    return [item for item in files if rel_matches(item.rel, patterns)]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def build_file_tree(files: list[ExportFile]) -> str:
    lines = ["# Project File Tree", "", "Only safe exported files are listed here.", ""]
    for item in files:
        lines.append(f"- `{item.rel}` ({item.size_bytes} bytes)")
    return "\n".join(lines)


def build_overview(files: list[ExportFile]) -> str:
    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return f"""# Claude Project Export Overview

Generated at: {generated_at}
Repository root: `{ROOT.name}`
Exported safe files: {len(files)}

## Purpose

This export is prepared for Claude project-level analysis with reduced token waste.

Claude should focus on:

1. architecture quality
2. deterministic decision logic
3. risk and governance controls
4. entry/exit and watcher edge cases
5. test coverage and missing tests
6. CI/CD reliability
7. auditability
8. production readiness
9. roadmap gaps

## Hard Analysis Rules

- Do not evaluate or assume trading profitability.
- Do not claim live-trading readiness.
- Treat this as a research and decision-support codebase.
- Focus on software quality, safety, correctness, determinism, auditability and maintainability.
- Check whether safeguards fail closed.
- Check whether public repository hygiene protects private edge configuration.

## Export Modes

- `lite`: overview, roadmap, README, dependency and governance context.
- `focus`: grouped technical areas such as entry/exit watcher, risk governance, decision engine, tests/CI and runtime evidence.
- `full`: all safe included source/documentation files.
"""


def write_lite_export(files: list[ExportFile]) -> None:
    lite_dir = EXPORT_ROOT / "lite"
    selected = select_by_patterns(files, LITE_PATTERNS)
    write(lite_dir / "00_OVERVIEW.md", build_overview(files))
    write(lite_dir / "01_FILE_TREE.md", build_file_tree(files))

    content = "# Lite Project Context\n\nCore public-safe project documents for quick Claude analysis.\n"
    for item in selected:
        content += file_block(item)
    write(lite_dir / "02_KEY_DOCS.md", content)


def write_focus_export(files: list[ExportFile], area: str) -> None:
    focus_dir = EXPORT_ROOT / "focus"
    areas = AREA_PATTERNS if area == "all" else {area: AREA_PATTERNS[area]}

    for area_name, patterns in areas.items():
        selected = select_by_patterns(files, patterns)
        content = f"# Focus Export: {area_name}\n\n"
        content += "Use this file for targeted technical review instead of uploading the full project context.\n"
        content += "\n## Included Files\n\n"
        if selected:
            for item in selected:
                content += f"- `{item.rel}`\n"
            for item in selected:
                content += file_block(item)
        else:
            content += "No matching safe files found.\n"
        write(focus_dir / f"{area_name}.md", content)


def write_full_export(files: list[ExportFile]) -> None:
    full_dir = EXPORT_ROOT / "full"
    content = "# Full Safe Code Context\n\n"
    content += "This file contains all safe included files. Prefer lite/focus exports first to reduce token usage.\n"
    for item in files:
        content += file_block(item)
    write(full_dir / "00_FULL_CODE_CONTEXT.md", content)


def create_zip() -> None:
    ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(EXPORT_ROOT.rglob("*.md")):
            archive.write(path, path.relative_to(EXPORT_ROOT.parent))


def main() -> int:
    args = parse_args()
    files = collect_files(max_file_bytes=args.max_file_bytes)

    if args.mode in {"lite", "all"}:
        write_lite_export(files)
    if args.mode in {"focus", "all"}:
        write_focus_export(files, area=args.area)
    if args.mode in {"full", "all"}:
        write_full_export(files)

    create_zip()

    print(f"Claude Markdown export created: {EXPORT_ROOT}")
    print(f"Claude ZIP export created: {ZIP_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
