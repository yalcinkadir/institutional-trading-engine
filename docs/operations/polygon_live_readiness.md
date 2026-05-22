# Polygon Live Readiness

P23B prepares the operational checks for the first real Polygon-powered run after the Stocks Developer subscription/API key is active.

This check does **not** call Polygon. It validates local readiness and prints the exact command sequence for real historical ingestion, current report generation, dry-run validation and watcher verification.

---

## Command

```bash
python scripts/check_polygon_live_readiness.py \
  --symbols SPY,QQQ,NVDA,AAPL,MSFT,AMD,TSLA,META,GOOGL,AMZN \
  --lookback-days 3650
```

Machine-readable output:

```bash
python scripts/check_polygon_live_readiness.py \
  --symbols SPY,QQQ,NVDA,AAPL,MSFT,AMD,TSLA,META,GOOGL,AMZN \
  --lookback-days 3650 \
  --json
```

---

## Why 3650 Days for Stocks Developer?

The Stocks Developer plan is appropriate for historical research, but it provides 10 years of history. That is roughly:

```text
3650 calendar days
```

Do not use 5000 days for this plan unless the subscription history limit supports it.

---

## Required Secret

```text
POLYGON_API_KEY
```

GitHub location:

```text
Repository Settings
→ Secrets and variables
→ Actions
→ New repository secret
```

---

## What The Check Validates

```text
POLYGON_API_KEY exists
lookback_days is reasonable
symbols are configured
portfolio_state.json exists
required command sequence is produced
live gates are visible
```

---

## Command Sequence After PASS

```bash
python scripts/ingest_historical_polygon.py \
  --symbols SPY,QQQ,NVDA,AAPL,MSFT,AMD,TSLA,META,GOOGL,AMZN \
  --start-date <calculated-start-date> \
  --end-date <today>
```

Then:

```bash
python scripts/generate_report.py --type intraday --output reports/manual-e2e-report.md
```

Then:

```bash
python scripts/run_e2e_dry_run.py --signals-file reports/signals/latest-signals.json
```

Then:

```bash
python scripts/run_entry_exit_watcher.py --signals-file reports/signals/latest-signals.json
```

---

## Live Gates

Before live Decision-Support:

```text
historical ingestion completes without unexpected errors
latest-signals.json is generated from real Polygon data
E2E dry-run returns PASS
manual watcher run completes successfully
Telegram/notification output is verified
5 consecutive entry-exit-watcher runs are green
historical strategy validation is completed before any trading decision
```

---

## Non-Goals

```text
No broker execution
No real orders
No live Polygon call in CI tests
No strategy backtest runner in P23B
```

---

## Strict Operating Rule

```text
API active does not mean trade-ready.
API active means real-data validation can start.
```

Next steps after real data ingestion:

```text
P24 Historical Entry / Stop / Exit Backtest Runner
P25 Out-of-Sample Validation and Adaptive Feedback Integration
P26 Paper-Live Observation Before Trading
```
