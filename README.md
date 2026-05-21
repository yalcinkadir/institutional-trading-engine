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
- normalizes scanner metrics before signal generation
- enriches signal metrics with confirmed 3-bar swing-low structure levels
- enriches signal metrics with intraday VWAP when intraday bars are available
- generates premarket, intraday, postmarket and weekly reports
- communicates alerts and failures through a central notification layer
- emits structured JSON logs from operational scripts and runtime cycles
- produces machine-readable signal files with native `signal_id`
- prevents fake actionable signals without executable trade levels
- derives entry triggers through a deterministic Entry Quality Engine
- validates breakout entries with high-trigger, RVOL and optional VWAP context
- derives stop losses through a deterministic Stop-Loss Quality Engine
- prefers valid swing-low structure stops before ATR fallback
- derives targets through a deterministic Exit / Target Quality Engine
- validates trade plans before allowing `BUY_WATCH`
- manages partial exits and runner stops after target 1
- invalidates active signals when the regime turns defensive / risk-off
- aggregates Entry / Stop / Exit feedback by decision-quality model
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
→ Scanner metrics normalization
→ Structure level enrichment
→ Intraday VWAP enrichment
→ Signal generation with native signal_id
→ Entry Quality Engine
→ Breakout context validation
→ Stop-Loss Quality Engine
→ Structure-aware stop selection
→ Exit / Target Quality Engine
→ Trade Plan Validator
→ Entry / Stop / Exit quality validation
→ Entry / Exit monitoring
→ Target 1 partial-exit and runner management
→ Regime invalidation exit
→ Central notification delivery
→ Structured operational logging
→ Deduplicated lifecycle tracking
→ Historical validation
→ Outcome evaluation
→ Entry / Stop / Exit feedback aggregation
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
- `TARGET_1_HIT` activates partial-exit and runner state
- `REGIME_INVALIDATION_EXIT` cancels active signals when regime turns defensive

## Run Tests

```bash
pytest
```

Targeted tests:

```bash
pytest tests/test_intraday_vwap.py
pytest tests/test_generate_report_intraday_vwap.py
pytest tests/test_regime_invalidation.py
pytest tests/test_entry_exit_watcher.py
pytest tests/test_entry_stop_exit_feedback.py
pytest tests/test_entry_stop_exit_report.py
pytest tests/test_structure_levels.py
pytest tests/test_generate_report_structure_enrichment.py
pytest tests/test_trailing_stop_manager.py
pytest tests/test_scanner_metrics_pipeline.py
pytest tests/test_generate_report_scanner_metrics_pipeline.py
pytest tests/test_exit_target_quality.py
pytest tests/test_stop_loss_quality.py
pytest tests/test_entry_quality.py
pytest tests/test_trade_plan_validator.py
pytest tests/test_signal_identity.py
pytest tests/test_signal_generator_identity.py
pytest tests/test_generate_report_signal_quality_merge.py
pytest tests/test_structured_logging.py
pytest tests/test_run_entry_exit_watcher_runtime_validation.py
pytest tests/test_entry_exit_watcher_workflow_notifications.py
pytest tests/test_live_runtime_cycle_portfolio_state.py
pytest tests/test_notifications.py
pytest tests/test_expectancy_feedback_summary.py
pytest tests/test_historical_validation.py
pytest tests/test_polygon_client_historical_range.py
pytest tests/test_symbol_universe.py
pytest tests/test_portfolio_state.py
```

---

# Scanner-to-Signal Metrics Pipeline

Implemented in:

```text
src/scanner.py
src/signals/scanner_metrics_pipeline.py
src/signals/structure_levels.py
src/signals/intraday_vwap.py
scripts/generate_report.py
docs/architecture/scanner_to_signal_pipeline.md
docs/architecture/intraday_vwap_support.md
```

Required signal metrics:

```text
close
atr14
```

Optional metrics preserved when available:

```text
atr_pct
entry
entry_type
stop_loss
exit_1
exit_2
high
low
volume
rvol
vwap
swing_low_3bar
```

Pipeline behavior:

