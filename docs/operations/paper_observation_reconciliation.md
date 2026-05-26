# Paper Observation Daily Reconciliation

Phase B1 starts the forward evidence period. It is observation-only.

The purpose is to compare the expected decision stream against the paper-observed stream every day. This does not authorize live capital or broker execution.

## Inputs

Each record may contain:

```text
observation_date or date
expected_action or backtest_action
paper_action or observed_action
expected_r or backtest_r
paper_r or observed_r
```

Actions are normalized, for example `buy` and `long` are treated as `enter_long`.

## Metrics

The reconciliation report calculates:

```text
observation_days
total_records
resolved_records
unresolved_records
action_matches
action_mismatches
action_mismatch_rate
expected_total_r
paper_total_r
total_drift_r
mean_daily_drift_r
max_abs_daily_drift_r
```

## Gates

The report is fail-closed when:

```text
observation_only_mode is false
observation_days is below the configured minimum
unresolved_records exceed tolerance
action_mismatch_rate exceeds tolerance
max_abs_daily_drift_r exceeds tolerance
```

Default configuration:

```text
min_observation_days = 63
target_observation_days = 126
max_action_mismatch_rate = 0.05
max_abs_daily_drift_r = 1.0
max_unresolved_records = 0
require_observation_only = true
```

## Output

The module can write both JSON and Markdown reports.

```text
paper_observation_reconciliation.json
paper_observation_reconciliation.md
```

## Operational Rule

Phase B1 is for evidence collection only. A passing reconciliation report means the paper stream is internally consistent enough to continue observation. It does not approve live trading.

Phase B should run for 3-6 months before the system can claim real forward evidence.
