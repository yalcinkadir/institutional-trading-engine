from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

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


def build_datafeed_liveness_record(
    *,
    scanner_metrics_map: dict[str, dict[str, Any]] | None,
    scanner_data_quality: dict[str, Any] | None,
    checked_at: str | None = None,
) -> DatafeedLivenessRecord:
    """Classify scanner market-data liveness for Paper Observation.

    This gate is intentionally stricter than normal no-trade handling. A run where
    every tracked symbol has `close=None` is infrastructure-blocked evidence, not a
    productive Paper Observation cycle.
    """
    metrics = scanner_metrics_map or {}
    data_quality = scanner_data_quality or {}
    total_symbols = _safe_int(data_quality.get("total_symbols"), len(metrics))
    valid_symbols = _safe_int(data_quality.get("valid_symbols"), 0)
    valid_close_count = sum(1 for row in metrics.values() if _is_number((row or {}).get("close")))
    missing_required_fields = _dict_of_lists(data_quality.get("missing_required_fields"))
    provider_failures = _dict_of_dicts(data_quality.get("market_data_failures"))
    blocked_symbols = sorted(
        {
            *(symbol for symbol, fields in missing_required_fields.items() if "close" in fields),
            *provider_failures.keys(),
            *(symbol for symbol, row in metrics.items() if not _is_number((row or {}).get("close"))),
        }
    )
    all_close_missing = total_symbols > 0 and valid_close_count == 0
    data_quality_status = str(data_quality.get("data_quality_status") or "UNKNOWN").upper()
    provider_failure_reason = _derive_provider_failure_reason(
        data_quality=data_quality,
        provider_failures=provider_failures,
        missing_required_fields=missing_required_fields,
        all_close_missing=all_close_missing,
    )

    notes: list[str] = []
    if all_close_missing:
        notes.append("all tracked symbols have missing/non-numeric close")
    if provider_failure_reason:
        notes.append(f"provider_failure_reason={provider_failure_reason}")
    if data_quality_status not in {"OK", "DEGRADED", "BLOCKED"}:
        notes.append(f"unknown data_quality_status={data_quality_status}")

    if all_close_missing or data_quality_status in {"BLOCKED", "UNKNOWN", "FAILED"}:
        status = DATAFEED_BLOCKED
    elif data_quality_status == "DEGRADED" or valid_symbols < total_symbols:
        status = DATAFEED_DEGRADED
    else:
        status = DATAFEED_OK

    return DatafeedLivenessRecord(
        datafeed_status=status,
        provider_failure_reason=provider_failure_reason,
        total_symbols=total_symbols,
        valid_close_count=valid_close_count,
        all_close_missing=all_close_missing,
        valid_symbols=valid_symbols,
        data_quality_status=data_quality_status,
        checked_at=checked_at or datetime.now(UTC).isoformat(),
        blocked_symbols=blocked_symbols,
        provider_failures=provider_failures,
        missing_required_fields=missing_required_fields,
        notes=notes,
    )


def write_datafeed_liveness_record(
    record: DatafeedLivenessRecord,
    *,
    output_dir: Path = Path("reports/health"),
    date_str: str | None = None,
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    date = date_str or datetime.now(UTC).strftime("%Y-%m-%d")
    dated_path = output_dir / f"{date}-datafeed-liveness.json"
    latest_path = output_dir / "datafeed-liveness-latest.json"
    payload = json.dumps(record.to_dict(), indent=2, sort_keys=True) + "\n"
    dated_path.write_text(payload, encoding="utf-8")
    latest_path.write_text(payload, encoding="utf-8")
    return dated_path, latest_path


def _derive_provider_failure_reason(
    *,
    data_quality: dict[str, Any],
    provider_failures: dict[str, dict[str, Any]],
    missing_required_fields: dict[str, list[str]],
    all_close_missing: bool,
) -> str | None:
    raw_reasons = " ".join(
        str(value or "")
        for failure in provider_failures.values()
        for value in (failure.get("kind"), failure.get("message"), failure.get("status_code"))
    ).lower()
    raw_reasons += " " + str(data_quality.get("provider_failure_reason") or "").lower()

    if "missing_api_key" in raw_reasons or "api key" in raw_reasons or "polygon_api_key" in raw_reasons:
        return PROVIDER_FAILURE_MISSING_API_KEY
    if "429" in raw_reasons or "rate" in raw_reasons or "limit" in raw_reasons:
        return PROVIDER_FAILURE_PROVIDER_LIMIT
    if "403" in raw_reasons or "401" in raw_reasons or "forbidden" in raw_reasons or "unauthorized" in raw_reasons:
        return PROVIDER_FAILURE_PROVIDER_FORBIDDEN
    if "empty" in raw_reasons or "no results" in raw_reasons:
        return PROVIDER_FAILURE_EMPTY_RESPONSE
    if provider_failures:
        return PROVIDER_FAILURE_UNKNOWN
    if all_close_missing and missing_required_fields:
        return PROVIDER_FAILURE_SCHEMA_MISMATCH
    if all_close_missing:
        return PROVIDER_FAILURE_EMPTY_RESPONSE
    return None


def _is_number(value: Any) -> bool:
    if isinstance(value, bool) or value is None:
        return False
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return number == number and number not in {float("inf"), float("-inf")}


def _safe_int(value: Any, fallback: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def _dict_of_lists(value: Any) -> dict[str, list[str]]:
    if not isinstance(value, dict):
        return {}
    result: dict[str, list[str]] = {}
    for key, raw_list in value.items():
        if isinstance(raw_list, list):
            result[str(key)] = [str(item) for item in raw_list]
    return result


def _dict_of_dicts(value: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(value, dict):
        return {}
    result: dict[str, dict[str, Any]] = {}
    for key, raw_dict in value.items():
        if isinstance(raw_dict, dict):
            result[str(key)] = dict(raw_dict)
    return result
