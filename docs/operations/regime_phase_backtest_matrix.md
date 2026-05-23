# P42: Regime-Phase Backtest Matrix

## Purpose

P42 validates historical edge metrics across separate market phases instead of one blended historical period.

A strategy that only works in one regime is not robust enough for deeper validation. P42 therefore applies the P41 historical edge metrics to each canonical market phase independently.

## Canonical Market Phases

```text
Low-Vol Bull       2019-01-01 to 2020-02-29
Panic/Dislocation  2020-03-01 to 2020-04-30
Recovery           2020-05-01 to 2021-12-31
High-Vol Regime    2022-01-01 to 2022-12-31
Neutral/Transition 2023-01-01 to 2024-06-30
```

## Input Records

Records are assigned to phases by date.

Primary date field:

```text
exit_date
```

Fallback fields:

```text
closed_at
signal_date
date
```

Result fields are inherited from P41:

```text
result_r
r_multiple fallback
```

## Per-Phase Metrics

Each phase receives a P41 validation report with:

```text
total_trades
win_rate
expectancy_r
profit_factor
max_drawdown
sharpe_ratio
max_consecutive_losses
recovery_time_trades
cumulative_r
```

## Matrix Gate

Default gate:

```text
at least 3 of 5 phases must pass
```

This prevents a single strong historical phase from hiding weak behavior elsewhere.

## Outputs

The matrix report includes:

```text
passed
passing_phases
required_passing_phases
total_phases
unassigned_records
phase_results
```

## Example

```python
from src.validation.regime_phase_backtest_matrix import build_regime_phase_backtest_matrix

records = [
    {"exit_date": "2021-03-15", "result_r": 1.0},
    {"exit_date": "2022-06-01", "result_r": -0.5},
]

report = build_regime_phase_backtest_matrix(records)
```

## Report Helpers

```python
from pathlib import Path
from src.validation.regime_phase_backtest_matrix import write_regime_phase_matrix_report

write_regime_phase_matrix_report(
    report,
    json_path=Path("reports/validation/regime-phase-matrix.json"),
    markdown_path=Path("reports/validation/regime-phase-matrix.md"),
)
```

## Tests

```bash
pytest tests/test_regime_phase_backtest_matrix.py
```

## Guardrails

This framework is decision-support only.

It does not:

- place orders
- connect to a broker
- authorize live trading
- replace walk-forward validation
- replace out-of-sample validation
