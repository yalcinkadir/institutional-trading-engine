# Signal Identity and Lifecycle Deduplication

Signal lifecycle data is only trustworthy when every signal has a stable identity.

P12 makes `signal_id` native at signal creation time. The watcher still keeps fallback identity assignment for older signal files.

---

## Components

```text
src/signals/signal_identity.py
src/signals/signal_generator.py
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

Newly generated signals receive `signal_id` in:

```text
src/signals/signal_generator.py
```

The shared deterministic identity builder lives in:

```text
src/signals/signal_identity.py
```

When a signal already contains `signal_id`, it is preserved.

When an older signal is missing `signal_id`, the watcher generates one from the same stable signal fields:

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

The generated id is symbol-based and deterministic.

---

## Where `signal_id` Appears

`signal_id` is included in:

- generated signal JSON files
- generated signal Markdown files
- decision payloads used by reports
- updated signal files
- watcher alerts
- lifecycle JSONL events
- nested lifecycle signal payloads

Important files:

```text
reports/signals/YYYY-MM-DD-signals.json
reports/signals/YYYY-MM-DD-signals.md
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

Different lifecycle events for the same signal are still allowed.

---

## Design Rules

- Signal generation emits `signal_id` natively.
- Existing `signal_id` always wins.
- Missing older `signal_id` is generated deterministically by the watcher fallback.
- Watcher updates must preserve `signal_id`.
- Lifecycle events must include top-level `signal_id`.
- Deduplication must not block different event types for the same signal.
- Corrupt legacy lifecycle lines are ignored during dedup key loading.

---

## Current Limitation

The current signal id is deterministic from signal fields, including generation time and derived trading levels.

If the same setup is regenerated in another report cycle, it is treated as a new signal. That is intentional for report-cycle traceability.
