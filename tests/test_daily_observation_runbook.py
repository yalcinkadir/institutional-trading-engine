import json
import subprocess
import sys
from pathlib import Path

from src.validation.daily_observation_runbook import (
    REQUIRED_DAILY_STEPS,
    review_daily_observation_runbook,
    write_runbook_template,
)

SCRIPT = Path("scripts/review_daily_observation_runbook.py")


def _complete_checklist(path: Path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["steps"] = {step: True for step in REQUIRED_DAILY_STEPS}
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_runbook_template_is_initially_incomplete(tmp_path: Path):
    checklist = tmp_path / "runbook.json"
    write_runbook_template(checklist, report_date="2026-05-27")

    report = review_daily_observation_runbook(checklist, expected_report_date="2026-05-27")

    assert report.passed is False
    assert set(report.missing_steps) == set(REQUIRED_DAILY_STEPS)
    assert report.observation_only is True


def test_completed_runbook_passes(tmp_path: Path):
    checklist = tmp_path / "runbook.json"
    write_runbook_template(checklist, report_date="2026-05-27")
    _complete_checklist(checklist)

    report = review_daily_observation_runbook(checklist, expected_report_date="2026-05-27")

    assert report.passed is True
    assert report.missing_steps == []
    assert len(report.completed_steps) == len(REQUIRED_DAILY_STEPS)


def test_blocked_confirmation_fails(tmp_path: Path):
    checklist = tmp_path / "runbook.json"
    write_runbook_template(checklist, report_date="2026-05-27")
    _complete_checklist(checklist)
    payload = json.loads(checklist.read_text(encoding="utf-8"))
    payload["blocked_confirmations"]["cash_deployment_authorized"] = True
    checklist.write_text(json.dumps(payload), encoding="utf-8")

    report = review_daily_observation_runbook(checklist, expected_report_date="2026-05-27")

    assert report.passed is False
    assert any(issue.field == "blocked_confirmations.cash_deployment_authorized" for issue in report.issues)


def test_cli_writes_template_and_reports(tmp_path: Path):
    checklist = tmp_path / "runbook.json"
    output_dir = tmp_path / "review"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--checklist",
            str(checklist),
            "--output-dir",
            str(output_dir),
            "--report-date",
            "2026-05-27",
            "--write-template",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Daily observation runbook review status: FAIL" in result.stdout
    assert (output_dir / "daily_observation_runbook_review.json").exists()
    assert (output_dir / "daily_observation_runbook_review.md").exists()
