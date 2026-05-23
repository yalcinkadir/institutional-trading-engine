from __future__ import annotations

import json
from pathlib import Path

from src.operations.operational_readiness_review import (
    render_operational_readiness_markdown,
    run_operational_readiness_review,
    write_operational_readiness_report,
)


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _write_ready_artifacts(root: Path) -> dict[str, Path]:
    backtest = root / "reports/backtests/historical-entry-exit-backtest.json"
    oos = root / "reports/backtests/out-of-sample-validation.json"
    paper_live = root / "reports/paper-live/paper-live-observation.json"
    portfolio = root / "data/portfolio_state.json"

    _write_json(
        backtest,
        {
            "metrics": {
                "total": 12,
                "expectancy_r": 0.42,
            }
        },
    )
    _write_json(
        oos,
        {
            "out_of_sample_count": 4,
            "out_of_sample_metrics": {
                "expectancy_r": 0.25,
            },
        },
    )
    _write_json(
        paper_live,
        {
            "ready_for_review": True,
            "terminal_event_count": 3,
        },
    )
    _write_json(
        portfolio,
        {
            "equity_start": 100000.0,
            "equity_current": 100000.0,
            "drawdown_percent": 0.0,
            "daily_loss_percent": 0.0,
        },
    )
    return {
        "backtest": backtest,
        "oos": oos,
        "paper_live": paper_live,
        "portfolio": portfolio,
    }


def test_operational_readiness_review_passes_with_all_artifacts(tmp_path: Path) -> None:
    paths = _write_ready_artifacts(tmp_path)

    report = run_operational_readiness_review(
        backtest_report=paths["backtest"],
        oos_report=paths["oos"],
        paper_live_report=paths["paper_live"],
        portfolio_state=paths["portfolio"],
    )

    assert report.ready_for_live_decision_support_review is True
    assert all(gate.passed for gate in report.gates)
    assert report.summary["backtest_total"] == 12
    assert report.summary["out_of_sample_count"] == 4
    assert report.summary["paper_live_ready_for_review"] is True
    assert report.summary["portfolio_drawdown_percent"] == 0.0


def test_operational_readiness_review_fails_when_artifacts_missing(tmp_path: Path) -> None:
    report = run_operational_readiness_review(
        backtest_report=tmp_path / "missing-backtest.json",
        oos_report=tmp_path / "missing-oos.json",
        paper_live_report=tmp_path / "missing-paper.json",
        portfolio_state=tmp_path / "missing-portfolio.json",
    )

    assert report.ready_for_live_decision_support_review is False
    failed = {gate.name for gate in report.gates if not gate.passed}
    assert "historical_backtest_report_present" in failed
    assert "out_of_sample_report_present" in failed
    assert "paper_live_report_present" in failed
    assert "portfolio_state_present" in failed
    assert "portfolio_drawdown_available" in failed


def test_operational_readiness_review_fails_when_counts_are_too_low(tmp_path: Path) -> None:
    paths = _write_ready_artifacts(tmp_path)

    report = run_operational_readiness_review(
        backtest_report=paths["backtest"],
        oos_report=paths["oos"],
        paper_live_report=paths["paper_live"],
        portfolio_state=paths["portfolio"],
        min_backtest_plans=20,
        min_oos_plans=10,
    )

    assert report.ready_for_live_decision_support_review is False
    failed = {gate.name for gate in report.gates if not gate.passed}
    assert "historical_backtest_has_plans" in failed
    assert "out_of_sample_has_plans" in failed


def test_write_operational_readiness_report_outputs_json_and_markdown(tmp_path: Path) -> None:
    paths = _write_ready_artifacts(tmp_path)
    report = run_operational_readiness_review(
        backtest_report=paths["backtest"],
        oos_report=paths["oos"],
        paper_live_report=paths["paper_live"],
        portfolio_state=paths["portfolio"],
    )

    json_path = tmp_path / "reports/readiness/review.json"
    markdown_path = tmp_path / "reports/readiness/review.md"
    write_operational_readiness_report(report, json_path=json_path, markdown_path=markdown_path)

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["ready_for_live_decision_support_review"] is True
    markdown = markdown_path.read_text(encoding="utf-8")
    assert "Operational Readiness Review" in markdown
    assert "historical_backtest_report_present" in markdown
    assert "Broker execution remains out of scope" in render_operational_readiness_markdown(report)
