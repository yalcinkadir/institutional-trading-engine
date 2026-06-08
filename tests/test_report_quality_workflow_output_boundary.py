"""P0-A regression: report-quality workflow output paths must satisfy the guard.

This couples `.github/workflows/report-quality.yml` to
`src/report_output_boundary.py` so the two can never silently diverge again.

Root cause it guards against: the workflow wrote generated reports to
`reports/<type>-report.md`, which is a PROTECTED_PUBLIC_REPORTS path, so
`assert_report_output_path_allowed` rejected every run (deterministic CI red).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from src.report_output_boundary import (
    ReportOutputBoundaryError,
    assert_report_output_path_allowed,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "report-quality.yml"

_OUTPUT_RE = re.compile(r'--output\s+"([^"]+)"')


def _matrix_report_types() -> list[str]:
    data = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    matrix = data["jobs"]["validate-reports"]["strategy"]["matrix"]
    types = matrix["report_type"]
    assert types, "report_type matrix must not be empty"
    return [str(t) for t in types]


def _output_path_template() -> str:
    text = WORKFLOW.read_text(encoding="utf-8")
    matches = _OUTPUT_RE.findall(text)
    assert matches, "no --output argument found in report-quality.yml"
    # All generate invocations must target the same template.
    assert len(set(matches)) == 1, f"inconsistent --output templates: {set(matches)}"
    return matches[0]


def _resolved_output_paths() -> list[str]:
    template = _output_path_template()
    return [
        template.replace("${{ matrix.report_type }}", rt)
        for rt in _matrix_report_types()
    ]


def test_every_matrix_output_path_is_allowed_by_guard() -> None:
    for path in _resolved_output_paths():
        # Must not raise. repo_root anchors normalization to the repo.
        assert_report_output_path_allowed(path, repo_root=REPO_ROOT)


def test_workflow_does_not_target_protected_public_report() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    # The exact protected pattern that caused the original failure.
    assert "reports/${{ matrix.report_type }}-report.md" not in text


def test_guard_still_protects_top_level_report_paths() -> None:
    # Sanity: the guard itself must keep rejecting the protected paths,
    # otherwise this test would pass vacuously after a guard weakening.
    for rt in _matrix_report_types():
        with pytest.raises(ReportOutputBoundaryError):
            assert_report_output_path_allowed(
                f"reports/{rt}-report.md", repo_root=REPO_ROOT
            )
