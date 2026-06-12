from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from uuid import uuid4


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

    def to_dict(self) -> dict[str, str | None]:
        return asdict(self)


def build_exception_audit_event(
    exc: BaseException,
    *,
    stage: str,
    behavior: str,
    component: str | None = None,
    rationale: str | None = None,
    trace_id: str | None = None,
) -> dict[str, str | None]:
    event = ExceptionAuditEvent(
        stage=stage,
        error_class=type(exc).__name__,
        error_message=str(exc),
        behavior=behavior,
        trace_id=trace_id or uuid4().hex,
        timestamp_utc=datetime.now(UTC).replace(microsecond=0).isoformat(),
        component=component,
        rationale=rationale,
    )
    return event.to_dict()


def format_exception_audit_summary(event: dict[str, str | None]) -> str:
    return (
        f"{event.get('stage')}: {event.get('error_class')}: {event.get('error_message')} "
        f"[behavior={event.get('behavior')} trace_id={event.get('trace_id')}]"
    )
