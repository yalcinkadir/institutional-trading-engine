#!/usr/bin/env python3
"""Send a research-only B1.1 paper observation notification."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.notifications.paper_observation_notification import (  # noqa: E402
    PaperObservationNotification,
    build_paper_observation_notification_message,
)
from src.notifications.telegram_report_dispatcher import (  # noqa: E402
    HttpTelegramTransport,
    TelegramDispatchConfig,
    dispatch_telegram_report,
    write_telegram_dispatch_result,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send a B1.1 paper observation Telegram notification.")
    parser.add_argument("--report-date", required=True, help="Observation date YYYY-MM-DD.")
    parser.add_argument("--status", default="STARTED", choices=("STARTED", "COMPLETED", "FAILED"))
    parser.add_argument("--output-json", default="reports/telegram_dispatch/paper-observation-notification.json")
    parser.add_argument("--dry-run", action="store_true", default=False)
    parser.add_argument("--send", action="store_true", default=False, help="Actually send via Telegram transport.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dry_run = not args.send or args.dry_run
    message = build_paper_observation_notification_message(
        PaperObservationNotification(report_date=args.report_date, status=args.status)
    )

    transport = None
    if not dry_run:
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        if not bot_token or not chat_id:
            raise SystemExit("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are required when --send is used")
        transport = HttpTelegramTransport(bot_token=bot_token, chat_id=chat_id)

    result = dispatch_telegram_report(
        message,
        config=TelegramDispatchConfig(dry_run=dry_run, report_only=True),
        transport=transport,
    )
    write_telegram_dispatch_result(result, Path(args.output_json))

    print(f"Paper observation notification status: {result.status.value}")
    print(f"Sent: {result.sent}")
    print(f"Findings: {len(result.findings)}")
    for finding in result.findings:
        print(f"{finding.severity.value.upper()} {finding.code}: {finding.match}")

    return 0 if result.status.value != "BLOCKED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