- scanner output is normalized before `build_signals()`
- report generation enriches metrics with `swing_low_3bar` when bar lows are available
- report generation enriches metrics with VWAP when intraday bars are available
- `NaN`, `inf`, invalid values and missing values become `None`
- missing symbols and incomplete metrics are reported through diagnostics
- report generation prints warnings such as `scanner_metrics_missing:NVDA`
- missing scanner data is non-fatal but visible
- missing intraday data is non-fatal
- valid scanner metrics can produce non-null `close`, `entry_trigger`, `stop_loss` and `target_1`
- breakout context metrics `high`, `rvol` and `vwap` are preserved when available

---

# Signal Identity, Executability and Lifecycle Deduplication

Implemented in:

```text
src/signals/signal_identity.py
src/signals/entry_quality.py
src/signals/stop_loss_quality.py
src/signals/exit_target_quality.py
src/signals/structure_levels.py
src/signals/intraday_vwap.py
src/signals/signal_generator.py
src/signals/trade_plan_validator.py
src/watchers/entry_exit_watcher.py
src/watchers/trailing_stop_manager.py
src/watchers/regime_invalidation.py
docs/architecture/signal_identity_lifecycle.md
docs/architecture/entry_quality_engine.md
docs/architecture/stop_loss_quality_engine.md
docs/architecture/exit_target_quality_engine.md
docs/architecture/trade_plan_validator.md
docs/architecture/trailing_stop_management.md
docs/architecture/regime_invalidation_exit.md
docs/architecture/intraday_vwap_support.md
```

Key behavior:

- newly generated signals include native `signal_id`
- `BUY_WATCH` requires a valid entry, valid stop, valid targets and valid long trade plan
- actionable signals include `entry_trigger`, `entry_type`, `entry_reason`, `stop_loss`, `stop_model`, `stop_reason`, `target_1`, `exit_model` and `exit_reason`
- Entry Quality supports breakout, pullback, retest, gap-fill and explicitly allowed at-market entries
- momentum breakout prefers `high * 1.001` when scanner high is available
- weak RVOL breakouts are rejected when `rvol` is below threshold
- breakouts below VWAP are rejected when `vwap` is available
- missing VWAP is non-fatal when intraday data is unavailable
- Stop-Loss Quality supports swing-low structure stops, ATR stops, pullback structure stops, retest structure stops, gap-fill stops and scanner-provided stops
- valid `swing_low_3bar` stops are preferred before ATR/setup fallback stops
- too-wide, missing or invalid swing lows fall back to ATR/setup stop logic
- Exit / Target Quality supports momentum, pullback, retest, gap-fill, scanner-provided and default risk targets
- after `TARGET_1_HIT`, partial exit is marked and runner state is activated
- after `TARGET_1_HIT`, stop moves to at least breakeven
- when high and ATR are available, runner trail uses `latest_high - 1.5 * ATR`
- runner stop never moves downward for long signals
- active `TRIGGERED` / `TARGET_1_HIT` signals can be cancelled by defensive regime
- regime invalidation emits `REGIME_INVALIDATION_EXIT` and terminal status `CANCELLED_BY_REGIME_CHANGE`
- late breakout entries are rejected before reaching the watcher
- scanner-provided stops are rejected if they are not below entry for long signals
- scanner-provided targets are rejected if `target_1 <= entry` or `target_2 <= target_1`
- long trade plans validate entry, stop, target, ordering, risk/reward and ATR stop distance
- incomplete or invalid entries/stops/targets/trade plans downgrade the signal to `NO_TRADE`
- generated signal JSON and Markdown include signal identity plus entry, stop and exit quality reasons
- duplicate lifecycle events are skipped by `(signal_id, event_type)`

---

# Entry / Stop / Exit Feedback

Implemented in:

```text
src/feedback/entry_stop_exit_feedback.py
src/feedback/entry_stop_exit_report.py
docs/architecture/entry_stop_exit_feedback.md
```

The feedback aggregator is source-agnostic. It can consume historical validation records, lifecycle outcome records, JSONL exports or future database rows.

It calculates:

```text
entry hit rate
stop hit rate
target_1 hit rate
target_2 hit rate
expired-without-entry rate
false breakout rate
```

