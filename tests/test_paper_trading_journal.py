import json

import pytest

from src.validation.paper_trading_journal import (
    PaperTradingJournalConfig,
    analyze_observation,
    analyze_paper_trading_journal,
    render_paper_trading_journal_markdown,
    write_paper_trading_journal_report,
)


def test_analyze_observation_calculates_slippage_in_r() -> None:
    observation = {
        "observation_id": "obs-1",
        "symbol": "SPY",
        "observation_date": "2024-01-03",
        "theoretical_entry": 100.0,
        "paper_fill_price": 100.5,
        "stop_loss": 98.0,
        "expected_result_r": 1.0,
        "outcome_5d_r": 0.5,
        "outcome_20d_r": 1.2,
    }

    report = analyze_paper_trading_journal([observation])
    analysis = report.observations[0]

    assert analysis.fill_available is True
    assert analysis.slippage_r == pytest.approx(0.25)
    assert analysis.fill_deviation_pct == pytest.approx(0.005)
    assert analysis.model_deviation_5d_r == pytest.approx(-0.5)
    assert analysis.model_deviation_20d_r == pytest.approx(0.2)


def test_execution_deviation_flag_uses_config_thresholds() -> None:
    report = analyze_paper_trading_journal(
        [
            {
                "observation_id": "obs-2",
                "symbol": "QQQ",
                "date": "2024-01-04",
                "entry_trigger": 100.0,
                "actual_fill_price": 101.0,
                "stop_loss": 98.0,
            }
        ],
        config=PaperTradingJournalConfig(
            max_acceptable_slippage_r=0.25,
            max_acceptable_fill_deviation_pct=0.0025,
        ),
    )

    assert report.execution_deviation_count == 1
    assert report.observations[0].has_execution_deviation is True


def test_model_deviation_flag_when_outcome_differs_by_one_r_or_more() -> None:
    report = analyze_paper_trading_journal(
        [
            {
                "observation_id": "obs-3",
                "symbol": "IWM",
                "observation_date": "2024-01-05",
                "theoretical_entry": 50.0,
                "paper_fill_price": 50.0,
                "stop_loss": 49.0,
                "expected_result_r": 1.0,
                "outcome_5d_r": -0.5,
            }
        ]
    )

    assert report.model_deviation_count == 1
    assert report.observations[0].has_model_deviation is True


def test_psychology_deviation_detects_manual_protocol_breaks() -> None:
    report = analyze_paper_trading_journal(
        [
            {
                "observation_id": "obs-4",
                "symbol": "DIA",
                "observation_date": "2024-01-08",
                "theoretical_entry": 100.0,
                "paper_fill_price": 100.0,
                "stop_loss": 99.0,
                "would_have_held": False,
                "impulse_to_deviate": True,
            }
        ]
    )

    assert report.psychology_deviation_count == 1
    assert report.observations[0].has_psychology_deviation is True


def test_missing_fill_price_adds_warning() -> None:
    report = analyze_paper_trading_journal(
        [
            {
                "observation_id": "obs-5",
                "symbol": "SPY",
                "observation_date": "2024-01-09",
                "theoretical_entry": 100.0,
                "stop_loss": 98.0,
            }
        ]
    )

    assert report.filled_count == 0
    assert "missing_paper_fill_price" in report.observations[0].warnings


def test_weekly_summary_groups_observations_by_week_start() -> None:
    report = analyze_paper_trading_journal(
        [
            {
                "observation_id": "obs-6",
                "symbol": "SPY",
                "observation_date": "2024-01-08",
                "theoretical_entry": 100.0,
                "paper_fill_price": 100.0,
                "stop_loss": 98.0,
                "outcome_5d_r": 1.0,
            },
            {
                "observation_id": "obs-7",
                "symbol": "QQQ",
                "observation_date": "2024-01-10",
                "theoretical_entry": 100.0,
                "paper_fill_price": 100.5,
                "stop_loss": 98.0,
                "outcome_5d_r": 0.0,
            },
        ]
    )

    assert len(report.weekly_summaries) == 1
    assert report.weekly_summaries[0].week_start == "2024-01-08"
    assert report.weekly_summaries[0].observation_count == 2
    assert report.weekly_summaries[0].average_5d_r == pytest.approx(0.5)


def test_render_markdown_contains_summary_tables() -> None:
    report = analyze_paper_trading_journal(
        [
            {
                "observation_id": "obs-8",
                "symbol": "SPY",
                "observation_date": "2024-01-08",
                "theoretical_entry": 100.0,
                "paper_fill_price": 100.0,
                "stop_loss": 98.0,
            }
        ]
    )

    markdown = render_paper_trading_journal_markdown(report)

    assert "# Paper Trading Journal / Live Observation v2" in markdown
    assert "Weekly Summary" in markdown
    assert "Observation Details" in markdown


def test_write_paper_trading_journal_report(tmp_path) -> None:
    report = analyze_paper_trading_journal(
        [
            {
                "observation_id": "obs-9",
                "symbol": "SPY",
                "observation_date": "2024-01-08",
                "theoretical_entry": 100.0,
                "paper_fill_price": 100.0,
                "stop_loss": 98.0,
            }
        ]
    )
    json_path = tmp_path / "paper-journal.json"
    markdown_path = tmp_path / "paper-journal.md"

    write_paper_trading_journal_report(report, json_path=json_path, markdown_path=markdown_path)

    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert data["observation_count"] == 1
    assert markdown_path.read_text(encoding="utf-8").startswith("# Paper Trading Journal")
