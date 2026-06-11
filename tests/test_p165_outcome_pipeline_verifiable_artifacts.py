from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts/generate_outcomes.py"
AUGMENT = ROOT / "scripts/augment_outcome_manifest_p165.py"
VALIDATOR = ROOT / "scripts/validate_outcome_manifest_p165.py"


def _run(
    tmp_path: Path,
    signals_dir: Path,
    outcomes_dir: Path,
    *,
    mode: str = "production",
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            "--days",
            "30",
            "--mode",
            mode,
            "--signals-dir",
            str(signals_dir),
            "--outcomes-dir",
            str(outcomes_dir),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def _augment(outcomes_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(AUGMENT), "--outcomes-dir", str(outcomes_dir)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def _validate(outcomes_dir: Path, *, allow_demo_no_data: bool = False) -> subprocess.CompletedProcess[str]:
    cmd = [
        sys.executable,
        str(VALIDATOR),
        "--manifest",
        str(outcomes_dir / "outcome-run-manifest.json"),
    ]
    if allow_demo_no_data:
        cmd.append("--allow-demo-no-data")
    return subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_p165_missing_signals_dir_writes_blocked_manifest(tmp_path: Path) -> None:
    signals_dir = tmp_path / "missing-signals"
    outcomes_dir = tmp_path / "outcomes"

    result = _run(tmp_path, signals_dir, outcomes_dir)

    assert result.returncode == 0
    manifest = json.loads((outcomes_dir / "outcome-run-manifest.json").read_text(encoding="utf-8"))
    assert manifest["run_status"] == "BLOCKED_MISSING_INPUTS"
    assert manifest["skip_reasons"] == ["signals_directory_missing"]
    assert manifest["outcome_learning_claim_allowed"] is False


def test_p165_empty_signals_dir_writes_blocked_no_valid_signals_manifest(tmp_path: Path) -> None:
    signals_dir = tmp_path / "signals"
    outcomes_dir = tmp_path / "outcomes"
    signals_dir.mkdir()

    result = _run(tmp_path, signals_dir, outcomes_dir)

    assert result.returncode == 0
    manifest = json.loads((outcomes_dir / "outcome-run-manifest.json").read_text(encoding="utf-8"))
    assert manifest["run_status"] == "BLOCKED_NO_VALID_SIGNALS"
    assert manifest["mode"] == "production"
    assert manifest["scanned_signal_files"] == 0
    assert manifest["total_input_signals"] == 0
    assert manifest["valid_signal_count"] == 0
    assert manifest["invalid_signal_count"] == 0
    assert manifest["skip_reasons"] == ["no_signal_files_in_window"]
    assert manifest["upstream_dependency_status"] == "NO_VALID_SIGNAL_INPUTS"
    assert manifest["outcome_learning_claim_allowed"] is False


def test_p165_fixture_signal_writes_success_manifest_and_outcome_files(tmp_path: Path) -> None:
    signals_dir = tmp_path / "signals"
    outcomes_dir = tmp_path / "outcomes"
    signals_dir.mkdir()
    (signals_dir / "2026-06-01-signals.json").write_text(
        json.dumps(
            {
                "signals": [
                    {
                        "symbol": "AAPL",
                        "action": "BUY_WATCH",
                        "status": "PENDING",
                        "entry_trigger": 100.0,
                        "close": 99.0,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    result = _run(tmp_path, signals_dir, outcomes_dir)

    assert result.returncode == 0
    manifest = json.loads((outcomes_dir / "outcome-run-manifest.json").read_text(encoding="utf-8"))
    assert manifest["run_status"] == "SUCCESS"
    assert manifest["signal_batch_count"] == 1
    assert manifest["scanned_signal_files"] == 1
    assert manifest["total_input_signals"] == 1
    assert manifest["valid_signal_count"] == 1
    assert manifest["invalid_signal_count"] == 0
    assert manifest["total_evaluated"] == 1
    assert manifest["outcome_learning_claim_allowed"] is True
    assert (outcomes_dir / "2026-06-01-outcomes.json").exists()
    assert (outcomes_dir / "latest-outcomes.md").exists()


def test_186_production_outcome_tracking_blocks_invalid_signal_window(tmp_path: Path) -> None:
    signals_dir = tmp_path / "signals"
    outcomes_dir = tmp_path / "outcomes"
    signals_dir.mkdir()
    (signals_dir / "2026-06-01-signals.json").write_text(
        json.dumps(
            {
                "signals": [
                    {"symbol": "AAPL", "action": "NO_TRADE", "status": "PENDING", "close": None},
                    {"symbol": "MSFT", "action": "NO_TRADE", "status": "PENDING", "close": None},
                ]
            }
        ),
        encoding="utf-8",
    )

    result = _run(tmp_path, signals_dir, outcomes_dir)
    assert result.returncode == 0

    manifest = json.loads((outcomes_dir / "outcome-run-manifest.json").read_text(encoding="utf-8"))
    assert manifest["run_status"] == "BLOCKED_NO_VALID_SIGNALS"
    assert manifest["scanned_signal_files"] == 1
    assert manifest["total_input_signals"] == 2
    assert manifest["valid_signal_count"] == 0
    assert manifest["invalid_signal_count"] == 2
    assert manifest["outcome_learning_claim_allowed"] is False
    assert "non_actionable_signal" in manifest["skip_reasons"]
    assert "missing_price_anchor" in manifest["skip_reasons"]

    augmented = _augment(outcomes_dir)
    assert augmented.returncode == 0, augmented.stderr

    validation = _validate(outcomes_dir)
    assert validation.returncode == 0, validation.stderr


def test_186_demo_no_data_requires_explicit_validator_allowance(tmp_path: Path) -> None:
    signals_dir = tmp_path / "signals"
    outcomes_dir = tmp_path / "outcomes"
    signals_dir.mkdir()

    result = _run(tmp_path, signals_dir, outcomes_dir, mode="demo")
    assert result.returncode == 0

    augmented = _augment(outcomes_dir)
    assert augmented.returncode == 0, augmented.stderr

    rejected = _validate(outcomes_dir)
    assert rejected.returncode != 0
    assert "DEMO_NO_DATA is not allowed" in rejected.stderr

    allowed = _validate(outcomes_dir, allow_demo_no_data=True)
    assert allowed.returncode == 0, allowed.stderr
