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
- stores signal history in the repository
- monitors entries, stops and targets
- records signal lifecycle events
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
→ Entry / Exit monitoring
→ Notification delivery
→ Lifecycle tracking
→ Historical validation
→ Outcome evaluation
→ Weekly expectancy feedback
→ Expectancy learning
→ Adaptive score / size adjustment
→ Adjustment audit history
→ Better future signals
```

The current implementation supports this structural flow:

```text
Reports → Signals → Watcher → Alerts → Notifications → Lifecycle → Outcomes → Expectancy → Scoring → Audit History
```

---

# Core Principles

The project is designed to be:

- modular
- auditable
- deterministic
- reproducible
- explainable
- risk-first
- testable
- production-oriented

The most important design rule:

```text
A signal is not a trade until its entry trigger is hit.
```

Therefore:

- untriggered signals are not counted as losses
- expired signals are tracked separately
- triggered signals are evaluated with real outcomes
- stop/target events are stored as lifecycle data
- historical learning is based on lifecycle-aware outcomes
- adaptive score changes are persisted in an audit log

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
- webhook endpoint for external notifications

## Installation

```bash
git clone https://github.com/yalcinkadir/institutional-trading-engine.git
cd institutional-trading-engine
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment Setup

Create `.env` locally or configure GitHub Secrets:

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

Market reports generate:

```text
Markdown report
Signal JSON / Markdown files
Scoring adjustment history when expectancy adjustments are used
```

Weekly reports are strategic-only and do not generate signals.

## Symbol Universe

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

Tests protect the universe from duplicate symbols, missing benchmark mappings and missing group metadata.

## Send Notifications

Central notification logic is implemented in:

```text
src/notifications.py
scripts/send_notification.py
docs/architecture/notifications.md
```

Dry-run example:

```bash
python scripts/send_notification.py \
  --message "communication test" \
  --telegram \
  --webhook \
  --dry-run
```

Send from file:

```bash
python scripts/send_notification.py \
  --message-file reports/weekly-expectancy-summary.txt \
  --telegram \
  --webhook
```

Missing Telegram or webhook config is non-fatal by default and returns structured `skipped` results.

## Run the Entry / Exit Watcher

```bash
python scripts/run_entry_exit_watcher.py \
  --signals-file reports/signals/latest-signals.json
```

The watcher runner now validates runtime configuration before execution:

- `POLYGON_API_KEY` must exist
- the configured signal file must exist
- the signal file must contain a JSON list
- every run prints a `WATCHER_CYCLE_ID`

## Configure Portfolio State for Governance

Live runtime governance reads portfolio risk state from:

```text
data/portfolio_state.json
```

Use the example file as a starting point:

```bash
cp data/portfolio_state.example.json data/portfolio_state.json
```

Documentation:

```text
docs/architecture/runtime_portfolio_state.md
```

The portfolio state is consumed by:

- kill switch checks
- drawdown risk limits
- daily-loss risk limits
- decision-log audit payloads
- runtime state / cache observability

Current limitation: the state is file-backed and must be updated by a caller, workflow or future broker/account integration. The system does not yet calculate account equity automatically from live broker execution data.

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

Historical validation uses Polygon daily aggregate bars and produces:

```text
reports/backtests/backtest_summary.json
```

Documentation:

```text
docs/architecture/historical_validation.md
```

## Generate Lifecycle-Aware Outcomes

```bash
python scripts/generate_outcomes.py --days 7
```

## Update Expectancy Report

```bash
python scripts/update_outcomes.py \
  --decision-log data/decision_log.csv \
  --output reports/expectancy-report.md
```

JSONL decision logs are also supported by the reader layer.

## Build Weekly Expectancy Summary

```bash
python scripts/build_weekly_expectancy_summary.py \
  --decision-log data/decision_log.csv \
  --output reports/weekly-expectancy-summary.txt
```

The weekly workflow is implemented in:

```text
.github/workflows/weekly-expectancy-feedback.yml
```

It can run manually or on the weekly schedule. Telegram/webhook delivery is routed through the central notification CLI.

## Run Tests

```bash
pytest
```

