# BT134 Stop-Loss Variant Research Workflow

Status date: 2026-06-12

Issue: #170

## Scope

BT134 is research-only. It compares stop-loss variants on the same evidence family and does not change production stop rules.

## Research script

```text
scripts/bt134_stop_loss_variant.py
```

This intentionally lives under `scripts/` instead of `src/` because BT134 is a research-only analyzer, not a production runtime module.

## Required variant groups

```text
baseline_fixed_stop
wider_fixed_stop
atr_stop
same_bar_handling
```

Each group must contain multiple parameter levels.

## Periods

```text
training
validation
out_of_sample
```

OOS degradation after in-sample improvement must be marked as:

```text
OVERFIT_RISK
REJECT_VARIANT
```

## Missing fields

Missing required fields must produce:

```text
SKIPPED_INSUFFICIENT_FIELDS
```

No missing entry/stop/target/ATR/high/low/close values may be guessed.

## Outputs

```text
reports/backtests/real_data/latest/bt134-stop-loss-variant-report.json
reports/backtests/real_data/latest/bt134-stop-loss-variant-report.md
reports/backtests/real_data/runs/<github_run_id>/bt134-stop-loss-variant-report.json
reports/backtests/real_data/runs/<github_run_id>/bt134-stop-loss-variant-report.md
```

## Guard tests

```text
tests/test_bt134_stop_loss_variant.py
```

## Safety

```text
research_only=true
broker_execution_mode=paper_only
production_rule_change=false
```
