# BT5 Walk-Forward / Out-of-Sample Robustness Gate

BT5 adds a deterministic public-safe gate for walk-forward and out-of-sample robustness evidence.

The goal is not to prove production edge. The goal is to prevent weak backtests from passing simply because in-sample results look good.

## Scope

BT5 validates:

- minimum walk-forward fold count
- complete fold identity and dataset metadata
- chronological train and OOS windows
- non-overlapping OOS folds
- required train and OOS metrics
- minimum OOS trade count per fold
- maximum OOS drawdown
- minimum OOS pass rate
- positive primary OOS metric rate
- train-to-OOS degradation limit
- public-safe demo tags
- research-only footer

## Public-safe command

```bash
python scripts/generate_bt5_walk_forward_report.py --demo
```

File-based command:

```bash
python scripts/generate_bt5_walk_forward_report.py \
  --input-json data/demo_bt5_walk_forward_folds.json \
  --output-json reports/bt5_walk_forward/robustness_report.json \
  --output-md reports/bt5_walk_forward/robustness_report.md
```

## Test command

```bash
pytest tests/test_bt5_walk_forward_robustness_gate.py -q
```

## Required fold fields

```text
fold_id
strategy_id
parameter_version
dataset_id
train_start
train_end
oos_start
oos_end
train_metrics
oos_metrics
tags
footer
```

Default required metrics:

```text
expectancy_r
sharpe
max_drawdown_pct
trade_count
```

## Hard rule

BT5 is a robustness gate only. It does not authorize live trading, broker execution, production thresholds, private strategy weights or real-money deployment.

Every generated report must remain compatible with the repository research-only footer.
