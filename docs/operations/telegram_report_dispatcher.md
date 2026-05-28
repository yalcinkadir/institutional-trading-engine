# TG1 Telegram Report Dispatcher

TG1 delivers research and paper-observation reports to Telegram without enabling live trading.

## Purpose

The dispatcher is allowed to send:

- Daily Evidence summaries
- Backtest summaries
- Paper Observation summaries
- Execution Quality summaries
- Kill-Switch status summaries
- Risk and drift warnings

It is not allowed to send:

- live trading authorization
- order-action language
- order buttons
- broker execution links
- private thresholds
- private scoring weights
- proprietary setup rankings
- private edge parameters

## Required footer

Every message must include:

```text
Research / Paper Observation Only. No live trading authorization.
```

## CLI

Dry-run mode is the default safe mode:

```bash
python scripts/send_telegram_report.py \
  --report-file reports/daily_evidence/latest.md \
  --title "Daily Evidence" \
  --dry-run
```

Actual Telegram sending requires explicit `--send` plus environment variables:

```bash
export TELEGRAM_BOT_TOKEN=...
export TELEGRAM_CHAT_ID=...

python scripts/send_telegram_report.py \
  --report-file reports/daily_evidence/latest.md \
  --title "Daily Evidence" \
  --send
```

## Guardrails

The dispatcher blocks messages that contain:

- live-trading phrases
- order-action phrases
- auto-execution language
- private-edge terminology
- production/live threshold terminology
- messages without the research-only footer
- messages over the configured Telegram length limit

## CI-safe design

TG1 has an injectable transport. Tests use dry-run and in-memory transports, so CI does not require Telegram credentials or network access.

## Security notes

- `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` must stay in GitHub Actions secrets or local environment variables.
- Do not commit chat IDs, bot tokens or screenshots containing bot credentials.
- Do not include private edge parameters in Telegram report text.

## Non-goals

TG1 does not:

- place orders
- call a broker
- approve live trading
- create buy/sell instructions
- expose private strategy edge
