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
from typing import Any, Callable, Generic, TextIO, TypeVar
from uuid import uuid4

T = TypeVar("T")

_VALID_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
EXCEPTION_AUDIT_POLICY = "EXPLICIT_EXCEPTION_AUDIT"


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


@dataclass(frozen=True)
class ExceptionAuditEvent:
    stage: str
    error_class: str
    error_message: str
    behavior: str
    trace_id: str
    timestamp_utc: str
    component: str | None = None
    rationale: str | None = None
    policy: str = EXCEPTION_AUDIT_POLICY
    severity: str = "DEGRADED"
    extra: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SafeCallResult(Generic[T]):
    ok: bool
    value: T
    audit_event: dict[str, Any]


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def build_exception_audit_event(
    exc: BaseException,
    *,
    stage: str,
    behavior: str = "structured_degraded_result",
    component: str | None = None,
    rationale: str | None = None,
    trace_id: str | None = None,
    severity: str = "DEGRADED",
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    event = ExceptionAuditEvent(
        stage=stage,
        error_class=type(exc).__name__,
        error_message=str(exc),
        behavior=behavior,
        trace_id=trace_id or uuid4().hex,
        timestamp_utc=utc_now_iso(),
        component=component,
        rationale=rationale,
        severity=severity,
        extra=dict(extra) if extra else None,
    )
    return event.to_dict()


def safe_call(
    func: Callable[[], T],
    *,
    stage: str,
    component: str,
    fallback_value: T,
    trace_id: str | None = None,
    severity: str = "DEGRADED",
    behavior: str = "structured_degraded_result",
    rationale: str | None = None,
    extra: dict[str, Any] | None = None,
) -> SafeCallResult[T]:
    try:
        return SafeCallResult(ok=True, value=func(), audit_event={})
    except Exception as exc:  # noqa: BLE001 - #198 converts broad failures into structured audit metadata.
        return SafeCallResult(
            ok=False,
            value=fallback_value,
            audit_event=build_exception_audit_event(
                exc,
                stage=stage,
                behavior=behavior,
                component=component,
                rationale=rationale,
                trace_id=trace_id,
                severity=severity,
                extra=extra,
            ),
        )


def format_exception_audit_summary(event: dict[str, Any]) -> str:
    return (
        f"{event.get('stage')}: {event.get('error_class')}: {event.get('error_message')} "
        f"[behavior={event.get('behavior')} trace_id={event.get('trace_id')}]"
    )


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
