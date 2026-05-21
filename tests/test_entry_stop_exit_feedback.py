from __future__ import annotations

from src.feedback.entry_stop_exit_feedback import (
    REGIME_AWARE_GROUP_FIELDS,
    aggregate_entry_stop_exit_feedback,
    aggregate_regime_aware_entry_stop_exit_feedback,
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
            "market_regime": "bullish",
            "risk_state": "risk_on",
            "volatility_regime": "low_vol",
            "outcome": "TARGET_2_HIT",
        },
        {
            "symbol": "MSFT",
            "setup_type": "momentum_breakout",
            "entry_type": "breakout",
            "stop_model": "atr_stop",
            "exit_model": "momentum_targets",
            "market_regime": "bullish",
            "risk_state": "risk_on",
            "volatility_regime": "normal_vol",
            "outcome": "STOP_HIT",
        },
        {
            "symbol": "AAPL",
            "setup_type": "pullback_continuation",
            "entry_type": "pullback",
            "stop_model": "pullback_structure_stop",
            "exit_model": "pullback_targets",
            "market_regime": "neutral",
            "risk_state": "cautious",
            "volatility_regime": "normal_vol",
            "outcome": "TARGET_1_HIT",
        },
        {
            "symbol": "AMD",
            "setup_type": "momentum_breakout",
            "entry_type": "breakout",
            "stop_model": "atr_stop",
            "exit_model": "momentum_targets",
            "market_regime": "risk_off",
            "risk_state": "defensive",
            "volatility_regime": "high_vol",
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


def test_default_grouping_remains_backward_compatible() -> None:
    report = aggregate_entry_stop_exit_feedback(_records())

    assert set(report.grouped) == {
        "entry_type",
        "setup_type",
        "stop_model",
        "exit_model",
    }


def test_regime_aware_group_fields_constant_includes_model_and_regime_dimensions() -> None:
    assert REGIME_AWARE_GROUP_FIELDS == (
        "entry_type",
        "setup_type",
        "stop_model",
        "exit_model",
        "market_regime",
        "risk_state",
        "volatility_regime",
    )


def test_regime_aware_feedback_groups_by_market_regime() -> None:
    report = aggregate_regime_aware_entry_stop_exit_feedback(_records())

    by_regime = {item.group_value: item for item in report.grouped["market_regime"]}

    assert by_regime["bullish"].total == 2
    assert by_regime["bullish"].entry_hits == 2
    assert by_regime["bullish"].stop_hits == 1
    assert by_regime["risk_off"].total == 1
    assert by_regime["risk_off"].expired_without_entry == 1


def test_regime_aware_feedback_groups_by_risk_state() -> None:
    report = aggregate_regime_aware_entry_stop_exit_feedback(_records())

    by_risk_state = {item.group_value: item for item in report.grouped["risk_state"]}

    assert by_risk_state["risk_on"].total == 2
    assert by_risk_state["cautious"].target_1_hits == 1
    assert by_risk_state["defensive"].expired_without_entry == 1


def test_regime_aware_feedback_groups_by_volatility_regime() -> None:
    report = aggregate_regime_aware_entry_stop_exit_feedback(_records())

    by_vol = {item.group_value: item for item in report.grouped["volatility_regime"]}

    assert by_vol["normal_vol"].total == 2
    assert by_vol["low_vol"].target_2_hits == 1
    assert by_vol["high_vol"].expired_without_entry == 1


def test_regime_aware_feedback_handles_missing_regime_fields_as_unknown() -> None:
    report = aggregate_regime_aware_entry_stop_exit_feedback([
        {"entry_type": "breakout", "outcome": "TARGET_1_HIT"},
        {"entry_type": "breakout", "outcome": "EXPIRED"},
    ])

    assert report.grouped["market_regime"][0].group_value == "unknown"
    assert report.grouped["market_regime"][0].total == 2
    assert report.grouped["risk_state"][0].group_value == "unknown"
    assert report.grouped["volatility_regime"][0].group_value == "unknown"


def test_custom_group_fields_can_request_only_regime_dimensions() -> None:
    report = aggregate_entry_stop_exit_feedback(
        _records(),
        group_fields=("market_regime", "risk_state"),
    )

    assert set(report.grouped) == {"market_regime", "risk_state"}
    assert {item.group_value for item in report.grouped["market_regime"]} == {
        "bullish",
        "neutral",
        "risk_off",
    }


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
    report = aggregate_regime_aware_entry_stop_exit_feedback(_records())
    markdown = format_entry_stop_exit_feedback_markdown(report)

    assert "# Entry / Stop / Exit Feedback" in markdown
    assert "Total records: **4**" in markdown
    assert "## By entry_type" in markdown
    assert "## By market_regime" in markdown
    assert "**breakout**" in markdown
    assert "**bullish**" in markdown
    assert "false breakout 25.0%" in markdown
