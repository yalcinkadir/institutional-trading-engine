# BT135 Symbol Selection Sensitivity Research Workflow

Status date: 2026-06-12

Issue: #171

## Scope

BT135 is research-only. It compares symbol-selection and sizing sensitivity variants on the same evidence family and does not change production universe or sizing rules.

## Research script

```text
scripts/bt135_symbol_selection_sensitivity.py
```

This intentionally lives under `scripts/` instead of `src/` because BT135 is a research-only analyzer, not a production runtime module.

## Required comparisons

```text
baseline_full_universe
exclude_worst_symbol_only
exclude_negative_expectancy_symbols
downweight_worst_symbols
best_symbol_only_sanity_check
```

## Downweight levels

```text
0.25x
0.50x
0.75x
```

## Periods

```text
training
validation
out_of_sample
```

## Recommendation contract

```text
KEEP_FULL_UNIVERSE
PROMOTE_TO_GUARDED_EXPERIMENT
NEEDS_MORE_DATA
REJECT_EXCLUSION
OVERFIT_RISK
```

## Required guards

```text
trades_per_symbol < 10 -> NEEDS_MORE_DATA
low effective signal-day clusters -> warning and NEEDS_MORE_DATA
missing required fields -> SKIPPED_INSUFFICIENT_FIELDS
```

## Outputs

```text
reports/backtests/real_data/latest/bt135-symbol-selection-sensitivity-report.json
reports/backtests/real_data/latest/bt135-symbol-selection-sensitivity-report.md
reports/backtests/real_data/runs/<github_run_id>/bt135-symbol-selection-sensitivity-report.json
reports/backtests/real_data/runs/<github_run_id>/bt135-symbol-selection-sensitivity-report.md
```

## Guard tests

```text
tests/test_bt135_symbol_selection_sensitivity.py
```

## Safety

```text
research_only=true
broker_execution_mode=paper_only
production_rule_change=false
```