CI also runs the full test suite through:

```text
.github/workflows/ci.yml
```

---

# Repository Structure

```text
institutional-trading-engine/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── institutional-reports.yml
│       ├── entry-exit-watcher.yml
│       ├── outcome-tracking.yml
│       ├── weekly-expectancy-feedback.yml
│       └── daily-backup.yml
│
├── data/
│   ├── portfolio_state.example.json
│   ├── decision_log.csv
│   ├── decision_log.jsonl
│   ├── signal_lifecycle.jsonl
│   └── scoring_adjustment_history.json
│
├── docs/
│   ├── architecture/
│   │   ├── adaptive_scoring_feedback_loop.md
│   │   ├── historical_validation.md
│   │   ├── live_runtime_integration.md
│   │   ├── notifications.md
│   │   ├── runtime_loop.md
│   │   ├── runtime_portfolio_state.md
│   │   └── decision_log_store.md
│   └── roadmap/
│       └── connection-and-communication.md
│
├── reports/
│   ├── premarket/
│   ├── intraday/
│   ├── postmarket/
│   ├── weekly/
│   ├── signals/
│   ├── alerts/
│   ├── backtests/
│   ├── outcomes/
│   ├── weekly-expectancy-summary.txt
│   └── expectancy-report.md
│
├── scripts/
│   ├── generate_report.py
│   ├── run_entry_exit_watcher.py
│   ├── run_historical_validation.py
│   ├── send_notification.py
│   ├── build_weekly_expectancy_summary.py
│   ├── generate_outcomes.py
│   └── update_outcomes.py
│
├── src/
│   ├── bridge/
│   ├── core/
│   ├── data/
│   ├── governance/
│   ├── monitoring/
│   ├── network/
│   ├── optimization/
│   ├── orchestration/
│   ├── outcomes/
│   ├── reporting/
│   ├── runtime/
│   ├── scoring/
│   ├── signals/
│   ├── simulation/
│   ├── storage/
│   ├── strategy/
│   └── watchers/
│
└── tests/
```

---

# Architecture Reality Check

The repository contains many institutional intelligence modules.

Not all modules are fully integrated into a single live, continuously running production pipeline yet.

Current state:

| Layer | Status |
|---|---|
| Report Automation | Implemented |
| Premarket / Intraday / Postmarket / Weekly Reports | Implemented |
| Machine-Readable Signals | Implemented |
| Expanded Symbol Universe | Implemented |
| Central Notification Client | Implemented |
| Notification CLI | Implemented |
| Weekly Workflow Notification Migration | Implemented |
| Entry / Exit Watcher | Implemented and workflow-hardened |
| Watcher Runtime Validation | Implemented |
| Watcher Telegram Success Alerts | Implemented |
| Watcher Telegram Failure Alerts | Implemented |
| Alerts Persistence | Implemented |
| Signal Lifecycle JSONL | Implemented |
| Lifecycle-Aware Outcomes | Implemented |
| Historical Polygon Validation | Implemented |
| Weekly Expectancy Feedback Workflow | Implemented |
| Entry-Type Expectancy Profiles | Implemented |
| Expectancy-Based Score Adjustment | Implemented |
| Scoring Adjustment Audit History | Implemented |
| Runtime Loop | Implemented |
| Decision Persistence | Implemented |
| File-Backed Portfolio State | Implemented |
| Portfolio-State Governance Integration | Implemented |
| CI Pytest Workflow | Implemented |
| End-to-End Institutional Flow | Partially implemented |
| Fully Unified Continuous Runtime | In progress |
| Watcher Notification Migration to CLI | Planned |
| Broker / Account Auto-Sync | Not implemented |
| Broker Execution | Not implemented |
| Streaming Intraday Data | Not implemented |
| Dashboard UI | Not implemented |

---

# Notification and Communication Layer

The central communication layer is implemented through:

```text
src/notifications.py
scripts/send_notification.py
```

Supported channels:

- Telegram `sendMessage`
- generic webhook POST via `REPORT_WEBHOOK_URL`

Delivery results are structured:

```text
delivered | skipped | dry_run | failed
```

