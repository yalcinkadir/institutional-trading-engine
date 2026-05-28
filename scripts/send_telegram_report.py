#!/usr/bin/env python3
"""Send a research-only Telegram report."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from src.notifications.telegram_report_dispatcher import (
    HttpTelegramTransport,
    TelegramDispatchConfig,
    build_report_message_from_file,
    dispatch_telegram_report,
    write_telegram_dispatch_result,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send Telegram report in research-only mode")
    parser.add_argument("--report-file", required=True, help="Markdown/text report file to send")
    parser.add_argument("--title", required=True, help="Telegram report title")
    parser.add_argument("--report-type", default="research_report")
    parser.add_argument("--output-json", default="reports/telegram_dispatch/dispatch-result.json")
    parser.add_argument("--dry-run", action="store_true", default=False)
    parser.add_argument("--send", action="store_true", default=False, help="Actually send via Telegram transport")
    parser.add_argument("--max-body-chars", type=int, default=3500)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dry_run = not args.send or args.dry_run
    config = TelegramDispatchConfig(dry_run=dry_run, report_only=True)
    message = build_report_message_from_file(
        Path(args.report_file),
        title=args.title,
        report_type=args.report_type,
        max_body_chars=args.max_body_chars,
    )

    transport = None
    if not dry_run:
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        if not bot_token or not chat_id:
            raise SystemExit("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are required when --send is used")
        transport = HttpTelegramTransport(bot_token=bot_token, chat_id=chat_id)

    result = dispatch_telegram_report(message, config=config, transport=transport)
    write_telegram_dispatch_result(result, Path(args.output_json))

    print(f"Telegram dispatch status: {result.status.value}")
    print(f"Sent: {result.sent}")
    print(f"Findings: {len(result.findings)}")
    for finding in result.findings:
        print(f"{finding.severity.value.upper()} {finding.code}: {finding.match}")

    return 0 if result.status.value != "BLOCKED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
