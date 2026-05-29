from __future__ import annotations

from dataclasses import dataclass

from src.config.paper_observation_universe import format_observation_universe
from src.notifications.telegram_report_dispatcher import TelegramReportMessage


@dataclass(frozen=True)
class PaperObservationNotification:
    report_date: str
    status: str = "STARTED"
    observation_mode: str = "paper_observation_only"
    include_universe: bool = True


def build_paper_observation_notification_message(
    notification: PaperObservationNotification,
) -> TelegramReportMessage:
    status = notification.status.strip().upper()
    if status not in {"STARTED", "COMPLETED", "FAILED"}:
        raise ValueError("status must be STARTED, COMPLETED or FAILED")

    body_lines = [
        f"Status: {status}",
        f"Report date: {notification.report_date}",
        f"Observation mode: {notification.observation_mode}",
        "Scope: B1.1 daily paper observation discipline",
        "Execution: none",
        "Real-money authorization: not granted",
    ]
    if notification.include_universe:
        body_lines.extend(["", "Observation universe:", format_observation_universe()])

    return TelegramReportMessage(
        title="B1.1 Paper Observation Notification",
        body="\n".join(body_lines),
        report_type="paper_observation_notification",
    )
