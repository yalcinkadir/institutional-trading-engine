# Institutional Trading Engine

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![CI](https://img.shields.io/badge/CI-pytest-brightgreen.svg)
![Status](https://img.shields.io/badge/status-production--oriented-orange.svg)

Institutional Trading Engine is a production-oriented market intelligence, screening, reporting, runtime orchestration, communication, observability, signal lifecycle, historical validation and outcome-learning platform.

The system is **not** a black-box trading bot and does **not** place live trades.

It is a Decision-Support and research system for:

- market regime analysis
- cross-asset scanning
- signal generation
- executable Entry / Stop / Exit planning
- watcher-based lifecycle tracking
- notification delivery
- historical Polygon data ingestion
- deterministic historical Entry / Stop / Exit backtesting
- historical signal reconstruction
- out-of-sample validation
- paper-live observation
- operational readiness review
- scheduled Decision-Support dry runs
- GitHub Actions based validation and operations
- feedback and expectancy analysis

---

# Core Flow

```text
Market analysis
→ Diversified universe scan
→ Scanner metrics normalization
→ Signal generation with native signal_id
→ Entry Quality Engine
→ Stop-Loss Quality Engine
→ Exit / Target Quality Engine
→ Trade Plan Validator
→ E2E dry-run artifact validation
→ Entry / Exit watcher
→ Partial exit / runner management
→ Regime invalidation monitoring
→ Notification delivery
→ Lifecycle tracking
→ Historical Polygon ingestion
→ Historical Entry / Stop / Exit backtest
→ Historical signal reconstruction
→ Out-of-sample validation
→ Paper-live observation
→ Operational readiness review
→ Scheduled Decision-Support dry runs
→ GitHub Actions validation artifact generation
→ Feedback aggregation
→ Regime-aware learning
→ live Decision-Support only after validation and human review
```

---

# Main Commands

## Run Tests

```bash
pytest
```

Targeted validation/observation/readiness tests:

```bash
pytest tests/test_historical_entry_exit_backtest.py
pytest tests/test_sample_historical_backtest_plans.py
pytest tests/test_out_of_sample_validation.py
pytest tests/test_paper_live_observation.py
pytest tests/test_operational_readiness_review.py
pytest tests/test_scheduled_decision_support_dry_run.py
```

## Check Polygon Live Readiness

```bash
python scripts/check_polygon_live_readiness.py \
  --symbols SPY,QQQ,NVDA,AAPL,MSFT,AMD,TSLA,META,GOOGL,AMZN \
  --lookback-days 3650
```

## Run Historical Polygon Ingestion

```bash
python scripts/ingest_historical_polygon.py \
  --symbols SPY,QQQ,NVDA,AAPL,MSFT,AMD,TSLA,META,GOOGL,AMZN \
  --start-date 2016-05-22 \
  --end-date 2026-05-22 \
  --json
```

Required environment variable:

```text
POLYGON_API_KEY
```

## Run Historical Entry / Stop / Exit Backtest Locally

```bash
python scripts/run_historical_entry_exit_backtest.py \
  --plans-file reports/signals/latest-signals.json \
  --bars-root data/historical/bars/1day \
  --max-bars 20
```

## Run Out-of-Sample Historical Validation Locally

```bash
python scripts/run_out_of_sample_validation.py \
  --symbols SPY,QQQ,NVDA,AAPL,MSFT,AMD,TSLA,META,GOOGL,AMZN \
  --bars-root data/historical/bars/1day \
  --split-date 2023-01-01 \
  --lookback-bars 20 \
  --every-nth-signal 20 \
  --max-bars 20
```

## Run Paper-Live Observation Locally

```bash
python scripts/run_paper_live_observation.py \
  --signals-file reports/signals/latest-signals.json \
  --lifecycle-file data/signal_lifecycle.jsonl \
  --alerts-file reports/alerts/latest-alerts.json \
  --min-lifecycle-events 5
```

## Run Operational Readiness Review Locally

```bash
python scripts/run_operational_readiness_review.py \
  --backtest-report reports/backtests/historical-entry-exit-backtest.json \
  --oos-report reports/backtests/out-of-sample-validation.json \
  --paper-live-report reports/paper-live/paper-live-observation.json \
  --portfolio-state data/portfolio_state.json \
  --min-backtest-plans 1 \
  --min-oos-plans 1
```

## Run Scheduled Decision-Support Dry Run Locally

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

Default outputs:

```text
reports/scheduled-runs/scheduled-decision-support-dry-run.json
reports/scheduled-runs/scheduled-decision-support-dry-run.md
```

---

# GitHub Actions Operations

## Historical Entry Exit Backtest

```text
Actions → Historical Entry Exit Backtest → Run workflow
```

## Out-of-Sample Historical Validation

```text
Actions → Out-of-Sample Historical Validation → Run workflow
```

## Paper Live Observation

```text
Actions → Paper Live Observation → Run workflow
```

## Operational Readiness Review

```text
Actions → Operational Readiness Review → Run workflow
```

## Scheduled Decision-Support Dry Run

```text
Actions → Scheduled Decision-Support Dry Run → Run workflow
```

Schedule:

```text
30 20 * * 1-5 UTC
```

Artifact:

```text
scheduled-decision-support-dry-run-artifacts
```

---

# Historical Entry / Stop / Exit Backtest

Implemented in:

```text
src/backtesting/historical_models.py
src/backtesting/historical_entry_exit_backtest.py
src/backtesting/historical_report.py
scripts/run_historical_entry_exit_backtest.py
scripts/create_sample_historical_backtest_plans.py
docs/operations/historical_entry_exit_backtest.md
docs/operations/historical_entry_exit_backtest_workflow.md
tests/test_historical_entry_exit_backtest.py
tests/test_sample_historical_backtest_plans.py
.github/workflows/historical-entry-exit-backtest.yml
```

---

# Out-of-Sample Historical Validation

Implemented in:

```text
src/backtesting/out_of_sample_validation.py
scripts/run_out_of_sample_validation.py
docs/operations/out_of_sample_validation.md
tests/test_out_of_sample_validation.py
.github/workflows/out-of-sample-validation.yml
```

Guardrail:

```text
P25 does not train a model.
P25 does not change adaptive scoring.
P25 does not authorize trading.
```

---

# Paper-Live Observation

Implemented in:

```text
src/operations/paper_live_observation.py
scripts/run_paper_live_observation.py
docs/operations/paper_live_observation.md
tests/test_paper_live_observation.py
.github/workflows/paper-live-observation.yml
```

Guardrail:

```text
P26 does not call a broker.
P26 does not place orders.
P26 does not authorize trading.
```

---

# Operational Readiness Review

Implemented in:

```text
src/operations/operational_readiness_review.py
scripts/run_operational_readiness_review.py
docs/operations/operational_readiness_review.md
tests/test_operational_readiness_review.py
.github/workflows/operational-readiness-review.yml
```

Guardrail:

```text
P27 does not authorize trading.
P27 does not connect broker execution.
P27 only determines whether artifacts are complete enough for human review of live Decision-Support scheduling.
```

---

# Scheduled Decision-Support Dry Runs

Implemented in:

```text
src/operations/scheduled_decision_support_dry_run.py
scripts/run_scheduled_decision_support_dry_run.py
docs/operations/scheduled_decision_support_dry_run.md
tests/test_scheduled_decision_support_dry_run.py
.github/workflows/scheduled-decision-support-dry-run.yml
```

P28 wraps the operational readiness review into manual and scheduled GitHub Actions operation.

Guardrail:

```text
P28 does not call a broker.
P28 does not place orders.
P28 does not authorize trading.
P28 only produces scheduled Decision-Support dry-run evidence.
```

---

# Implemented Components

| Layer | Status |
|---|---|
| Report Automation | Implemented |
| Scanner-to-Signal Metrics Pipeline | Implemented |
| Native Signal ID Generation | Implemented |
| Entry Quality Engine | Implemented |
| Stop-Loss Quality Engine | Implemented |
| Exit / Target Quality Engine | Implemented |
| Trade Plan Validator | Implemented |
| Intraday VWAP Support | Implemented |
| Structure-Aware Stops | Implemented |
| Trailing Stop / Partial Exit Management | Implemented |
| Regime Invalidation Exit | Implemented |
| Entry / Exit Watcher | Implemented |
| Central Notification Layer | Implemented |
| Structured Runtime Logging | Implemented |
| E2E Dry Run | Implemented |
| Polygon Live Readiness | Implemented |
| Historical Polygon Data Ingestion | Implemented |
| Historical Entry / Stop / Exit Backtest Runner | Implemented |
| Historical Backtest GitHub Actions Workflow | Implemented |
| Historical Signal Reconstruction | Implemented |
| Out-of-Sample Historical Validation | Implemented |
| Paper-Live Observation | Implemented |
| Operational Readiness Review | Implemented |
| Scheduled Decision-Support Dry Runs | Implemented |
| Entry / Stop / Exit Feedback Aggregation | Implemented |
| Regime-Aware Feedback Grouping | Implemented |
| File-Backed Portfolio State | Implemented |
| Broker Execution | Not implemented |
| Dashboard UI | Not implemented |

---

# Portfolio State

Initial file:

```text
data/portfolio_state.json
```

This file is used by governance/runtime checks for drawdown and daily-loss context.

It is **not** broker synchronization. Until broker/account integration exists, it must be maintained manually or by a trusted external process.

---

# Go-Live Gates

Live mode means:

```text
Decision-Support only
```

Before scheduled live Decision-Support:

```text
1. CI green
2. POLYGON_API_KEY set
3. Telegram/notification secrets verified when alerts are enabled
4. data/portfolio_state.json present and intentionally initialized
5. latest-signals.json generated from real Polygon data
6. E2E dry-run returns PASS
7. manual watcher run completes successfully
8. 5 consecutive entry-exit-watcher runs are green
9. historical strategy validation completed before any trading decision
10. out-of-sample validation reviewed
11. paper-live observation completed and reviewed
12. operational readiness review completed and reviewed
13. scheduled dry-run evidence reviewed
```

Non-goals:

```text
No broker execution
No automatic live orders
No real trading without out-of-sample validation, paper-live observation, operational readiness review and scheduled dry-run review
```

---

# Roadmap

## Done

- scanner-to-signal metrics pipeline
- native scanner structure metric
- intraday VWAP support
- polygon live-readiness checks
- historical Polygon data ingestion
- historical Entry / Stop / Exit backtest runner
- historical Entry Exit Backtest GitHub Actions workflow
- historical signal reconstruction
- out-of-sample historical validation
- paper-live observation
- operational readiness review
- scheduled Decision-Support dry runs
- initial file-backed portfolio state
- E2E dry-run
- breakout entry context upgrade
- structure-aware stops
- trailing stop and partial exit management
- regime invalidation exit
- pending signal regime invalidation
- Entry / Stop / Exit feedback aggregation
- regime-aware feedback grouping
- native signal identity
- executable signal quality gate
- watcher workflow hardening
- lifecycle deduplication

## Planned Next

1. Session-aware VWAP and intraday entry confirmation.
2. Cross-field feedback grouping such as entry_type x market_regime.
3. Static dashboard / HTML reporting.
4. Long-term persistence with Postgres or analytics storage.
5. Broker/account integration for automatic portfolio-state calculation.

---

# Disclaimer

This project is intended for research, education, institutional analysis experiments, systematic market screening, signal lifecycle analysis and adaptive scoring research.

It is not financial advice and does not execute trades.
