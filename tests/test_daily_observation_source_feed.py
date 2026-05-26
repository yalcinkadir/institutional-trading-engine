import json
import subprocess
import sys
from pathlib import Path

from src.validation.daily_observation_source_feed import persist_daily_observation_sources
from src.validation.daily_evidence_input_builder import build_daily_evidence_inputs
from src.validation.daily_evidence_input_validation import validate_daily_evidence_inputs


SCRIPT = Path("scripts/persist_daily_observation_sources.py")


def _write_incoming_files(incoming_dir: Path):
    incoming_dir.mkdir(parents=True, exist_ok=True)
    (incoming_dir / "paper_observations.json").write_text(
        json.dumps(
            [
                {
                    "observation_date": "2026-05-26",
                    "expected_action": "ENTER",
                    "paper_action": "ENTER",
                    "expected_result_r": 0.3,
                    "paper_result_r": 0.3,
                    "resolved": True,
                }
            ]
        ),
        encoding="utf-8",
    )
    (incoming_dir / "backtest_results.json").write_text(json.dumps([{"result_r": 0.2}]), encoding="utf-8")
    (incoming_dir / "forward_results.json").write_text(json.dumps([{"result_r": 0.25}]), encoding="utf-8")
    (incoming_dir / "regime_observations.json").write_text(
        json.dumps([{"regime_label": "neutral", "volatility_pct": 0.18, "corr": 0.42, "drawdown_pct": 0.02}]),
        encoding="utf-8",
    )
    (incoming_dir / "position_snapshots.json").write_text(
        json.dumps(
            [
                {
                    "symbol": "AAPL",
                    "sector": "Technology",
                    "portfolio_weight": 1.0,
                    "paper_r": 0.2,
                    "beta": 1.1,
                    "market_r": 0.1,
                    "factor_exposures": {"momentum": 0.5},
                    "factor_returns": {"momentum": 0.2},
                }
            ]
        ),
        encoding="utf-8",
    )


def test_persist_daily_observation_sources_writes_feed_files(tmp_path: Path):
    incoming_dir = tmp_path / "incoming"
    feed_dir = tmp_path / "feed"
    _write_incoming_files(incoming_dir)

    report = persist_daily_observation_sources(incoming_dir, feed_dir, report_date="2026-05-26")

    assert report.passed is True
    assert len(report.files) == 5
    assert (feed_dir / "paper_observations.json").exists()
    persisted = json.loads((feed_dir / "paper_observations.json").read_text(encoding="utf-8"))
    assert persisted[0]["source"] == "daily_observation_source_feed"
    assert persisted[0]["feed_report_date"] == "2026-05-26"


def test_persist_daily_observation_sources_is_idempotent(tmp_path: Path):
    incoming_dir = tmp_path / "incoming"
    feed_dir = tmp_path / "feed"
    _write_incoming_files(incoming_dir)

    first = persist_daily_observation_sources(incoming_dir, feed_dir, report_date="2026-05-26")
    second = persist_daily_observation_sources(incoming_dir, feed_dir, report_date="2026-05-26")

    assert first.passed is True
    assert second.passed is True
    assert all(item.appended_records == 0 for item in second.files)


def test_persisted_feed_can_feed_builder_and_validator(tmp_path: Path):
    incoming_dir = tmp_path / "incoming"
    feed_dir = tmp_path / "feed"
    input_dir = tmp_path / "inputs"
    _write_incoming_files(incoming_dir)

    persist_report = persist_daily_observation_sources(incoming_dir, feed_dir, report_date="2026-05-26")
    build_report = build_daily_evidence_inputs(feed_dir, input_dir)
    validation_report = validate_daily_evidence_inputs(input_dir)

    assert persist_report.passed is True
    assert build_report.passed is True
    assert validation_report.passed is True


def test_persist_daily_observation_sources_fails_when_incoming_file_missing(tmp_path: Path):
    incoming_dir = tmp_path / "incoming"
    feed_dir = tmp_path / "feed"
    _write_incoming_files(incoming_dir)
    (incoming_dir / "forward_results.json").unlink()

    report = persist_daily_observation_sources(incoming_dir, feed_dir, report_date="2026-05-26")

    assert report.passed is False
    assert any("missing incoming source file: forward_results.json" in error for error in report.errors)


def test_persist_daily_observation_sources_cli_writes_reports(tmp_path: Path):
    incoming_dir = tmp_path / "incoming"
    feed_dir = tmp_path / "feed"
    report_dir = tmp_path / "reports"
    _write_incoming_files(incoming_dir)

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--incoming-dir",
            str(incoming_dir),
            "--feed-dir",
            str(feed_dir),
            "--report-dir",
            str(report_dir),
            "--report-date",
            "2026-05-26",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Daily observation source feed status: PASS" in result.stdout
    assert (report_dir / "daily_observation_source_feed.json").exists()
    assert (report_dir / "daily_observation_source_feed.md").exists()
