"""Central notification client for runtime and workflow communication.

The notification layer is deliberately small and defensive:

- missing configuration is treated as a skipped delivery, not a crash
- HTTP failures are returned as structured results
- callers can use dry-run mode for tests and local validation
- Telegram and generic webhook delivery share the same result model
"""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from typing import Any, Callable

import requests


@dataclass(frozen=True)
class NotificationResult:
    channel: str
    status: str
    message: str
    status_code: int | None = None
    error: str | None = None

    @property
    def delivered(self) -> bool:
        return self.status == "delivered"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class NotificationClient:
    """Send notifications to configured communication channels."""

    def __init__(
        self,
        *,
        telegram_bot_token: str | None = None,
        telegram_chat_id: str | None = None,
        webhook_url: str | None = None,
        timeout_seconds: int = 15,
        dry_run: bool = False,
        post: Callable[..., Any] | None = None,
    ) -> None:
        self.telegram_bot_token = telegram_bot_token if telegram_bot_token is not None else os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = telegram_chat_id if telegram_chat_id is not None else os.getenv("TELEGRAM_CHAT_ID")
        self.webhook_url = webhook_url if webhook_url is not None else os.getenv("REPORT_WEBHOOK_URL")
        self.timeout_seconds = timeout_seconds
        self.dry_run = dry_run
        self._post = post or requests.post

    def send_telegram(self, text: str) -> NotificationResult:
        if self.dry_run:
            return NotificationResult(
                channel="telegram",
                status="dry_run",
                message="Telegram notification skipped because dry_run=True.",
            )

        if not self.telegram_bot_token or not self.telegram_chat_id:
            return NotificationResult(
                channel="telegram",
                status="skipped",
                message="Telegram notification skipped because TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is missing.",
            )

        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        try:
            response = self._post(
                url,
                data={"chat_id": self.telegram_chat_id, "text": text},
                timeout=self.timeout_seconds,
            )
            if 200 <= int(response.status_code) < 300:
                return NotificationResult(
                    channel="telegram",
                    status="delivered",
                    message="Telegram notification delivered.",
                    status_code=int(response.status_code),
                )
            return NotificationResult(
                channel="telegram",
                status="failed",
                message="Telegram notification failed.",
                status_code=int(response.status_code),
                error=getattr(response, "text", None),
            )
        except Exception as exc:  # pragma: no cover - defensive boundary
            return NotificationResult(
                channel="telegram",
                status="failed",
                message="Telegram notification raised an exception.",
                error=f"{type(exc).__name__}: {exc}",
            )

    def send_webhook(self, payload: dict[str, Any]) -> NotificationResult:
        if self.dry_run:
            return NotificationResult(
                channel="webhook",
                status="dry_run",
                message="Webhook notification skipped because dry_run=True.",
            )

        if not self.webhook_url:
            return NotificationResult(
                channel="webhook",
                status="skipped",
                message="Webhook notification skipped because REPORT_WEBHOOK_URL is missing.",
            )

        try:
            response = self._post(
                self.webhook_url,
                json=payload,
                timeout=self.timeout_seconds,
            )
            if 200 <= int(response.status_code) < 300:
                return NotificationResult(
                    channel="webhook",
                    status="delivered",
                    message="Webhook notification delivered.",
                    status_code=int(response.status_code),
                )
            return NotificationResult(
                channel="webhook",
                status="failed",
                message="Webhook notification failed.",
                status_code=int(response.status_code),
                error=getattr(response, "text", None),
            )
        except Exception as exc:  # pragma: no cover - defensive boundary
            return NotificationResult(
                channel="webhook",
                status="failed",
                message="Webhook notification raised an exception.",
                error=f"{type(exc).__name__}: {exc}",
            )

    def send_text(self, text: str, *, include_webhook: bool = False) -> list[NotificationResult]:
        results = [self.send_telegram(text)]
        if include_webhook:
            results.append(self.send_webhook({"text": text}))
        return results