Design rules:

- missing secrets do not crash workflows by default
- delivery failures are returned as structured results
- strict mode is available for future hard-failure workflows
- real network calls are mockable in tests

Current migrated workflow:

```text
.github/workflows/weekly-expectancy-feedback.yml
```

Next migration target:

```text
.github/workflows/entry-exit-watcher.yml
```

---

# Historical Validation

Historical validation is implemented through:

```text
src/data/polygon_client.py
src/historical_validation.py
scripts/run_historical_validation.py
```

It fetches Polygon daily aggregate bars, validates BacktestSignal-like inputs and writes machine-readable summaries.

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

Tests use mocked historical bars and do not require real Polygon network calls.

---

# Weekly Expectancy Feedback

Weekly expectancy feedback is implemented through:

```text
src/expectancy_feedback_summary.py
scripts/build_weekly_expectancy_summary.py
.github/workflows/weekly-expectancy-feedback.yml
```

The workflow:

- runs every Sunday at 08:00 UTC
- can be started manually with `workflow_dispatch`
- refreshes outcomes when `POLYGON_API_KEY` is available
- still generates a report from existing logs when Polygon credentials are missing
- writes `reports/expectancy-report.md`
- writes `reports/weekly-expectancy-summary.txt`
- commits changed report outputs
- uploads artifacts
- sends Telegram/webhook summary through the central notification CLI

---

# Entry / Exit Watcher

The watcher is implemented in:

```text
src/watchers/entry_exit_watcher.py
scripts/run_entry_exit_watcher.py
```

The core watcher logic is pure and testable. It does not fetch market data directly.

The CLI runner is responsible for:

```text
latest-signals.json
→ Polygon daily bars
→ watcher evaluation
→ alerts
→ lifecycle JSONL
→ updated latest-signals.json
```

The workflow is implemented in:

```text
.github/workflows/entry-exit-watcher.yml
```

Current watcher hardening:

- explicit signal-file resolution
- `WATCHER_CYCLE_ID` for every run
- fail-fast validation for missing `POLYGON_API_KEY`
- fail-fast validation for missing or invalid signal files
- alert artifacts uploaded even on failure where possible
- Telegram success alerts only after successful execution
- Telegram failure alerts on workflow failure when secrets are configured

Current watcher events:

```text
ENTRY_TRIGGERED
STOP_HIT
TARGET_1_HIT
TARGET_2_HIT
EXPIRED
```

Conservative backtest rule:

```text
If a single price bar touches both stop and target, STOP_HIT is evaluated first.
```

This avoids optimistic backtest bias.

Generated files:

```text
reports/alerts/YYYY-MM-DD-alerts.json
reports/alerts/latest-alerts.json
data/signal_lifecycle.jsonl
```

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
  ↓ JSONL persistence including portfolio_state
runtime_state.update()
  ↓ cycle state
in_memory_state_cache.set()
  ↓ latest runtime access
