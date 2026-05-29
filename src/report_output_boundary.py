"""Fail-closed guardrails for generated report output paths."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

PUBLIC_REPORT_OUTPUT_BOUNDARY_VERSION = "report-output-boundary-v1"

PROTECTED_PUBLIC_REPORTS = frozenset(
    {
        "reports/premarket-report.md",
        "reports/postmarket-report.md",
        "reports/weekly-report.md",
    }
)


class ReportOutputBoundaryError(ValueError):
    """Raised when a generated report targets a protected public artifact."""


def normalize_report_output_path(path: str | Path, *, repo_root: str | Path | None = None) -> str:
    candidate = Path(path).expanduser()
    base = Path(repo_root).expanduser().resolve() if repo_root is not None else Path.cwd().resolve()
    if candidate.is_absolute():
        try:
            candidate = candidate.resolve().relative_to(base)
        except ValueError:
            return candidate.resolve().as_posix()
    else:
        candidate = Path(candidate.as_posix())
    return candidate.as_posix().lstrip("./")


def is_protected_public_report_path(
    path: str | Path,
    *,
    repo_root: str | Path | None = None,
    protected_paths: Iterable[str] = PROTECTED_PUBLIC_REPORTS,
) -> bool:
    normalized = normalize_report_output_path(path, repo_root=repo_root)
    protected = {Path(item).as_posix().lstrip("./") for item in protected_paths}
    return normalized in protected


def assert_report_output_path_allowed(
    path: str | Path,
    *,
    repo_root: str | Path | None = None,
    protected_paths: Iterable[str] = PROTECTED_PUBLIC_REPORTS,
) -> None:
    normalized = normalize_report_output_path(path, repo_root=repo_root)
    protected = {Path(item).as_posix().lstrip("./") for item in protected_paths}
    if normalized in protected:
        raise ReportOutputBoundaryError(
            f"Refusing generated report write to protected public artifact: {normalized}. "
            f"Use a non-committed output directory instead. Boundary={PUBLIC_REPORT_OUTPUT_BOUNDARY_VERSION}."
        )


def write_report_text_guarded(
    path: str | Path,
    content: str,
    *,
    repo_root: str | Path | None = None,
    encoding: str = "utf-8",
) -> Path:
    output_path = Path(path)
    assert_report_output_path_allowed(output_path, repo_root=repo_root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding=encoding)
    return output_path
