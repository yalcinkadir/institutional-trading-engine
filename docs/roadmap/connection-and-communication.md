# Connection and Communication Roadmap

The next operational focus is not more trading intelligence. It is reliable connection and communication.

The system must be able to communicate alerts, failures, summaries and operational states through a central, testable layer instead of scattered workflow-specific shell snippets.

---

## P7 — Harden Connection and Communication Layer

### Goal

Create a single notification foundation for runtime scripts and GitHub Actions.

### Implemented

- Central notification client in `src/notifications.py`
- Notification CLI in `scripts/send_notification.py`
- Telegram delivery support
- Generic webhook delivery support via `REPORT_WEBHOOK_URL`
- Dry-run mode
- Structured `NotificationResult`
- Non-fatal skipped delivery when configuration is missing
- Non-fatal failed delivery by default
- Optional strict mode for future hard-failure workflows
- Unit tests in `tests/test_notifications.py`
- Weekly expectancy workflow migrated to the central notification CLI
- Architecture documentation in `docs/architecture/notifications.md`

### Environment Variables

```text
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
REPORT_WEBHOOK_URL
```

### CLI Examples

```bash
python scripts/send_notification.py \
  --message "test" \
  --telegram \
  --dry-run
```

```bash
python scripts/send_notification.py \
  --message-file reports/weekly-expectancy-summary.txt \
  --telegram \
  --webhook
```

### Current Workflow Integration

Implemented:

```text
.github/workflows/weekly-expectancy-feedback.yml
```

Next migration target:

```text
.github/workflows/entry-exit-watcher.yml
```

---

## Planned Next Features

### P8 — Signal Identity and Lifecycle Deduplication

Problem:

Signals and lifecycle events need stronger identity guarantees so repeated watcher runs do not create ambiguous or duplicated lifecycle state.

Planned:

- Add deterministic `signal_id` to generated signals
- Use `signal_id` in lifecycle JSONL
- Prevent duplicate lifecycle events for the same signal/event pair
- Add tests for id stability and deduplication
- Update docs and README

### P9 — Structured Runtime Logging

Problem:

Operational debugging still depends too much on plain text logs.

Planned:

- Add structured JSON log helpers
- Include cycle ids consistently
- Include workflow ids where available
- Add runtime event types for scanner, watcher, governance, notification and expectancy
- Add tests for log payload shape

### P10 — Communication Migration Completion

Problem:

Some workflows still use direct shell/curl notification logic.

Planned:

- Migrate entry-exit watcher success alert to `scripts/send_notification.py`
- Migrate entry-exit watcher failure alert to `scripts/send_notification.py`
- Add reusable message templates
- Add notification dry-run job for manual verification

---

## Operating Rule

Every new operational feature should follow this sequence:

```text
Plan in roadmap / issue
Implement
Test
Document
Update README
Verify CI
```

No new runtime or communication feature is considered done until CI is green.
