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
- communicates alerts and failures through a central notification layer
- emits structured JSON logs from operational scripts and runtime cycles
- produces machine-readable signal files with native `signal_id`
- prevents fake actionable signals without executable trade levels
- derives entry triggers through a deterministic Entry Quality Engine
- validates trade plans before allowing `BUY_WATCH`
- prioritizes excellent Entry / Stop Loss / Exit decision quality
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
→ Signal generation with native signal_id
→ Entry Quality Engine
→ Trade Plan Validator
→ Entry / Stop / Exit quality validation
→ Entry / Exit monitoring
→ Central notification delivery
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
- the signal file must contain a JSON list or generated object payload with `signals[]`
- every run prints a `WATCHER_CYCLE_ID`
- structured log events include `WATCHER_CYCLE_ID` as `cycle_id`
- native `signal_id` values are preserved
- missing legacy `signal_id` values are assigned deterministically as fallback
- lifecycle events are deduplicated by `signal_id` + `event_type`

Watcher workflow notifications are routed through:

```text
scripts/send_notification.py
```

The workflow sends watcher alert summaries and watcher failure messages through the same central CLI used by weekly expectancy feedback.

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
pytest tests/test_entry_quality.py
pytest tests/test_trade_plan_validator.py
pytest tests/test_signal_identity.py
pytest tests/test_signal_generator_identity.py
pytest tests/test_structured_logging.py
pytest tests/test_run_entry_exit_watcher_runtime_validation.py
pytest tests/test_entry_exit_watcher_workflow_notifications.py
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

# Signal Identity, Executability and Lifecycle Deduplication

Signal identity, signal executability and lifecycle deduplication are implemented in:

```text
src/signals/signal_identity.py
src/signals/entry_quality.py
src/signals/signal_generator.py
src/signals/trade_plan_validator.py
src/watchers/entry_exit_watcher.py
docs/architecture/signal_identity_lifecycle.md
docs/architecture/entry_quality_engine.md
docs/architecture/trade_plan_validator.md
```

Key behavior:

- newly generated signals include native `signal_id`
- `BUY_WATCH` requires a valid entry and long trade plan
- actionable signals include `entry_trigger`, `entry_type` and `entry_reason`
- Entry Quality supports breakout, pullback, retest, gap-fill and explicitly allowed at-market entries
- late breakout entries are rejected before reaching the watcher
- long trade plans validate entry, stop, target, ordering, risk/reward and ATR stop distance
- incomplete or invalid entries/trade plans downgrade the signal to `NO_TRADE`
- downgraded signals keep `signal_id`, context and explanatory notes
- downgraded signals use `position_size = 0.0`
- generated signal JSON files include `signal_id` and `entry_reason`
- generated signal Markdown files include `signal_id` and entry reason
- decision payloads used by reports include `signal_id`
- existing `signal_id` values are preserved
- missing older `signal_id` values are generated deterministically by the watcher fallback
- watcher alerts include `signal_id`
- lifecycle JSONL records include top-level `signal_id`
- updated signal files preserve `signal_id`
- duplicate lifecycle events are skipped by `(signal_id, event_type)`
- different event types for the same signal are still allowed

---

# Entry / Stop / Exit Decision Quality

The roadmap is documented in:

```text
docs/roadmap/entry-stop-exit-quality.md
```

Implemented foundation:

```text
src/signals/entry_quality.py
src/signals/trade_plan_validator.py
```

Operating rule:

```text
A high setup score is not enough.
A BUY_WATCH requires a complete, valid and explainable trade plan.
```

A complete trade plan requires:

```text
entry_trigger + entry_reason
stop_loss + stop_reason
target_1 + exit_reason
risk_reward validation
quality gate passed
```

Current Entry Quality checks:

```text
breakout entry
pullback entry
retest entry
gap-fill entry
explicit at-market entry only when allowed
late breakout rejection
missing close / ATR rejection
```

Current Trade Plan Validator checks:

```text
entry_trigger exists
stop_loss exists
target_1 exists
stop_loss < entry_trigger
target_1 > entry_trigger
target_2 > target_1 when present
risk_reward >= minimum threshold
stop distance is not too tight or too wide when ATR is available
```

Planned next modules:

- Stop-Loss Quality Engine
- Exit / Target Quality Engine
- Entry/Stop/Exit backtest feedback grouped by entry_type and setup_type

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

---

# Notification and Communication Layer

Central notification logic is implemented in:

```text
src/notifications.py
scripts/send_notification.py
docs/architecture/notifications.md
```

Supported channels:

- Telegram delivery
- generic webhook POST via `REPORT_WEBHOOK_URL`

Delivery results are structured:

```text
delivered | skipped | dry_run | failed
```

Migrated workflows:

```text
.github/workflows/weekly-expectancy-feedback.yml
.github/workflows/entry-exit-watcher.yml
```

Regression guard:

```text
tests/test_entry_exit_watcher_workflow_notifications.py
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
| Watcher Workflow Notification Migration | Implemented |
| Native Signal ID Generation | Implemented |
| Executable Signal Quality Gate | Implemented |
| Entry Quality Engine | Implemented |
| Trade Plan Validator | Implemented |
| Entry / Stop / Exit Quality Roadmap | Planned |
| Entry / Exit Watcher | Implemented and workflow-hardened |
| Watcher Runtime Validation | Implemented |
| Signal Identity Fallback | Implemented |
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

For Entry / Stop / Exit decision logic, also require:

```text
- complete executable trade plan
- explicit entry_reason, stop_reason and exit_reason
- risk/reward validation
- downgrade behavior for invalid plans
- tests for positive and negative cases
```

---

# Roadmap

## Done

- report automation
- signal generation
- native signal_id generation
- executable signal quality gate
- entry quality engine
- trade plan validator
- signal persistence
- expanded cross-asset symbol universe
- central notification client
- notification CLI
- structured runtime logging helper
- notification CLI structured logs
- watcher runner structured logs
- live runtime cycle structured logs
- weekly workflow notification migration
- watcher workflow notification migration
- Entry / Exit Watcher V1
- watcher runtime validation
- watcher workflow hardening
- signal identity fallback for legacy signals
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

- Entry / Stop / Exit decision quality hardening
- observability hardening
- connection and communication hardening
- unified continuous runtime maturity
- operational observation of watcher stability across real scheduled runs

## Planned Next

1. Implement Stop-Loss Quality Engine.
2. Implement Exit / Target Quality Engine.
3. Add Entry/Stop/Exit backtest feedback by entry_type and setup_type.
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
