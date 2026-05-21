# Institutional Trading Engine

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![CI](https://img.shields.io/badge/CI-pytest-brightgreen.svg)
![Status](https://img.shields.io/badge/status-production--oriented-orange.svg)

Institutional Trading Engine is a production-oriented market intelligence, screening, reporting, runtime orchestration, communication, observability, signal lifecycle and outcome-learning platform.

The system is **not** a black-box trading bot and does **not** place live trades.

It is designed as an institutional decision-support and research platform that:

- analyzes market regimes
- evaluates risk conditions
- ranks opportunities
- scans a diversified symbol universe across indices, sectors, bonds, commodities and leaders
- generates premarket, intraday, postmarket and weekly reports
- communicates alerts and summaries through a central notification layer
- emits structured JSON logs from operational scripts and runtime cycles
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
→ Structured operational logging
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

# Main Commands

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
- structured log events include `WATCHER_CYCLE_ID` as `cycle_id`
- missing `signal_id` values are assigned deterministically
- lifecycle events are deduplicated by `signal_id` + `event_type`

Watcher structured events include:

```text
watcher_runner_started
watcher_runtime_validation_succeeded
watcher_runtime_validation_failed
watcher_signals_loaded
watcher_no_actionable_signals
watcher_symbol_fetch_failed
watcher_evaluation_completed
watcher_events_persisted
watcher_no_events_detected
watcher_runner_completed
```

## Send Notifications

```bash
python scripts/send_notification.py \
  --message "communication test" \
  --telegram \
  --webhook \
  --dry-run \
  --cycle-id manual-test
```

```bash
python scripts/send_notification.py \
  --message-file reports/weekly-expectancy-summary.txt \
  --telegram \
  --webhook \
  --cycle-id weekly-expectancy
```

The notification CLI emits structured JSON events:

```text
notification_send_started
notification_send_completed
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
pytest tests/test_structured_logging.py
pytest tests/test_run_entry_exit_watcher_runtime_validation.py
pytest tests/test_live_runtime_cycle_portfolio_state.py
pytest tests/test_entry_exit_watcher.py
pytest tests/test_notifications.py
pytest tests/test_expectancy_feedback_summary.py
pytest tests/test_historical_validation.py
pytest tests/test_polygon_client_historical_range.py
pytest tests/test_symbol_universe.py
pytest tests/test_portfolio_state.py
```

---

# Structured Runtime Logging

Structured logging is implemented in:

```text
src/structured_logging.py
docs/architecture/structured_logging.md
```

Operational integrations:

```text
scripts/send_notification.py
scripts/run_entry_exit_watcher.py
src/runtime/live_runtime_cycle.py
```

Structured log events include:

```text
timestamp
level
event_type
component
message
cycle_id
workflow_run_id
workflow_run_attempt
context
```

Supported levels:

```text
DEBUG, INFO, WARNING, ERROR, CRITICAL
```

Live runtime structured events include:

```text
live_runtime_cycle_started
live_runtime_governance_passed
live_runtime_governance_blocked
live_runtime_data_quality_warning
live_runtime_portfolio_state_warning
live_runtime_cycle_completed
```

JSON-line output is designed for:

- GitHub Actions logs
- local debugging
- future log collection
- runtime audit review

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

# Architecture Reality Check

| Layer | Status |
|---|---|
| Report Automation | Implemented |
| Expanded Symbol Universe | Implemented |
| Central Notification Client | Implemented |
| Notification CLI | Implemented |
| Structured Runtime Logging Helper | Implemented |
| Notification CLI Structured Logs | Implemented |
| Watcher Runner Structured Logs | Implemented |
| Live Runtime Cycle Structured Logs | Implemented |
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

For market intelligence, lifecycle, observability and communication features, also require:

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
- structured runtime logging helper
- notification CLI structured logs
- watcher runner structured logs
- live runtime cycle structured logs
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

- observability hardening
- connection and communication hardening
- unified continuous runtime maturity
- operational observation of watcher stability across real scheduled runs

## Planned Next

1. Generate native `signal_id` at signal creation time.
2. Migrate entry-exit watcher notifications to the central notification CLI.
3. Improve intraday data support with higher-frequency bars if Polygon plan allows.
4. Add dashboard or static HTML reporting.
5. Move long-term persistence from Git files to Postgres.
6. Add regime similarity memory.
7. Add scoring adjustment quality review.
8. Add adaptive scoring guardrails by market regime.
9. Add broker/account integration for automatic portfolio-state calculation.

---

# Disclaimer

This project is intended for research, education, institutional analysis experiments, systematic market screening, signal lifecycle analysis and adaptive scoring research.

It is not financial advice and does not execute trades.
