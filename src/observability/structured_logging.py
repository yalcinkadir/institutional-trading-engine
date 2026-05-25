from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class StructuredLogEvent:
    event: str
    level: str = "INFO"
    component: str = "institutional_trading_engine"
    message: str = ""
    fields: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": self.level.upper(),
            "component": self.component,
            "event": self.event,
        }
        if self.message:
            payload["message"] = self.message
        payload.update(_json_safe(self.fields))
        return payload

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, default=str)


def emit_structured_log(
    logger: logging.Logger,
    *,
    event: str,
    level: str = "INFO",
    component: str = "institutional_trading_engine",
    message: str = "",
    **fields: Any,
) -> None:
    log_event = StructuredLogEvent(
        event=event,
        level=level,
        component=component,
        message=message,
        fields=fields,
    )
    levelno = getattr(logging, level.upper(), logging.INFO)
    logger.log(levelno, log_event.to_json())


def configure_json_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(level=level, format="%(message)s")


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(item) for item in value]
    if hasattr(value, "to_dict"):
        return _json_safe(value.to_dict())
    if hasattr(value, "__dataclass_fields__"):
        return _json_safe(asdict(value))
    try:
        json.dumps(value)
        return value
    except TypeError:
        return str(value)
