import json

from src.validation.historical_edge_validation import HistoricalEdgeValidationConfig
from src.validation.regime_phase_backtest_matrix import (
    build_regime_phase_backtest_matrix,
    default_regime_phases,
    render_regime_phase_matrix_markdown,
    write_regime_phase_matrix_report,
)


def _winning_records(date_value: str, count: int) -> list[dict[str, object]]:
    return [{"exit_date": date_value, "result_r": 1.0} for _ in range(count)]


def _losing_records(date_value: str, count: int) -> list[dict[str, object]]:
    return [{"exit_date": date_value, "result_r": -1.0} for _ in range(count)]


def test_default_regime_phases_cover_required_market_periods() -> None:
    phases = default_regime_phases()

    assert [phase.name for phase in phases] == [
        "Low-Vol Bull",
        "Panic/Dislocation",
        "Recovery",
        "High-Vol Regime",
        "Neutral/Transition",
    ]
    assert phases[0].start_date.isoformat() == "2019-01-01"
    assert phases[-1].end_date.isoformat() == "2024-06-30"


def test_records_are_assigned_to_correct_phases() -> None:
    records = [
        {"exit_date": "2019-06-01", "result_r": 1.0},
        {"exit_date": "2020-03-15", "result_r": 1.0},
        {"exit_date": "2021-01-15", "result_r": 1.0},
        {"exit_date": "2022-06-01", "result_r": -1.0},
        {"exit_date": "2023-07-01", "result_r": 1.0},
    ]
    config = HistoricalEdgeValidationConfig(min_total_trades=1, min_expectancy_r=-10, min_profit_factor=0, max_drawdown_limit=10, min_sharpe_ratio=-10)

    report = build_regime_phase_backtest_matrix(records, config=config, required_passing_phases=1)

    assert [result.total_records for result in report.phase_results] == [1, 1, 1, 1, 1]
    assert report.unassigned_records == 0


def test_unassigned_records_are_counted() -> None:
    records = [
        {"exit_date": "2018-12-31", "result_r": 1.0},
        {"exit_date": "2024-07-01", "result_r": 1.0},
        {"exit_date": "invalid", "result_r": 1.0},
    ]

    report = build_regime_phase_backtest_matrix(records)

    assert report.unassigned_records == 3
    assert all(result.total_records == 0 for result in report.phase_results)


def test_matrix_passes_when_at_least_three_phases_pass() -> None:
    records = []
    records += _winning_records("2019-06-01", 3)
    records += _winning_records("2020-03-15", 3)
    records += _winning_records("2021-03-15", 3)
    records += _losing_records("2022-06-01", 3)
    records += _losing_records("2023-06-01", 3)
    config = HistoricalEdgeValidationConfig(
        min_total_trades=3,
        min_expectancy_r=0.5,
        min_profit_factor=1.0,
        max_drawdown_limit=10,
        min_sharpe_ratio=0.0,
    )

    report = build_regime_phase_backtest_matrix(records, config=config, required_passing_phases=3)

    assert report.passed is True
    assert report.passing_phases == 3
    assert report.total_phases == 5


def test_matrix_fails_when_fewer_than_three_phases_pass() -> None:
    records = []
    records += _winning_records("2019-06-01", 3)
    records += _winning_records("2020-03-15", 3)
    records += _losing_records("2021-03-15", 3)
    records += _losing_records("2022-06-01", 3)
    records += _losing_records("2023-06-01", 3)
    config = HistoricalEdgeValidationConfig(
        min_total_trades=3,
        min_expectancy_r=0.5,
        min_profit_factor=1.0,
        max_drawdown_limit=10,
        min_sharpe_ratio=0.0,
    )

    report = build_regime_phase_backtest_matrix(records, config=config, required_passing_phases=3)

    assert report.passed is False
    assert report.passing_phases == 2


def test_fallback_date_fields_are_supported() -> None:
    records = [{"signal_date": "2020-06-01", "r_multiple": 1.0}]
    config = HistoricalEdgeValidationConfig(min_total_trades=1, min_expectancy_r=-10, min_profit_factor=0, max_drawdown_limit=10, min_sharpe_ratio=-10)

    report = build_regime_phase_backtest_matrix(records, config=config, result_field="result_r", required_passing_phases=1)

    recovery_result = next(result for result in report.phase_results if result.phase.name == "Recovery")
    assert recovery_result.total_records == 1
    assert report.unassigned_records == 0


def test_render_markdown_contains_phase_table() -> None:
    report = build_regime_phase_backtest_matrix(
        _winning_records("2019-06-01", 1),
        config=HistoricalEdgeValidationConfig(min_total_trades=1, min_expectancy_r=-10, min_profit_factor=0, max_drawdown_limit=10, min_sharpe_ratio=-10),
        required_passing_phases=1,
    )

    markdown = render_regime_phase_matrix_markdown(report)

    assert "# Regime-Phase Backtest Matrix" in markdown
    assert "Low-Vol Bull" in markdown
    assert "Passing phases" in markdown


def test_write_regime_phase_matrix_report(tmp_path) -> None:
    report = build_regime_phase_backtest_matrix(
        _winning_records("2019-06-01", 1),
        config=HistoricalEdgeValidationConfig(min_total_trades=1, min_expectancy_r=-10, min_profit_factor=0, max_drawdown_limit=10, min_sharpe_ratio=-10),
        required_passing_phases=1,
    )
    json_path = tmp_path / "matrix.json"
    markdown_path = tmp_path / "matrix.md"

    write_regime_phase_matrix_report(report, json_path=json_path, markdown_path=markdown_path)

    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert data["total_phases"] == 5
    assert markdown_path.read_text(encoding="utf-8").startswith("# Regime-Phase Backtest Matrix")
