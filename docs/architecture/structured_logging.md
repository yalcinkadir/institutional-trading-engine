# Structured Runtime Logging

Structured logging makes operational debugging and audit review easier than plain free-text logs.

The project uses a lightweight JSON-line logging helper for runtime scripts, workflows and future observability integrations.

---

## Components

```text
src/structured_logging.py
```

Key functions:

```text
build_structured_log_event()
emit_structured_log()
```

Operational integrations:

```text
scripts/send_notification.py
scripts/run_entry_exit_watcher.py
src/runtime/live_runtime_cycle.py
```

---

## Event Shape

Every structured log event has a deterministic payload shape:

```json
{
  "timestamp": "2026-05-21T07:30:00+00:00",
  "level": "INFO",
  "event_type": "notification_send_started",
  "component": "notification_cli",
  "message": "Notification delivery started.",
  "cycle_id": "optional-cycle-id",
  "workflow_run_id": "optional-github-run-id",
  "workflow_run_attempt": "optional-github-run-attempt",
  "context": {}
}
```

---

## Required Fields

| Field | Meaning |
|---|---|
| `timestamp` | UTC timestamp |
| `level` | `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL` |
| `event_type` | Machine-readable event type |
| `component` | Emitting component or script |
| `message` | Human-readable message |
| `context` | JSON-serializable event details |

Optional fields:

- `cycle_id`
- `workflow_run_id`
- `workflow_run_attempt`

---

## JSON-Line Output

`emit_structured_log()` writes one JSON object per line to stdout by default.

This is friendly for:

- GitHub Actions logs
- local shell output
- future log collectors
- file redirection

---

## Notification CLI Events

`scripts/send_notification.py` emits:

```text
notification_send_started
notification_send_completed
```

The completion event includes delivery result details from `NotificationResult`.

---

## Watcher Runner Events

`scripts/run_entry_exit_watcher.py` emits:

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

All watcher events use component:

```text
entry_exit_watcher_runner
```

and include `WATCHER_CYCLE_ID` as `cycle_id`.

---

## Live Runtime Events

`src/runtime/live_runtime_cycle.py` emits:

```text
live_runtime_cycle_started
live_runtime_governance_passed
live_runtime_governance_blocked
live_runtime_data_quality_warning
live_runtime_portfolio_state_warning
live_runtime_cycle_completed
```

All live runtime events use component:

```text
live_runtime_cycle
```

Governance-block logs include:

- block reason
- governance details
- VIX level where available
- portfolio drawdown
- daily loss
- portfolio state source

---

## Design Rules

- Logs must be JSON-serializable.
- Event shape must remain stable.
- Operational scripts should include `cycle_id` where available.
- Event types should be machine-readable and consistent.
- Do not hide delivery, governance or runtime failures inside unstructured text only.
- Keep existing human-readable logs where useful, but pair them with machine-readable structured events.

---

## Next Integration Targets

- migrate entry-exit watcher notification delivery to `scripts/send_notification.py`
- add structured logs to outcome tracking workflow scripts
- add structured logs to report generation scripts
