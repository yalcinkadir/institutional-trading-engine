# C5 Daily Execution Reconciliation Workflow

## Purpose

C5 adds a deterministic daily reconciliation layer between expected/backtest execution records and observed paper/live execution records.

It compares:

```text
Backtest / expected execution
vs.
Paper or live observed execution
vs.
Fill and portfolio-derived realized result
```

This is an audit and validation workflow only. It does not submit orders, cancel orders, fetch broker state or authorize live trading.

## Implemented module

```text
src/validation/daily_execution_reconciliation.py
```

Primary API:

```python
reconcile_daily_execution(
    expected_records=[...],
    observed_records=[...],
)
```

CLI:

```bash
python scripts/reconcile_daily_execution.py \
  --expected-file reports/daily_expected_execution/expected.json \
  --observed-file reports/daily_observed_execution/observed.json \
  --output-dir reports/daily_execution_reconciliation
```

## Input contract

Expected records require:

```text
signal_id
symbol
side
expected_quantity
expected_avg_price
expected_r
strategy_id optional
expected_order_id optional
```

Observed records require:

```text
signal_id
symbol
side
filled_quantity
average_fill_price
realized_r
status
strategy_id optional
order_id optional
commission optional
```

The matching key is `expected_order_id/order_id` when present, otherwise `signal_id`.

## Gates

The workflow fails closed on:

```text
missing_observed_execution
unexpected_observed_execution
duplicate_expected_execution
duplicate_observed_execution
signal_id_mismatch
symbol_mismatch
side_mismatch
quantity_drift_exceeded
price_drift_exceeded
r_drift_exceeded
total_r_drift_exceeded
invalid expected or observed record shape
```

Default tolerances:

```text
max_abs_quantity_drift = 0.000001
max_abs_price_drift_pct = 0.01
max_abs_r_drift = 0.25
max_abs_total_r_drift = 0.5
```

## Output

The report emits JSON and Markdown with:

```text
passed
status
metrics
comparisons[]
issues[]
notes[]
```

Metrics include:

```text
expected_count
observed_count
matched_count
missing_count
unexpected_count
expected_total_r
observed_total_r
total_r_drift
max_abs_quantity_drift
max_abs_price_drift_pct
max_abs_r_drift
```

## Safety boundary

C5 remains decision-support infrastructure only.

```text
daily_execution_reconciliation_only
backtest_expected_vs_observed_paper_or_live_records
no_order_submission_performed
no_live_trading_authorization_granted
```

Real-money execution remains disabled by design.

## Test coverage

```text
tests/test_daily_execution_reconciliation.py
```

Covered scenarios:

```text
matching expected and observed executions pass
missing observed execution fails closed
unexpected observed execution fails closed
missing observed can be warning-only when explicitly configured
quantity, price and R drift fail closed
total daily R drift fails closed
symbol, side and signal mismatches fail closed
duplicate expected/observed keys fail closed
JSON load and report write path works
```
