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
- Entry Quality Engine
- Stop-Loss Quality Engine
- Exit / Target Quality Engine
- Trade Plan Validator
- Scanner-to-Signal Metrics Pipeline normalizer

The executable-level quality gate means:

```text
BUY_WATCH requires entry_trigger, stop_loss, target_1 and a valid quality gate result.
```

If those fields or quality gates are incomplete, the signal is downgraded to:

```text
NO_TRADE
```

---

## Immediate Operational Priority

### P15 — Scanner-to-Signal Data Pipeline Repair

#### Problem

If live `close` and `atr14` do not reach signal generation, Entry Quality fails with:

```text
entry_quality: missing_close
```

That makes the whole Entry / Stop / Exit stack operationally useless, even if the quality engines are correct.

#### Requirements

- Verify scanner output contains `close`, `atr14`, `atr_pct` for every candidate.
- Verify bridge/orchestrator passes those fields into `scanner_metrics_map`.
- Add regression test: generated report candidate with scanner metrics must produce non-null `close`, `entry_trigger`, `stop_loss`, `target_1`.
- Add failure visibility when scanner metrics are missing.
- Do not silently produce empty scanner metrics for symbols that should have live data.

#### Acceptance Criteria

- At least one test proves scanner metrics reach `build_signals()` through the report path.
- Missing `close` / `atr14` is visible as a data-pipeline warning, not only as a downgraded signal note.
- Real report generation no longer produces all `NO_TRADE` solely because all `close` values are null when data is available.

#### Status

Implemented. CI verification pending.

---

## P14 — Excellent Entry / Stop / Exit Decision Quality

### Goal

Make Entry / Stop Loss / Exit logic institutionally serious.

The engine should only produce actionable signals when the trade plan is:

- executable
- explainable
- risk-valid
- structure-aware
- context-aware
- test-covered
- falsifiable through outcomes and backtests

---

## P14.1 Trade Plan Validator — Implemented

### Required Checks

- required levels exist
- entry, stop and target ordering is valid
- risk/reward is acceptable
- stop distance is acceptable
- reasons exist for entry, stop and exit

### Status

Implemented and CI-green.

---

## P14.2 Entry Quality Engine — Implemented

### Supported Entry Types

- breakout entry
- pullback entry
- retest entry
- gap-fill entry
- at-market only when explicitly allowed

### Status

Implemented and CI-green.

---

## P14.3 Stop-Loss Quality Engine — Implemented

### Supported Stop Models

- ATR stop
- pullback structure stop
- retest structure stop
- gap-fill stop
- scanner-provided stop

### Status

Implemented and CI-green.

---

## P14.4 Exit / Target Quality Engine — Implemented

### Supported Exit Models

- momentum targets
- pullback targets
- retest targets
- gap-fill targets
- scanner-provided targets
- default risk targets

### Status

Implemented and CI-green.

---

## P18A — Breakout Entry Context Upgrade

### Problem

Current breakout entry derivation is deterministic and ATR-based. That is testable, but it is still weak for excellent entry quality because it can ignore market context.

Current baseline:

```text
momentum_breakout entry = close + 0.5 ATR
```

This is acceptable as a fallback, but not as the preferred breakout trigger.

### Requirements

#### High-of-Day / Daily High Trigger

Use scanner-provided `high` as preferred breakout trigger when available:

```text
entry = high * 1.001
entry_type = breakout
entry_reason = breakout above recent high with 0.1% buffer
```

Fallback remains:

```text
entry = close + 0.5 ATR
```

#### Relative Volume Confirmation

For `momentum_breakout`, require enough volume context when `rvol` exists:

```text
if rvol < 0.8:
    reject insufficient_volume_for_breakout
```

If `rvol` is missing, do not silently pass as excellent; either downgrade or add a configurable fallback policy.

#### VWAP Context

VWAP should be supported as an optional strict filter when available:

```text
if vwap exists and close < vwap and setup_type == momentum_breakout:
    reject breakout_entry_below_vwap
```

Important: current daily scanner output does not reliably provide VWAP. VWAP requires either intraday bars or scanner enhancement. Therefore VWAP must be implemented as optional first and strict only when the data source is available.

### Acceptance Criteria

- Momentum breakout prefers `high * 1.001` over `close + 0.5 ATR` when `high` is available.
- Low `rvol` breakout is rejected with `insufficient_volume_for_breakout`.
- VWAP filter rejects breakout below VWAP when `vwap` is available.
- Missing VWAP does not crash entry generation.
- Tests cover high-trigger, ATR fallback, RVOL pass/fail, VWAP pass/fail and missing VWAP.

---

## P16 — Trailing Stop and Partial Exit Management

### Problem

Target levels exist, but the lifecycle engine does not yet manage the position after `TARGET_1_HIT`.

### Requirements

