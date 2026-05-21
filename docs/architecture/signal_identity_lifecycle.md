# Signal Identity and Lifecycle Deduplication

Signal lifecycle data is only trustworthy when every signal has a stable identity.

P8 introduces deterministic `signal_id` handling and duplicate lifecycle-event protection.

---

## Components

```text
src/watchers/entry_exit_watcher.py
```

Key functions:

```text
build_signal_id()
ensure_signal_identity()
append_lifecycle_updates()
```

---

## Signal ID Strategy

When a signal already contains `signal_id`, it is preserved.

When a signal is missing `signal_id`, the watcher generates one deterministically from stable signal fields:

```text
symbol
action
signal_date
generated_at
entry_trigger
stop_loss
target_1
target_2
valid_until
```

The generated format is symbol-based and deterministic:

```text
sig_<SYMBOL>_<short_hash>
```

---

## Where `signal_id` Appears

`signal_id` is included in:

- updated signal files
- watcher alerts
- lifecycle JSONL events
- nested lifecycle signal payloads

Important files:

```text
reports/signals/latest-signals.json
reports/alerts/latest-alerts.json
data/signal_lifecycle.jsonl
```

---

## Lifecycle Deduplication

Lifecycle writes are deduplicated by:

```text
(signal_id, event_type)
```

That means the same event is not appended twice for the same signal when the watcher is re-run.

Allowed:

```text
signal A + ENTRY_TRIGGERED
signal A + STOP_HIT
```

Skipped as duplicate:

```text
signal A + ENTRY_TRIGGERED
signal A + ENTRY_TRIGGERED
```

---

## Design Rules

- Existing `signal_id` always wins.
- Missing `signal_id` is generated deterministically.
- Watcher updates must preserve `signal_id`.
- Lifecycle events must include top-level `signal_id`.
- Deduplication must not block different event types for the same signal.
- Corrupt legacy lifecycle lines are ignored during dedup key loading.

---

## Current Limitation

The watcher now guarantees identity when it evaluates and persists signals.

Signal generation should still be upgraded later so newly generated signals already include `signal_id` before the watcher sees them.

Until then, watcher-side identity assignment provides backward-compatible protection.
