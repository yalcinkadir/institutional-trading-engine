# Performance Drift Detection

Phase B2 adds a drift check between the historical backtest baseline and forward paper observation results.

The goal is to detect whether forward paper performance is materially worse than the validated baseline. This is not a broker-execution approval gate.

## Inputs

The detector accepts either numeric R values or dictionaries containing:

```text
result_r
r_multiple
paper_r
```

Backtest records define the baseline. Forward records define the paper-observation stream.

## Metrics

The report calculates:

```text
backtest_observations
forward_observations
backtest_expectancy_r
forward_expectancy_r
expectancy_drift_r
backtest_win_rate
forward_win_rate
win_rate_drift
backtest_total_r
forward_total_r
cumulative_drift_r
backtest_std_r
standard_error_r
z_score
```

## Gates

Default fail-closed gates:

```text
min_backtest_observations = 30
min_forward_observations = 10
max_abs_expectancy_drift_r = 0.25
max_abs_win_rate_drift = 0.15
max_abs_cumulative_drift_r = 5.0
max_abs_z_score = 2.0
require_positive_forward_expectancy = true
```

A failure means the forward stream should be investigated before evidence is trusted.

## Outputs

The module can write:

```text
performance_drift_detection.json
performance_drift_detection.md
```

## Operational Rule

Drift detection is an evidence-quality gate. It does not authorize live capital. If drift fails, continue observation, investigate causes and do not escalate toward live execution.
