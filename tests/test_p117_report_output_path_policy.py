from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from src.report_output_boundary import (
    ReportOutputBoundaryError,
    assert_report_output_path_allowed,
    is_generated_report_output_path,
)


ALLOWED_GENERATED_PATHS = [
    "reports/generated/premarket-report.md",
    "reports/premarket/2026-06-04-premarket.md",
    "reports/intraday/2026-06-04-intraday.md",
    "reports/postmarket/2026-06-04-postmarket.md",
    "reports/weekly/2026-W23-weekly.md",
    "reports/signals/latest-signals.json",
    "reports/validation/paper-observation-health.md",
]


PROTECTED_OR_INVALID_PATHS = [
    "reports/premarket-report.md",
    "reports/postmarket-report.md",
    "reports/weekly-report.md",
    "reports/random.md",
    "docs/generated-report.md",
]


def test_p117_allowed_generated_report_paths_are_consistent() -> None:
    for path in ALLOWED_GENERATED_PATHS:
        assert is_generated_report_output_path(path)
        assert_report_output_path_allowed(path)


def test_p117_protected_or_invalid_paths_fail_with_clear_policy_error() -> None:
    for path in PROTECTED_OR_INVALID_PATHS:
        with pytest.raises(ReportOutputBoundaryError, match="Allowed generated report roots"):
            assert_report_output_path_allowed(path)


def test_p117_institutional_reports_workflow_uses_only_allowed_report_paths() -> None:
    workflow = yaml.safe_load(Path(".github/workflows/institutional-reports.yml").read_text(encoding="utf-8"))
    run_script = next(
        step["run"]
        for step in workflow["jobs"]["report"]["steps"]
        if step.get("name") == "Resolve report type"
    )

    expected_paths = [
        "reports/weekly",
        "reports/${REPORT_TYPE}",
        "reports/generated/${REPORT_TYPE}-report.md",
    ]
    for expected in expected_paths:
        assert expected in run_script

    forbidden_paths = [
        "reports/premarket-report.md",
        "reports/postmarket-report.md",
        "reports/weekly-report.md",
    ]
    for forbidden in forbidden_paths:
        assert forbidden not in run_script
