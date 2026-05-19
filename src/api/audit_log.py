from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path


AUDIT_LOG_PATH = Path("logs/audit.log")


class AuditLogger:
    def __init__(self) -> None:
        AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    def log(self, event: str, details: str) -> None:
        timestamp = datetime.now(UTC).isoformat()

        line = f"{timestamp} | {event} | {details}\n"

        with AUDIT_LOG_PATH.open("a", encoding="utf-8") as file:
            file.write(line)


audit_logger = AuditLogger()
