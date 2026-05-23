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
→ Feedback aggregation
→ Regime-aware learning
→ Paper-live observation
→ trading decision only after validation
```

---

# Main Commands

## Run Tests

```bash
pytest
```

Targeted P24 tests:

```bash
pytest tests/test_historical_entry_exit_backtest.py
```

## Check Polygon Live Readiness

```bash
python scripts/check_polygon_live_readiness.py \
  --symbols SPY,QQQ,NVDA,AAPL,MSFT,AMD,TSLA,META,GOOGL,AMZN \
  --lookback-days 3650
```

The Stocks Developer plan provides 10 years of historical data. Use roughly:

```text
3650 calendar days
```

## Run Historical Polygon Ingestion

```bash
python scripts/ingest_historical_polygon.py \
  --symbols SPY,QQQ,NVDA,AAPL,MSFT,AMD,TSLA,META,GOOGL,AMZN \
  --start-date 2016-05-22 \
  --end-date 2026-05-22 \
  --json
```

Historical storage:

```text
data/historical/bars/1day/<SYMBOL>.csv
data/historical/metadata/ingestion_status.json
```

Required environment variable:

```text
POLYGON_API_KEY
```

## Run Historical Entry / Stop / Exit Backtest

```bash
python scripts/run_historical_entry_exit_backtest.py \
  --plans-file reports/signals/latest-signals.json \
  --bars-root data/historical/bars/1day \
  --max-bars 20
```

Default outputs:

```text
reports/backtests/historical-entry-exit-backtest.json
reports/backtests/historical-entry-exit-backtest.md
```

The runner accepts:

```text
[]
{ "plans": [] }
{ "signals": [] }
```

Each long plan needs:

```text
symbol
signal_date, date or created_at
entry_trigger
stop_loss
target_1
```

Optional:

```text
signal_id
target_2
valid_until
entry_type
setup_type
stop_model
exit_model
```

## Run E2E Dry Run

```bash
python scripts/run_e2e_dry_run.py \
  --signals-file reports/signals/latest-signals.json
```

## Run Entry / Exit Watcher

```bash
python scripts/run_entry_exit_watcher.py \
  --signals-file reports/signals/latest-signals.json
```

---

# Historical Entry / Stop / Exit Backtest

Implemented in:

```text
src/backtesting/historical_models.py
src/backtesting/historical_entry_exit_backtest.py
src/backtesting/historical_report.py
scripts/run_historical_entry_exit_backtest.py
docs/operations/historical_entry_exit_backtest.md
tests/test_historical_entry_exit_backtest.py
```

P24 simulates already-generated long trade plans against historical daily OHLCV bars.

Outcomes:

```text
ENTRY_NOT_HIT
EXPIRED
STOP_HIT
TARGET_1_HIT
TARGET_2_HIT
```

Metrics:

```text
total
entry_hit_rate
expired_without_entry_rate
stop_hit_rate
target_1_hit_rate
target_2_hit_rate
false_breakout_rate
average_r
expectancy_r
```

Conservative daily-bar rule:

```text
If stop and target are touched in the same daily bar, stop wins.
```

This avoids optimistic bias when only daily bars are available.

P24 does **not** generate historical signals from scratch. It tests provided trade plans.

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
```

Non-goals:

```text
No broker execution
No automatic live orders
No real trading without out-of-sample validation and paper-live observation
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

1. P25 — Out-of-Sample Validation and Adaptive Feedback Integration.
2. P26 — Paper-Live Observation Before Trading.
3. Session-aware VWAP and intraday entry confirmation.
4. Cross-field feedback grouping such as entry_type x market_regime.
5. Static dashboard / HTML reporting.
6. Long-term persistence with Postgres or analytics storage.
7. Broker/account integration for automatic portfolio-state calculation.

---

# Disclaimer

This project is intended for research, education, institutional analysis experiments, systematic market screening, signal lifecycle analysis and adaptive scoring research.

It is not financial advice and does not execute trades.
