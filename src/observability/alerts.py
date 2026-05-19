from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class Alert:
    level: str
    message: str
    created_at: str


@dataclass
class AlertManager:
    alerts: list[Alert] = field(default_factory=list)

    def trigger(self, level: str, message: str) -> Alert:
        alert = Alert(
            level=level,
            message=message,
            created_at=datetime.now(UTC).isoformat(),
        )

        self.alerts.append(alert)

        return alert

    def active_count(self) -> int:
        return len(self.alerts)


alert_manager = AlertManager()
