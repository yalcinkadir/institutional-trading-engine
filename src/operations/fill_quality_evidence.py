"""
Fill Quality Evidence.

PSR3 adds a public-safe fill-quality evidence artifact for paper/observation
execution review.

The goal is not to prove trading edge. The goal is to make paper execution
quality auditable:
- accepted / rejected fill status
- expected vs actual fill price
- slippage in absolute price units
- slippage in basis points
- reconciliation status
- PASS / WARN / FAIL summary

This module is deterministic and side-effect free except for explicit JSON
write helpers.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "PSR3_FILL_QUALITY_EVIDENCE_V1"
DEFAULT_FILL_QUALITY_DIR = Path("reports/evidence/fill_quality")

PASS_STATUSES = {"FILLED"}
WARN_STATUSES = {"PARTIAL_FILL"}
FAIL_STATUSES = {"REJECTED", "CANCELLED", "EXPIRED", "FAILED"}
RECONCILED_STATUSES = {"RECONCILED"}
UNRECONCILED_STATUSES = {"UNRECONCILED", "MISSING", "MISMATCH"}


@dataclass(frozen=True)
class FillQualityRecord:
    """One paper execution fill-quality record."""

    order_id: str
    signal_id: str | None
    symbol: str
    side: str
    quantity: float
    expected_price: float
    actual_price: float | None
    fill_status: str
    reconciliation_status: str
    timestamp: str | None
    slippage_absolute: float | None
    slippage_bps: float | None
    status: str
    warnings: list[str]


@dataclass(frozen=True)
class FillQualityEvidence:
    """Daily fill-quality evidence summary."""

    schema_version: str
    trading_date: str
    created_at: str
    status: str
    total_records: int
    filled_count: int
    partial_fill_count: int
    failed_count: int
    unreconciled_count: int
    average_slippage_bps: float | None
    max_abs_slippage_bps: float | None
    records: list[FillQualityRecord]
    notes: list[str]
    live_trading_authorized: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["records"] = [asdict(record) for record in self.records]
        return payload


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _normalize_status(value: Any) -> str:
    if value is None:
        return "MISSING"
    return str(value).strip().upper() or "MISSING"


def _slippage(expected_price: float, actual_price: float | None, side: str) -> tuple[float | None, float | None]:
    if actual_price is None or expected_price <= 0:
        return None, None

    normalized_side = side.upper()
    raw = actual_price - expected_price

    # For BUY, positive slippage is worse. For SELL, lower actual price is worse.
    signed_slippage = raw if normalized_side == "BUY" else -raw
    bps = (signed_slippage / expected_price) * 10_000

    return signed_slippage, bps


def _record_status(
    *,
    fill_status: str,
    reconciliation_status: str,
    slippage_bps: float | None,
    max_warn_slippage_bps: float,
    max_fail_slippage_bps: float,
) -> tuple[str, list[str]]:
    warnings: list[str] = []

    if fill_status in FAIL_STATUSES:
        warnings.append("fill_status_failed")
        return "FAIL", warnings

    if fill_status not in PASS_STATUSES and fill_status not in WARN_STATUSES:
        warnings.append("fill_status_unknown")
        return "FAIL", warnings

    if reconciliation_status in UNRECONCILED_STATUSES:
        warnings.append("reconciliation_not_clean")
        return "FAIL", warnings

    if reconciliation_status not in RECONCILED_STATUSES:
        warnings.append("reconciliation_status_unknown")
        return "FAIL", warnings

    if slippage_bps is None:
        warnings.append("slippage_unavailable")
        return "WARN", warnings

    abs_slippage = abs(slippage_bps)
    if abs_slippage > max_fail_slippage_bps:
        warnings.append("slippage_fail_threshold_exceeded")
        return "FAIL", warnings

    if abs_slippage > max_warn_slippage_bps:
        warnings.append("slippage_warn_threshold_exceeded")
        return "WARN", warnings

    if fill_status in WARN_STATUSES:
        warnings.append("partial_fill")
        return "WARN", warnings

    return "PASS", warnings


def build_fill_quality_record(
    raw: dict[str, Any],
    *,
    max_warn_slippage_bps: float = 25.0,
    max_fail_slippage_bps: float = 75.0,
) -> FillQualityRecord:
    """Build one normalized fill-quality record from a raw dict."""
    order_id = str(raw.get("order_id") or raw.get("id") or "")
    signal_id = raw.get("signal_id")
    symbol = str(raw.get("symbol") or "")
    side = str(raw.get("side") or "BUY").upper()
    quantity = _safe_float(raw.get("quantity")) or 0.0
    expected_price = _safe_float(raw.get("expected_price")) or 0.0
    actual_price = _safe_float(raw.get("actual_price"))
    fill_status = _normalize_status(raw.get("fill_status") or raw.get("status"))
    reconciliation_status = _normalize_status(raw.get("reconciliation_status"))
    timestamp = raw.get("timestamp")

    slippage_absolute, slippage_bps = _slippage(
        expected_price=expected_price,
        actual_price=actual_price,
        side=side,
    )

    status, warnings = _record_status(
        fill_status=fill_status,
        reconciliation_status=reconciliation_status,
        slippage_bps=slippage_bps,
        max_warn_slippage_bps=max_warn_slippage_bps,
        max_fail_slippage_bps=max_fail_slippage_bps,
    )

    if not order_id:
        warnings.append("order_id_missing")
        status = "FAIL"
    if not symbol:
        warnings.append("symbol_missing")
        status = "FAIL"
    if quantity <= 0:
        warnings.append("quantity_non_positive")
        status = "FAIL"
    if expected_price <= 0:
        warnings.append("expected_price_non_positive")
        status = "FAIL"

    return FillQualityRecord(
        order_id=order_id,
        signal_id=str(signal_id) if signal_id is not None else None,
        symbol=symbol,
        side=side,
        quantity=quantity,
        expected_price=expected_price,
        actual_price=actual_price,
        fill_status=fill_status,
        reconciliation_status=reconciliation_status,
        timestamp=str(timestamp) if timestamp is not None else None,
        slippage_absolute=slippage_absolute,
        slippage_bps=slippage_bps,
        status=status,
        warnings=warnings,
    )


def build_fill_quality_evidence(
    *,
    trading_date: str | date,
    raw_records: Iterable[dict[str, Any]],
    created_at: str | None = None,
    notes: Iterable[str] = (),
    max_warn_slippage_bps: float = 25.0,
    max_fail_slippage_bps: float = 75.0,
) -> FillQualityEvidence:
    """Build daily fill-quality evidence from raw execution/fill rows."""
    trading_date_str = (
        trading_date.isoformat() if isinstance(trading_date, date) else str(trading_date)
    )

    records = [
        build_fill_quality_record(
            raw,
            max_warn_slippage_bps=max_warn_slippage_bps,
            max_fail_slippage_bps=max_fail_slippage_bps,
        )
        for raw in raw_records
    ]

    filled_count = sum(1 for record in records if record.fill_status == "FILLED")
    partial_fill_count = sum(1 for record in records if record.fill_status == "PARTIAL_FILL")
    failed_count = sum(1 for record in records if record.status == "FAIL")
    unreconciled_count = sum(
        1 for record in records if record.reconciliation_status in UNRECONCILED_STATUSES
    )

    available_slippage = [
        record.slippage_bps
        for record in records
        if record.slippage_bps is not None
    ]

    average_slippage_bps = (
        sum(available_slippage) / len(available_slippage)
        if available_slippage
        else None
    )
    max_abs_slippage_bps = (
        max(abs(value) for value in available_slippage)
        if available_slippage
        else None
    )

    if not records:
        status = "WARN"
    elif any(record.status == "FAIL" for record in records):
        status = "FAIL"
    elif any(record.status == "WARN" for record in records):
        status = "WARN"
    else:
        status = "PASS"

    return FillQualityEvidence(
        schema_version=SCHEMA_VERSION,
        trading_date=trading_date_str,
        created_at=created_at or utc_now_iso(),
        status=status,
        total_records=len(records),
        filled_count=filled_count,
        partial_fill_count=partial_fill_count,
        failed_count=failed_count,
        unreconciled_count=unreconciled_count,
        average_slippage_bps=average_slippage_bps,
        max_abs_slippage_bps=max_abs_slippage_bps,
        records=records,
        notes=list(notes),
        live_trading_authorized=False,
    )


def write_fill_quality_evidence(
    evidence: FillQualityEvidence,
    *,
    output_dir: str | Path = DEFAULT_FILL_QUALITY_DIR,
) -> Path:
    """Write daily fill-quality evidence JSON."""
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    output_path = target_dir / f"{evidence.trading_date}-fill-quality-evidence.json"
    latest_path = target_dir / "latest-fill-quality-evidence.json"

    payload = json.dumps(evidence.to_dict(), indent=2, sort_keys=True)
    output_path.write_text(payload, encoding="utf-8")
    latest_path.write_text(payload, encoding="utf-8")

    return output_path


def load_fill_quality_evidence(path: str | Path) -> FillQualityEvidence:
    """Load fill-quality evidence JSON."""
    payload = json.loads(Path(path).read_text(encoding="utf-8"))

    records = [
        FillQualityRecord(
            order_id=str(item["order_id"]),
            signal_id=item.get("signal_id"),
            symbol=str(item["symbol"]),
            side=str(item["side"]),
            quantity=float(item["quantity"]),
            expected_price=float(item["expected_price"]),
            actual_price=(
                float(item["actual_price"]) if item.get("actual_price") is not None else None
            ),
            fill_status=str(item["fill_status"]),
            reconciliation_status=str(item["reconciliation_status"]),
            timestamp=item.get("timestamp"),
            slippage_absolute=(
                float(item["slippage_absolute"])
                if item.get("slippage_absolute") is not None
                else None
            ),
            slippage_bps=(
                float(item["slippage_bps"])
                if item.get("slippage_bps") is not None
                else None
            ),
            status=str(item["status"]),
            warnings=[str(value) for value in item.get("warnings", [])],
        )
        for item in payload.get("records", [])
    ]

    return FillQualityEvidence(
        schema_version=str(payload["schema_version"]),
        trading_date=str(payload["trading_date"]),
        created_at=str(payload["created_at"]),
        status=str(payload["status"]),
        total_records=int(payload["total_records"]),
        filled_count=int(payload["filled_count"]),
        partial_fill_count=int(payload["partial_fill_count"]),
        failed_count=int(payload["failed_count"]),
        unreconciled_count=int(payload["unreconciled_count"]),
        average_slippage_bps=(
            float(payload["average_slippage_bps"])
            if payload.get("average_slippage_bps") is not None
            else None
        ),
        max_abs_slippage_bps=(
            float(payload["max_abs_slippage_bps"])
            if payload.get("max_abs_slippage_bps") is not None
            else None
        ),
        records=records,
        notes=[str(value) for value in payload.get("notes", [])],
        live_trading_authorized=bool(payload.get("live_trading_authorized", False)),
    )


def validate_fill_quality_evidence(evidence: FillQualityEvidence) -> dict[str, Any]:
    """Validate fill-quality evidence consistency."""
    errors: list[str] = []

    if evidence.schema_version != SCHEMA_VERSION:
        errors.append("invalid_schema_version")

    if evidence.live_trading_authorized:
        errors.append("live_trading_authorized_must_be_false")

    if evidence.total_records != len(evidence.records):
        errors.append("total_records_mismatch")

    expected_failed_count = sum(1 for record in evidence.records if record.status == "FAIL")
    if evidence.failed_count != expected_failed_count:
        errors.append("failed_count_mismatch")

    expected_unreconciled_count = sum(
        1
        for record in evidence.records
        if record.reconciliation_status in UNRECONCILED_STATUSES
    )
    if evidence.unreconciled_count != expected_unreconciled_count:
        errors.append("unreconciled_count_mismatch")

    expected_status = "WARN"
    if evidence.records and not any(record.status == "FAIL" for record in evidence.records):
        expected_status = (
            "WARN"
            if any(record.status == "WARN" for record in evidence.records)
            else "PASS"
        )
    elif any(record.status == "FAIL" for record in evidence.records):
        expected_status = "FAIL"

    if evidence.status != expected_status:
        errors.append("status_mismatch")

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
    }