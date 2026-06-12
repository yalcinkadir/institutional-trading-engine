# P45 / #197: Out-of-Sample Validation Lockbox

## Purpose

P45 protects out-of-sample data from accidental tuning and measures whether performance degrades when the system is evaluated on later unseen data.

#197 adds direct guard coverage for the lockbox module itself, not only downstream workflows.

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

Contamination fields:

```text
signal_id / id / trade_id
symbol / ticker
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

## Contamination Guards

#197 direct tests require the lockbox to fail closed on:

```text
duplicate_signal_ids:<ids>
duplicate_record_dates:<dates>
leaked_symbols:<symbols>
insufficient_in_sample_records:<actual><<minimum>
insufficient_out_of_sample_records:<actual><<minimum>
purged_overlap_records:<count>
embargoed_records:<count>
```

These are lockbox-level invalidation reasons and are recorded in:

```text
invalidation_reasons
```

## Manifest

The report writer can persist an optional manifest:

```text
out_of_sample_lockbox_manifest.v1
```

The manifest records:

```text
split_parameters
date_ranges
counts
source_records_sha256
report_sha256
evidence_contract_hash
invalidation_reasons
```

## Report Fields

```text
passed
split_date
purge_days
embargo_days
threshold_version
evidence_contract_hash
in_sample_count
out_of_sample_count
unassigned_records
purged_records
embargoed_records
in_sample_report
out_of_sample_report
degradation_checks
invalidation_reasons
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
    manifest_path=Path("reports/validation/oos-lockbox.manifest.json"),
    source_records=records,
    config=config,
)
```

## Tests

```bash
pytest tests/test_197_oos_lockbox_direct.py
```

## BT139 prerequisite

BT139 sample expansion is still sample-size constrained. Any future promotion from expanded research samples requires the #197 OOS lockbox contamination guards and manifest to pass.

## Guardrails

This framework is decision-support only.

It does not:

- place orders
- connect to a broker
- authorize live trading
- guarantee future performance
- replace paper-live observation
