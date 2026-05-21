from __future__ import annotations

from src.feedback.entry_stop_exit_feedback import (
    aggregate_entry_stop_exit_feedback,
    format_entry_stop_exit_feedback_markdown,
)


def _records() -> list[dict]:
    return [
        {
            "symbol": "NVDA",
            "setup_type": "momentum_breakout",
            "entry_type": "breakout",
            "stop_model": "swing_low_structure_stop",
            "exit_model": "momentum_targets",
            "outcome": "TARGET_2_HIT",
        },
        {
            "symbol": "MSFT",
            "setup_type": "momentum_breakout",
            "entry_type": "breakout",
            "stop_model": "atr_stop",
            "exit_model": "momentum_targets",
            "outcome": "STOP_HIT",
        },
        {
            "symbol": "AAPL",
            "setup_type": "pullback_continuation",
            "entry_type": "pullback",
            "stop_model": "pullback_structure_stop",
            "exit_model": "pullback_targets",
            "outcome": "TARGET_1_HIT",
        },
        {
            "symbol": "AMD",
            "setup_type": "momentum_breakout",
            "entry_type": "breakout",
            "stop_model": "atr_stop",
            "exit_model": "momentum_targets",
            "outcome": "EXPIRED",
        },
    ]


def test_aggregate_entry_stop_exit_feedback_overall_math() -> None:
    report = aggregate_entry_stop_exit_feedback(_records())

    overall = report.overall
    assert report.total_records == 4
    assert overall.total == 4
    assert overall.entry_hits == 3
    assert overall.stop_hits == 1
    assert overall.target_1_hits == 2
    assert overall.target_2_hits == 1
    assert overall.expired_without_entry == 1
    assert overall.false_breakouts == 1
    assert overall.entry_hit_rate == 0.75
    assert overall.stop_hit_rate == 0.25
    assert overall.target_1_hit_rate == 0.5
    assert overall.target_2_hit_rate == 0.25
    assert overall.expired_without_entry_rate == 0.25
    assert overall.false_breakout_rate == 0.25


def test_aggregate_entry_stop_exit_feedback_groups_by_entry_type() -> None:
    report = aggregate_entry_stop_exit_feedback(_records())

    by_entry = {item.group_value: item for item in report.grouped["entry_type"]}

    assert by_entry["breakout"].total == 3
    assert by_entry["breakout"].entry_hits == 2
    assert by_entry["breakout"].target_2_hits == 1
    assert by_entry["pullback"].total == 1
    assert by_entry["pullback"].target_1_hits == 1


def test_aggregate_entry_stop_exit_feedback_groups_by_models() -> None:
    report = aggregate_entry_stop_exit_feedback(_records())

    by_stop = {item.group_value: item for item in report.grouped["stop_model"]}
    by_exit = {item.group_value: item for item in report.grouped["exit_model"]}
    by_setup = {item.group_value: item for item in report.grouped["setup_type"]}

    assert by_stop["atr_stop"].total == 2
    assert by_stop["atr_stop"].stop_hits == 1
    assert by_stop["swing_low_structure_stop"].target_2_hits == 1
    assert by_exit["momentum_targets"].total == 3
    assert by_setup["momentum_breakout"].total == 3


def test_aggregate_entry_stop_exit_feedback_handles_empty_data() -> None:
    report = aggregate_entry_stop_exit_feedback([])

    assert report.total_records == 0
    assert report.overall.total == 0
    assert report.overall.entry_hit_rate == 0.0
    assert report.grouped == {
        "entry_type": [],
        "setup_type": [],
        "stop_model": [],
        "exit_model": [],
    }


def test_aggregate_entry_stop_exit_feedback_handles_missing_fields() -> None:
    report = aggregate_entry_stop_exit_feedback([
        {"outcome": "TARGET_1_HIT"},
        {"outcome": "EXPIRED"},
    ])

    by_entry = report.grouped["entry_type"]
    assert len(by_entry) == 1
    assert by_entry[0].group_value == "unknown"
    assert by_entry[0].total == 2
    assert by_entry[0].entry_hits == 1
    assert by_entry[0].expired_without_entry == 1


def test_false_breakout_can_be_explicit() -> None:
    report = aggregate_entry_stop_exit_feedback([
        {
            "entry_type": "breakout",
            "setup_type": "momentum_breakout",
            "stop_model": "atr_stop",
            "exit_model": "momentum_targets",
            "false_breakout": True,
        }
    ])

    assert report.overall.false_breakouts == 1
    assert report.overall.false_breakout_rate == 1.0


def test_boolean_fields_can_drive_aggregation_without_status() -> None:
    report = aggregate_entry_stop_exit_feedback([
        {
            "entry_type": "breakout",
            "entry_hit": True,
            "target_1_hit": True,
        }
    ])

    assert report.overall.entry_hits == 1
    assert report.overall.target_1_hits == 1
    assert report.overall.stop_hits == 0


def test_report_to_dict_is_serializable() -> None:
    report = aggregate_entry_stop_exit_feedback(_records())
    payload = report.to_dict()

    assert payload["total_records"] == 4
    assert payload["overall"]["entry_hit_rate"] == 0.75
    assert payload["grouped"]["entry_type"]


def test_format_entry_stop_exit_feedback_markdown() -> None:
    report = aggregate_entry_stop_exit_feedback(_records())
    markdown = format_entry_stop_exit_feedback_markdown(report)

    assert "# Entry / Stop / Exit Feedback" in markdown
    assert "Total records: **4**" in markdown
    assert "## By entry_type" in markdown
    assert "**breakout**" in markdown
    assert "false breakout 25.0%" in markdown
