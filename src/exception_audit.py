from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any, Callable, Generic, TypeVar
from uuid import uuid4

T = TypeVar("T")

EXCEPTION_AUDIT_POLICY = "EXPLICIT_EXCEPTION_AUDIT"


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
        timestamp_utc=datetime.now(UTC).replace(microsecond=0).isoformat(),
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
