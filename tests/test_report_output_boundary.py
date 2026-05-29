from __future__ import annotations

from pathlib import Path

import pytest

from src.report_output_boundary import (
    PROTECTED_PUBLIC_REPORTS,
    PUBLIC_REPORT_OUTPUT_BOUNDARY_VERSION,
    ReportOutputBoundaryError,
    assert_report_output_path_allowed,
    is_protected_public_report_path,
    normalize_report_output_path,
    write_report_text_guarded,
)


@pytest.mark.parametrize("protected_path", sorted(PROTECTED_PUBLIC_REPORTS))
def test_protected_public_report_paths_are_blocked(protected_path: str) -> None:
    with pytest.raises(ReportOutputBoundaryError) as exc_info:
        assert_report_output_path_allowed(protected_path)

    message = str(exc_info.value)
    assert protected_path in message
    assert PUBLIC_REPORT_OUTPUT_BOUNDARY_VERSION in message


@pytest.mark.parametrize(
    "allowed_path",
    [
        "reports/generated/premarket-report.md",
        "reports/live/premarket-report-live.md",
        "reports/private/postmarket-report-private.md",
        "outputs/weekly-report.md",
        "tmp/premarket-report.md",
    ],
)
def test_non_committed_generated_report_paths_are_allowed(allowed_path: str) -> None:
    assert_report_output_path_allowed(allowed_path)
    assert is_protected_public_report_path(allowed_path) is False


def test_absolute_path_inside_repo_is_normalized_for_boundary_check(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    protected = repo_root / "reports" / "weekly-report.md"

    assert normalize_report_output_path(protected, repo_root=repo_root) == "reports/weekly-report.md"
    assert is_protected_public_report_path(protected, repo_root=repo_root) is True
    with pytest.raises(ReportOutputBoundaryError):
        assert_report_output_path_allowed(protected, repo_root=repo_root)


def test_relative_parent_segments_cannot_bypass_boundary(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    candidate = "reports/generated/../premarket-report.md"

    assert normalize_report_output_path(candidate, repo_root=repo_root) == "reports/premarket-report.md"
    with pytest.raises(ReportOutputBoundaryError):
        assert_report_output_path_allowed(candidate, repo_root=repo_root)


def test_guarded_writer_refuses_protected_public_artifact(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    protected = repo_root / "reports" / "premarket-report.md"
    protected.parent.mkdir(parents=True)
    protected.write_text("original synthetic example", encoding="utf-8")

    with pytest.raises(ReportOutputBoundaryError):
        write_report_text_guarded(protected, "generated content", repo_root=repo_root)

    assert protected.read_text(encoding="utf-8") == "original synthetic example"


def test_guarded_writer_allows_generated_output(tmp_path: Path) -> None:
    output = tmp_path / "repo" / "reports" / "generated" / "premarket-report.md"

    written = write_report_text_guarded(output, "generated content", repo_root=tmp_path / "repo")

    assert written == output
    assert output.read_text(encoding="utf-8") == "generated content"
