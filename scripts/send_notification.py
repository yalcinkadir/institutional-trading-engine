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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send runtime/workflow notification.")
    parser.add_argument("--message", help="Message text to send.")
    parser.add_argument("--message-file", help="Path to a text file containing the message.")
    parser.add_argument("--telegram", action="store_true", help="Send to Telegram.")
    parser.add_argument("--webhook", action="store_true", help="Send to generic REPORT_WEBHOOK_URL.")
    parser.add_argument("--dry-run", action="store_true", help="Do not send; return dry-run results.")
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

    client = NotificationClient(dry_run=args.dry_run)
    results = []

    if args.telegram:
        results.append(client.send_telegram(message))
    if args.webhook:
        results.append(client.send_webhook({"text": message}))

    for result in results:
        print(json.dumps(result.to_dict(), sort_keys=True))

    if args.strict and any(result.status == "failed" for result in results):
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
