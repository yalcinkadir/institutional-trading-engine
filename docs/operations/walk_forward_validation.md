# P43: Walk-Forward Validation

## Purpose

P43 reduces overfitting risk by separating development windows from forward test windows.

Instead of validating one full historical period at once, the framework creates rolling cycles:

```text
training window -> forward test window -> step forward -> repeat
```

Only the test window is evaluated for edge quality.

## Default Window Structure

```text
training window 18 months
test window      6 months
step size        3 months
minimum cycles   6
```

## Inputs

Records are assigned by date.

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

## Cycle Validation

Each test window is validated with P41 historical edge validation:

```text
win_rate
expectancy_r
profit_factor
max_drawdown
sharpe_ratio
max_consecutive_losses
recovery_time_trades
cumulative_r
```

## Report Fields

```text
passed
generated_cycles
passing_cycles
min_required_cycles
min_required_passing_cycles
unassigned_records
cycle_results
```

## Example

```python
from src.validation.walk_forward_validation import build_walk_forward_validation

records = [
    {"exit_date": "2021-03-15", "result_r": 1.0},
    {"exit_date": "2021-04-15", "result_r": -0.5},
]

report = build_walk_forward_validation(records)
```

## Report Helpers

```python
from pathlib import Path
from src.validation.walk_forward_validation import write_walk_forward_report

write_walk_forward_report(
    report,
    json_path=Path("reports/validation/walk-forward.json"),
    markdown_path=Path("reports/validation/walk-forward.md"),
)
```

## Tests

```bash
pytest tests/test_walk_forward_validation.py
```

## Guardrails

This framework is decision-support only.

It does not:

- place orders
- connect to a broker
- authorize live trading
- replace execution realism validation
- replace out-of-sample lockbox validation
