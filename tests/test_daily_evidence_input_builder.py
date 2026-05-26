import json
import subprocess
import sys
from pathlib import Path

from src.validation.daily_evidence_input_builder import build_daily_evidence_inputs
from src.validation.daily_evidence_input_validation import validate_daily_evidence_inputs


SCRIPT = Path("scripts/build_daily_evidence_inputs.py")


def _write_source_files(source_dir: Path):
    (source_dir / "paper_observations.json").write_text(
        json.dumps(
            [
                {
                    "date": "2026-05-25",
                    "expected_action": "ENTER",
                    "paper_action": "ENTER",
                    "expected_result_r": "0.3",
                    "paper_result_r": 0.3,
                    "resolved": True,
                }
            ]
        ),
        encoding="utf-8",
    )
    (source_dir / "backtest_results.json").write_text(json.dumps([{"r": 0.2}, {"pnl_r": -0.1}]), encoding="utf-8")
    (source_dir / "forward_results.json").write_text(json.dumps([{"paper_r": 0.25}, {"result_r": -0.05}]), encoding="utf-8")
    (source_dir / "regime_observations.json").write_text(
        json.dumps([{"regime_label": "neutral", "volatility_pct": 0.18, "corr": 0.42, "drawdown_pct": 0.02}]),
        encoding="utf-8",
    )
    (source_dir / "position_snapshots.json").write_text(
        json.dumps(
            [
                {
                    "symbol": "AAPL",
                    "sector": "Technology",
                    "portfolio_weight": "1.0",
                    "paper_r": 0.2,
                    "beta": 1.1,
                    "market_r": 0.1,
                    "factor_exposures": {"momentum": "0.5"},
                    "factor_returns": {"momentum": 0.2},
                }
            ]
        ),
        encoding="utf-8",
    )


def test_build_daily_evidence_inputs_writes_normalized_files(tmp_path: Path):
    source_dir = tmp_path / "source"
    output_dir = tmp_path / "inputs"
    source_dir.mkdir()
    _write_source_files(source_dir)

    report = build_daily_evidence_inputs(source_dir, output_dir)

    assert report.passed is True
    assert len(report.files) == 5
    assert (output_dir / "paper_observation_records.json").exists()
    assert (output_dir / "forward_records.json").exists()
    validation = validate_daily_evidence_inputs(output_dir)
    assert validation.passed is True


def test_build_daily_evidence_inputs_fails_when_source_file_missing(tmp_path: Path):
    source_dir = tmp_path / "source"
    output_dir = tmp_path / "inputs"
    source_dir.mkdir()
    _write_source_files(source_dir)
    (source_dir / "forward_results.json").unlink()

    report = build_daily_evidence_inputs(source_dir, output_dir)

    assert report.passed is False
    assert any("missing source file: forward_results.json" in error for error in report.errors)


def test_build_daily_evidence_inputs_cli_writes_reports(tmp_path: Path):
    source_dir = tmp_path / "source"
    output_dir = tmp_path / "inputs"
    report_dir = tmp_path / "reports"
    source_dir.mkdir()
    _write_source_files(source_dir)

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--source-dir",
            str(source_dir),
            "--output-dir",
            str(output_dir),
            "--report-dir",
            str(report_dir),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Daily evidence input build status: PASS" in result.stdout
    assert (report_dir / "daily_evidence_input_build.json").exists()
    assert (report_dir / "daily_evidence_input_build.md").exists()


def test_build_daily_evidence_inputs_cli_exits_one_on_invalid_sources(tmp_path: Path):
    source_dir = tmp_path / "source"
    output_dir = tmp_path / "inputs"
    report_dir = tmp_path / "reports"
    source_dir.mkdir()

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--source-dir",
            str(source_dir),
            "--output-dir",
            str(output_dir),
            "--report-dir",
            str(report_dir),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Daily evidence input build status: FAIL" in result.stdout
    assert (report_dir / "daily_evidence_input_build.json").exists()
