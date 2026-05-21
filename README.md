# Institutional Trading Engine

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![CI](https://img.shields.io/badge/CI-pytest-brightgreen.svg)
![Status](https://img.shields.io/badge/status-production--oriented-orange.svg)

Institutional Trading Engine is a production-oriented market intelligence, screening, reporting, runtime orchestration, communication, signal lifecycle and outcome-learning platform.

The system is **not** a black-box trading bot and does **not** place live trades.

It is designed as an institutional decision-support and research platform that:

- analyzes market regimes
- evaluates risk conditions
- ranks opportunities
- scans a diversified symbol universe across indices, sectors, bonds, commodities and leaders
- generates premarket, intraday, postmarket and weekly reports
- communicates alerts and summaries through a central notification layer
- produces machine-readable signal files
- assigns stable signal identity for lifecycle tracking
- stores signal history in the repository
- monitors entries, stops and targets
- records deduplicated signal lifecycle events
- evaluates triggered vs expired vs pending signals separately
- tracks real outcomes from market data
- validates setups against historical Polygon aggregate bars
- builds adaptive expectancy profiles
- generates weekly expectancy feedback summaries
- feeds historical expectancy back into future scoring
- persists scoring adjustments for auditability
- persists runtime and decision history for reproducibility

---

# Core Flow

```text
Market analysis
→ Diversified universe scan
→ Signal generation
→ Signal identity
→ Entry / Exit monitoring
→ Notification delivery
→ Deduplicated lifecycle tracking
→ Historical validation
→ Outcome evaluation
→ Weekly expectancy feedback
→ Expectancy learning
→ Adaptive score / size adjustment
→ Adjustment audit history
→ Better future signals
```

---

# Quick Start

## Requirements

- Python 3.11+
- Git
- Polygon.io API key
- GitHub Actions enabled

Optional:

- Telegram bot token
- Telegram chat ID
- generic webhook endpoint

## Installation

```bash
git clone https://github.com/yalcinkadir/institutional-trading-engine.git
cd institutional-trading-engine
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment Setup

```env
POLYGON_API_KEY=your_polygon_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
REPORT_WEBHOOK_URL=optional_webhook_url
```

---

# Main Commands

## Generate Reports

```bash
python scripts/generate_report.py --type premarket --output reports/premarket/test-report.md
python scripts/generate_report.py --type intraday --output reports/intraday/test-report.md
python scripts/generate_report.py --type postmarket --output reports/postmarket/test-report.md
python scripts/generate_report.py --type weekly --output reports/weekly/test-report.md
```

## Run the Entry / Exit Watcher

```bash
python scripts/run_entry_exit_watcher.py \
  --signals-file reports/signals/latest-signals.json
```

The watcher validates runtime configuration before execution:

- `POLYGON_API_KEY` must exist
- the configured signal file must exist
- the signal file must contain a JSON list
- every run prints a `WATCHER_CYCLE_ID`
- missing `signal_id` values are assigned deterministically
- lifecycle events are deduplicated by `signal_id` + `event_type`

## Send Notifications

```bash
python scripts/send_notification.py \
  --message "communication test" \
  --telegram \
  --webhook \
  --dry-run
```

```bash
python scripts/send_notification.py \
  --message-file reports/weekly-expectancy-summary.txt \
  --telegram \
  --webhook
```

Missing Telegram or webhook configuration is non-fatal by default and returns structured `skipped` results.

## Configure Portfolio State for Governance

```bash
cp data/portfolio_state.example.json data/portfolio_state.json
```

Runtime governance reads:

```text
data/portfolio_state.json
```

Documentation:

```text
docs/architecture/runtime_portfolio_state.md
```

## Run Historical Validation

```bash
python scripts/run_historical_validation.py \
  --signals-file data/backtest_signals.json \
  --symbols AAPL,MSFT,NVDA \
  --start-date 2024-01-01 \
  --end-date 2024-12-31 \
  --horizons 5,10,20 \
  --output reports/backtests/backtest_summary.json
```

## Build Weekly Expectancy Summary

```bash
python scripts/build_weekly_expectancy_summary.py \
  --decision-log data/decision_log.csv \
  --output reports/weekly-expectancy-summary.txt
```

## Run Tests

```bash
pytest
```

Targeted tests:

```bash
pytest tests/test_entry_exit_watcher.py
pytest tests/test_notifications.py
pytest tests/test_expectancy_feedback_summary.py
pytest tests/test_historical_validation.py
pytest tests/test_polygon_client_historical_range.py
pytest tests/test_symbol_universe.py
pytest tests/test_portfolio_state.py
pytest tests/test_live_runtime_cycle_portfolio_state.py
```

---

# Symbol Universe

The default scanner universe is centralized in:

```text
src/config.py
```

It includes:

- core indices: `SPY`, `QQQ`, `IWM`, `DIA`
- rates / bonds: `TLT`, `IEF`, `SHY`
- sectors: `XLK`, `XLF`, `XLE`, `XLV`, `XLY`, `XLP`, `XLI`
- mega caps: `AAPL`, `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`
- semiconductors: `SMH`, `MU`, `AMD`, `AVGO`
- commodities: `GLD`, `SLV`, `USO`
- legacy quality: `CSCO`

Benchmark and group metadata are maintained through:

```text
BENCHMARK_MAP
SYMBOL_GROUP_MAP
SYMBOL_UNIVERSE_GROUPS
```

---

# Signal Identity and Lifecycle Deduplication

Signal identity and lifecycle deduplication are implemented in:

```text
src/watchers/entry_exit_watcher.py
docs/architecture/signal_identity_lifecycle.md
```

Key behavior:

- existing `signal_id` values are preserved
- missing `signal_id` values are generated deterministically from stable signal fields
- watcher alerts include `signal_id`
- lifecycle JSONL records include top-level `signal_id`
- updated signal files preserve `signal_id`
- duplicate lifecycle events are skipped by `(signal_id, event_type)`
- different event types for the same signal are still allowed

Important files:

```text
reports/signals/latest-signals.json
reports/alerts/latest-alerts.json
data/signal_lifecycle.jsonl
```

Current limitation:

```text
Signal generation should later emit signal_id before the watcher sees the signal.
Watcher-side identity assignment currently provides backward-compatible protection.
```

---

# Notification and Communication Layer

Central notification logic is implemented in:

```text
src/notifications.py
scripts/send_notification.py
docs/architecture/notifications.md
```

Supported channels:

- Telegram `sendMessage`
- generic webhook POST via `REPORT_WEBHOOK_URL`

Delivery results are structured:

```text
delivered | skipped | dry_run | failed
```

Current migrated workflow:

```text
.github/workflows/weekly-expectancy-feedback.yml
```

Next migration target:

```text
.github/workflows/entry-exit-watcher.yml
```

---

# Weekly Expectancy Feedback

Implemented through:

```text
src/expectancy_feedback_summary.py
scripts/build_weekly_expectancy_summary.py
.github/workflows/weekly-expectancy-feedback.yml
```

The workflow:

- runs every Sunday at 08:00 UTC
- can be started manually
- refreshes outcomes when `POLYGON_API_KEY` is available
- writes `reports/expectancy-report.md`
- writes `reports/weekly-expectancy-summary.txt`
- uploads artifacts
- sends Telegram/webhook summary through the central notification CLI

---

# Historical Validation

Implemented through:

```text
src/data/polygon_client.py
src/historical_validation.py
scripts/run_historical_validation.py
docs/architecture/historical_validation.md
```

Default output:

```text
reports/backtests/backtest_summary.json
```

Metrics by horizon:

- sample size
- win rate
- average return
- max adverse excursion
- false-positive rate

---

# Runtime Architecture

Runtime modules include:

```text
src/runtime/runtime_loop.py
src/runtime/runtime_state.py
src/runtime/in_memory_state_cache.py
src/runtime/runtime_market_snapshot.py
src/runtime/live_runtime_cycle.py
src/runtime/portfolio_state.py
```

Runtime flow:

```text
scanner.py
  ↓ metrics_map + vix_data
PortfolioStateStore.load()
  ↓ drawdown + daily loss context
governance pre-check
  ↓ kill switch / risk limits
scanner_to_orchestrator.translate()
  ↓ InstitutionalDecisionInputs
institutional_decision_orchestrator.evaluate()
  ↓ InstitutionalDecisionResult
RuntimeMarketSnapshot.create()
  ↓ immutable audit record
decision_log_store.append()
runtime_state.update()
in_memory_state_cache.set()
```

Governance always runs before institutional decision creation.

---

# GitHub Actions Workflows

Main workflows:

```text
.github/workflows/ci.yml
.github/workflows/institutional-reports.yml
.github/workflows/entry-exit-watcher.yml
.github/workflows/outcome-tracking.yml
.github/workflows/weekly-expectancy-feedback.yml
.github/workflows/daily-backup.yml
```

---

# Architecture Reality Check

| Layer | Status |
|---|---|
| Report Automation | Implemented |
| Expanded Symbol Universe | Implemented |
| Central Notification Client | Implemented |
| Notification CLI | Implemented |
| Weekly Workflow Notification Migration | Implemented |
| Entry / Exit Watcher | Implemented and workflow-hardened |
| Watcher Runtime Validation | Implemented |
| Signal Identity | Implemented in watcher path |
| Lifecycle Deduplication | Implemented |
| Alerts Persistence | Implemented |
| Signal Lifecycle JSONL | Implemented |
| Lifecycle-Aware Outcomes | Implemented |
| Historical Polygon Validation | Implemented |
| Weekly Expectancy Feedback Workflow | Implemented |
| Runtime Loop | Implemented |
| File-Backed Portfolio State | Implemented |
| Portfolio-State Governance Integration | Implemented |
| CI Pytest Workflow | Implemented |
| End-to-End Institutional Flow | Partially implemented |
| Fully Unified Continuous Runtime | In progress |
| Signal Generation Native `signal_id` | Planned |
| Watcher Notification Migration to CLI | Planned |
| Broker Execution | Not implemented |
| Dashboard UI | Not implemented |

---

# Current Limitations

- no live broker execution
- no automatic broker/account portfolio sync yet
- portfolio state is file-backed and must be maintained by a caller/workflow/integration
- no real-time websocket watcher
- no streaming intraday bars in the core implementation
- historical validation uses daily bars only in the first implementation
- signal extraction into historical-validation input is not fully automated yet
- signal generation should later emit native `signal_id`
- watcher notification migration to the central CLI is still planned
- Git-based persistence is not final production storage
- no dashboard UI yet
- no Postgres persistence yet

---

# Development Standard

No new feature should be added without:

```text
- roadmap / issue plan
- implementation
- tests
- architecture documentation
- README update
- CI verification
- deterministic behavior
```

For market intelligence, lifecycle and communication features, also require:

```text
- machine-readable output
- lifecycle-aware state handling
- non-fatal failure mode
- clear audit trail
- communication with existing reports/signals/outcomes/scoring features
```

---

# Roadmap

## Done

- report automation
- signal generation
- signal persistence
- expanded cross-asset symbol universe
- central notification client
- notification CLI
- weekly workflow notification migration
- Entry / Exit Watcher V1
- watcher runtime validation
- watcher workflow hardening
- signal identity in watcher lifecycle path
- lifecycle event deduplication
- alerts persistence
- lifecycle JSONL
- lifecycle-aware outcomes
- historical Polygon aggregate validation
- weekly expectancy feedback workflow
- runtime loop
- decision persistence
- VIX-aware runtime context
- governance-first runtime cycle
- file-backed portfolio state
- portfolio-state-backed governance
- minimal pytest CI workflow

## In Progress

- connection and communication hardening
- unified continuous runtime maturity
- operational observation of watcher stability across real scheduled runs

## Planned Next

1. Generate native `signal_id` at signal creation time.
2. Migrate entry-exit watcher notifications to the central notification CLI.
3. Add structured JSON logging.
4. Improve intraday data support with higher-frequency bars if Polygon plan allows.
5. Add dashboard or static HTML reporting.
6. Move long-term persistence from Git files to Postgres.
7. Add regime similarity memory.
8. Add scoring adjustment quality review.
9. Add adaptive scoring guardrails by market regime.
10. Add broker/account integration for automatic portfolio-state calculation.

---

# Disclaimer

This project is intended for research, education, institutional analysis experiments, systematic market screening, signal lifecycle analysis and adaptive scoring research.

It is not financial advice and does not execute trades.
