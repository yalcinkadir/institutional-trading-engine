# BT176 Guarded Entry Confirmation Experiment

Status date: 2026-06-10

## Purpose

BT176 promotes the BT133 research finding into a guarded, reviewable, paper-only shadow experiment.

It does **not** change production entry rules. It creates an evidence layer that compares the current baseline breakout trigger against one selected next-bar close confirmation candidate before any future production-promotion issue is considered.

## Source evidence

BT176 depends on the same real-data evidence contract used by BT131 and BT133:

- `reports/backtests/real_data/latest/real-data-backtest-evidence.json`
- `reports/backtests/real_data/latest/bt133-entry-confirmation-variant-report.json`

The analyzer requires:

- `data_source=real_data`
- `is_demo=false`
- `input_pack_gate_status=PASSED`
- `run_health_status=OK`
- `live_trading_authorized=false`
- `broker_execution_mode=paper_only`
- BT133 `final_recommendation=PROMOTE_TO_GUARDED_EXPERIMENT`

## Selected candidate

Default candidate:

```text
next_bar_close_confirmation_1bar
```

Reason:

- It is the simplest promoted next-bar confirmation candidate.
- It keeps the baseline unchanged.
- It is easier to review than stricter multi-bar variants.
- It remains a shadow experiment until separate promotion evidence exists.

## Implementation

Analyzer:

```text
scripts/analyze_bt176_guarded_entry_confirmation_experiment.py
```

Tests:

```text
tests/test_bt176_guarded_entry_confirmation_experiment.py
```

Workflow integration:

```text
.github/workflows/bt131_real_data_backtest_evidence.yml
```

## Output artifacts

BT176 writes reviewable JSON and Markdown reports:

```text
reports/backtests/bt133-guarded-entry-confirmation-experiment.json
reports/backtests/bt133-guarded-entry-confirmation-experiment.md
```

The BT131 evidence workflow persists them into:

```text
reports/backtests/real_data/runs/<github_run_id>/bt133-guarded-entry-confirmation-experiment.json
reports/backtests/real_data/runs/<github_run_id>/bt133-guarded-entry-confirmation-experiment.md
reports/backtests/real_data/latest/bt133-guarded-entry-confirmation-experiment.json
reports/backtests/real_data/latest/bt133-guarded-entry-confirmation-experiment.md
```

The report index records:

```text
bt176_guard_status
bt176_candidate_variant_id
bt176_experiment_scope
bt176_production_rule_change_allowed
```

## Reported metrics

Both baseline and guarded experiment report:

- total trades considered
- accepted trades
- filtered / skipped trades
- false-breakout rate
- stop-hit rate
- target-1 hit rate
- target-2 hit rate
- average R
- expectancy R

## Guard status

BT176 returns one of:

```text
READY_FOR_PAPER_SHADOW
BLOCKED
```

The experiment is blocked if:

- fewer than two trades remain accepted after confirmation filtering
- stop-hit rate worsens versus baseline
- false-breakout rate worsens versus baseline
- expectancy R falls below baseline
- candidate variant is missing, unpromoted, unevaluated or has missing required fields
- source evidence is demo, non-real-data, live-authorized or not paper-only

## Safety boundary

BT176 is research-only and paper-observation-only.

It does not authorize:

- live trading
- broker execution
- capital allocation
- automatic promotion
- production entry-rule changes

Production promotion requires a separate issue, fresh forward evidence, explicit approval and green CI with before/after evidence.
