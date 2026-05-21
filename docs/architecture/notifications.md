# Notification and Communication Layer

The notification layer centralizes outbound runtime and workflow communication.

It exists so GitHub Actions, runtime scripts and future operational tools do not duplicate shell-level `curl` logic for Telegram or webhooks.

---

## Components

```text
src/notifications.py
scripts/send_notification.py
```

`src/notifications.py` provides:

- `NotificationClient`
- `NotificationResult`
- Telegram `sendMessage` delivery
- generic webhook POST delivery
- dry-run mode
- structured delivery results
- non-fatal delivery failure handling

`scripts/send_notification.py` provides a CLI wrapper for GitHub Actions and manual tests.

---

## Environment Variables

| Variable | Purpose |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token for Telegram delivery |
| `TELEGRAM_CHAT_ID` | Telegram chat id |
| `REPORT_WEBHOOK_URL` | Optional generic webhook endpoint |

Missing configuration does not crash by default. The client returns a structured `skipped` result.

---

## CLI Usage

Send text directly:

```bash
python scripts/send_notification.py \
  --message "Weekly expectancy summary ready" \
  --telegram
```

Send from file:

```bash
python scripts/send_notification.py \
  --message-file reports/weekly-expectancy-summary.txt \
  --telegram \
  --webhook
```

Dry run:

```bash
python scripts/send_notification.py \
  --message "test" \
  --telegram \
  --webhook \
  --dry-run
```

Strict mode:

```bash
python scripts/send_notification.py \
  --message "test" \
  --telegram \
  --strict
```

Strict mode exits non-zero only for `failed` deliveries. Skipped deliveries remain non-fatal.

---

## Result Model

Every delivery returns a `NotificationResult`:

```json
{
  "channel": "telegram",
  "status": "delivered",
  "message": "Telegram notification delivered.",
  "status_code": 200,
  "error": null
}
```

Possible statuses:

| Status | Meaning |
|---|---|
| `delivered` | Sent successfully |
| `skipped` | Configuration missing or channel not configured |
| `dry_run` | Dry-run mode, no network call |
| `failed` | HTTP or exception failure |

---

## Current Workflow Integrations

Weekly expectancy feedback:

```text
.github/workflows/weekly-expectancy-feedback.yml
```

uses:

```bash
python scripts/send_notification.py \
  --message-file reports/weekly-expectancy-summary.txt \
  --telegram \
  --webhook
```

Entry/exit watcher:

```text
.github/workflows/entry-exit-watcher.yml
```

uses the same CLI for both success alerts and failure notifications:

```bash
python scripts/send_notification.py \
  --message-file reports/alerts/watcher-alert-summary.txt \
  --telegram \
  --webhook \
  --cycle-id "$WATCHER_CYCLE_ID"
```

```bash
python scripts/send_notification.py \
  --message-file reports/watcher-failure-message.txt \
  --telegram \
  --webhook \
  --cycle-id "${WATCHER_CYCLE_ID:-unknown}"
```

---

## Regression Guard

The watcher workflow migration is protected by:

```text
tests/test_entry_exit_watcher_workflow_notifications.py
```

The test checks that:

- the workflow uses `scripts/send_notification.py`
- alert and failure message files are passed via `--message-file`
- webhook delivery is supported
- direct Telegram HTTP calls are not reintroduced

---

## Design Rules

- Notification delivery must not crash the trading/runtime pipeline by default.
- Real network calls must be mockable in tests.
- Missing secrets must be visible but non-fatal.
- Delivery results must be structured and loggable.
- Workflow shell code should call the Python CLI instead of duplicating HTTP logic.
