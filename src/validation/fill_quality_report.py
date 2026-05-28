from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Iterable


class FillQualitySeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class FillQualityStatus(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


@dataclass(frozen=True)
class FillQualityConfig:
    max_abs_slippage_bps: float = 25.0
    max_avg_abs_slippage_bps: float = 15.0
    max_spread_bps: float = 20.0
    max_avg_delay_seconds: float = 300.0
    min_fill_rate: float = 0.95
    min_full_fill_rate: float = 0.80
    fail_on_missing_reference_price: bool = True


@dataclass(frozen=True)
class FillQualityRecord:
    order_id: str
    symbol: str
    side: str
    requested_quantity: float
    filled_quantity: float
    arrival_price: float | None
    average_fill_price: float | None
    submitted_at: str | None = None
    first_fill_at: str | None = None
    bid_price: float | None = None
    ask_price: float | None = None
    strategy_id: str = "default"
    signal_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FillQualityIssue:
    severity: FillQualitySeverity
    code: str
    message: str
    order_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["severity"] = self.severity.value
        return payload


@dataclass(frozen=True)
class FillQualityComparison:
    order_id: str
    symbol: str
    side: str
    requested_quantity: float
    filled_quantity: float
    fill_ratio: float
    slippage_bps: float | None
    spread_bps: float | None
    delay_seconds: float | None
    status: FillQualityStatus
    issues: list[FillQualityIssue] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["status"] = self.status.value
        payload["issues"] = [issue.to_dict() for issue in self.issues]
        return payload


@dataclass(frozen=True)
class FillQualityMetrics:
    record_count: int
    filled_record_count: int
    total_requested_quantity: float
    total_filled_quantity: float
    fill_rate: float
    full_fill_rate: float
    partial_fill_count: int
    avg_slippage_bps: float
    avg_abs_slippage_bps: float
    max_abs_slippage_bps: float
    avg_spread_bps: float
    max_spread_bps: float
    avg_delay_seconds: float
    max_delay_seconds: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FillQualityReport:
    passed: bool
    status: FillQualityStatus
    metrics: FillQualityMetrics
    comparisons: list[FillQualityComparison] = field(default_factory=list)
    issues: list[FillQualityIssue] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "status": self.status.value,
            "metrics": self.metrics.to_dict(),
            "comparisons": [comparison.to_dict() for comparison in self.comparisons],
            "issues": [issue.to_dict() for issue in self.issues],
            "notes": list(self.notes),
        }


def analyze_fill_quality(
    records: Iterable[FillQualityRecord | dict[str, Any]],
    *,
    config: FillQualityConfig = FillQualityConfig(),
) -> FillQualityReport:
    normalized = [_record_from(item) for item in records]
    issues: list[FillQualityIssue] = []
    seen_order_ids: set[str] = set()
    comparisons: list[FillQualityComparison] = []

    for record in normalized:
        record_issues = _validate_record(record, config=config)
        if record.order_id in seen_order_ids:
            record_issues.append(
                FillQualityIssue(
                    FillQualitySeverity.ERROR,
                    "duplicate_order_id",
                    "duplicate order_id in fill-quality input",
                    record.order_id,
                )
            )
        seen_order_ids.add(record.order_id)

        comparison = _compare_record(record, config=config, issues=record_issues)
        comparisons.append(comparison)
        issues.extend(record_issues)

    metrics = _build_metrics(comparisons)
    gate_issues = _build_gate_issues(metrics, config=config)
    issues.extend(gate_issues)

    has_errors = any(issue.severity == FillQualitySeverity.ERROR for issue in issues)
    has_warnings = any(issue.severity == FillQualitySeverity.WARNING for issue in issues)
    status = FillQualityStatus.FAIL if has_errors else FillQualityStatus.WARN if has_warnings else FillQualityStatus.PASS

    return FillQualityReport(
        passed=not has_errors,
        status=status,
        metrics=metrics,
        comparisons=comparisons,
        issues=issues,
        notes=[
            "fill_quality_audit_only",
            "paper_or_observed_fill_quality_only",
            "no_order_submission_performed",
            "no_live_trading_authorization_granted",
        ],
    )


def load_fill_quality_records(path: Path) -> list[FillQualityRecord]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = payload.get("records", []) if isinstance(payload, dict) else payload
    if not isinstance(records, list):
        raise ValueError("fill-quality input must be a JSON list or an object with records[]")
    return [_record_from(record) for record in records if isinstance(record, dict)]


def write_fill_quality_report(report: FillQualityReport, *, json_path: Path, markdown_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_fill_quality_markdown(report), encoding="utf-8")


