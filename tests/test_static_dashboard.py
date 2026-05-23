from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from src.operations.static_dashboard import build_static_dashboard, collect_dashboard_inputs


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_build_static_dashboard_with_available_inputs(tmp_path: Path) -> None:
    _write_json(
        tmp_path / "reports/signals/latest-signals.json",
        {"signals": [{"symbol": "SPY", "action": "NO_TRADE"}, {"symbol": "QQQ", "action": "BUY_WATCH"}]},
    )
    _write_json(
        tmp_path / "data/portfolio_state.json",
        {
            "equity_current": 100000,
            "drawdown_percent": 0.0,
            "daily_loss_percent": 0.0,
            "open_positions": [],
            "source": "unit_test",
        },
    )

    result = build_static_dashboard(
        root=tmp_path,
        output_html=tmp_path / "reports/dashboard/index.html",
        output_json=tmp_path / "reports/dashboard/dashboard.json",
        input_paths={
            "latest_signals": "reports/signals/latest-signals.json",
            "portfolio_state": "data/portfolio_state.json",
        },
    )

    assert result.status == "PASS"
    assert result.warnings == ()
    html = (tmp_path / "reports/dashboard/index.html").read_text(encoding="utf-8")
    payload = json.loads((tmp_path / "reports/dashboard/dashboard.json").read_text(encoding="utf-8"))
    assert "Institutional Trading Engine Dashboard" in html
    assert payload["status"] == "PASS"
    assert payload["inputs"][0]["summary"]["signal_count"] == 2
    assert payload["inputs"][1]["summary"]["equity_current"] == 100000


def test_build_static_dashboard_with_missing_inputs_is_partial(tmp_path: Path) -> None:
    _write_json(
        tmp_path / "data/portfolio_state.json",
        {"equity_current": 90000, "open_positions": [{"symbol": "SPY"}]},
    )

    result = build_static_dashboard(
        root=tmp_path,
        output_html=tmp_path / "dashboard.html",
        output_json=tmp_path / "dashboard.json",
        input_paths={
            "latest_signals": "reports/signals/latest-signals.json",
            "portfolio_state": "data/portfolio_state.json",
        },
    )

    assert result.status == "PARTIAL"
    assert "latest_signals:file_missing" in result.warnings
    payload = json.loads((tmp_path / "dashboard.json").read_text(encoding="utf-8"))
    assert payload["status"] == "PARTIAL"
    assert payload["inputs"][0]["status"] == "missing"
    assert payload["inputs"][1]["status"] == "available"


def test_build_static_dashboard_with_all_missing_inputs_is_empty(tmp_path: Path) -> None:
    result = build_static_dashboard(
        root=tmp_path,
        output_html=tmp_path / "dashboard.html",
        output_json=tmp_path / "dashboard.json",
        input_paths={"latest_signals": "reports/signals/latest-signals.json"},
    )

    assert result.status == "EMPTY"
    assert result.warnings == ("latest_signals:file_missing",)


def test_collect_dashboard_inputs_marks_invalid_json(tmp_path: Path) -> None:
    invalid = tmp_path / "reports/signals/latest-signals.json"
    invalid.parent.mkdir(parents=True, exist_ok=True)
    invalid.write_text("{invalid", encoding="utf-8")

    inputs = collect_dashboard_inputs(
        root=tmp_path,
        input_paths={"latest_signals": "reports/signals/latest-signals.json"},
    )

    assert inputs[0].status == "invalid"
    assert inputs[0].error.startswith("invalid_json")


def test_static_dashboard_cli_outputs_json(tmp_path: Path) -> None:
    _write_json(
        tmp_path / "data/portfolio_state.json",
        {"equity_current": 100000, "open_positions": []},
    )

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/build_static_dashboard.py",
            "--root",
            str(tmp_path),
            "--output-html",
            str(tmp_path / "out/index.html"),
            "--output-json",
            str(tmp_path / "out/dashboard.json"),
            "--json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(completed.stdout)
    assert payload["status"] in {"PARTIAL", "PASS"}
    assert (tmp_path / "out/index.html").exists()
    assert (tmp_path / "out/dashboard.json").exists()
