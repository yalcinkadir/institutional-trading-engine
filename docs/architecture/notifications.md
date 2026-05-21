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
| `TELEGRAM_BOT_TOKEN` | Telegram bot token for `sendMessage` |
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

## Current Workflow Integration

The first migrated workflow is:

```text
.github/workflows/weekly-expectancy-feedback.yml
```

It now calls:

```bash
python scripts/send_notification.py \
  --message-file reports/weekly-expectancy-summary.txt \
  --telegram \
  --webhook
```

The next migration target is:

```text
.github/workflows/entry-exit-watcher.yml
```

---

## Design Rules

- Notification delivery must not crash the trading/runtime pipeline by default.
- Real network calls must be mockable in tests.
- Missing secrets must be visible but non-fatal.
- Delivery results must be structured and loggable.
- Workflow shell code should call the Python CLI instead of duplicating HTTP logic.