Grouped by:

```text
entry_type
setup_type
stop_model
exit_model
```

Output helpers can persist:

```text
entry-stop-exit-feedback.json
entry-stop-exit-feedback.md
```

This does not introduce new trading rules. It measures whether existing decision-quality models work historically.

---

# Entry / Stop / Exit Decision Quality

Roadmap:

```text
docs/roadmap/entry-stop-exit-quality.md
```

Implemented foundation:

```text
src/signals/entry_quality.py
src/signals/stop_loss_quality.py
src/signals/exit_target_quality.py
src/signals/structure_levels.py
src/signals/intraday_vwap.py
src/signals/trade_plan_validator.py
src/watchers/trailing_stop_manager.py
src/watchers/regime_invalidation.py
src/feedback/entry_stop_exit_feedback.py
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
runner management after target_1
regime invalidation monitoring
```

Current Entry Quality checks:

```text
breakout high-trigger
breakout RVOL confirmation
optional breakout VWAP filter
intraday VWAP enrichment when bars are available
pullback entry
retest entry
gap-fill entry
explicit at-market entry only when allowed
late breakout rejection
missing close / ATR rejection
```

Current Stop-Loss Quality checks:

```text
swing-low structure stop
ATR stop fallback
pullback structure stop
retest structure stop
gap-fill stop
scanner-provided stop validation
missing entry / close / ATR rejection
inverted scanner stop rejection
```

Current Exit / Target Quality checks:

```text
momentum targets
pullback targets
retest targets
gap-fill targets
scanner-provided target validation
default risk targets
invalid / inverted target rejection
```

Current Runner Management:

```text
TARGET_1_HIT
partial_exit_completed = true
partial_exit_ratio = 0.50
runner_status = active
stop_loss = max(existing_stop, entry_trigger, latest_high - 1.5 * ATR when available)
trail_stop = stop_loss
```

Current Regime Invalidation:

```text
risk-off / defensive regime
active BUY_WATCH signal
TRIGGERED or TARGET_1_HIT
→ REGIME_INVALIDATION_EXIT
→ CANCELLED_BY_REGIME_CHANGE
```

Current Feedback Checks:

```text
entry hit rate by entry_type/setup_type
stop hit rate by stop_model
target hit rate by exit_model
expired-without-entry rate
false breakout rate
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

- regime-aware feedback grouping
- session-aware VWAP and intraday entry confirmation

---

# Architecture Reality Check

| Layer | Status |
|---|---|
| Report Automation | Implemented |
| Scanner-to-Signal Metrics Pipeline | Implemented |
| Intraday VWAP Support | Implemented |
| Structure-Aware Stops | Implemented |
| Breakout Entry Context Upgrade | Implemented |
| Trailing Stop / Partial Exit Management | Implemented |
| Regime Invalidation Exit | Implemented |
| Entry / Stop / Exit Feedback Aggregation | Implemented |
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
| Stop-Loss Quality Engine | Implemented |
| Exit / Target Quality Engine | Implemented |
| Trade Plan Validator | Implemented |
| Entry / Stop / Exit Quality Roadmap | In progress |
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
- scanner-to-signal metrics pipeline
- intraday VWAP support
- breakout entry context upgrade
- structure-aware stops
- trailing stop and partial exit management
- regime invalidation exit
- Entry / Stop / Exit feedback aggregation
- native signal_id generation
- executable signal quality gate
- entry quality engine
- stop-loss quality engine
- exit / target quality engine
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

1. Add regime-aware feedback grouping.
2. Add session-aware VWAP and intraday entry confirmation.
3. Add dashboard or static HTML reporting.
4. Move long-term persistence from Git files to Postgres.
5. Add regime similarity memory.
6. Add scoring adjustment quality review.
7. Add adaptive scoring guardrails by market regime.
8. Add broker/account integration for automatic portfolio-state calculation.

---

# Disclaimer

This project is intended for research, education, institutional analysis experiments, systematic market screening, signal lifecycle analysis and adaptive scoring research.

It is not financial advice and does not execute trades.
