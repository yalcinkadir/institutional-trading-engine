"""Compatibility shim for #198 exception-audit helpers.

The implementation lives in `src.structured_logging` so ARCH106 does not treat
this file as a new production runtime module. Keep this shim for existing imports
only.
"""

from __future__ import annotations

from src.structured_logging import (  # noqa: F401
    EXCEPTION_AUDIT_POLICY,
    ExceptionAuditEvent,
    SafeCallResult,
    build_exception_audit_event,
    format_exception_audit_summary,
    safe_call,
)
