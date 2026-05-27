import json
import subprocess
import sys
from pathlib import Path

from src.validation.daily_observation_cadence import review_daily_observation_cadence

SCRIPT = Path("scripts/review_daily_observation_cadence.py")


def _write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _write_raw_sources(raw_dir: Path):
    _write_json(raw_dir / "paper_observations.json", [{"observation_date": "2026-05-27", "paper_r": 0.1}])
    _write_json(raw_dir / "backtest_results.json", [{"result_r": 0.1}])
    _write_json(raw_dir / "regime_observations.json", [{"date": "2026-05-27", "regime": "neutral"}])
    _write_json(raw_dir / "position_snapshots.json", [{"symbol": "AAPL", "weight": 0.5}])


def _write_artifact_tree(root: Path, report_date: str = "2026-05-27"):
    _write_json(root / "daily_observation_feed" / "paper_observations.json", [{"paper_r": 0.1}])
    _write_json(root / "daily_evidence_input_validation" / "daily_evidence_input_validation.json", {"passed": True})
    component_dir = root / "daily_evidence_components"
    for filename in (
        "paper_observation_reconciliation.json",
        "performance_drift_detection.json",
        "sequential_edge_decay.json",
        "regime_change_detection.json",
        "position_risk_attribution.json",
        "monte_carlo_robustness.json",
    ):
        _write_json(component_dir / filename, {"passed": True})
    (component_dir / "component_exit_code.txt").write_text("0", encoding="utf-8")
    evidence_dir = root / "daily_evidence"
    _write_json(evidence_dir / f"daily_evidence_report_{report_date}.json", {"passed": True})
    (evidence_dir / f"daily_evidence_report_{report_date}.md").write_text("# Daily Evidence\n", encoding="utf-8")
    (evidence_dir / "report_exit_code.txt").write_text("0", encoding="utf-8")


def test_cadence_review_passes_when_raw_sources_and_artifacts_exist(tmp_path: Path):
    raw_dir = tmp_path / "raw"
    artifact_root = tmp_path / "reports"
    _write_raw_sources(raw_dir)
    _write_artifact_tree(artifact_root)

    report = review_daily_observation_cadence(
        report_date="2026-05-27",
        raw_source_dir=raw_dir,
        artifact_root=artifact_root,
    )

    assert report.passed is True
    assert all(gate.passed for gate in report.gates)
    assert report.observation_only is True


def test_cadence_review_fails_when_raw_source_file_is_missing(tmp_path: Path):
    raw_dir = tmp_path / "raw"
    artifact_root = tmp_path / "reports"
    _write_raw_sources(raw_dir)
    (raw_dir / "position_snapshots.json").unlink()
    _write_artifact_tree(artifact_root)

    report = review_daily_observation_cadence(
        report_date="2026-05-27",
        raw_source_dir=raw_dir,
        artifact_root=artifact_root,
    )

    assert report.passed is False
    failed = [gate.name for gate in report.gates if not gate.passed]
    assert "raw_source_files_complete" in failed


def test_cadence_review_cli_writes_reports(tmp_path: Path):
    raw_dir = tmp_path / "raw"
    artifact_root = tmp_path / "reports"
    output_dir = tmp_path / "cadence"
    _write_raw_sources(raw_dir)
    _write_artifact_tree(artifact_root)

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--report-date",
            "2026-05-27",
            "--raw-source-dir",
            str(raw_dir),
            "--artifact-root",
            str(artifact_root),
            "--output-dir",
            str(output_dir),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Daily observation cadence review status: PASS" in result.stdout
    assert (output_dir / "daily_observation_cadence_review.json").exists()
    assert (output_dir / "daily_observation_cadence_review.md").exists()
