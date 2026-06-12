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

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from src.validation.historical_edge_validation import coerce_finite_float

REQUIRED_SIGNAL_METRICS = ("close", "atr14")
REQUIRED_PROVENANCE_FIELDS = ("source", "source_timestamp", "fallback_level")
OPTIONAL_NUMERIC_SIGNAL_METRICS = (
    "atr_pct",
    "entry",
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
OPTIONAL_SIGNAL_METRICS = (*OPTIONAL_NUMERIC_SIGNAL_METRICS, "entry_type")
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
DEFAULT_DATAFEED_LIVENESS_DIR = Path("reports") / "datafeed_liveness"

DATAFEED_OK = "DATAFEED_OK"
DATAFEED_DEGRADED = "DATAFEED_DEGRADED"
DATAFEED_BLOCKED = "DATAFEED_BLOCKED"

PROVIDER_FAILURE_MISSING_API_KEY = "MISSING_POLYGON_API_KEY"
PROVIDER_FAILURE_PROVIDER_LIMIT = "PROVIDER_LIMIT_OR_RATE_LIMIT"
PROVIDER_FAILURE_PROVIDER_FORBIDDEN = "PROVIDER_FORBIDDEN_OR_UNAUTHORIZED"
PROVIDER_FAILURE_EMPTY_RESPONSE = "EMPTY_PROVIDER_RESPONSE"
PROVIDER_FAILURE_SCHEMA_MISMATCH = "SCHEMA_MISMATCH_OR_MISSING_BARS"
PROVIDER_FAILURE_UNKNOWN = "UNKNOWN_PROVIDER_FAILURE"


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


@dataclass(frozen=True)
class DatafeedLivenessRecord:
    datafeed_status: str
    provider_failure_reason: str | None
    total_symbols: int
    valid_close_count: int
    all_close_missing: bool
    valid_symbols: int
    data_quality_status: str
    checked_at: str
    source: str = "scanner_metrics_pipeline"
    blocked_symbols: list[str] = field(default_factory=list)
    provider_failures: dict[str, dict[str, Any]] = field(default_factory=dict)
    missing_required_fields: dict[str, list[str]] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _safe_float(value: Any) -> float | None:
    return coerce_finite_float(value)


def _safe_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def normalize_symbol_metrics(metrics: dict[str, Any]) -> dict[str, Any]:
    """Normalize one scanner metrics row while preserving compatible fields."""
    row = dict(metrics)
    for field_name in (*REQUIRED_SIGNAL_METRICS, *OPTIONAL_NUMERIC_SIGNAL_METRICS):
        if field_name in row:
            row[field_name] = _safe_float(row.get(field_name))
    return row


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
    age = now_utc - parsed
    if age < timedelta(0):
        return "source_timestamp_in_future"
    if age > timedelta(minutes=max_staleness_minutes):
        return "source_timestamp_too_old"
    return None


def classify_provider_failure(metrics: dict[str, Any]) -> str | None:
    kind = str(metrics.get("data_failure_kind") or "").upper()
    status_code = metrics.get("provider_status_code")
    message = str(metrics.get("data_failure_message") or "").lower()

    if kind in {"MISSING_API_KEY", "NO_API_KEY"}:
        return PROVIDER_FAILURE_MISSING_API_KEY
    if kind in {"RATE_LIMIT", "TOO_MANY_REQUESTS"} or status_code == 429:
        return PROVIDER_FAILURE_PROVIDER_LIMIT
    if kind in {"AUTH_FORBIDDEN", "FORBIDDEN", "UNAUTHORIZED"} or status_code in {401, 403}:
        return PROVIDER_FAILURE_PROVIDER_FORBIDDEN
    if kind in {"EMPTY_BARS", "EMPTY_RESPONSE"}:
        return PROVIDER_FAILURE_EMPTY_RESPONSE
    if kind in {"SCHEMA_MISMATCH", "PARSE_ERROR"}:
        return PROVIDER_FAILURE_SCHEMA_MISMATCH
    if kind:
        return PROVIDER_FAILURE_UNKNOWN
    if "api key" in message or "missing" in message:
        return PROVIDER_FAILURE_MISSING_API_KEY
    if "rate" in message or "limit" in message:
        return PROVIDER_FAILURE_PROVIDER_LIMIT
    if "forbidden" in message or "unauthorized" in message:
        return PROVIDER_FAILURE_PROVIDER_FORBIDDEN
    return None


def _market_data_failure_details(metrics: dict[str, Any]) -> dict[str, Any] | None:
    failure_reason = classify_provider_failure(metrics)
    if failure_reason is None:
        return None
    return {
        "kind": metrics.get("data_failure_kind") or failure_reason,
        "reason": failure_reason,
        "message": metrics.get("data_failure_message"),
        "status_code": metrics.get("provider_status_code"),
    }


def normalize_scanner_metrics_map(
    metrics_map: dict[str, dict[str, Any]] | None,
    required_symbols: list[str] | tuple[str, ...],
    *,
    now_utc: datetime | None = None,
    max_staleness_minutes: int = DEFAULT_MAX_STALENESS_MINUTES,
) -> tuple[dict[str, dict[str, Any]], ScannerMetricsDiagnostics]:
    now_utc = now_utc or datetime.now(UTC)
    if metrics_map is None:
        return {}, ScannerMetricsDiagnostics(
            total_symbols=len(required_symbols),
            valid_symbols=0,
            missing_symbols=list(required_symbols),
        )

    raw_map = metrics_map
    normalized: dict[str, dict[str, Any]] = {}
    missing_symbols: list[str] = []
    missing_required_fields: dict[str, list[str]] = {}
    missing_provenance_fields: dict[str, list[str]] = {}
    stale_symbols: dict[str, str] = {}
    market_data_failures: dict[str, dict[str, Any]] = {}

    for symbol in required_symbols:
        raw_metrics = raw_map.get(symbol)
        if not raw_metrics:
            missing_symbols.append(symbol)
            normalized[symbol] = {}
            continue

        row = normalize_symbol_metrics(raw_metrics)
        numeric_required_missing: list[str] = [
            field_name for field_name in REQUIRED_SIGNAL_METRICS if row.get(field_name) is None
        ]
        provenance_missing = [field_name for field_name in REQUIRED_PROVENANCE_FIELDS if not _safe_text(row.get(field_name))]
        failure_detail = _market_data_failure_details(row)
        if failure_detail is not None:
            market_data_failures[symbol] = failure_detail
        if numeric_required_missing:
            missing_required_fields[symbol] = numeric_required_missing
        if provenance_missing:
            missing_provenance_fields[symbol] = provenance_missing

        stale_reason = None
        if not provenance_missing:
            stale_reason = _staleness_reason(
                row.get("source_timestamp"),
                now_utc=now_utc,
                max_staleness_minutes=max_staleness_minutes,
            )
            if stale_reason is not None:
                stale_symbols[symbol] = stale_reason

        if failure_detail is not None or numeric_required_missing:
            row["data_status"] = "BLOCKED"
        elif provenance_missing or stale_reason is not None:
            row["data_status"] = "DEGRADED"
        else:
            row["data_status"] = row.get("data_status") or "OK"

        normalized[symbol] = row

    valid_symbols = sum(
        1
        for symbol in required_symbols
        if symbol in normalized
        and symbol not in missing_symbols
        and symbol not in missing_required_fields
        and symbol not in market_data_failures
        and symbol not in missing_provenance_fields
        and symbol not in stale_symbols
    )
    diagnostics = ScannerMetricsDiagnostics(
        total_symbols=len(required_symbols),
        valid_symbols=valid_symbols,
        missing_symbols=missing_symbols,
        missing_required_fields=missing_required_fields,
        missing_provenance_fields=missing_provenance_fields,
        stale_symbols=stale_symbols,
        market_data_failures=market_data_failures,
    )
    return normalized, diagnostics


def _coerce_checked_at(value: datetime | str | None) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, str) and value.strip():
        return value.strip()
    return datetime.now(UTC).isoformat()


