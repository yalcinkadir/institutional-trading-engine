import json
from datetime import date

import pytest

from src.validation.historical_edge_validation import HistoricalEdgeValidationConfig
from src.validation.walk_forward_validation import (
    WalkForwardConfig,
    build_walk_forward_validation,
    generate_walk_forward_cycles,
    render_walk_forward_markdown,
    write_walk_forward_report,
)


def _records_for_months(start_year: int, start_month: int, months: int, result_r: float = 1.0) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    year = start_year
    month = start_month
    for _ in range(months):
        records.append({"exit_date": f"{year:04d}-{month:02d}-15", "result_r": result_r})
        month += 1
        if month > 12:
            month = 1
            year += 1
    return records


def test_generate_walk_forward_cycles_uses_default_window_structure() -> None:
    cycles = generate_walk_forward_cycles(
        start_date=date(2019, 1, 1),
        end_date=date(2023, 12, 31),
    )

    assert len(cycles) >= 6
    assert cycles[0].training_start == date(2019, 1, 1)
    assert cycles[0].training_end == date(2020, 6, 30)
    assert cycles[0].test_start == date(2020, 7, 1)
    assert cycles[0].test_end == date(2020, 12, 31)
    assert cycles[1].training_start == date(2019, 4, 1)


def test_generate_walk_forward_cycles_rejects_invalid_config() -> None:
    with pytest.raises(ValueError):
        generate_walk_forward_cycles(
            start_date=date(2020, 1, 1),
            end_date=date(2021, 1, 1),
            training_months=0,
        )


def test_walk_forward_validation_passes_when_required_cycles_pass() -> None:
    records = _records_for_months(2019, 1, 60, result_r=1.0)
    config = WalkForwardConfig(
        min_cycles=6,
        edge_config=HistoricalEdgeValidationConfig(
            min_total_trades=1,
            min_expectancy_r=0.1,
            min_profit_factor=0.0,
            max_drawdown_limit=10,
            min_sharpe_ratio=0.0,
        ),
    )

    report = build_walk_forward_validation(records, config=config, min_required_passing_cycles=6)

    assert report.passed is True
    assert report.generated_cycles >= 6
    assert report.passing_cycles >= 6
    assert report.unassigned_records == 0


def test_walk_forward_validation_fails_with_insufficient_cycles() -> None:
    records = _records_for_months(2022, 1, 20, result_r=1.0)
    config = WalkForwardConfig(
        min_cycles=6,
        edge_config=HistoricalEdgeValidationConfig(
            min_total_trades=1,
            min_expectancy_r=0.1,
            min_profit_factor=0.0,
            max_drawdown_limit=10,
            min_sharpe_ratio=0.0,
        ),
    )

    report = build_walk_forward_validation(records, config=config)

    assert report.passed is False
    assert report.generated_cycles < 6


def test_walk_forward_validation_assigns_training_and_test_records() -> None:
    records = _records_for_months(2019, 1, 30, result_r=1.0)
    config = WalkForwardConfig(
        training_months=3,
        test_months=2,
        step_months=2,
        min_cycles=1,
        edge_config=HistoricalEdgeValidationConfig(
            min_total_trades=1,
            min_expectancy_r=-10,
            min_profit_factor=0.0,
            max_drawdown_limit=10,
            min_sharpe_ratio=-10,
        ),
    )

    report = build_walk_forward_validation(records, config=config, min_required_passing_cycles=1)
    first_cycle = report.cycle_results[0]

    assert first_cycle.training_records == 3
    assert first_cycle.test_records == 2
    assert first_cycle.passed is True


def test_walk_forward_validation_counts_unassigned_records() -> None:
    records = [{"exit_date": "invalid", "result_r": 1.0}, {"result_r": 1.0}]

    report = build_walk_forward_validation(records)

    assert report.passed is False
    assert report.generated_cycles == 0
    assert report.unassigned_records == 2


def test_fallback_date_field_is_supported() -> None:
    records = [{"signal_date": "2019-01-15", "r_multiple": 1.0}] + _records_for_months(2019, 2, 30, result_r=1.0)
    config = WalkForwardConfig(
        training_months=3,
        test_months=2,
        step_months=2,
        min_cycles=1,
        edge_config=HistoricalEdgeValidationConfig(
            min_total_trades=1,
            min_expectancy_r=-10,
            min_profit_factor=0.0,
            max_drawdown_limit=10,
            min_sharpe_ratio=-10,
        ),
    )

    report = build_walk_forward_validation(records, config=config, result_field="result_r", min_required_passing_cycles=1)

    assert report.unassigned_records == 0
    assert report.generated_cycles >= 1


def test_render_walk_forward_markdown_contains_cycle_table() -> None:
    records = _records_for_months(2019, 1, 30, result_r=1.0)
    config = WalkForwardConfig(
        training_months=3,
        test_months=2,
        step_months=2,
        min_cycles=1,
        edge_config=HistoricalEdgeValidationConfig(
            min_total_trades=1,
            min_expectancy_r=-10,
            min_profit_factor=0.0,
            max_drawdown_limit=10,
            min_sharpe_ratio=-10,
        ),
    )
    report = build_walk_forward_validation(records, config=config, min_required_passing_cycles=1)

    markdown = render_walk_forward_markdown(report)

    assert "# Walk-Forward Validation" in markdown
    assert "Generated cycles" in markdown
    assert "Train Window" in markdown


def test_write_walk_forward_report(tmp_path) -> None:
    records = _records_for_months(2019, 1, 30, result_r=1.0)
    config = WalkForwardConfig(
        training_months=3,
        test_months=2,
        step_months=2,
        min_cycles=1,
        edge_config=HistoricalEdgeValidationConfig(
            min_total_trades=1,
            min_expectancy_r=-10,
            min_profit_factor=0.0,
            max_drawdown_limit=10,
            min_sharpe_ratio=-10,
        ),
    )
    report = build_walk_forward_validation(records, config=config, min_required_passing_cycles=1)
    json_path = tmp_path / "walk-forward.json"
    markdown_path = tmp_path / "walk-forward.md"

    write_walk_forward_report(report, json_path=json_path, markdown_path=markdown_path)

    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert data["generated_cycles"] >= 1
    assert markdown_path.read_text(encoding="utf-8").startswith("# Walk-Forward Validation")
