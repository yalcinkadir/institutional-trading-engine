"""Structured JSON logging helpers for runtime observability.

The helper intentionally stays lightweight:

- deterministic payload shape
- JSON-serializable output
- optional cycle/workflow context
- stdout JSON-line emission for GitHub Actions and local scripts
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any, TextIO


_VALID_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


@dataclass(frozen=True)
class StructuredLogEvent:
    timestamp: str
    level: str
    event_type: str
    component: str
    message: str
    cycle_id: str | None = None
    workflow_run_id: str | None = None
    workflow_run_attempt: str | None = None
    context: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, default=str)


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def build_structured_log_event(
    *,
    level: str,
    event_type: str,
    component: str,
    message: str,
    cycle_id: str | None = None,
    context: dict[str, Any] | None = None,
    timestamp: str | None = None,
) -> StructuredLogEvent:
    normalized_level = level.upper()
    if normalized_level not in _VALID_LEVELS:
        raise ValueError(f"Invalid log level: {level}")

    return StructuredLogEvent(
        timestamp=timestamp or utc_now_iso(),
        level=normalized_level,
        event_type=event_type,
        component=component,
        message=message,
        cycle_id=cycle_id,
        workflow_run_id=os.getenv("GITHUB_RUN_ID"),
        workflow_run_attempt=os.getenv("GITHUB_RUN_ATTEMPT"),
        context=context or {},
    )


def emit_structured_log(
    *,
    level: str,
    event_type: str,
    component: str,
    message: str,
    cycle_id: str | None = None,
    context: dict[str, Any] | None = None,
    stream: TextIO | None = None,
) -> StructuredLogEvent:
    event = build_structured_log_event(
        level=level,
        event_type=event_type,
        component=component,
        message=message,
        cycle_id=cycle_id,
        context=context,
    )
    output = stream or sys.stdout
    output.write(event.to_json() + "\n")
    output.flush()
    return event
