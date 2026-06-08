from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts/generate_outcomes.py"


def _run(tmp_path: Path, signals_dir: Path, outcomes_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            "--days",
            "30",
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


def test_p165_missing_signals_dir_writes_blocked_manifest(tmp_path: Path) -> None:
    signals_dir = tmp_path / "missing-signals"
    outcomes_dir = tmp_path / "outcomes"

    result = _run(tmp_path, signals_dir, outcomes_dir)

    assert result.returncode == 1
    manifest = json.loads((outcomes_dir / "outcome-run-manifest.json").read_text(encoding="utf-8"))
    assert manifest["run_status"] == "BLOCKED_MISSING_INPUTS"
    assert manifest["skip_reasons"] == ["signals_directory_missing"]


def test_p165_empty_signals_dir_writes_no_eligible_manifest(tmp_path: Path) -> None:
    signals_dir = tmp_path / "signals"
    outcomes_dir = tmp_path / "outcomes"
    signals_dir.mkdir()

    result = _run(tmp_path, signals_dir, outcomes_dir)

    assert result.returncode == 0
    manifest = json.loads((outcomes_dir / "outcome-run-manifest.json").read_text(encoding="utf-8"))
    assert manifest["run_status"] == "NO_ELIGIBLE_SIGNALS"
    assert manifest["skip_reasons"] == ["no_signal_files_in_window"]


def test_p165_fixture_signal_writes_ok_manifest_and_outcome_files(tmp_path: Path) -> None:
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
    assert manifest["run_status"] == "OK"
    assert manifest["signal_batch_count"] == 1
    assert manifest["total_input_signals"] == 1
    assert manifest["total_evaluated"] == 1
    assert (outcomes_dir / "2026-06-01-outcomes.json").exists()
    assert (outcomes_dir / "latest-outcomes.md").exists()
