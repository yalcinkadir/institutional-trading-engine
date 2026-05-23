# Operational Readiness Review

P27 consolidates validation and observation artifacts before live Decision-Support scheduling is considered.

It does not authorize trading.

---

## Local Command

```bash
python scripts/run_operational_readiness_review.py \
  --backtest-report reports/backtests/historical-entry-exit-backtest.json \
  --oos-report reports/backtests/out-of-sample-validation.json \
  --paper-live-report reports/paper-live/paper-live-observation.json \
  --portfolio-state data/portfolio_state.json \
  --min-backtest-plans 1 \
  --min-oos-plans 1
```

Outputs:

```text
reports/readiness/operational-readiness-review.json
reports/readiness/operational-readiness-review.md
```

---

## GitHub Actions Workflow

```text
Actions → Operational Readiness Review → Run workflow
```

Recommended first run:

```text
backtest_report: reports/backtests/historical-entry-exit-backtest.json
oos_report: reports/backtests/out-of-sample-validation.json
paper_live_report: reports/paper-live/paper-live-observation.json
portfolio_state: data/portfolio_state.json
min_backtest_plans: 1
min_oos_plans: 1
```

Artifact:

```text
operational-readiness-review-artifacts
```

Expected report files:

```text
reports/readiness/operational-readiness-review.json
reports/readiness/operational-readiness-review.md
```

---

## Gates

P27 checks:

```text
historical_backtest_report_present
historical_backtest_has_plans
out_of_sample_report_present
out_of_sample_has_plans
paper_live_report_present
paper_live_ready_for_review
portfolio_state_present
portfolio_drawdown_available
portfolio_daily_loss_available
```

---

## Summary Metrics

The report summarizes:

```text
backtest_total
backtest_expectancy_r
out_of_sample_count
out_of_sample_expectancy_r
paper_live_ready_for_review
paper_live_terminal_event_count
portfolio_drawdown_percent
portfolio_daily_loss_percent
```

---

## Interpretation

```text
ready_for_live_decision_support_review=false
```

means at least one required validation/observation artifact is missing or insufficient.

```text
ready_for_live_decision_support_review=true
```

means the artifact chain is complete enough for human review of live Decision-Support scheduling.

It still does not authorize trading.

---

## Strict Guardrail

```text
No broker execution.
No live orders.
No adaptive scoring mutation.
No trading authorization.
Human review is still required.
```

---

## Required Artifact Chain

```text
P24 historical-entry-exit-backtest.json
P25 out-of-sample-validation.json
P26 paper-live-observation.json
portfolio_state.json
```

If these files only exist as GitHub Actions artifacts, download or persist them before running P27 against the repository workspace.

---

## Next Step After P27

Only after a green P27 review:

```text
schedule live Decision-Support runs
observe repeated stability
review notifications
do not connect broker execution
```
