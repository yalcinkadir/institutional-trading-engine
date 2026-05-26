import json
import subprocess
import sys
from pathlib import Path

from src.validation.daily_evidence_input_builder import build_daily_evidence_inputs
from src.validation.daily_evidence_input_validation import validate_daily_evidence_inputs
from src.validation.daily_evidence_source_bootstrap import bootstrap_daily_evidence_sources


SCRIPT = Path("scripts/bootstrap_daily_evidence_sources.py")


def test_bootstrap_daily_evidence_sources_writes_required_source_files(tmp_path: Path):
    source_dir = tmp_path / "sources"

    report = bootstrap_daily_evidence_sources(source_dir, report_date="2026-05-26")

    assert report.passed is True
    assert report.observation_only is True
    assert len(report.files) == 5
    assert (source_dir / "paper_observations.json").exists()
    assert (source_dir / "backtest_results.json").exists()
    assert (source_dir / "forward_results.json").exists()
    assert (source_dir / "regime_observations.json").exists()
    assert (source_dir / "position_snapshots.json").exists()


def test_bootstrap_sources_can_feed_builder_and_validator(tmp_path: Path):
    source_dir = tmp_path / "sources"
    input_dir = tmp_path / "inputs"
    bootstrap_daily_evidence_sources(source_dir, report_date="2026-05-26")

    build_report = build_daily_evidence_inputs(source_dir, input_dir)
    validation_report = validate_daily_evidence_inputs(input_dir)

    assert build_report.passed is True
    assert validation_report.passed is True
    assert validation_report.metrics.files_valid == 5


def test_bootstrap_source_records_are_marked_observation_only(tmp_path: Path):
    source_dir = tmp_path / "sources"
    bootstrap_daily_evidence_sources(source_dir, report_date="2026-05-26")

    paper_records = json.loads((source_dir / "paper_observations.json").read_text(encoding="utf-8"))

    assert paper_records
    assert all(record["source"] == "observation_only_bootstrap" for record in paper_records)


def test_bootstrap_cli_writes_source_and_report_files(tmp_path: Path):
    source_dir = tmp_path / "sources"
    report_dir = tmp_path / "reports"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--output-dir",
            str(source_dir),
            "--report-dir",
            str(report_dir),
            "--report-date",
            "2026-05-26",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Daily evidence source bootstrap status: PASS" in result.stdout
    assert (source_dir / "paper_observations.json").exists()
    assert (report_dir / "daily_evidence_source_bootstrap.json").exists()
    assert (report_dir / "daily_evidence_source_bootstrap.md").exists()
