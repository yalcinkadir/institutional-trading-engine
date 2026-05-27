import json
import subprocess
import sys
from pathlib import Path

from src.validation.daily_evidence_input_builder import build_daily_evidence_inputs
from src.validation.daily_evidence_input_validation import validate_daily_evidence_inputs
from src.validation.daily_paper_observation_source import build_daily_paper_observation_sources


SCRIPT = Path("scripts/build_daily_paper_observation_sources.py")


def _write_real_sources(source_dir: Path) -> None:
    source_dir.mkdir(parents=True, exist_ok=True)
    paper = [
        {
            "observation_date": "2026-05-25",
            "expected_action": "enter",
            "paper_action": "enter",
            "expected_r": 0.4,
            "paper_r": 0.35,
            "resolved": True,
            "source": "paper_reconciliation_log",
        },
        {
            "observation_date": "2026-05-26",
            "expected_action": "skip",
            "paper_action": "skip",
            "expected_r": 0.0,
            "paper_r": 0.0,
            "resolved": True,
            "source": "paper_reconciliation_log",
        },
    ]
    backtest = [{"result_r": 0.2 + (index % 3) * 0.05, "source": "lockbox_baseline"} for index in range(30)]
    regime = [
        {
            "date": f"2026-05-{day:02d}",
            "regime_label": "neutral",
            "volatility_pct": 0.18,
            "corr": 0.42,
            "drawdown_pct": 0.02,
            "source": "market_regime_snapshot",
        }
        for day in range(1, 22)
    ]
    positions = [
        {
            "symbol": "AAPL",
            "sector": "Technology",
            "portfolio_weight": 0.5,
            "paper_r": 0.3,
            "beta": 1.1,
            "market_r": 0.1,
            "factor_exposures": {"momentum": 0.4},
            "factor_returns": {"momentum": 0.2},
            "source": "paper_position_snapshot",
        }
    ]
    (source_dir / "paper_observations.json").write_text(json.dumps(paper), encoding="utf-8")
    (source_dir / "backtest_results.json").write_text(json.dumps(backtest), encoding="utf-8")
    (source_dir / "regime_observations.json").write_text(json.dumps(regime), encoding="utf-8")
    (source_dir / "position_snapshots.json").write_text(json.dumps(positions), encoding="utf-8")


def test_build_daily_paper_observation_sources_writes_feed_compatible_sources(tmp_path: Path):
    raw_dir = tmp_path / "raw"
    source_dir = tmp_path / "incoming"
    _write_real_sources(raw_dir)

    report = build_daily_paper_observation_sources(raw_dir, source_dir)

    assert report.passed is True
    assert len(report.files) == 5
    assert (source_dir / "paper_observations.json").exists()
    assert (source_dir / "forward_results.json").exists()

    forward = json.loads((source_dir / "forward_results.json").read_text(encoding="utf-8"))
    assert forward[0]["result_r"] == 0.35
    assert all(record["source"] == "daily_paper_observation_source" for record in forward)


def test_real_paper_sources_feed_builder_and_validator(tmp_path: Path):
    raw_dir = tmp_path / "raw"
    source_dir = tmp_path / "incoming"
    input_dir = tmp_path / "inputs"
    _write_real_sources(raw_dir)

    source_report = build_daily_paper_observation_sources(raw_dir, source_dir)
    build_report = build_daily_evidence_inputs(source_dir, input_dir)
    validation_report = validate_daily_evidence_inputs(input_dir)

    assert source_report.passed is True
    assert build_report.passed is True
    assert validation_report.passed is True


def test_bootstrap_source_is_rejected(tmp_path: Path):
    raw_dir = tmp_path / "raw"
    source_dir = tmp_path / "incoming"
    _write_real_sources(raw_dir)
    paper = json.loads((raw_dir / "paper_observations.json").read_text(encoding="utf-8"))
    paper[0]["source"] = "observation_only_bootstrap"
    (raw_dir / "paper_observations.json").write_text(json.dumps(paper), encoding="utf-8")

    report = build_daily_paper_observation_sources(raw_dir, source_dir)

    assert report.passed is False
    assert "prohibited bootstrap source" in report.errors[0]


def test_cli_writes_reports(tmp_path: Path):
    raw_dir = tmp_path / "raw"
    source_dir = tmp_path / "incoming"
    report_dir = tmp_path / "reports"
    _write_real_sources(raw_dir)

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--source-dir",
            str(raw_dir),
            "--output-dir",
            str(source_dir),
            "--report-dir",
            str(report_dir),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Daily paper observation source status: PASS" in result.stdout
    assert (report_dir / "daily_paper_observation_source.json").exists()
    assert (report_dir / "daily_paper_observation_source.md").exists()
