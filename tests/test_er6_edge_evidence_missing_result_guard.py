from types import SimpleNamespace

from src.backtesting.edge_evidence_backtest import build_edge_evidence_diagnostics


def _validation_report(expectancy_r: float = 0.0) -> SimpleNamespace:
    return SimpleNamespace(
        metrics=SimpleNamespace(
            expectancy_r=expectancy_r,
            profit_factor=1.0,
            sharpe_ratio=0.0,
            to_dict=lambda: {
                "total_trades": 0,
                "expectancy_r": expectancy_r,
                "profit_factor": 1.0,
                "max_drawdown": 0.0,
                "sharpe_ratio": 0.0,
            },
        ),
        gates=[],
    )


def _walk_forward_report() -> SimpleNamespace:
    return SimpleNamespace(
        passed=True,
        generated_cycles=0,
        passing_cycles=0,
        min_required_cycles=0,
        min_required_passing_cycles=0,
        unassigned_records=0,
        cycle_results=[],
    )


def _oos_report() -> SimpleNamespace:
    return SimpleNamespace(
        passed=True,
        split_date="2024-01-01",
        in_sample_count=0,
        out_of_sample_count=0,
        unassigned_records=0,
        in_sample_report=_validation_report(),
        out_of_sample_report=_validation_report(),
        degradation_checks=[],
    )


def test_er6_missing_result_r_is_not_counted_as_breakeven() -> None:
    diagnostics = build_edge_evidence_diagnostics(
        [
            {"signal_id": "missing", "exit_date": "2026-06-01"},
            {"signal_id": "zero", "exit_date": "2026-06-01", "result_r": 0.0},
            {"signal_id": "win", "exit_date": "2026-06-01", "result_r": 1.0},
        ],
        walk_forward_report=_walk_forward_report(),
        oos_report=_oos_report(),
    )

    historical = diagnostics["historical_results"]

    assert historical["total"] == 2
    assert historical["missing_result_count"] == 1
    assert historical["breakeven"] == 1
    assert historical["wins"] == 1
    assert historical["average_r"] == 0.5
