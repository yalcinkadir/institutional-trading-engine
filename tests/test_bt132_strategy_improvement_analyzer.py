from __future__ import annotations

import json
from pathlib import Path

from scripts.analyze_bt132_strategy_improvement import analyze, render_markdown, write_report


def _evidence(tmp_path: Path) -> Path:
    payload = {
        "run_id": "bt131-real-data-manual",
        "data_source": "real_data",
        "is_demo": False,
        "input_pack_gate_status": "PASSED",
        "input_completeness_status": "OK",
        "run_health_status": "OK",
        "metrics": {"total": 4, "expectancy_r": 0.25, "false_breakout_rate": 0.5, "stop_hit_rate": 0.5},
        "results": [
            {"signal_id": "s1", "symbol": "AAA", "signal_date": "2024-01-01", "outcome": "TARGET_2_HIT", "entry_hit": True, "target_1_hit": True, "target_2_hit": True, "stop_hit": False, "false_breakout": False, "r_multiple": 3.0, "reason": "target_2_hit", "bars_evaluated": 5},
            {"signal_id": "s2", "symbol": "AAA", "signal_date": "2024-01-02", "outcome": "STOP_HIT", "entry_hit": True, "target_1_hit": False, "target_2_hit": False, "stop_hit": True, "false_breakout": True, "r_multiple": -1.0, "reason": "stop_hit", "bars_evaluated": 4},
            {"signal_id": "s3", "symbol": "BBB", "signal_date": "2024-01-03", "outcome": "STOP_HIT", "entry_hit": True, "target_1_hit": True, "target_2_hit": False, "stop_hit": True, "false_breakout": False, "r_multiple": -1.0, "reason": "stop_hit", "bars_evaluated": 8},
            {"signal_id": "s4", "symbol": "BBB", "signal_date": "2024-01-04", "outcome": "EXPIRED", "entry_hit": False, "target_1_hit": False, "target_2_hit": False, "stop_hit": False, "false_breakout": True, "r_multiple": 0.0, "reason": "entry_not_hit", "bars_evaluated": 20},
        ],
    }
    path = tmp_path / "real-data-backtest-evidence.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_bt132_analyzer_produces_reviewable_findings(tmp_path: Path) -> None:
    report = analyze(_evidence(tmp_path))

    assert report.report_version == "bt132.v1"
    assert report.data_source == "real_data"
    assert report.is_demo is False
    assert report.input_pack_gate_status == "PASSED"
    assert report.run_health_status == "OK"
    assert report.total_trades == 4
    assert report.review_status == "READY_FOR_REVIEW"
    assert report.stop_loss_findings["stop_hit_rate"] == 0.5
    assert report.entry_findings["false_breakout_rate"] == 0.5
    assert report.recommendations
    assert any(item["area"] == "entry" for item in report.recommendations)
    assert any(item["area"] == "stop_loss" for item in report.recommendations)


def test_bt132_analyzer_writes_json_and_markdown(tmp_path: Path) -> None:
    report = analyze(_evidence(tmp_path))
    output_json = tmp_path / "bt132.json"
    output_md = tmp_path / "bt132.md"

    write_report(report, output_json=output_json, output_md=output_md)

    payload = json.loads(output_json.read_text(encoding="utf-8"))
    markdown = output_md.read_text(encoding="utf-8")
    assert payload["report_version"] == "bt132.v1"
    assert payload["review_status"] == "READY_FOR_REVIEW"
    assert "# BT132 Strategy Improvement Report" in markdown
    assert "## Recommendations" in markdown
    assert "Research only. No live trading authorization." in markdown
    assert render_markdown(report) == markdown


def test_bt132_analyzer_refuses_demo_evidence(tmp_path: Path) -> None:
    path = _evidence(tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["is_demo"] = True
    path.write_text(json.dumps(payload), encoding="utf-8")

    try:
        analyze(path)
    except SystemExit as exc:
        assert "refuses demo evidence" in str(exc)
    else:  # pragma: no cover - defensive assertion
        raise AssertionError("BT132 must refuse demo evidence")
