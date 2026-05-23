# Scheduled Live Decision-Support Dry Runs

P28 adds scheduled and manual dry-run reporting for Live Decision-Support readiness.

It wraps the operational readiness review and stores a scheduled-run artifact.

It does not place trades.

---

## Local Command

```bash
python scripts/run_scheduled_decision_support_dry_run.py \
  --run-mode manual \
  --backtest-report reports/backtests/historical-entry-exit-backtest.json \
  --oos-report reports/backtests/out-of-sample-validation.json \
  --paper-live-report reports/paper-live/paper-live-observation.json \
  --portfolio-state data/portfolio_state.json \
  --min-backtest-plans 1 \
  --min-oos-plans 1
```

Outputs:

```text
reports/scheduled-runs/scheduled-decision-support-dry-run.json
reports/scheduled-runs/scheduled-decision-support-dry-run.md
```

---

## GitHub Actions Workflow

```text
Actions → Scheduled Decision-Support Dry Run → Run workflow
```

Recommended manual run:

```text
run_mode: manual
backtest_report: reports/backtests/historical-entry-exit-backtest.json
oos_report: reports/backtests/out-of-sample-validation.json
paper_live_report: reports/paper-live/paper-live-observation.json
portfolio_state: data/portfolio_state.json
min_backtest_plans: 1
min_oos_plans: 1
```

Artifact:

```text
scheduled-decision-support-dry-run-artifacts
```

Expected report files:

```text
reports/scheduled-runs/scheduled-decision-support-dry-run.json
reports/scheduled-runs/scheduled-decision-support-dry-run.md
```

---

## Schedule

The workflow currently runs on weekdays:

```text
30 20 * * 1-5 UTC
```

This is evening UTC after the regular US market session.

---

## What P28 Does

```text
1. Checkout repository
2. Setup Python
3. Install dependencies
4. Run scheduled dry-run wrapper
5. Embed operational readiness review result
6. Print Markdown report
7. Upload artifacts
```

---

## What P28 Does Not Do

```text
No broker calls
No orders
No trading authorization
No adaptive scoring mutation
No profitability claim
```

---

## Required Artifact Chain

P28 expects the following files to exist in the repository workspace or be generated before the run:

```text
reports/backtests/historical-entry-exit-backtest.json
reports/backtests/out-of-sample-validation.json
reports/paper-live/paper-live-observation.json
data/portfolio_state.json
```

If reports exist only as GitHub Actions artifacts, they must be persisted or re-created before P28 can pass all gates.

---

## Interpretation

```text
ready_for_live_decision_support_review=false
```

means the dry-run found missing or insufficient readiness evidence.

```text
ready_for_live_decision_support_review=true
```

means the artifact chain is complete enough for human review of scheduled Live Decision-Support operation.

It still does not authorize trading.