- After `target_1` hit, mark partial exit event.
- Support configurable partial exit ratio, default 50%.
- Move stop to breakeven or breakeven plus buffer after target_1 hit.
- Add ATR trailing stop for runner position.
- Persist updated stop in signal state.
- Deduplicate lifecycle events.

### Initial Trailing Rules

```text
After T1 hit:
partial_exit_ratio = 0.50
new_stop = max(existing_stop, entry_trigger)
runner_status = active
runner_trail = max(current_stop, latest_high - 1.5 * ATR)
```

### Acceptance Criteria

- Watcher records `TARGET_1_HIT` and a partial-exit lifecycle update.
- Updated signal state contains adjusted stop.
- Runner stop only moves upward for long signals.
- Tests cover T1 hit, breakeven stop move, ATR trail move and no duplicate partial-exit events.

---

## P17 — Structure-Aware Stops

### Problem

Current stops are deterministic and ATR-based, but not yet based on real market structure. The label `structure_stop` is only partially true until real pivots / swing lows are used.

### Requirements

- Detect recent 3-bar swing lows for long setups in scanner metrics.
- Preserve `swing_low_3bar` through the scanner-to-signal metrics pipeline.
- Use swing-low stop before ATR fallback when valid.
- Apply a wick/structure buffer below the swing low.
- Store `stop_model = swing_low_structure_stop` when used.
- Add support-zone / invalidation-level hooks for later enrichment.

### Initial Rule

```text
swing_low = scanner_metrics["swing_low_3bar"]
if swing_low and swing_low < entry_trigger:
    stop = swing_low * 0.998
    if (entry_trigger - stop) / atr <= 3.0:
        use swing_low_structure_stop
    else:
        fallback to ATR stop
```

### Acceptance Criteria

- Scanner can produce `swing_low_3bar`.
- Metrics pipeline preserves `swing_low_3bar`.
- Stop quality can choose a swing-low stop.
- Invalid or too-wide structure stops are rejected or ignored.
- Tests cover valid swing low, missing swing low and too-wide swing low stop.

---

## P18B — VWAP / Intraday Entry Timing Upgrade

### Problem

Entry Quality is deterministic, but not fully intraday-aware. P18A supports VWAP only when available. P18B makes VWAP/intraday timing a first-class data source.

### Requirements

- Add VWAP calculation from intraday bars where Polygon plan allows.
- Add close-above-VWAP confirmation for breakout setups.
- Add late-breakout rejection against VWAP/context, not only ATR extension.
- Add `entry_confirmation` fields.

### Acceptance Criteria

- Entry quality can attach `entry_confirmation`.
- Breakout entries can require price above VWAP when configured.
- Tests cover VWAP pass/fail and missing VWAP fallback.

---

## P20 — Regime Invalidation Exit

### Problem

Open positions and runner states are not yet force-exited when the broader regime invalidates the original thesis.

### Requirements

- Detect regime shift into `risk_off` / equivalent defensive state.
- Mark runner or open signal as regime-invalidated.
- Emit lifecycle event such as `REGIME_INVALIDATION_EXIT`.
- Do not duplicate the event.

### Acceptance Criteria

- Watcher or runtime cycle can close/invalidate active runner state on regime deterioration.
- Tests cover regime change, no-change and duplicate-event prevention.

---

## P19 — Short-Side Decision Path

### Problem

The current system is long-only. That limits hedge, downside and market-neutral use cases.

### Requirements

- Add short entry quality derivation.
- Add short stop quality derivation using stop above entry.
- Add short target quality derivation using targets below entry.
- Add validator support for short trade plans.

### Acceptance Criteria

- `SELL_WATCH` or equivalent short action can be generated.
- Short plan validates entry > target and stop > entry.
- Long and short validation paths are tested separately.

---

## P14.5 — Entry / Stop / Exit Backtest Feedback

### Required Measurements

- entry hit rate
- stop hit before target
- target_1 hit rate
- target_2 hit rate
- false breakout rate
- expired-without-entry rate
- results grouped by `entry_type`, `setup_type`, `stop_model`, `exit_model`

### Acceptance Criteria

- Reports include Entry / Stop / Exit statistics.
- Weekly expectancy includes entry-type and exit-model breakdown.
- Poor entry or exit models can reduce future score or downgrade setups.

---

## Updated Implementation Order

```text
1. Finish P15 CI verification and close scanner-to-signal data pipeline repair
2. P18A Breakout Entry Context Upgrade: high-trigger + RVOL + optional VWAP filter
3. P16 Trailing Stop and Partial Exit Management
4. P17 Structure-Aware Stops with 3-bar swing low
5. P14.5 Entry/Stop/Exit Backtest Feedback
6. P18B VWAP / Intraday Entry Timing Upgrade
7. P20 Regime Invalidation Exit
8. P19 Short-Side Decision Path
9. README + architecture documentation after every patch
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
score + regime + live data + executable trade plan + risk validation + lifecycle management
```

all pass together.
