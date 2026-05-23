# Entry/Exit Watcher Health

P30 adds a diagnostic health layer around Entry/Exit Watcher artifacts.

It improves observability without broker integration.

---

## Purpose

The watcher health check verifies that signal and lifecycle artifacts are present, parseable and meaningful enough for Decision-Support review.

It does not execute trades.

---

## Local Command

```bash
python scripts/check_entry_exit_watcher_health.py \
  --signals-file reports/signals/latest-signals.json \
  --lifecycle-file data/signal_lifecycle.jsonl \
  --min-signals 1 \
  --min-lifecycle-events 1
```

Require at least one terminal event:

```bash
python scripts/check_entry_exit_watcher_health.py \
  --signals-file reports/signals/latest-signals.json \
  --lifecycle-file data/signal_lifecycle.jsonl \
  --min-signals 1 \
  --min-lifecycle-events 1 \
  --require-terminal-event
```

Outputs:

```text
reports/watcher/entry-exit-watcher-health.json
reports/watcher/entry-exit-watcher-health.md
```

---

## GitHub Actions Workflow

```text
Actions → Entry Exit Watcher Health → Run workflow
```

Recommended first run:

```text
signals_file: reports/signals/latest-signals.json
lifecycle_file: data/signal_lifecycle.jsonl
min_signals: 1
min_lifecycle_events: 1
require_terminal_event: false
```

Artifact:

```text
entry-exit-watcher-health-artifacts
```

---

## Gates

```text
signals_file_present_and_parseable
minimum_signals_loaded
lifecycle_file_present_and_parseable
minimum_lifecycle_events_loaded
no_malformed_lifecycle_lines
terminal_event_observed, only when require_terminal_event=true
```

---

## Report Summary

```text
healthy
signal_count
buy_watch_count
lifecycle_event_count
terminal_event_count
malformed_lifecycle_lines
lifecycle_event_types
gates
```

---

## Terminal Events

```text
STOP_HIT
TARGET_1_HIT
TARGET_2_HIT
EXPIRED
CANCELLED_BY_REGIME_CHANGE
REGIME_INVALIDATION_EXIT
```

---

## Interpretation

```text
healthy=false
```

means the watcher artifact chain is incomplete, malformed or operationally insufficient.

```text
healthy=true
```

means the observed artifacts passed the configured diagnostic gates.

It still does not authorize trading.

---

## Guardrail

```text
No broker integration.
No order placement.
No trading authorization.
No rewrite of watcher engine.
Diagnostics only.
```

---

## Why This Matters

Paper-live observation and readiness review depend on reliable lifecycle artifacts.

If watcher artifacts are missing, malformed or empty, later readiness reports may be technically generated but operationally weak.
