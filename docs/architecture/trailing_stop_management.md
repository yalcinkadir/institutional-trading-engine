# Trailing Stop and Partial Exit Management

P16 adds deterministic lifecycle management after `TARGET_1_HIT`.

The watcher does not execute broker orders. It updates signal state so downstream consumers can understand how the remaining runner position should be managed.

---

## Components

```text
src/watchers/trailing_stop_manager.py
src/watchers/entry_exit_watcher.py
```

Tests:

```text
tests/test_trailing_stop_manager.py
tests/test_entry_exit_watcher.py
```

---

## Trigger

Runner management is applied when the watcher detects:

```text
TARGET_1_HIT
```

The normal watcher status transition remains:

```text
TRIGGERED -> TARGET_1_HIT
```

After this transition, the updated signal state is enriched with partial-exit and runner fields.

---

## Default Rules

When target 1 is hit:

```text
partial_exit_ratio = 0.50
runner_status = active
stop_loss = max(existing_stop, entry_trigger)
trail_stop = stop_loss
partial_exit_completed = true
```

If `latest_high` and ATR are available:

```text
trail_candidate = latest_high - 1.5 * ATR
stop_loss = max(current_stop, entry_trigger, previous_trail_stop, trail_candidate)
trail_stop = stop_loss
```

The stop can only move upward for long signals. It never moves downward.

---

## Signal Fields

After `TARGET_1_HIT`, the updated signal can include:

```text
partial_exit_completed
partial_exit_ratio
runner_status
trail_stop
stop_adjustment_reason
```

Example:

```json
{
  "status": "TARGET_1_HIT",
  "partial_exit_completed": true,
  "partial_exit_ratio": 0.5,
  "runner_status": "active",
  "stop_loss": 104.5,
  "trail_stop": 104.5,
  "stop_adjustment_reason": "target_1_hit_breakeven_and_atr_trail"
}
```

---

## Duplicate Protection

Runner management is idempotent.

If a signal already has:

```text
partial_exit_completed = true
```

then the helper returns without creating another partial-exit state update.

Lifecycle JSONL deduplication still uses:

```text
signal_id + event_type
```

---

## Design Rules

- No broker execution.
- No real order placement.
- T1 hit activates runner state.
- Stop moves to at least breakeven.
- ATR trail can move the stop upward when high/ATR are available.
- Runner stop never moves downward.
- Updated signal state is persisted through the existing watcher signal-file update flow.

---

## Next Steps

Future improvements:

```text
separate PARTIAL_EXIT_FILLED lifecycle event
runner trail update on every later bar
regime invalidation exit
short-side trailing logic
```
