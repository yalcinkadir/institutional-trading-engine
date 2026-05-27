import json
import subprocess
import sys
from pathlib import Path

from src.validation.paper_observation_raw_contract import (
    validate_raw_observation_contract,
    write_raw_contract_template,
)

SCRIPT = Path("scripts/validate_paper_observation_raw_contract.py")


def test_template_validates_successfully(tmp_path: Path):
    source_dir = tmp_path / "raw"
    write_raw_contract_template(source_dir, report_date="2026-05-27")

    report = validate_raw_observation_contract(source_dir)

    assert report.passed is True
    assert len(report.files) == 4
    assert report.observation_only is True


def test_missing_required_field_fails_contract(tmp_path: Path):
    source_dir = tmp_path / "raw"
    write_raw_contract_template(source_dir, report_date="2026-05-27")
    path = source_dir / "paper_observations.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    del payload[0]["signal_id"]
    path.write_text(json.dumps(payload), encoding="utf-8")

    report = validate_raw_observation_contract(source_dir)

    assert report.passed is False
    assert any(issue.field == "signal_id" for issue in report.issues)


def test_bootstrap_source_type_is_rejected(tmp_path: Path):
    source_dir = tmp_path / "raw"
    write_raw_contract_template(source_dir, report_date="2026-05-27")
    path = source_dir / "paper_observations.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload[0]["source_type"] = "observation_only_bootstrap"
    path.write_text(json.dumps(payload), encoding="utf-8")

    report = validate_raw_observation_contract(source_dir)

    assert report.passed is False
    assert any("bootstrap" in issue.message for issue in report.issues)


def test_cli_writes_template_and_reports(tmp_path: Path):
    source_dir = tmp_path / "raw"
    report_dir = tmp_path / "report"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--source-dir",
            str(source_dir),
            "--report-dir",
            str(report_dir),
            "--write-template",
            "--report-date",
            "2026-05-27",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Raw paper observation contract status: PASS" in result.stdout
    assert (report_dir / "paper_observation_raw_contract.json").exists()
    assert (report_dir / "paper_observation_raw_contract.md").exists()
