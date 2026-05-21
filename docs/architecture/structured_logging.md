# Structured Runtime Logging

Structured logging makes operational debugging and audit review easier than plain free-text logs.

P9 adds a lightweight JSON-line logging helper that can be used by runtime scripts, workflows and future observability integrations.

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

The first operational integration is:

```text
scripts/send_notification.py
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

Example:

```python
emit_structured_log(
    level="INFO",
    event_type="runtime_cycle_started",
    component="live_runtime_cycle",
    message="Runtime cycle started.",
    cycle_id="cycle-1",
    context={"symbols": 28},
)
```

---

## Notification CLI Integration

`scripts/send_notification.py` now emits structured events:

```text
notification_send_started
notification_send_completed
```

The completion event includes delivery result details from `NotificationResult`.

---

## Design Rules

- Logs must be JSON-serializable.
- Event shape must remain stable.
- Operational scripts should include `cycle_id` where available.
- Event types should be machine-readable and consistent.
- Do not hide delivery or runtime failures inside unstructured text only.

---

## Next Integration Targets

- `scripts/run_entry_exit_watcher.py`
- `src/runtime/live_runtime_cycle.py`
- governance block logging
- weekly expectancy feedback workflow cycle ids
