"""Compatibility exports for datafeed liveness helpers.

The implementation lives in `src.signals.scanner_metrics_pipeline`, which is the
ARCH106-classified runtime module on the report/signal path. This shim keeps
existing imports stable without adding a second production implementation.
"""

from __future__ import annotations

from src.signals.scanner_metrics_pipeline import (
    DATAFEED_BLOCKED,
    DATAFEED_DEGRADED,
    DATAFEED_OK,
    PROVIDER_FAILURE_EMPTY_RESPONSE,
    PROVIDER_FAILURE_MISSING_API_KEY,
    PROVIDER_FAILURE_PROVIDER_FORBIDDEN,
    PROVIDER_FAILURE_PROVIDER_LIMIT,
    PROVIDER_FAILURE_SCHEMA_MISMATCH,
    PROVIDER_FAILURE_UNKNOWN,
    DatafeedLivenessRecord,
    build_datafeed_liveness_record,
    write_datafeed_liveness_record,
)

__all__ = [
    "DATAFEED_BLOCKED",
    "DATAFEED_DEGRADED",
    "DATAFEED_OK",
    "PROVIDER_FAILURE_EMPTY_RESPONSE",
    "PROVIDER_FAILURE_MISSING_API_KEY",
    "PROVIDER_FAILURE_PROVIDER_FORBIDDEN",
    "PROVIDER_FAILURE_PROVIDER_LIMIT",
    "PROVIDER_FAILURE_SCHEMA_MISMATCH",
    "PROVIDER_FAILURE_UNKNOWN",
    "DatafeedLivenessRecord",
    "build_datafeed_liveness_record",
    "write_datafeed_liveness_record",
]
