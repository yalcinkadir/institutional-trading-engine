#!/usr/bin/env python3
"""Send notifications through the central notification client."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.notifications import NotificationClient
from src.structured_logging import emit_structured_log


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send runtime/workflow notification.")
    parser.add_argument("--message", help="Message text to send.")
    parser.add_argument("--message-file", help="Path to a text file containing the message.")
    parser.add_argument("--telegram", action="store_true", help="Send to Telegram.")
    parser.add_argument("--webhook", action="store_true", help="Send to generic REPORT_WEBHOOK_URL.")
    parser.add_argument("--dry-run", action="store_true", help="Do not send; return dry-run results.")
    parser.add_argument("--cycle-id", help="Optional operational cycle id for structured logs.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any requested delivery fails. Skipped deliveries remain non-fatal.",
    )
    return parser.parse_args()


def _resolve_message(args: argparse.Namespace) -> str:
    if args.message_file:
        return Path(args.message_file).read_text(encoding="utf-8")
    if args.message:
        return args.message
    raise ValueError("Either --message or --message-file is required.")


def main() -> int:
    args = parse_args()
    message = _resolve_message(args)

    if not args.telegram and not args.webhook:
        args.telegram = True

    requested_channels = []
    if args.telegram:
        requested_channels.append("telegram")
    if args.webhook:
        requested_channels.append("webhook")

    emit_structured_log(
        level="INFO",
        event_type="notification_send_started",
        component="notification_cli",
        message="Notification delivery started.",
        cycle_id=args.cycle_id,
        context={
            "channels": requested_channels,
            "dry_run": args.dry_run,
            "strict": args.strict,
            "message_source": "file" if args.message_file else "argument",
        },
    )

    client = NotificationClient(dry_run=args.dry_run)
    results = []

    if args.telegram:
        results.append(client.send_telegram(message))
    if args.webhook:
        results.append(client.send_webhook({"text": message}))

    for result in results:
        print(json.dumps(result.to_dict(), sort_keys=True))

    failed = any(result.status == "failed" for result in results)
    emit_structured_log(
        level="ERROR" if failed else "INFO",
        event_type="notification_send_completed",
        component="notification_cli",
        message="Notification delivery completed.",
        cycle_id=args.cycle_id,
        context={
            "results": [result.to_dict() for result in results],
            "failed": failed,
        },
    )

    if args.strict and failed:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
