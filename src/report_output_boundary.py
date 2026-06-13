"""Fail-closed guardrails for generated report output paths."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

PUBLIC_REPORT_OUTPUT_BOUNDARY_VERSION = "report-output-boundary-v2"

PROTECTED_PUBLIC_REPORTS = frozenset(
    {
        "reports/premarket-report.md",
        "reports/postmarket-report.md",
        "reports/weekly-report.md",
    }
)

ALLOWED_GENERATED_REPORT_ROOTS = frozenset(
    {
        "reports/generated",
        "reports/premarket",
        "reports/intraday",
        "reports/postmarket",
        "reports/weekly",
        "reports/signals",
        "reports/validation",
        "reports/datafeed_liveness",
    }
)


class ReportOutputBoundaryError(ValueError):
    """Raised when a generated report targets a protected or invalid artifact path."""


def normalize_report_output_path(path: str | Path, *, repo_root: str | Path | None = None) -> str:
    candidate = Path(path).expanduser()
    base = Path(repo_root).expanduser().resolve() if repo_root is not None else Path.cwd().resolve()
    if not candidate.is_absolute():
        candidate = base / candidate
    try:
        return candidate.resolve().relative_to(base).as_posix()
    except ValueError:
        return candidate.resolve().as_posix()


def _normalized_roots(roots: Iterable[str]) -> set[str]:
    return {Path(item).as_posix().strip("/").lstrip("./") for item in roots}


def is_protected_public_report_path(
    path: str | Path,
    *,
    repo_root: str | Path | None = None,
    protected_paths: Iterable[str] = PROTECTED_PUBLIC_REPORTS,
) -> bool:
    normalized = normalize_report_output_path(path, repo_root=repo_root)
    protected = {Path(item).as_posix().lstrip("./") for item in protected_paths}
    return normalized in protected


def is_generated_report_output_path(
    path: str | Path,
    *,
    repo_root: str | Path | None = None,
    allowed_roots: Iterable[str] = ALLOWED_GENERATED_REPORT_ROOTS,
) -> bool:
    normalized = normalize_report_output_path(path, repo_root=repo_root).strip("/").lstrip("./")
    for root in _normalized_roots(allowed_roots):
        if normalized == root or normalized.startswith(f"{root}/"):
            return True
    return False


def assert_report_output_path_allowed(
    path: str | Path,
    *,
    repo_root: str | Path | None = None,
    protected_paths: Iterable[str] = PROTECTED_PUBLIC_REPORTS,
    allowed_roots: Iterable[str] = ALLOWED_GENERATED_REPORT_ROOTS,
) -> None:
    normalized = normalize_report_output_path(path, repo_root=repo_root)
    protected = {Path(item).as_posix().lstrip("./") for item in protected_paths}
    allowed = sorted(_normalized_roots(allowed_roots))

    if normalized in protected:
        raise ReportOutputBoundaryError(
            f"Refusing generated report write to protected public artifact: {normalized}. "
            f"Allowed generated report roots: {allowed}. "
            f"Boundary={PUBLIC_REPORT_OUTPUT_BOUNDARY_VERSION}."
        )

    if not is_generated_report_output_path(path, repo_root=repo_root, allowed_roots=allowed_roots):
        raise ReportOutputBoundaryError(
            f"Refusing generated report write outside generated-report roots: {normalized}. "
            f"Allowed generated report roots: {allowed}. "
            f"Boundary={PUBLIC_REPORT_OUTPUT_BOUNDARY_VERSION}."
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