def _date_from_checked_at(checked_at: str) -> str:
    return checked_at[:10] if len(checked_at) >= 10 else datetime.now(UTC).date().isoformat()


def _diagnostics_from_summary(summary: dict[str, Any], total_symbols: int) -> ScannerMetricsDiagnostics:
    return ScannerMetricsDiagnostics(
        total_symbols=int(summary.get("total_symbols", total_symbols)),
        valid_symbols=int(summary.get("valid_symbols", 0)),
        missing_symbols=list(summary.get("missing_symbols", [])),
        missing_required_fields=dict(summary.get("missing_required_fields", {})),
        missing_provenance_fields=dict(summary.get("missing_provenance_fields", {})),
        stale_symbols=dict(summary.get("stale_symbols", {})),
        market_data_failures=dict(summary.get("market_data_failures", {})),
    )


def build_datafeed_liveness_record(
    normalized: dict[str, dict[str, Any]] | None = None,
    diagnostics: ScannerMetricsDiagnostics | None = None,
    *,
    scanner_metrics_map: dict[str, dict[str, Any]] | None = None,
    scanner_data_quality: dict[str, Any] | None = None,
    checked_at: datetime | str | None = None,
) -> DatafeedLivenessRecord:
    if normalized is None:
        normalized = {symbol: normalize_symbol_metrics(metrics) for symbol, metrics in (scanner_metrics_map or {}).items()}
    if diagnostics is None:
        if scanner_data_quality is not None:
            diagnostics = _diagnostics_from_summary(scanner_data_quality, len(normalized))
        else:
            normalized, diagnostics = normalize_scanner_metrics_map(normalized, list(normalized))

    checked = _coerce_checked_at(checked_at)
    total = diagnostics.total_symbols
    valid_close_count = sum(
        1
        for metrics in normalized.values()
        if _safe_float(metrics.get("close")) is not None
    )
    all_close_missing = total > 0 and valid_close_count == 0
    provider_reasons = sorted({detail.get("reason") for detail in diagnostics.market_data_failures.values() if detail.get("reason")})
    provider_failure_reason = ",".join(provider_reasons) if provider_reasons else None
    datafeed_status = DATAFEED_OK
    notes: list[str] = []

    if diagnostics.market_data_failures:
        datafeed_status = DATAFEED_BLOCKED
        notes.append("provider_failures_present")
    elif all_close_missing:
        datafeed_status = DATAFEED_BLOCKED
        provider_failure_reason = provider_failure_reason or PROVIDER_FAILURE_SCHEMA_MISMATCH
        notes.append("all_close_values_missing")
    elif diagnostics.missing_required_fields:
        datafeed_status = DATAFEED_DEGRADED
        notes.append("missing_required_fields")
    elif diagnostics.stale_symbols or diagnostics.missing_provenance_fields:
        datafeed_status = DATAFEED_DEGRADED
        notes.append("provenance_or_freshness_warning")

    return DatafeedLivenessRecord(
        datafeed_status=datafeed_status,
        provider_failure_reason=provider_failure_reason,
        total_symbols=total,
        valid_close_count=valid_close_count,
        all_close_missing=all_close_missing,
        valid_symbols=diagnostics.valid_symbols,
        data_quality_status=diagnostics.data_quality_status,
        checked_at=checked,
        blocked_symbols=sorted(set(diagnostics.missing_symbols) | set(diagnostics.missing_required_fields) | set(diagnostics.market_data_failures)),
        provider_failures=diagnostics.market_data_failures,
        missing_required_fields=diagnostics.missing_required_fields,
        notes=notes,
    )


def write_datafeed_liveness_record(
    record: DatafeedLivenessRecord,
    path: Path | None = None,
    *,
    output_dir: Path | None = None,
    date_str: str | None = None,
) -> Path | tuple[Path, Path]:
    if output_dir is None and path is None:
        output_dir = DEFAULT_DATAFEED_LIVENESS_DIR
        date_str = date_str or _date_from_checked_at(record.checked_at)

    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        dated_path = output_dir / f"{date_str or datetime.now(UTC).date().isoformat()}-datafeed-liveness.json"
        latest_path = output_dir / "datafeed-liveness-latest.json"
        payload = json.dumps(record.to_dict(), indent=2, sort_keys=True)
        dated_path.write_text(payload, encoding="utf-8")
        latest_path.write_text(payload, encoding="utf-8")
        return dated_path, latest_path

    if path is None:
        raise ValueError("path or output_dir is required")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    return path
