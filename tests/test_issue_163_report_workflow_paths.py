from __future__ import annotations

from pathlib import Path

from src.report_output_boundary import assert_report_output_path_allowed


WORKFLOW_DIR = Path(".github/workflows")


def _lines_containing(text: str, needle: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if needle in line]


def test_report_quality_workflow_commits_only_generated_reports() -> None:
    workflow = (WORKFLOW_DIR / "report-quality.yml").read_text(encoding="utf-8")

    assert "--output \"reports/generated/${{ matrix.report_type }}-report.md\"" in workflow
    assert "--file \"reports/generated/${{ matrix.report_type }}-report.md\"" in workflow
    assert "path: reports/generated/${{ matrix.report_type }}-report.md" in workflow
    assert "path: reports/generated" in workflow
    assert "git add reports/generated/*report.md" in workflow
    assert "git add reports/*report.md" not in workflow
    assert all(
        line.startswith("git add reports/generated/")
        for line in _lines_containing(workflow, "git add reports/")
    )


def test_institutional_reports_workflow_does_not_stage_entire_reports_tree() -> None:
    workflow = (WORKFLOW_DIR / "institutional-reports.yml").read_text(encoding="utf-8")

    assert 'git add "$REPORT_FILE" "$LATEST_FILE"' in workflow
    assert "git add reports/signals/*.json reports/signals/*.md" in workflow
    assert "git add reports/validation/*.json reports/validation/*.md" in workflow
    assert "git add reports/datafeed_liveness/*.json" in workflow
    assert all(
        line.startswith("git add reports/signals/")
        or line.startswith("git add reports/validation/")
        or line.startswith("git add reports/datafeed_liveness/")
        or line.startswith('git add "$SCHEDULED_LIVENESS_FILE"')
        for line in _lines_containing(workflow, "git add reports/")
    )


def test_institutional_reports_workflow_artifacts_fail_when_expected_files_are_missing() -> None:
    workflow = (WORKFLOW_DIR / "institutional-reports.yml").read_text(encoding="utf-8")

    assert "path: ${{ steps.report_type.outputs.report_file }}" in workflow
    assert "path: ${{ steps.report_type.outputs.latest_file }}" in workflow
    assert workflow.count("if-no-files-found: error") >= 4


def test_issue_163_declared_report_outputs_are_boundary_allowed() -> None:
    allowed_paths = [
        "reports/generated/premarket-report.md",
        "reports/generated/postmarket-report.md",
        "reports/generated/weekly-report.md",
        "reports/premarket/2026-06-08-premarket.md",
        "reports/intraday/2026-06-08-intraday.md",
        "reports/postmarket/2026-06-08-postmarket.md",
        "reports/weekly/2026-W24-weekly.md",
        "reports/signals/latest-signals.json",
        "reports/validation/latest-paper-observation-health.json",
        "reports/datafeed_liveness/datafeed-liveness-latest.json",
    ]

    for path in allowed_paths:
        assert_report_output_path_allowed(path)
