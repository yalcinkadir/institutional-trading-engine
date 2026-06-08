"""Scanner-to-signal metrics pipeline helpers.

Signal quality engines require numeric `close` and `atr14` values. This module
normalizes scanner output before it is passed into signal generation and creates
visible diagnostics for missing required data.

DATA1 adds an explicit data-quality contract: market-data rows must carry
source/provenance and freshness metadata when they are used by production paths.
Missing metadata is not hidden behind a green no-op; it is surfaced as degraded
data-quality diagnostics so callers can block, degrade, report, or alert.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any


REQUIRED_SIGNAL_METRICS = ("close", "atr14")
REQUIRED_PROVENANCE_FIELDS = ("source", "source_timestamp", "fallback_level")
OPTIONAL_SIGNAL_METRICS = (
    "atr_pct",
    "entry",
    "entry_type",
    "stop_loss",
    "exit_1",
    "exit_2",
    "high",
    "low",
    "volume",
    "rvol",
    "vwap",
    "swing_low_3bar",
)
PROVENANCE_FIELDS = (
    "source",
    "source_timestamp",
    "fallback_level",
    "data_status",
)
MARKET_DATA_FAILURE_FIELDS = (
    "data_failure_kind",
    "data_failure_message",
    "provider_status_code",
)
DEFAULT_MAX_STALENESS_MINUTES = 24 * 60


@dataclass(frozen=True)
class ScannerMetricsDiagnostics:
    total_symbols: int
    valid_symbols: int
    missing_symbols: list[str] = field(default_factory=list)
    missing_required_fields: dict[str, list[str]] = field(default_factory=dict)
    missing_provenance_fields: dict[str, list[str]] = field(default_factory=dict)
    stale_symbols: dict[str, str] = field(default_factory=dict)
    market_data_failures: dict[str, dict[str, Any]] = field(default_factory=dict)

    @property
    def has_warnings(self) -> bool:
        return bool(
            self.missing_symbols
            or self.missing_required_fields
            or self.missing_provenance_fields
            or self.stale_symbols
            or self.market_data_failures
        )

    @property
    def data_quality_status(self) -> str:
        if self.missing_symbols or self.missing_required_fields or self.market_data_failures:
            return "BLOCKED"
        if self.missing_provenance_fields or self.stale_symbols:
            return "DEGRADED"
        return "OK"

    def warning_lines(self) -> list[str]:
        lines: list[str] = []
        for symbol in self.missing_symbols:
            lines.append(f"scanner_metrics_missing:{symbol}")
        for symbol, fields in self.missing_required_fields.items():
            lines.append(f"scanner_metrics_incomplete:{symbol}:{','.join(fields)}")
        for symbol, detail in self.market_data_failures.items():
            kind = str(detail.get("kind") or "UNKNOWN")
            status_code = detail.get("status_code")
            suffix = f":{status_code}" if status_code is not None else ""
            lines.append(f"market_data_failure:{symbol}:{kind}{suffix}")
        for symbol, fields in self.missing_provenance_fields.items():
            lines.append(f"scanner_metrics_missing_provenance:{symbol}:{','.join(fields)}")
        for symbol, reason in self.stale_symbols.items():
            lines.append(f"scanner_metrics_stale:{symbol}:{reason}")
        return lines

    def as_summary(self) -> dict[str, Any]:
        return {
            "data_quality_status": self.data_quality_status,
            "total_symbols": self.total_symbols,
            "valid_symbols": self.valid_symbols,
            "missing_symbols": self.missing_symbols,
            "missing_required_fields": self.missing_required_fields,
            "missing_provenance_fields": self.missing_provenance_fields,
            "stale_symbols": self.stale_symbols,
            "market_data_failures": self.market_data_failures,
        }


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(result) or math.isinf(result):
        return None
    return result


def _safe_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _parse_timestamp(value: Any) -> datetime | None:
    text = _safe_text(value)
    if text is None:
        return None
    normalized = text.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def _staleness_reason(
    source_timestamp: Any,
    *,
    now_utc: datetime,
    max_staleness_minutes: int,
) -> str | None:
    parsed = _parse_timestamp(source_timestamp)
    if parsed is None:
        return "invalid_source_timestamp"
    threshold = timedelta(minutes=max_staleness_minutes)
    if now_utc - parsed > threshold:
        return "source_timestamp_too_old"
    if parsed - now_utc > timedelta(minutes=5):
        return "source_timestamp_in_future"
    return None


def normalize_symbol_metrics(metrics: dict[str, Any] | None) -> dict[str, Any] | None:
    """Normalize a raw scanner metrics row for signal generation.

    Numeric values are converted to floats where possible. Pandas `NA`, NaN and
    infinity are converted to `None`. Non-numeric labels, provenance fields, and
    canonical market-data failure fields are preserved.
    """
    if not metrics:
        return None

    normalized: dict[str, Any] = {}
    for key in (*REQUIRED_SIGNAL_METRICS, *OPTIONAL_SIGNAL_METRICS):
        if key not in metrics:
            continue
        if key == "entry_type":
            normalized[key] = metrics.get(key)
        else:
            normalized[key] = _safe_float(metrics.get(key))

    for key in PROVENANCE_FIELDS:
        if key in metrics:
            normalized[key] = _safe_text(metrics.get(key))

    if "provider_status_code" in metrics:
        normalized["provider_status_code"] = _safe_float(metrics.get("provider_status_code"))
    for key in ("data_failure_kind", "data_failure_message"):
        if key in metrics:
            normalized[key] = _safe_text(metrics.get(key))

    if "symbol" in metrics:
        normalized["symbol"] = metrics.get("symbol")
    if "warnings" in metrics:
        normalized["warnings"] = metrics.get("warnings") or []

    return normalized


def normalize_scanner_metrics_map(
    scanner_metrics_map: dict[str, Any] | None,
    expected_symbols: list[str],
    *,
    now_utc: datetime | None = None,
    max_staleness_minutes: int = DEFAULT_MAX_STALENESS_MINUTES,
) -> tuple[dict[str, dict[str, Any]], ScannerMetricsDiagnostics]:
    """Normalize scanner metrics map and return diagnostics.

    Missing or incomplete metrics are not fatal here. They are made visible through
    diagnostics so callers can block, degrade, report, or alert without silently
    hiding operational data-quality problems.
    """
    source = scanner_metrics_map or {}
    now = (now_utc or datetime.now(UTC)).astimezone(UTC)
    normalized: dict[str, dict[str, Any]] = {}
    missing_symbols: list[str] = []
    missing_required_fields: dict[str, list[str]] = {}
    missing_provenance_fields: dict[str, list[str]] = {}
    stale_symbols: dict[str, str] = {}
    market_data_failures: dict[str, dict[str, Any]] = {}

    for symbol in expected_symbols:
        row = normalize_symbol_metrics(source.get(symbol))
        if row is None:
            missing_symbols.append(symbol)
            continue

        failure_kind = row.get("data_failure_kind")
        if failure_kind:
            market_data_failures[symbol] = {
                "kind": failure_kind,
                "message": row.get("data_failure_message"),
                "status_code": row.get("provider_status_code"),
            }

        missing_fields = [
            field for field in REQUIRED_SIGNAL_METRICS
            if row.get(field) is None
        ]
        if missing_fields:
            missing_required_fields[symbol] = missing_fields

        missing_provenance = [
            field for field in REQUIRED_PROVENANCE_FIELDS
            if row.get(field) is None
        ]
        if missing_provenance:
            missing_provenance_fields[symbol] = missing_provenance

        if row.get("source_timestamp") is not None:
            stale_reason = _staleness_reason(
                row.get("source_timestamp"),
                now_utc=now,
                max_staleness_minutes=max_staleness_minutes,
            )
            if stale_reason:
                stale_symbols[symbol] = stale_reason

        if missing_fields or failure_kind:
            row["data_status"] = "BLOCKED"
        elif missing_provenance or symbol in stale_symbols:
            row["data_status"] = "DEGRADED"
        else:
            row["data_status"] = row.get("data_status") or "OK"

        normalized[symbol] = row

    valid_symbols = sum(
        1 for symbol in expected_symbols
        if symbol in normalized and symbol not in missing_required_fields and symbol not in market_data_failures
    )

    diagnostics = ScannerMetricsDiagnostics(
        total_symbols=len(expected_symbols),
        valid_symbols=valid_symbols,
        missing_symbols=missing_symbols,
        missing_required_fields=missing_required_fields,
        missing_provenance_fields=missing_provenance_fields,
        stale_symbols=stale_symbols,
        market_data_failures=market_data_failures,
    )
    return normalized, diagnostics
