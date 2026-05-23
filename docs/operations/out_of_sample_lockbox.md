# P45: Out-of-Sample Validation Lockbox

## Purpose

P45 protects out-of-sample data from accidental tuning and measures whether performance degrades when the system is evaluated on later unseen data.

This layer is separate from the older P25 reconstructed-plan OOS workflow. P45 works on completed trade records and validates them with P41 historical edge metrics.

## Default Split

```text
in-sample:      before 2024-01-01
out-of-sample:  2024-01-01 onward
```

## Input Records

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

Result fields:

```text
result_r
r_multiple fallback
```

## Validation

Both segments are validated independently with P41:

```text
in_sample_report
out_of_sample_report
```

Core metrics compared:

```text
expectancy_r
profit_factor
sharpe_ratio
max_drawdown
```

## Degradation Gate

Default rule:

```text
OOS degradation must not exceed 20%
```

For higher-is-better metrics:

```text
degradation = (in_sample_value - out_of_sample_value) / abs(in_sample_value)
```

For lower-is-better metrics such as max drawdown:

```text
degradation = (out_of_sample_value - in_sample_value) / abs(in_sample_value)
```

## Report Fields

```text
passed
split_date
in_sample_count
out_of_sample_count
unassigned_records
in_sample_report
out_of_sample_report
degradation_checks
```

## Example

```python
from src.validation.out_of_sample_lockbox import build_out_of_sample_lockbox

records = [
    {"exit_date": "2023-06-01", "result_r": 1.0},
    {"exit_date": "2024-06-01", "result_r": 0.8},
]

report = build_out_of_sample_lockbox(records)
```

## Report Helpers

```python
from pathlib import Path
from src.validation.out_of_sample_lockbox import write_out_of_sample_lockbox_report

write_out_of_sample_lockbox_report(
    report,
    json_path=Path("reports/validation/oos-lockbox.json"),
    markdown_path=Path("reports/validation/oos-lockbox.md"),
)
```

## Tests

```bash
pytest tests/test_out_of_sample_lockbox.py
```

## Guardrails

This framework is decision-support only.

It does not:

- place orders
- connect to a broker
- authorize live trading
- guarantee future performance
- replace paper-live observation
