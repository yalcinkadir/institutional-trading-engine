import json
import subprocess
import sys
from pathlib import Path

from src.validation.daily_evidence_input_validation import validate_daily_evidence_inputs


SCRIPT = Path("scripts/validate_daily_evidence_inputs.py")


def _write_valid_inputs(input_dir: Path):
    (input_dir / "paper_observation_records.json").write_text(
        json.dumps(
            [
                {
                    "observation_date": "2026-05-25",
                    "expected_action": "ENTER",
                    "paper_action": "ENTER",
                    "expected_r": 0.3,
                    "paper_r": 0.3,
                    "resolved": True,
                }
            ]
        ),
        encoding="utf-8",
    )
    (input_dir / "backtest_records.json").write_text(json.dumps([{"result_r": 0.2}]), encoding="utf-8")
    (input_dir / "forward_records.json").write_text(json.dumps([{"result_r": 0.2}]), encoding="utf-8")
    (input_dir / "regime_records.json").write_text(
        json.dumps([{"regime": "neutral", "volatility": 0.18, "correlation": 0.42, "drawdown": 0.02}]),
        encoding="utf-8",
    )
    (input_dir / "position_records.json").write_text(
        json.dumps(
            [
                {
                    "symbol": "AAPL",
                    "sector": "Technology",
                    "weight": 1.0,
                    "result_r": 0.2,
                    "beta": 1.1,
                    "market_return_r": 0.1,
                    "factor_exposures": {"momentum": 0.5},
                    "factor_returns": {"momentum": 0.2},
                }
            ]
        ),
        encoding="utf-8",
    )


def test_validate_daily_evidence_inputs_passes_for_valid_files(tmp_path: Path):
    input_dir = tmp_path / "inputs"
    input_dir.mkdir()
    _write_valid_inputs(input_dir)

    report = validate_daily_evidence_inputs(input_dir)

    assert report.passed is True
    assert report.metrics.files_present == 5
    assert report.metrics.files_valid == 5
    assert report.metrics.files_failed == 0


def test_validate_daily_evidence_inputs_fails_when_required_file_missing(tmp_path: Path):
    input_dir = tmp_path / "inputs"
    input_dir.mkdir()
    _write_valid_inputs(input_dir)
    (input_dir / "forward_records.json").unlink()

    report = validate_daily_evidence_inputs(input_dir)

    assert report.passed is False
    assert any(item.filename == "forward_records.json" and not item.present for item in report.files)


def test_validate_daily_evidence_inputs_fails_on_wrong_schema(tmp_path: Path):
    input_dir = tmp_path / "inputs"
    input_dir.mkdir()
    _write_valid_inputs(input_dir)
    (input_dir / "position_records.json").write_text(json.dumps([{"symbol": "AAPL", "weight": "large"}]), encoding="utf-8")

    report = validate_daily_evidence_inputs(input_dir)

    assert report.passed is False
    position_file = next(item for item in report.files if item.filename == "position_records.json")
    assert any("missing sector" in error for error in position_file.errors)
    assert any("field weight must be numeric" in error for error in position_file.errors)


def test_validate_daily_evidence_inputs_cli_writes_reports(tmp_path: Path):
    input_dir = tmp_path / "inputs"
    output_dir = tmp_path / "validation"
    input_dir.mkdir()
    _write_valid_inputs(input_dir)

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Daily evidence input validation status: PASS" in result.stdout
    assert (output_dir / "daily_evidence_input_validation.json").exists()
    assert (output_dir / "daily_evidence_input_validation.md").exists()


def test_validate_daily_evidence_inputs_cli_exits_one_on_failure(tmp_path: Path):
    input_dir = tmp_path / "inputs"
    output_dir = tmp_path / "validation"
    input_dir.mkdir()

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Daily evidence input validation status: FAIL" in result.stdout
    assert (output_dir / "daily_evidence_input_validation.json").exists()
