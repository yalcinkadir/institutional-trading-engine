# Institutional Trading Engine

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![CI](https://img.shields.io/badge/CI-pytest-brightgreen.svg)
![Status](https://img.shields.io/badge/status-production--oriented-orange.svg)

Institutional Trading Engine is a production-oriented market intelligence, screening, reporting, runtime orchestration, communication, observability, signal lifecycle, historical validation and outcome-learning platform.

The system is **not** a black-box trading bot and does **not** place live trades.

It is a Decision-Support and research system for:

- market regime analysis
- cross-asset scanning
- expanded market-data universe coverage
- signal generation
- executable Entry / Stop / Exit planning
- watcher-based lifecycle tracking
- watcher health diagnostics
- notification delivery
- manual portfolio synchronization without broker integration
- historical Polygon data ingestion
- deterministic historical Entry / Stop / Exit backtesting
- historical signal reconstruction
- out-of-sample validation
- paper-live observation
- operational readiness review
- scheduled Decision-Support dry runs
- persistent report archive
- GitHub Actions based validation and operations
- feedback and expectancy analysis

---

# Core Flow

```text
Market analysis
→ Expanded cross-asset universe scan
→ Scanner metrics normalization
→ Signal generation with native signal_id
→ Entry Quality Engine
→ Stop-Loss Quality Engine
→ Exit / Target Quality Engine
→ Trade Plan Validator
→ E2E dry-run artifact validation
→ Entry / Exit watcher
→ Entry / Exit watcher health diagnostics
→ Manual portfolio sync
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
→ Report archive
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

Targeted validation/observation/readiness/archive/universe tests:

```bash
pytest tests/test_symbol_universe.py
pytest tests/test_historical_entry_exit_backtest.py
pytest tests/test_sample_historical_backtest_plans.py
pytest tests/test_out_of_sample_validation.py
pytest tests/test_paper_live_observation.py
pytest tests/test_operational_readiness_review.py
pytest tests/test_scheduled_decision_support_dry_run.py
pytest tests/test_report_archive.py
pytest tests/test_entry_exit_watcher_health.py
pytest tests/test_manual_portfolio_sync.py
```

## Market Data Coverage

Configured in:

```text
src/config.py
```

Default groups:

```text
core_indices: SPY, QQQ, IWM, DIA
rates_bonds: TLT, IEF, SHY
dollar_proxy: UUP
sectors: XLK, XLF, XLE, XLV, XLY, XLP, XLI, XLU, XLB, XLRE
mega_caps: AAPL, MSFT, NVDA, AMZN, GOOGL, META, TSLA
semiconductors: SMH, MU, AMD, AVGO
commodities: GLD, SLV, USO
legacy_quality: CSCO
```

P32 improves market breadth, bond/rates context, dollar context, sector rotation context and commodity proxy coverage without broker APIs.

## Manual Portfolio Sync

```bash
python scripts/sync_manual_portfolio_state.py \
  --snapshot data/manual_portfolio_snapshot.example.json \
  --portfolio-state-out data/portfolio_state.json \
  --report-json-out reports/portfolio/manual-portfolio-sync.json \
  --report-md-out reports/portfolio/manual-portfolio-sync.md
```

This calculates governance-compatible fields:

```text
drawdown_percent
daily_loss_percent
total_position_value
total_unrealized_pnl
```

It does **not** use broker APIs and does **not** execute orders.

## Check Polygon Live Readiness

```bash
python scripts/check_polygon_live_readiness.py \
  --symbols SPY,QQQ,IWM,DIA,TLT,IEF,SHY,UUP,XLK,XLF,XLE,XLV,XLY,XLP,XLI,XLU,XLB,XLRE,GLD,SLV,USO \
  --lookback-days 3650
```

## Run Historical Polygon Ingestion

```bash
python scripts/ingest_historical_polygon.py \
  --symbols SPY,QQQ,IWM,DIA,TLT,IEF,SHY,UUP,XLK,XLF,XLE,XLV,XLY,XLP,XLI,XLU,XLB,XLRE,GLD,SLV,USO \
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
  --symbols SPY,QQQ,IWM,DIA,TLT,IEF,SHY,UUP,XLK,XLF,XLE,XLV,XLY,XLP,XLI,XLU,XLB,XLRE,GLD,SLV,USO \
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

## Run Entry / Exit Watcher Health Locally

```bash
python scripts/check_entry_exit_watcher_health.py \
  --signals-file reports/signals/latest-signals.json \
  --lifecycle-file data/signal_lifecycle.jsonl \
  --min-signals 1 \
  --min-lifecycle-events 1
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

## Archive Reports Locally

```bash
python scripts/archive_reports.py
```

---

# GitHub Actions Operations

## Manual Portfolio Sync

```text
Actions → Manual Portfolio Sync → Run workflow
```

Artifact:

```text
manual-portfolio-sync-artifacts
```

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

## Entry Exit Watcher Health

```text
Actions → Entry Exit Watcher Health → Run workflow
```

Artifact:

```text
entry-exit-watcher-health-artifacts
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

## Archive Reports

```text
Actions → Archive Reports → Run workflow
```

Artifact:

```text
report-archive-artifacts
```

---

# Market Data Coverage

Implemented in:

```text
src/config.py
docs/operations/market_data_coverage.md
tests/test_symbol_universe.py
```

P32 adds/validates:

```text
Core indices: SPY, QQQ, IWM, DIA
Rates/Bonds: TLT, IEF, SHY
Dollar proxy: UUP
Sectors: XLK, XLF, XLE, XLV, XLY, XLP, XLI, XLU, XLB, XLRE
Commodities: GLD, SLV, USO
```

Guardrail:

```text
P32 does not connect broker execution.
P32 does not place orders.
P32 does not authorize trading.
P32 only expands Decision-Support market-data coverage.
```

---

# Manual Portfolio Sync

Implemented in:

```text
src/operations/manual_portfolio_sync.py
scripts/sync_manual_portfolio_state.py
data/manual_portfolio_snapshot.example.json
docs/operations/manual_portfolio_sync.md
tests/test_manual_portfolio_sync.py
.github/workflows/manual-portfolio-sync.yml
```

---

# Entry / Exit Watcher Health

Implemented in:

```text
src/operations/entry_exit_watcher_health.py
scripts/check_entry_exit_watcher_health.py
docs/operations/entry_exit_watcher_health.md
tests/test_entry_exit_watcher_health.py
.github/workflows/entry-exit-watcher-health.yml
```

---

# Report Archive

Implemented in:

```text
src/operations/report_archive.py
scripts/archive_reports.py
docs/operations/report_archive.md
tests/test_report_archive.py
.github/workflows/archive-reports.yml
```

---

# Implemented Components

| Layer | Status |
|---|---|
| Report Automation | Implemented |
| Expanded Market Data Coverage | Implemented |
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
| Entry / Exit Watcher Health Diagnostics | Implemented |
| Manual Portfolio Sync | Implemented |
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
| Persistent Report Archive | Implemented |
| Entry / Stop / Exit Feedback Aggregation | Implemented |
| Regime-Aware Feedback Grouping | Implemented |
| File-Backed Portfolio State | Implemented |
| Broker Execution | Not implemented |
| Dashboard UI | Not implemented |

---

# Portfolio State

Primary runtime file:

```text
data/portfolio_state.json
```

Manual input template:

```text
data/manual_portfolio_snapshot.example.json
```

Manual sync report outputs:

```text
reports/portfolio/manual-portfolio-sync.json
reports/portfolio/manual-portfolio-sync.md
```

This is **not** broker synchronization. The snapshot must be maintained manually or by a trusted external process.

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
4. expanded market-data coverage reviewed
5. data/portfolio_state.json present and intentionally initialized
6. manual portfolio sync completed and reviewed
7. latest-signals.json generated from real Polygon data
8. E2E dry-run returns PASS
9. manual watcher run completes successfully
10. entry-exit-watcher health report reviewed
11. 5 consecutive entry-exit-watcher runs are green
12. historical strategy validation completed before any trading decision
13. out-of-sample validation reviewed
14. paper-live observation completed and reviewed
15. operational readiness review completed and reviewed
16. scheduled dry-run evidence reviewed
17. report archive created and reviewed
```

Non-goals:

```text
No broker execution
No automatic live orders
No real trading without out-of-sample validation, paper-live observation, operational readiness review, scheduled dry-run review and report archive review
```

---

# Roadmap

## Done

- expanded market-data coverage without broker integration
- manual portfolio-state calculation without broker integration
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
- persistent report archive
- entry-exit watcher health diagnostics
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

1. Static dashboard / HTML reporting.
2. External artifact storage such as S3/R2/Supabase Storage.
3. Session-aware VWAP and intraday entry confirmation.
4. Cross-field feedback grouping such as entry_type x market_regime.
5. Long-term persistence with Postgres or analytics storage.

---

# Disclaimer

This project is intended for research, education, institutional analysis experiments, systematic market screening, signal lifecycle analysis and adaptive scoring research.

It is not financial advice and does not execute trades.