def render_fill_quality_markdown(report: FillQualityReport) -> str:
    metrics = report.metrics
    lines = [
        "# C6 Fill Quality Report",
        "",
        f"Status: **{report.status.value}**",
        f"Passed: **{str(report.passed).lower()}**",
        "",
        "## Metrics",
        "",
        f"- Records: {metrics.record_count}",
        f"- Filled records: {metrics.filled_record_count}",
        f"- Fill rate: {metrics.fill_rate:.2%}",
        f"- Full-fill rate: {metrics.full_fill_rate:.2%}",
        f"- Partial fills: {metrics.partial_fill_count}",
        f"- Average slippage: {metrics.avg_slippage_bps:.4f} bps",
        f"- Average absolute slippage: {metrics.avg_abs_slippage_bps:.4f} bps",
        f"- Max absolute slippage: {metrics.max_abs_slippage_bps:.4f} bps",
        f"- Average spread: {metrics.avg_spread_bps:.4f} bps",
        f"- Max spread: {metrics.max_spread_bps:.4f} bps",
        f"- Average delay: {metrics.avg_delay_seconds:.2f}s",
        f"- Max delay: {metrics.max_delay_seconds:.2f}s",
        "",
        "## Issues",
        "",
    ]
    if report.issues:
        for issue in report.issues:
            lines.append(f"- **{issue.severity.value.upper()}** `{issue.code}` {issue.order_id or ''} — {issue.message}".strip())
    else:
        lines.append("- None")
    lines.extend(["", "## Safety Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    return "\n".join(lines).rstrip() + "\n"


def _record_from(record: FillQualityRecord | dict[str, Any]) -> FillQualityRecord:
    if isinstance(record, FillQualityRecord):
        return record
    return FillQualityRecord(
        order_id=str(record.get("order_id", record.get("client_order_id", ""))).strip(),
        symbol=str(record.get("symbol", "")).strip().upper(),
        side=str(record.get("side", "")).strip().lower(),
        requested_quantity=float(record.get("requested_quantity", record.get("quantity", 0.0))),
        filled_quantity=float(record.get("filled_quantity", record.get("filled_qty", 0.0))),
        arrival_price=_optional_float(record.get("arrival_price", record.get("reference_price"))),
        average_fill_price=_optional_float(record.get("average_fill_price", record.get("fill_price"))),
        submitted_at=_optional_str(record.get("submitted_at", record.get("created_at"))),
        first_fill_at=_optional_str(record.get("first_fill_at", record.get("filled_at"))),
        bid_price=_optional_float(record.get("bid_price", record.get("bid"))),
        ask_price=_optional_float(record.get("ask_price", record.get("ask"))),
        strategy_id=str(record.get("strategy_id", "default")).strip() or "default",
        signal_id=_optional_str(record.get("signal_id")),
    )


def _validate_record(record: FillQualityRecord, *, config: FillQualityConfig) -> list[FillQualityIssue]:
    issues: list[FillQualityIssue] = []
    if not record.order_id:
        issues.append(_error("missing_order_id", "order_id is required", record.order_id))
    if not record.symbol:
        issues.append(_error("missing_symbol", "symbol is required", record.order_id))
    if record.side not in {"buy", "sell"}:
        issues.append(_error("invalid_side", "side must be buy or sell", record.order_id))
    if record.requested_quantity <= 0:
        issues.append(_error("invalid_requested_quantity", "requested_quantity must be positive", record.order_id))
    if record.filled_quantity < 0:
        issues.append(_error("invalid_filled_quantity", "filled_quantity must not be negative", record.order_id))
    if record.filled_quantity > record.requested_quantity:
        issues.append(_error("overfilled_order", "filled_quantity exceeds requested_quantity", record.order_id))
    if record.arrival_price is None or record.arrival_price <= 0:
        severity = FillQualitySeverity.ERROR if config.fail_on_missing_reference_price else FillQualitySeverity.WARNING
        issues.append(FillQualityIssue(severity, "missing_arrival_price", "arrival/reference price is required for slippage", record.order_id))
    if record.average_fill_price is None or (record.average_fill_price <= 0 and record.filled_quantity > 0):
        issues.append(_error("invalid_average_fill_price", "average_fill_price must be positive for filled records", record.order_id))
    if (record.bid_price is None) != (record.ask_price is None):
        issues.append(FillQualityIssue(FillQualitySeverity.WARNING, "incomplete_spread_quote", "bid and ask are both required for spread quality", record.order_id))
    if record.bid_price is not None and record.ask_price is not None and record.ask_price < record.bid_price:
        issues.append(_error("crossed_spread", "ask_price must be greater than or equal to bid_price", record.order_id))
    return issues


def _compare_record(
    record: FillQualityRecord,
    *,
    config: FillQualityConfig,
    issues: list[FillQualityIssue],
) -> FillQualityComparison:
    fill_ratio = round(record.filled_quantity / record.requested_quantity, 6) if record.requested_quantity > 0 else 0.0
    slippage_bps = _slippage_bps(record)
    spread_bps = _spread_bps(record)
    delay_seconds = _delay_seconds(record)

    if slippage_bps is not None and abs(slippage_bps) > config.max_abs_slippage_bps:
        issues.append(_error("max_abs_slippage_bps_exceeded", "absolute slippage exceeds configured tolerance", record.order_id))
    if spread_bps is not None and spread_bps > config.max_spread_bps:
        issues.append(FillQualityIssue(FillQualitySeverity.WARNING, "max_spread_bps_exceeded", "spread is wider than configured tolerance", record.order_id))
    if delay_seconds is not None and delay_seconds < 0:
        issues.append(_error("negative_fill_delay", "first_fill_at is before submitted_at", record.order_id))

    has_error = any(issue.severity == FillQualitySeverity.ERROR for issue in issues)
    has_warning = any(issue.severity == FillQualitySeverity.WARNING for issue in issues)
    status = FillQualityStatus.FAIL if has_error else FillQualityStatus.WARN if has_warning else FillQualityStatus.PASS

    return FillQualityComparison(
        order_id=record.order_id,
        symbol=record.symbol,
        side=record.side,
        requested_quantity=round(record.requested_quantity, 6),
        filled_quantity=round(record.filled_quantity, 6),
        fill_ratio=fill_ratio,
        slippage_bps=slippage_bps,
        spread_bps=spread_bps,
        delay_seconds=delay_seconds,
        status=status,
        issues=list(issues),
    )


def _build_metrics(comparisons: list[FillQualityComparison]) -> FillQualityMetrics:
    total_requested = round(sum(item.requested_quantity for item in comparisons), 6)
    total_filled = round(sum(item.filled_quantity for item in comparisons), 6)
    filled_records = sum(1 for item in comparisons if item.filled_quantity > 0)
    full_fills = sum(1 for item in comparisons if item.requested_quantity > 0 and item.filled_quantity >= item.requested_quantity)
    partial_fills = sum(1 for item in comparisons if 0 < item.filled_quantity < item.requested_quantity)
    slippages = [item.slippage_bps for item in comparisons if item.slippage_bps is not None]
    spreads = [item.spread_bps for item in comparisons if item.spread_bps is not None]
    delays = [item.delay_seconds for item in comparisons if item.delay_seconds is not None]
    return FillQualityMetrics(
        record_count=len(comparisons),
        filled_record_count=filled_records,
        total_requested_quantity=total_requested,
        total_filled_quantity=total_filled,
        fill_rate=round(total_filled / total_requested, 6) if total_requested > 0 else 0.0,
        full_fill_rate=round(full_fills / len(comparisons), 6) if comparisons else 0.0,
        partial_fill_count=partial_fills,
        avg_slippage_bps=round(sum(slippages) / len(slippages), 6) if slippages else 0.0,
        avg_abs_slippage_bps=round(sum(abs(value) for value in slippages) / len(slippages), 6) if slippages else 0.0,
        max_abs_slippage_bps=round(max((abs(value) for value in slippages), default=0.0), 6),
        avg_spread_bps=round(sum(spreads) / len(spreads), 6) if spreads else 0.0,
        max_spread_bps=round(max(spreads, default=0.0), 6),
        avg_delay_seconds=round(sum(delays) / len(delays), 6) if delays else 0.0,
        max_delay_seconds=round(max(delays, default=0.0), 6),
    )


def _build_gate_issues(metrics: FillQualityMetrics, *, config: FillQualityConfig) -> list[FillQualityIssue]:
    issues: list[FillQualityIssue] = []
    if metrics.fill_rate < config.min_fill_rate:
        issues.append(_error("fill_rate_below_minimum", "aggregate fill rate is below configured minimum", None))
    if metrics.full_fill_rate < config.min_full_fill_rate:
        issues.append(_error("full_fill_rate_below_minimum", "full-fill rate is below configured minimum", None))
    if metrics.avg_abs_slippage_bps > config.max_avg_abs_slippage_bps:
        issues.append(_error("avg_abs_slippage_bps_exceeded", "average absolute slippage exceeds configured tolerance", None))
    if metrics.avg_delay_seconds > config.max_avg_delay_seconds:
        issues.append(FillQualityIssue(FillQualitySeverity.WARNING, "avg_delay_seconds_exceeded", "average fill delay exceeds configured tolerance", None))
    return issues


def _slippage_bps(record: FillQualityRecord) -> float | None:
    if record.arrival_price is None or record.average_fill_price is None or record.arrival_price <= 0:
        return None
    raw = (record.average_fill_price - record.arrival_price) / record.arrival_price * 10000
    if record.side == "sell":
        raw = -raw
    return round(raw, 6)


def _spread_bps(record: FillQualityRecord) -> float | None:
    if record.bid_price is None or record.ask_price is None:
        return None
    midpoint = (record.bid_price + record.ask_price) / 2
    if midpoint <= 0:
        return None
    return round((record.ask_price - record.bid_price) / midpoint * 10000, 6)


def _delay_seconds(record: FillQualityRecord) -> float | None:
    if not record.submitted_at or not record.first_fill_at:
        return None
    submitted = _parse_datetime(record.submitted_at)
    first_fill = _parse_datetime(record.first_fill_at)
    if submitted is None or first_fill is None:
        return None
    return round((first_fill - submitted).total_seconds(), 6)


def _parse_datetime(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _optional_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _error(code: str, message: str, order_id: str | None) -> FillQualityIssue:
    return FillQualityIssue(FillQualitySeverity.ERROR, code, message, order_id)
