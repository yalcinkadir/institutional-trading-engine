import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/run_daily_evidence_report.py")


def _write_component(path: Path, passed: bool = True, **metrics):
    path.write_text(json.dumps({"passed": passed, "metrics": metrics or {"observations": 30}}), encoding="utf-8")


def _write_all_components(input_dir: Path):
    _write_component(input_dir / "paper_observation_reconciliation.json", True, observation_days=30)
    _write_component(input_dir / "performance_drift_detection.json", True, forward_expectancy_r=0.2)
    _write_component(input_dir / "sequential_edge_decay.json", True, decision="continue_observation")
    _write_component(input_dir / "regime_change_detection.json", True, state="stable")
    _write_component(input_dir / "position_risk_attribution.json", True, portfolio_r=1.0)
    _write_component(input_dir / "monte_carlo_robustness.json", True, observed_expectancy_r=0.2)


def test_daily_evidence_cli_writes_reports_and_exits_zero(tmp_path: Path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    _write_all_components(input_dir)

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
            "--report-date",
            "2026-05-25",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Daily evidence status: PASS" in result.stdout
    assert (output_dir / "daily_evidence_report_2026-05-25.json").exists()
    assert (output_dir / "daily_evidence_report_2026-05-25.md").exists()


def test_daily_evidence_cli_exits_one_when_component_fails(tmp_path: Path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    _write_all_components(input_dir)
    _write_component(input_dir / "regime_change_detection.json", False, state="regime_change_alert")

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
            "--report-date",
            "2026-05-25",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Daily evidence status: FAIL" in result.stdout
    payload = json.loads((output_dir / "daily_evidence_report_2026-05-25.json").read_text(encoding="utf-8"))
    assert payload["passed"] is False


def test_daily_evidence_cli_allows_missing_optional_components(tmp_path: Path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    _write_component(input_dir / "paper_observation_reconciliation.json", True, observation_days=30)
    _write_component(input_dir / "performance_drift_detection.json", True, forward_expectancy_r=0.2)
    _write_component(input_dir / "sequential_edge_decay.json", True, decision="continue_observation")
    _write_component(input_dir / "regime_change_detection.json", True, state="stable")

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
            "--report-date",
            "2026-05-25",
            "--allow-missing-risk-attribution",
            "--allow-missing-monte-carlo",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    payload = json.loads((output_dir / "daily_evidence_report_2026-05-25.json").read_text(encoding="utf-8"))
    assert payload["passed"] is True