```

Governance always runs before institutional decision creation.

If governance blocks a cycle:

```text
- no decision snapshot is produced
- no exposure decision is persisted
- a governance block event is persisted for auditability
- the portfolio state used for the block is persisted in the block payload
```

---

# Persistence Strategy

The project currently uses repository-based persistence.

Important persisted outputs:

```text
reports/
data/
```

Key persisted files:

```text
reports/signals/*.json
reports/alerts/*.json
reports/backtests/backtest_summary.json
reports/outcomes/*.json
reports/expectancy-report.md
reports/weekly-expectancy-summary.txt
data/portfolio_state.json
data/portfolio_state.example.json
data/decision_log.csv
data/decision_log.jsonl
data/signal_lifecycle.jsonl
data/scoring_adjustment_history.json
```

Current persistence style:

```text
Git repository + JSON / JSONL / CSV files
```

Future production target:

```text
Postgres-backed institutional persistence
```

The current Git-based approach is useful because it provides:

- audit trail
- versioned signal history
- reproducibility
- easy inspection
- simple GitHub Actions integration

But it is not the final production-grade storage layer.

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

## CI Workflow

Implemented in:

```text
.github/workflows/ci.yml
```

Responsibilities:

- install Python dependencies
- run `pytest`
- verify runtime, governance, watcher, outcome and reporting behavior

## Entry / Exit Watcher Workflow

Schedule:

```text
15:00 UTC   First intraday check
17:30 UTC   Mid-session check
21:00 UTC   Postmarket lifecycle check
```

Responsibilities:

- validate runtime configuration
- load latest signals
- check entry/stop/target events
- update signal statuses
- write alerts
- append lifecycle events
- commit reports/signals, reports/alerts and data
- send Telegram alert summary if configured
- send Telegram failure alert if configured

## Outcome Tracking Workflow

Schedule:

```text
02:00 UTC daily
```

Responsibilities:

- generate lifecycle-aware outcomes
- update expectancy report
- commit outcome files and data
- upload artifacts

The workflow is robust against missing decision logs.

It prefers:

```text
data/decision_log.csv
```

and can fall back to:

```text
data/decision_log.jsonl
```

## Weekly Expectancy Feedback Workflow

Schedule:

```text
08:00 UTC Sundays
```

Responsibilities:

- update expectancy report
- build compact weekly feedback summary
- commit changed outputs
- upload artifacts
- send optional Telegram/webhook summary through `scripts/send_notification.py`

---

# Decision Safety Architecture

One of the most important architectural principles:

```text
High scores alone are NOT enough.
```

The platform includes risk and override logic.

Purpose:
Prevent dangerous recommendations even when setup scores are high.

Governance inputs now include:

- VIX context where available
- portfolio drawdown from `data/portfolio_state.json`
- daily loss from `data/portfolio_state.json`
- severe anomaly count where supplied

Important behavior:

- missing VIX is not treated as falsely calm
- missing portfolio state is non-fatal but visibly warned
- corrupt portfolio state fails explicitly
- governance-block events are persisted for auditability

---

# VIX Handling

VIX is used as a risk context input.

Current scanner implementation attempts to fetch:

```text
I:VIX
```

If VIX is unavailable, the system should not crash.

Rules:

- scanner can continue with `vix_data = None`
- bridge uses conservative fallback assumptions
- governance does not treat missing VIX as falsely calm
- missing VIX should reduce confidence, not automatically block every signal
- degraded-data warnings are preserved for auditability

---

# Current Limitations

The system is stronger than a simple report generator, but it is not yet a fully institutional production platform.

Current limitations:

- no live broker execution
- no automatic broker/account portfolio sync yet
- portfolio state is file-backed and must be maintained by a caller/workflow/integration
- no real-time websocket watcher
- no streaming intraday bars in the core implementation
- historical validation uses daily bars only in the first implementation
- signal extraction into historical-validation input is not fully automated yet
- weekly expectancy quality depends on accumulated evaluated samples
- watcher notification migration to the central CLI is still planned
- Git-based persistence is not final production storage
- no dashboard UI yet
- no Postgres persistence yet
- no regime similarity memory yet
- no ML inference layer yet
- no full observability dashboard yet

Important:

```text
This project currently supports research, screening, alerting, lifecycle analysis, file-backed portfolio-state governance, central notifications, historical validation, weekly expectancy feedback and adaptive scoring.
It does not execute trades.
```

---

# Testing

Run all tests:

```bash
pytest
```

Useful targeted tests:

```bash
pytest tests/test_runtime_loop.py
pytest tests/test_decision_log_store.py
pytest tests/test_in_memory_state_cache.py
pytest tests/test_scanner_to_orchestrator_bridge.py
pytest tests/test_runtime_market_snapshot.py
pytest tests/test_live_runtime_cycle.py
pytest tests/test_live_runtime_cycle_portfolio_state.py
pytest tests/test_portfolio_state.py
pytest tests/test_historical_validation.py
pytest tests/test_polygon_client_historical_range.py
pytest tests/test_symbol_universe.py
pytest tests/test_notifications.py
pytest tests/test_expectancy_feedback_summary.py
pytest tests/test_scanner_market_snapshot_builder.py
pytest tests/test_end_to_end_institutional_flow.py
pytest tests/test_entry_exit_watcher.py
pytest tests/test_run_entry_exit_watcher_runtime_validation.py
pytest tests/test_expectancy_adjuster.py
pytest tests/test_decision_report_expectancy_integration.py
pytest tests/test_adjustment_history.py
```

Test coverage includes:

- governance
- portfolio-state governance integration
- expanded symbol universe integrity
- central notification client
- historical validation
- Polygon historical range fetcher behavior
- weekly expectancy feedback summary
- reporting
- signal generation
- entry/exit watcher logic
- watcher runtime validation
- lifecycle persistence
- outcome tracking
- adaptive expectancy
- expectancy-based score adjustment
- scoring adjustment history persistence
- runtime state handling
- decision persistence
- scanner-to-runtime bridge logic
- end-to-end institutional flow

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

For market intelligence and communication features, also require:

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
- Telegram success alerts for watcher events
- Telegram failure alerts for watcher failures
- alerts persistence
- lifecycle JSONL
- lifecycle-aware outcomes
- historical Polygon aggregate validation
- weekly expectancy feedback workflow
- entry-type expectancy profiles
- expectancy-based score adjustment
- scoring adjustment history
- runtime loop
- decision persistence
- VIX-aware runtime context
- governance-first runtime cycle
- file-backed portfolio state
- portfolio-state-backed governance
- portfolio-state documentation and example file
- minimal pytest CI workflow

## In Progress

- connection and communication hardening
- unified continuous runtime maturity
- operational observation of watcher stability across real scheduled runs

## Planned Next

1. Migrate entry-exit watcher notifications to the central notification CLI.
2. Add explicit `signal_id` to every generated signal.
3. Prevent duplicate lifecycle events for the same signal/event pair.
4. Add structured JSON logging.
5. Improve intraday data support with higher-frequency bars if Polygon plan allows.
6. Add dashboard or static HTML reporting.
7. Move long-term persistence from Git files to Postgres.
8. Add regime similarity memory.
9. Add scoring adjustment quality review.
10. Add adaptive scoring guardrails by market regime.
11. Add broker/account integration for automatic portfolio-state calculation.

## Known Limitations

- no broker execution
- no automatic broker/account portfolio sync yet
- no real-time websocket watcher
- no streaming intraday bars in the core implementation
- no dashboard UI
- no Postgres persistence
- historical validation uses daily bars only
- signal extraction into historical-validation input is not fully automated yet
- weekly expectancy quality depends on accumulated evaluated samples
- watcher notification migration to the central CLI is still planned

---

# Example End-to-End Day

```text
12:30 UTC — Premarket report
  → reports/premarket/YYYY-MM-DD-premarket.md
  → reports/signals/YYYY-MM-DD-signals.json
  → data/scoring_adjustment_history.json when adjustments are used

15:00 UTC — Intraday report + watcher
  → reports/intraday/YYYY-MM-DD-intraday.md
  → watcher validates runtime config
  → watcher checks entries and exits
  → reports/alerts/YYYY-MM-DD-alerts.json
  → data/signal_lifecycle.jsonl

17:30 UTC — Watcher check
  → additional entry/stop/target alerts if triggered

21:00 UTC — Postmarket report + watcher
  → reports/postmarket/YYYY-MM-DD-postmarket.md
  → updated signals
  → updated lifecycle
  → data/scoring_adjustment_history.json when adjustments are used

02:00 UTC — Outcome tracking
  → reports/outcomes/YYYY-MM-DD-outcomes.md/json
  → reports/expectancy-report.md

Sunday 08:00 UTC — Weekly expectancy feedback
  → reports/expectancy-report.md
  → reports/weekly-expectancy-summary.txt
  → optional Telegram/webhook summary through notification CLI
```

---

# License

Currently:

```text
All Rights Reserved
```

Until an open-source license is explicitly added.

---

# Disclaimer

This project is intended for:

- research
- education
- institutional analysis experiments
- systematic market screening
- signal lifecycle analysis
- adaptive scoring research

It is not financial advice.

It does not place trades.

Any trading or investment decision remains the responsibility of the user.
