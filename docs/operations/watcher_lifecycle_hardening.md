# Watcher Lifecycle Hardening

Status date: 2026-05-27

This document defines the conservative lifecycle contract for Entry / Exit Watcher evaluation.

## Purpose

The watcher must not convert a stale `PENDING` setup into an active trade plan after its original stop boundary has already been breached.

This is a decision-support platform. No live broker execution is performed here.

## P0 Contract: Pending Invalidation Before Entry

For long-side `BUY_WATCH` signals:

```text
previous_status == PENDING
and latest bar low <= stop_loss
→ event_type = INVALIDATED_BEFORE_ENTRY
→ new_status = INVALIDATED_BEFORE_ENTRY
→ terminal state
```

The event is intentionally not named `STOP_HIT`, because no active trade has been triggered yet. The trade plan is invalidated before entry.

## Conservative Same-Bar Ordering

If a single bar touches both the stop boundary and the entry trigger while the signal is still pending, the stop-boundary breach wins.

```text
PENDING + low <= stop_loss + high >= entry_trigger
→ INVALIDATED_BEFORE_ENTRY
```

This avoids optimistic assumptions and prevents later activation of an already-invalid plan.

For active signals, stop still wins before targets:

```text
TRIGGERED + low <= stop_loss + high >= target_1
→ STOP_HIT
```

## Terminal Status

`INVALIDATED_BEFORE_ENTRY` is terminal.

A signal with this status must not later emit:

```text
ENTRY_TRIGGERED
TARGET_1_HIT
TARGET_2_HIT
STOP_HIT
```

## Runner Management After Target 1

When `TARGET_1_HIT` is detected, runner management is applied in the same watcher cycle using:

```text
latest_high = current bar high
atr = signal.atr14 or signal.atr
```

The runner stop is moved to at least breakeven and may be trailed upward by the ATR rule. This prevents delayed runner protection.

## Setup-Specific Exit Profiles

Exit target derivation now includes dedicated profiles for setup families where the generic default is conceptually too blunt:

```text
mean_reversion     → mean_reversion_targets
defensive_rotation → defensive_rotation_targets
```

Mean-reversion exits are quicker and ATR-capped. Defensive rotation exits are moderated and use an ATR floor.

## Regression Tests

Core tests live in:

```text
tests/test_entry_exit_watcher.py
tests/test_exit_target_quality.py
```

Required scenarios:

```text
pending long gap below stop → INVALIDATED_BEFORE_ENTRY
pending long same-bar entry and stop touch → INVALIDATED_BEFORE_ENTRY
invalidated signal never retriggers
triggered same-bar stop and target touch → STOP_HIT
TARGET_1_HIT uses high + atr14 immediately for runner stop
mean_reversion uses dedicated exit profile
defensive_rotation uses dedicated exit profile
```
