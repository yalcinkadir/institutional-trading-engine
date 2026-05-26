import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/generate_daily_evidence_components.py")


def test_generate_components_cli_writes_real_component_reports_from_smoke_fixture(tmp_path: Path):
    output_dir = tmp_path / "components"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--output-dir",
            str(output_dir),
            "--report-date",
            "2026-05-25",
            "--use-smoke-fixture",
            "--min-observation-days",
            "1",
            "--simulations",
            "25",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "All generated daily evidence components passed" in result.stdout
    expected_files = {
        "paper_observation_reconciliation.json",
        "performance_drift_detection.json",
        "sequential_edge_decay.json",
        "regime_change_detection.json",
        "position_risk_attribution.json",
        "monte_carlo_robustness.json",
    }
    assert expected_files.issubset({path.name for path in output_dir.glob("*.json")})
    reconciliation = json.loads((output_dir / "paper_observation_reconciliation.json").read_text(encoding="utf-8"))
    assert reconciliation["passed"] is True
    assert reconciliation["metrics"]["observation_days"] >= 1


def test_generate_components_cli_requires_inputs_without_smoke_fixture(tmp_path: Path):
    output_dir = tmp_path / "components"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--output-dir",
            str(output_dir),
            "--report-date",
            "2026-05-25",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "Missing evidence input files" in result.stderr


def test_generate_components_cli_real_input_overrides_smoke_fixture(tmp_path: Path):
    input_dir = tmp_path / "inputs"
    output_dir = tmp_path / "components"
    input_dir.mkdir()

    custom_paper_records = [
        {
            "observation_date": "2026-05-25",
            "expected_action": "ENTER",
            "paper_action": "ENTER",
            "expected_r": 0.3,
            "paper_r": 0.3,
            "resolved": True,
        }
    ]
    (input_dir / "paper_observation_records.json").write_text(json.dumps(custom_paper_records), encoding="utf-8")

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
            "--use-smoke-fixture",
            "--min-observation-days",
            "1",
            "--simulations",
            "25",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    reconciliation = json.loads((output_dir / "paper_observation_reconciliation.json").read_text(encoding="utf-8"))
    assert reconciliation["metrics"]["total_records"] == 1
    assert reconciliation["metrics"]["paper_total_r"] == 0.3
