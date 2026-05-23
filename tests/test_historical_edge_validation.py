import json

import pytest

from src.validation.historical_edge_validation import (
    HistoricalEdgeValidationConfig,
    calculate_max_consecutive_losses,
    calculate_max_drawdown,
    calculate_profit_factor,
    calculate_recovery_time_trades,
    calculate_sharpe_ratio,
    render_historical_edge_markdown,
    validate_historical_edge,
    write_historical_edge_report,
)


def test_positive_edge_passes_with_custom_thresholds() -> None:
    records = [{"result_r": 1.0}] * 8 + [{"result_r": -0.5}] * 2
    config = HistoricalEdgeValidationConfig(
        min_total_trades=10,
        min_expectancy_r=0.5,
        min_profit_factor=1.4,
        max_drawdown_limit=0.5,
        min_sharpe_ratio=0.1,
    )

    report = validate_historical_edge(records, config=config)

    assert report.passed is True
    assert report.metrics.total_trades == 10
    assert report.metrics.win_rate == pytest.approx(0.8)
    assert report.metrics.expectancy_r == pytest.approx(0.7)
    assert report.metrics.profit_factor == pytest.approx(8.0)


def test_insufficient_sample_size_fails() -> None:
    records = [{"result_r": 1.0}] * 5
    config = HistoricalEdgeValidationConfig(min_total_trades=10)

    report = validate_historical_edge(records, config=config)

    sample_gate = next(gate for gate in report.gates if gate.name == "minimum_sample_size")
    assert report.passed is False
    assert sample_gate.passed is False
    assert sample_gate.value == 5


def test_negative_expectancy_and_low_profit_factor_fail() -> None:
    records = [{"result_r": 0.5}] * 4 + [{"result_r": -1.0}] * 6
    config = HistoricalEdgeValidationConfig(
        min_total_trades=10,
        min_expectancy_r=0.1,
        min_profit_factor=1.1,
        max_drawdown_limit=1.0,
        min_sharpe_ratio=-10,
    )

    report = validate_historical_edge(records, config=config)

    expectancy_gate = next(gate for gate in report.gates if gate.name == "positive_expectancy")
    profit_gate = next(gate for gate in report.gates if gate.name == "profit_factor")
    assert expectancy_gate.passed is False
    assert profit_gate.passed is False
    assert report.metrics.expectancy_r < 0
    assert report.metrics.profit_factor < 1.1


def test_profit_factor_handles_no_losses() -> None:
    assert calculate_profit_factor([1.0, 2.0, 0.5]) == float("inf")
    assert calculate_profit_factor([-1.0, -0.5]) == 0.0


def test_drawdown_and_recovery_metrics() -> None:
    values = [2.0, -1.0, -1.0, 1.0, 2.0]

    assert calculate_max_drawdown(values) == pytest.approx(2.0)
    assert calculate_max_consecutive_losses(values) == 2
    assert calculate_recovery_time_trades(values) == 3


def test_sharpe_ratio_returns_zero_for_insufficient_or_constant_data() -> None:
    assert calculate_sharpe_ratio([1.0]) == 0.0
    assert calculate_sharpe_ratio([1.0, 1.0, 1.0]) == 0.0


def test_extracts_r_multiple_fallback() -> None:
    records = [{"r_multiple": 1.5}, {"result_r": -0.5}, {"result_r": "invalid"}]
    config = HistoricalEdgeValidationConfig(
        min_total_trades=2,
        min_expectancy_r=0.0,
        min_profit_factor=1.0,
        max_drawdown_limit=1.0,
        min_sharpe_ratio=-10,
    )

    report = validate_historical_edge(records, config=config)

    assert report.metrics.total_trades == 2
    assert report.metrics.cumulative_r == pytest.approx(1.0)


def test_render_markdown_contains_status_and_metrics() -> None:
    report = validate_historical_edge(
        [{"result_r": 1.0}, {"result_r": -0.5}],
        config=HistoricalEdgeValidationConfig(
            min_total_trades=2,
            min_expectancy_r=0.0,
            min_profit_factor=1.0,
            max_drawdown_limit=1.0,
            min_sharpe_ratio=-10,
        ),
    )

    markdown = render_historical_edge_markdown(report)

    assert "# Historical Edge Validation" in markdown
    assert "Total trades" in markdown
    assert "profit_factor" in markdown


def test_write_historical_edge_report(tmp_path) -> None:
    report = validate_historical_edge(
        [{"result_r": 1.0}, {"result_r": -0.5}],
        config=HistoricalEdgeValidationConfig(
            min_total_trades=2,
            min_expectancy_r=0.0,
            min_profit_factor=1.0,
            max_drawdown_limit=1.0,
            min_sharpe_ratio=-10,
        ),
    )
    json_path = tmp_path / "edge.json"
    markdown_path = tmp_path / "edge.md"

    write_historical_edge_report(report, json_path=json_path, markdown_path=markdown_path)

    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert data["metrics"]["total_trades"] == 2
    assert markdown_path.read_text(encoding="utf-8").startswith("# Historical Edge Validation")
