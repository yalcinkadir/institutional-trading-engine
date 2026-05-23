from __future__ import annotations

import json
from pathlib import Path

from src.operations.scheduled_decision_support_dry_run import (
    render_scheduled_dry_run_markdown,
    run_scheduled_decision_support_dry_run,
    write_scheduled_dry_run_report,
)


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _write_ready_artifacts(root: Path) -> dict[str, Path]:
    backtest = root / "reports/backtests/historical-entry-exit-backtest.json"
    oos = root / "reports/backtests/out-of-sample-validation.json"
    paper_live = root / "reports/paper-live/paper-live-observation.json"
    portfolio = root / "data/portfolio_state.json"
    _write_json(backtest, {"metrics": {"total": 8, "expectancy_r": 0.1}})
    _write_json(oos, {"out_of_sample_count": 3, "out_of_sample_metrics": {"expectancy_r": 0.05}})
    _write_json(paper_live, {"ready_for_review": True, "terminal_event_count": 2})
    _write_json(portfolio, {"drawdown_percent": 0.0, "daily_loss_percent": 0.0})
    return {"backtest": backtest, "oos": oos, "paper_live": paper_live, "portfolio": portfolio}


def test_scheduled_decision_support_dry_run_passes_with_ready_artifacts(tmp_path: Path) -> None:
    paths = _write_ready_artifacts(tmp_path)

    report = run_scheduled_decision_support_dry_run(
        run_mode="manual",
        backtest_report=paths["backtest"],
        oos_report=paths["oos"],
        paper_live_report=paths["paper_live"],
        portfolio_state=paths["portfolio"],
    )

    assert report.run_mode == "manual"
    assert report.ready_for_live_decision_support_review is True
    assert report.readiness_report.ready_for_live_decision_support_review is True
    assert report.input_paths["backtest_report"] == str(paths["backtest"])


def test_scheduled_decision_support_dry_run_fails_when_artifacts_missing(tmp_path: Path) -> None:
    report = run_scheduled_decision_support_dry_run(
        run_mode="scheduled",
        backtest_report=tmp_path / "missing-backtest.json",
        oos_report=tmp_path / "missing-oos.json",
        paper_live_report=tmp_path / "missing-paper.json",
        portfolio_state=tmp_path / "missing-portfolio.json",
    )

    assert report.run_mode == "scheduled"
    assert report.ready_for_live_decision_support_review is False
    failed = {gate.name for gate in report.readiness_report.gates if not gate.passed}
    assert "historical_backtest_report_present" in failed
    assert "out_of_sample_report_present" in failed
    assert "paper_live_report_present" in failed
    assert "portfolio_state_present" in failed


def test_write_scheduled_dry_run_report_outputs_json_and_markdown(tmp_path: Path) -> None:
    paths = _write_ready_artifacts(tmp_path)
    report = run_scheduled_decision_support_dry_run(
        run_mode="manual",
        backtest_report=paths["backtest"],
        oos_report=paths["oos"],
        paper_live_report=paths["paper_live"],
        portfolio_state=paths["portfolio"],
    )

    json_path = tmp_path / "reports/scheduled-runs/report.json"
    markdown_path = tmp_path / "reports/scheduled-runs/report.md"
    write_scheduled_dry_run_report(report, json_path=json_path, markdown_path=markdown_path)

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["run_mode"] == "manual"
    assert payload["ready_for_live_decision_support_review"] is True
    markdown = markdown_path.read_text(encoding="utf-8")
    assert "Scheduled Live Decision-Support Dry Run" in markdown
    assert "Readiness Gates" in markdown
    assert "No broker execution" in render_scheduled_dry_run_markdown(report)
