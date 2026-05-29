# BT6 Evidence Baseline Regression Gate

BT6 compares a newly generated evidence snapshot against a previously accepted baseline snapshot.

The goal is to block silent evidence degradation. A new backtest or walk-forward result must not pass only because it is valid in isolation. It must also remain acceptable compared with the previous accepted baseline.

## Scope

BT6 is a research and evidence-quality gate. It is not a live-trading authorization mechanism.

BT6 validates:

```text
baseline and current run identity
strategy comparability
dataset comparability
required metric presence
numeric metric validity
artifact hash references
expectancy degradation
Sharpe degradation
OOS pass-rate degradation
drawdown increase
trade-count collapse
public-safe tags
research-only footer
```

## Required Snapshot Fields

Each snapshot must contain:

```text
run_id
strategy_id
dataset_id
parameter_version
evidence_type
metrics
artifact_hashes
tags
footer
```

Required metrics:

```text
expectancy_r
sharpe
max_drawdown_pct
oos_pass_rate_pct
trade_count
```

## Demo Command

```bash
python scripts/generate_bt6_baseline_regression_report.py --demo
```

## File-Based Command

```bash
python scripts/generate_bt6_baseline_regression_report.py \
  --input-json data/demo_bt6_evidence_baseline.json \
  --output-json reports/bt6_baseline_regression/report.json \
  --output-md reports/bt6_baseline_regression/report.md
```

## Test Command

```bash
pytest tests/test_bt6_evidence_baseline_regression_gate.py -q
```

## CI Workflow

Dedicated workflow:

```text
.github/workflows/bt6.yml
```

The workflow runs the BT6 test suite and generates a public-safe demo report.

## Default Regression Limits

```text
max_expectancy_degradation_pct: 20.0
max_sharpe_degradation_pct: 25.0
max_oos_pass_rate_degradation_pct: 10.0
max_drawdown_increase_pct: 15.0
max_trade_count_drop_pct: 40.0
```

These are demo/default public framework limits. Real production limits belong behind the private-edge boundary.

## Hard Rule

BT6 can block weak or degraded evidence. BT6 cannot approve live trading.

Every generated report must remain compatible with:

```text
Research / Paper Observation Only. Execution is not authorized by this report.
```
