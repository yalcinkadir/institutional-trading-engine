from __future__ import annotations

import json
from pathlib import Path

from src.operations.e2e_dry_run import run_e2e_dry_run_validation


def _write_signal_file(path: Path, signals: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"signals": signals}), encoding="utf-8")


def _valid_buy_watch() -> dict:
    return {
        "signal_id": "sig_NVDA_test",
        "symbol": "NVDA",
        "action": "BUY_WATCH",
        "entry_trigger": 101.0,
        "stop_loss": 96.0,
        "target_1": 110.0,
        "entry_reason": "breakout trigger",
        "stop_reason": "structure stop",
        "exit_reason": "momentum targets",
    }


def test_e2e_dry_run_passes_with_valid_signal_file(tmp_path: Path) -> None:
    signal_file = tmp_path / "reports" / "signals" / "latest-signals.json"
    _write_signal_file(signal_file, [_valid_buy_watch(), {"signal_id": "sig_AAPL", "symbol": "AAPL", "action": "NO_TRADE"}])

    result = run_e2e_dry_run_validation(
        signal_file=signal_file,
        alerts_dir=tmp_path / "reports" / "alerts",
        lifecycle_dir=tmp_path / "data",
    )

    assert result.passed
    assert all(check.passed for check in result.checks)
    assert result.to_dict()["passed"] is True


def test_e2e_dry_run_fails_when_signal_file_missing(tmp_path: Path) -> None:
    result = run_e2e_dry_run_validation(
        signal_file=tmp_path / "missing.json",
        alerts_dir=tmp_path / "alerts",
        lifecycle_dir=tmp_path / "data",
    )

    assert not result.passed
    assert any(check.name == "signal_file_exists" and not check.passed for check in result.checks)


def test_e2e_dry_run_fails_with_invalid_json(tmp_path: Path) -> None:
    signal_file = tmp_path / "signals.json"
    signal_file.write_text("{not-json", encoding="utf-8")

    result = run_e2e_dry_run_validation(
        signal_file=signal_file,
        alerts_dir=tmp_path / "alerts",
        lifecycle_dir=tmp_path / "data",
    )

    assert not result.passed
    assert any(check.name == "signal_file_json" and not check.passed for check in result.checks)


def test_e2e_dry_run_fails_with_invalid_signal_payload_shape(tmp_path: Path) -> None:
    signal_file = tmp_path / "signals.json"
    signal_file.write_text(json.dumps({"items": []}), encoding="utf-8")

    result = run_e2e_dry_run_validation(
        signal_file=signal_file,
        alerts_dir=tmp_path / "alerts",
        lifecycle_dir=tmp_path / "data",
    )

    assert not result.passed
    assert any(check.name == "signals_array" and not check.passed for check in result.checks)


def test_e2e_dry_run_fails_when_signal_identity_fields_are_missing(tmp_path: Path) -> None:
    signal_file = tmp_path / "signals.json"
    _write_signal_file(signal_file, [{"symbol": "NVDA", "action": "BUY_WATCH"}])

    result = run_e2e_dry_run_validation(
        signal_file=signal_file,
        alerts_dir=tmp_path / "alerts",
        lifecycle_dir=tmp_path / "data",
    )

    assert not result.passed
    assert any(check.name == "signal_identity_fields" and not check.passed for check in result.checks)


def test_e2e_dry_run_fails_when_buy_watch_trade_plan_is_incomplete(tmp_path: Path) -> None:
    signal_file = tmp_path / "signals.json"
    incomplete = _valid_buy_watch()
    incomplete.pop("stop_loss")
    _write_signal_file(signal_file, [incomplete])

    result = run_e2e_dry_run_validation(
        signal_file=signal_file,
        alerts_dir=tmp_path / "alerts",
        lifecycle_dir=tmp_path / "data",
    )

    assert not result.passed
    failed = [check for check in result.checks if check.name == "buy_watch_trade_plans"]
    assert failed
    assert "NVDA:stop_loss" in failed[0].message


def test_e2e_dry_run_accepts_empty_signal_list(tmp_path: Path) -> None:
    signal_file = tmp_path / "signals.json"
    _write_signal_file(signal_file, [])

    result = run_e2e_dry_run_validation(
        signal_file=signal_file,
        alerts_dir=tmp_path / "alerts",
        lifecycle_dir=tmp_path / "data",
    )

    assert result.passed
