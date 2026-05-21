# Entry / Stop / Exit Decision Quality Roadmap

Decision logic must work excellently. The system must not only produce signals; it must produce executable, explainable and falsifiable trade plans.

The most important rule:

```text
No BUY_WATCH without a complete and valid trade plan.
```

A complete trade plan requires:

```text
entry_trigger + entry_reason
stop_loss + stop_reason
target_1 + exit_reason
risk_reward validation
quality gate passed
```

---

## Current Baseline

Implemented so far:

- native `signal_id` generation
- watcher fallback identity for older signals
- lifecycle deduplication by `signal_id + event_type`
- central notification CLI
- structured runtime logs
- executable-level quality gate

The executable-level quality gate means:

```text
BUY_WATCH requires entry_trigger, stop_loss and target_1.
```

If those fields are incomplete, the signal is downgraded to:

```text
NO_TRADE
```

---

## P14 — Excellent Entry / Stop / Exit Decision Quality

### Goal

Make Entry / Stop Loss / Exit logic institutionally serious.

The engine should only produce actionable signals when the trade plan is:

- executable
- explainable
- risk-valid
- structure-aware
- test-covered
- falsifiable through outcomes and backtests

---

## P14.1 Trade Plan Validator

### Problem

Signal generation needs a central validator after levels are derived.

### Required Checks

- required levels exist
- entry, stop and target ordering is valid
- risk/reward is acceptable
- stop distance is acceptable
- entry is not already too late
- reasons exist for entry, stop and exit

### Acceptance Criteria

- Validator returns a structured result.
- Invalid trade plans downgrade to `NO_TRADE`.
- Validation reasons are persisted in notes or quality fields.
- Tests cover all validation failure modes.

---

## P14.2 Entry Quality Engine

### Required Entry Types

- breakout entry
- pullback entry
- retest entry
- gap-fill entry
- at-market only when explicitly allowed

### Acceptance Criteria

- Every `BUY_WATCH` has `entry_trigger` and `entry_type`.
- Every entry has `entry_reason`.
- Late entries are blocked or downgraded.
- Entry accounts for volatility and recent structure.
- Tests cover valid and invalid entry cases.

---

## P14.3 Stop-Loss Quality Engine

### Required Stop Models

- ATR stop
- recent swing low/high stop
- structure invalidation stop
- volatility-adjusted stop

### Acceptance Criteria

- Every `BUY_WATCH` has `stop_loss` and `stop_reason`.
- Long-signal stop must be below entry.
- Stop distance must not be too tight or too wide.
- Invalid stops downgrade to `NO_TRADE`.
- Tests cover too-tight, too-wide, inverted and valid stops.

---

## P14.4 Exit / Target Quality Engine

### Required Exit Models

- target_1 partial exit
- target_2 runner exit
- trailing stop after target_1
- time stop / expiry
- regime invalidation exit

### Acceptance Criteria

- Every `BUY_WATCH` has `target_1`.
- `target_2` is optional but must be valid if present.
- Target must be above entry for long signals.
- Risk/reward must meet configured minimum.
- Tests cover valid target, invalid target, low risk/reward and runner cases.

---

## P14.5 Entry / Stop / Exit Backtest Feedback

### Required Measurements

- entry hit rate
- stop hit before target
- target_1 hit rate
- target_2 hit rate
- false breakout rate
- expired-without-entry rate
- results grouped by `entry_type` and `setup_type`

### Acceptance Criteria

- Reports include Entry / Stop / Exit statistics.
- Weekly expectancy includes entry-type breakdown.
- Poor entry types can reduce future score or downgrade setups.

---

## Implementation Order

```text
1. Trade Plan Validator
2. Entry Quality Engine
3. Stop-Loss Quality Engine
4. Exit / Target Quality Engine
5. Entry/Stop/Exit Backtest Feedback
6. README + architecture documentation after every patch
```

---

## Non-Goals

- broker execution
- live order placement
- full ML prediction engine
- dashboard UI

---

## Operating Rule

From this point forward, a signal is not good because it has a high score.

A signal is only actionable when:

```text
score + regime + executable trade plan + risk validation
```

all pass together.
