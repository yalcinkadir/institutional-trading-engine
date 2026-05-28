from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Iterable


class DailyExecutionSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class DailyExecutionStatus(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


@dataclass(frozen=True)
class DailyExecutionReconciliationConfig:
    max_abs_quantity_drift: float = 0.000001
    max_abs_price_drift_pct: float = 0.01
    max_abs_r_drift: float = 0.25
    max_abs_total_r_drift: float = 0.5
    require_observed_for_each_expected: bool = True
    fail_on_unexpected_observed: bool = True


@dataclass(frozen=True)
class ExpectedExecutionRecord:
    signal_id: str
    symbol: str
    side: str
    expected_quantity: float
    expected_avg_price: float
    expected_r: float
    strategy_id: str = "default"
    expected_order_id: str | None = None

    def key(self) -> str:
        return self.expected_order_id or self.signal_id

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ObservedExecutionRecord:
    signal_id: str
    symbol: str
    side: str
    filled_quantity: float
    average_fill_price: float
    realized_r: float
    status: str
    strategy_id: str = "default"
    order_id: str | None = None
    commission: float = 0.0

    def key(self) -> str:
        return self.order_id or self.signal_id

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DailyExecutionIssue:
    severity: DailyExecutionSeverity
    code: str
    message: str
    key: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["severity"] = self.severity.value
        return payload


@dataclass(frozen=True)
class ExecutionComparison:
    key: str
    signal_id: str
    symbol: str
    side: str
    quantity_drift: float
    price_drift_pct: float
    r_drift: float
    status: DailyExecutionStatus
    issues: list[DailyExecutionIssue] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["status"] = self.status.value
        payload["issues"] = [issue.to_dict() for issue in self.issues]
        return payload


@dataclass(frozen=True)
class DailyExecutionMetrics:
    expected_count: int
    observed_count: int
    matched_count: int
    missing_count: int
    unexpected_count: int
    failed_comparison_count: int
    warning_comparison_count: int
    expected_total_r: float
    observed_total_r: float
    total_r_drift: float
    max_abs_quantity_drift: float
    max_abs_price_drift_pct: float
    max_abs_r_drift: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DailyExecutionReconciliationReport:
    passed: bool
    status: DailyExecutionStatus
    metrics: DailyExecutionMetrics
    comparisons: list[ExecutionComparison] = field(default_factory=list)
    issues: list[DailyExecutionIssue] = field(default_factory=list)
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


def reconcile_daily_execution(
    *,
    expected_records: Iterable[ExpectedExecutionRecord | dict[str, Any]],
    observed_records: Iterable[ObservedExecutionRecord | dict[str, Any]],
    config: DailyExecutionReconciliationConfig = DailyExecutionReconciliationConfig(),
) -> DailyExecutionReconciliationReport:
    """Compare expected/backtest execution records with observed paper/live records.

    C5 is an audit layer only. It never places orders, cancels orders, fetches broker
    state or authorizes live trading. It compares already-captured records and fails
    closed when observation differs from expectation beyond configured tolerances.
    """

    expected = [_expected_from(record) for record in expected_records]
    observed = [_observed_from(record) for record in observed_records]
    issues: list[DailyExecutionIssue] = []

    expected_by_key = _index_expected(expected, issues)
    observed_by_key = _index_observed(observed, issues)

    comparisons: list[ExecutionComparison] = []
    for key, expected_record in expected_by_key.items():
        observed_record = observed_by_key.get(key)
        if observed_record is None:
            severity = DailyExecutionSeverity.ERROR if config.require_observed_for_each_expected else DailyExecutionSeverity.WARNING
            issues.append(
                DailyExecutionIssue(
                    severity=severity,
                    code="missing_observed_execution",
                    message=f"expected execution has no observed record: {key}",
                    key=key,
                )
            )
            continue
        comparisons.append(_compare_records(key, expected_record, observed_record, config=config))

    for key in sorted(set(observed_by_key) - set(expected_by_key)):
        severity = DailyExecutionSeverity.ERROR if config.fail_on_unexpected_observed else DailyExecutionSeverity.WARNING
        issues.append(
            DailyExecutionIssue(
                severity=severity,
                code="unexpected_observed_execution",
                message=f"observed execution has no expected/backtest record: {key}",
                key=key,
            )
        )

    comparison_issues = [issue for comparison in comparisons for issue in comparison.issues]
    issues.extend(comparison_issues)
    metrics = _build_metrics(expected, observed, comparisons, issues)

    if metrics.matched_count > 0 and abs(metrics.total_r_drift) > config.max_abs_total_r_drift:
        issues.append(
            DailyExecutionIssue(
                severity=DailyExecutionSeverity.ERROR,
                code="total_r_drift_exceeded",
                message="observed total R drift exceeds configured tolerance",
                key=None,
            )
        )
        metrics = _build_metrics(expected, observed, comparisons, issues)

    has_errors = any(issue.severity == DailyExecutionSeverity.ERROR for issue in issues)
    has_warnings = any(issue.severity == DailyExecutionSeverity.WARNING for issue in issues)
    status = DailyExecutionStatus.FAIL if has_errors else DailyExecutionStatus.WARN if has_warnings else DailyExecutionStatus.PASS

    return DailyExecutionReconciliationReport(
        passed=not has_errors,
        status=status,
        metrics=metrics,
        comparisons=comparisons,
        issues=issues,
        notes=[
            "daily_execution_reconciliation_only",
            "backtest_expected_vs_observed_paper_or_live_records",
            "no_order_submission_performed",
            "no_live_trading_authorization_granted",
        ],
    )


def render_daily_execution_reconciliation_markdown(report: DailyExecutionReconciliationReport) -> str:
    metrics = report.metrics
    lines = [
        "# C5 Daily Execution Reconciliation",
        "",
        f"Status: **{report.status.value}**",
        "",
        "## Metrics",
        "",
        f"- Expected records: {metrics.expected_count}",
        f"- Observed records: {metrics.observed_count}",
        f"- Matched records: {metrics.matched_count}",
        f"- Missing observed records: {metrics.missing_count}",
        f"- Unexpected observed records: {metrics.unexpected_count}",
        f"- Expected total R: {metrics.expected_total_r:.4f}",
        f"- Observed total R: {metrics.observed_total_r:.4f}",
        f"- Total R drift: {metrics.total_r_drift:.4f}",
        f"- Max abs quantity drift: {metrics.max_abs_quantity_drift:.6f}",
        f"- Max abs price drift pct: {metrics.max_abs_price_drift_pct:.4%}",
        f"- Max abs R drift: {metrics.max_abs_r_drift:.4f}",
        "",
        "## Comparisons",
        "",
        "| Key | Status | Symbol | Side | Quantity Drift | Price Drift % | R Drift |",
        "|---|---:|---|---:|---:|---:|---:|",
    ]
    for comparison in report.comparisons:
        lines.append(
            f"| {comparison.key} | {comparison.status.value} | {comparison.symbol} | {comparison.side} | "
            f"{comparison.quantity_drift:.6f} | {comparison.price_drift_pct:.4%} | {comparison.r_drift:.4f} |"
        )
    lines.extend(["", "## Issues", ""])
    if not report.issues:
        lines.append("- none")
    else:
        for issue in report.issues:
            lines.append(f"- **{issue.severity.value}** `{issue.code}`: {issue.message}")
    lines.extend(["", "## Safety Boundary", ""])
    for note in report.notes:
        lines.append(f"- {note}")
    return "\n".join(lines).rstrip() + "\n"


def write_daily_execution_reconciliation_report(
    report: DailyExecutionReconciliationReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_daily_execution_reconciliation_markdown(report), encoding="utf-8")


def load_expected_execution_records(path: Path) -> list[ExpectedExecutionRecord]:
    return [_expected_from(item) for item in _load_json_list(path)]


def load_observed_execution_records(path: Path) -> list[ObservedExecutionRecord]:
    return [_observed_from(item) for item in _load_json_list(path)]


def _load_json_list(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        records = payload.get("records", [])
    else:
        records = payload
    if not isinstance(records, list):
        raise ValueError("execution reconciliation input must be a JSON list or an object with records[]")
    return [record for record in records if isinstance(record, dict)]


def _expected_from(record: ExpectedExecutionRecord | dict[str, Any]) -> ExpectedExecutionRecord:
    if isinstance(record, ExpectedExecutionRecord):
        return record
    return ExpectedExecutionRecord(
        signal_id=str(record.get("signal_id", "")).strip(),
        symbol=str(record.get("symbol", "")).strip().upper(),
        side=str(record.get("side", "")).strip().lower(),
        expected_quantity=float(record.get("expected_quantity", record.get("quantity", 0.0))),
        expected_avg_price=float(record.get("expected_avg_price", record.get("average_price", 0.0))),
        expected_r=float(record.get("expected_r", record.get("result_r", 0.0))),
        strategy_id=str(record.get("strategy_id", "default")).strip() or "default",
        expected_order_id=_optional_str(record.get("expected_order_id", record.get("order_id"))),
    )


def _observed_from(record: ObservedExecutionRecord | dict[str, Any]) -> ObservedExecutionRecord:
    if isinstance(record, ObservedExecutionRecord):
        return record
    return ObservedExecutionRecord(
        signal_id=str(record.get("signal_id", "")).strip(),
        symbol=str(record.get("symbol", "")).strip().upper(),
        side=str(record.get("side", "")).strip().lower(),
        filled_quantity=float(record.get("filled_quantity", record.get("quantity", 0.0))),
        average_fill_price=float(record.get("average_fill_price", record.get("fill_price", record.get("average_price", 0.0)))),
        realized_r=float(record.get("realized_r", record.get("result_r", 0.0))),
        status=str(record.get("status", "observed")).strip().lower(),
        strategy_id=str(record.get("strategy_id", "default")).strip() or "default",
        order_id=_optional_str(record.get("order_id", record.get("expected_order_id"))),
        commission=float(record.get("commission", 0.0)),
    )


def _index_expected(records: list[ExpectedExecutionRecord], issues: list[DailyExecutionIssue]) -> dict[str, ExpectedExecutionRecord]:
    indexed: dict[str, ExpectedExecutionRecord] = {}
    for record in records:
        key = record.key()
        _validate_expected_record(record, issues, key)
        if key in indexed:
            issues.append(_issue("duplicate_expected_execution", key, "duplicate expected execution key"))
        indexed[key] = record
    return indexed


def _index_observed(records: list[ObservedExecutionRecord], issues: list[DailyExecutionIssue]) -> dict[str, ObservedExecutionRecord]:
    indexed: dict[str, ObservedExecutionRecord] = {}
    for record in records:
        key = record.key()
        _validate_observed_record(record, issues, key)
        if key in indexed:
            issues.append(_issue("duplicate_observed_execution", key, "duplicate observed execution key"))
        indexed[key] = record
    return indexed


def _validate_expected_record(record: ExpectedExecutionRecord, issues: list[DailyExecutionIssue], key: str) -> None:
    if not record.signal_id:
        issues.append(_issue("missing_expected_signal_id", key, "expected record is missing signal_id"))
    if not record.symbol:
        issues.append(_issue("missing_expected_symbol", key, "expected record is missing symbol"))
    if record.side not in {"buy", "sell"}:
        issues.append(_issue("invalid_expected_side", key, "expected side must be buy or sell"))
    if record.expected_quantity <= 0:
        issues.append(_issue("invalid_expected_quantity", key, "expected quantity must be positive"))
    if record.expected_avg_price <= 0:
        issues.append(_issue("invalid_expected_price", key, "expected average price must be positive"))


def _validate_observed_record(record: ObservedExecutionRecord, issues: list[DailyExecutionIssue], key: str) -> None:
    if not record.signal_id:
        issues.append(_issue("missing_observed_signal_id", key, "observed record is missing signal_id"))
    if not record.symbol:
        issues.append(_issue("missing_observed_symbol", key, "observed record is missing symbol"))
    if record.side not in {"buy", "sell"}:
        issues.append(_issue("invalid_observed_side", key, "observed side must be buy or sell"))
    if record.filled_quantity < 0:
        issues.append(_issue("invalid_observed_quantity", key, "observed filled quantity must not be negative"))
    if record.average_fill_price <= 0 and record.filled_quantity > 0:
        issues.append(_issue("invalid_observed_price", key, "observed average fill price must be positive when quantity is filled"))
    if record.commission < 0:
        issues.append(_issue("invalid_observed_commission", key, "observed commission must not be negative"))


def _compare_records(
    key: str,
    expected: ExpectedExecutionRecord,
    observed: ObservedExecutionRecord,
    *,
    config: DailyExecutionReconciliationConfig,
) -> ExecutionComparison:
    issues: list[DailyExecutionIssue] = []
    if expected.signal_id != observed.signal_id:
        issues.append(_issue("signal_id_mismatch", key, "expected and observed signal_id differ"))
    if expected.symbol != observed.symbol:
        issues.append(_issue("symbol_mismatch", key, "expected and observed symbol differ"))
    if expected.side != observed.side:
        issues.append(_issue("side_mismatch", key, "expected and observed side differ"))

    quantity_drift = round(observed.filled_quantity - expected.expected_quantity, 6)
    price_drift_pct = round(
        (observed.average_fill_price - expected.expected_avg_price) / expected.expected_avg_price
        if expected.expected_avg_price > 0
        else 0.0,
        6,
    )
    r_drift = round(observed.realized_r - expected.expected_r, 6)

    if abs(quantity_drift) > config.max_abs_quantity_drift:
        issues.append(_issue("quantity_drift_exceeded", key, "observed filled quantity differs from expected quantity"))
    if abs(price_drift_pct) > config.max_abs_price_drift_pct:
        issues.append(_issue("price_drift_exceeded", key, "observed average fill price drift exceeds tolerance"))
    if abs(r_drift) > config.max_abs_r_drift:
        issues.append(_issue("r_drift_exceeded", key, "observed realized R differs from expected R beyond tolerance"))

    has_errors = any(issue.severity == DailyExecutionSeverity.ERROR for issue in issues)
    return ExecutionComparison(
        key=key,
        signal_id=expected.signal_id,
        symbol=expected.symbol,
        side=expected.side,
        quantity_drift=quantity_drift,
        price_drift_pct=price_drift_pct,
        r_drift=r_drift,
        status=DailyExecutionStatus.FAIL if has_errors else DailyExecutionStatus.PASS,
        issues=issues,
    )


def _build_metrics(
    expected: list[ExpectedExecutionRecord],
    observed: list[ObservedExecutionRecord],
    comparisons: list[ExecutionComparison],
    issues: list[DailyExecutionIssue],
) -> DailyExecutionMetrics:
    expected_keys = {record.key() for record in expected}
    observed_keys = {record.key() for record in observed}
    expected_total_r = round(sum(record.expected_r for record in expected), 6)
    observed_total_r = round(sum(record.realized_r for record in observed if record.key() in expected_keys), 6)
    return DailyExecutionMetrics(
        expected_count=len(expected),
        observed_count=len(observed),
        matched_count=len(comparisons),
        missing_count=len(expected_keys - observed_keys),
        unexpected_count=len(observed_keys - expected_keys),
        failed_comparison_count=sum(1 for comparison in comparisons if comparison.status == DailyExecutionStatus.FAIL),
        warning_comparison_count=sum(1 for issue in issues if issue.severity == DailyExecutionSeverity.WARNING),
        expected_total_r=expected_total_r,
        observed_total_r=observed_total_r,
        total_r_drift=round(observed_total_r - expected_total_r, 6),
        max_abs_quantity_drift=max((abs(comparison.quantity_drift) for comparison in comparisons), default=0.0),
        max_abs_price_drift_pct=max((abs(comparison.price_drift_pct) for comparison in comparisons), default=0.0),
        max_abs_r_drift=max((abs(comparison.r_drift) for comparison in comparisons), default=0.0),
    )


def _issue(code: str, key: str | None, message: str) -> DailyExecutionIssue:
    return DailyExecutionIssue(
        severity=DailyExecutionSeverity.ERROR,
        code=code,
        message=message,
        key=key,
    )


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
