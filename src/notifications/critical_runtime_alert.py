from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.notifications.telegram_report_dispatcher import (
    TelegramDispatchConfig,
    TelegramDispatchResult,
    TelegramDispatchStatus,
    TelegramReportMessage,
    TelegramTransport,
    dispatch_telegram_report,
    write_telegram_dispatch_result,
)

CRITICAL_ALERT_TYPES = {"STOP", "EXIT"}
CRITICAL_NOTIFICATION_FAILED_STATUS = "NOTIFICATION_FAILED"


class CriticalRuntimeAlertNotificationError(RuntimeError):
    """Raised when a critical STOP/EXIT alert cannot be delivered or persisted safely."""


@dataclass(frozen=True)
class CriticalRuntimeAlert:
    alert_type: str
    signal_id: str
    symbol: str
    reason: str
    lifecycle_status: str = "critical_runtime_alert"


@dataclass(frozen=True)
class CriticalRuntimeAlertDeliveryResult:
    alert_type: str
    signal_id: str
    symbol: str
    dispatch_status: str
    alert_result_path: str
    alert_persisted_before_repo: bool
    repository_persisted: bool
    repository_error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "alert_type": self.alert_type,
            "signal_id": self.signal_id,
            "symbol": self.symbol,
            "dispatch_status": self.dispatch_status,
            "alert_result_path": self.alert_result_path,
            "alert_persisted_before_repo": self.alert_persisted_before_repo,
            "repository_persisted": self.repository_persisted,
            "repository_error": self.repository_error,
        }


def build_critical_runtime_alert_message(alert: CriticalRuntimeAlert) -> TelegramReportMessage:
    alert_type = _normalize_alert_type(alert.alert_type)
    body = "\n".join(
        [
            f"Alert type: {alert_type}",
            f"Signal ID: {alert.signal_id}",
            f"Symbol: {alert.symbol.upper()}",
            f"Lifecycle status: {alert.lifecycle_status}",
            f"Reason: {alert.reason}",
            "Execution: none",
            "Repository persistence: after alert delivery only",
            "Real-money authorization: not granted",
        ]
    )
    return TelegramReportMessage(
        title=f"RGP5/RGP6 Critical {alert_type} Runtime Alert",
        body=body,
        report_type="critical_runtime_alert",
    )


def deliver_critical_runtime_alert_before_repo_persistence(
    alert: CriticalRuntimeAlert,
    *,
    alert_result_path: Path | str,
    repository_persistence: Callable[[], None] | None = None,
    config: TelegramDispatchConfig | None = None,
    transport: TelegramTransport | None = None,
    strict_notification: bool = True,
) -> CriticalRuntimeAlertDeliveryResult:
    """Dispatch and persist a critical STOP/EXIT alert before repository persistence.

    RGP5 requires critical lifecycle alerts to be delivered or persisted before any
    git commit/rebase/push style persistence can fail. RGP6 adds strict
    notification handling: notification delivery/persistence failures are not
    masked and repository persistence is not attempted after notification failure.
    """

    alert_type = _normalize_alert_type(alert.alert_type)
    message = build_critical_runtime_alert_message(alert)
    output_path = Path(alert_result_path)

    try:
        dispatch_result = dispatch_telegram_report(message, config=config, transport=transport)
        write_telegram_dispatch_result(dispatch_result, output_path)
    except Exception as exc:  # noqa: BLE001 - critical notification failure must be persisted then raised
        _write_critical_notification_failure(alert=alert, alert_result_path=output_path, error=exc)
        raise CriticalRuntimeAlertNotificationError(
            f"critical {alert_type} notification failed before repository persistence: {exc}"
        ) from exc

    if strict_notification and dispatch_result.status == TelegramDispatchStatus.BLOCKED:
        raise CriticalRuntimeAlertNotificationError(
            f"critical {alert_type} notification blocked by guardrails before repository persistence"
        )

    alert_persisted = output_path.exists()
    repository_persisted = False
    repository_error: str | None = None

    if repository_persistence is not None:
        try:
            repository_persistence()
            repository_persisted = True
        except Exception as exc:  # noqa: BLE001 - repository failure must be captured as evidence
            repository_error = str(exc)

    return CriticalRuntimeAlertDeliveryResult(
        alert_type=alert_type,
        signal_id=alert.signal_id,
        symbol=alert.symbol.upper(),
        dispatch_status=dispatch_result.status.value,
        alert_result_path=str(output_path),
        alert_persisted_before_repo=alert_persisted,
        repository_persisted=repository_persisted,
        repository_error=repository_error,
    )


def _normalize_alert_type(alert_type: str) -> str:
    normalized = str(alert_type).strip().upper()
    if normalized not in CRITICAL_ALERT_TYPES:
        raise ValueError("critical runtime alert type must be STOP or EXIT")
    return normalized


def _write_critical_notification_failure(
    *,
    alert: CriticalRuntimeAlert,
    alert_result_path: Path,
    error: Exception,
) -> None:
    alert_result_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "status": CRITICAL_NOTIFICATION_FAILED_STATUS,
        "sent": False,
        "alert_type": _normalize_alert_type(alert.alert_type),
        "signal_id": alert.signal_id,
        "symbol": alert.symbol.upper(),
        "error": str(error),
        "repository_persistence_attempted": False,
        "live_trading_authorization": "not_granted",
    }
    alert_result_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
