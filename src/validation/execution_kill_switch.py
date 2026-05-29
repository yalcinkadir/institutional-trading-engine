from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Iterable


class ExecutionKillSwitchStatus(str, Enum):
    ALLOW = "ALLOW"
    WATCH = "WATCH"
    BLOCK = "BLOCK"


class ExecutionKillSwitchSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class DrawdownSourceType(str, Enum):
    BROKER_EQUITY = "broker_equity"
    RECONCILED_PAPER_EQUITY = "reconciled_paper_equity"
    BACKTEST_ONLY = "backtest_only"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ExecutionKillSwitchConfig:
    block_on_failed_daily_reconciliation: bool = True
    block_on_failed_fill_quality: bool = True
    block_on_manual_risk_flag: bool = True
    max_total_r_drift: float = 0.5
    max_avg_abs_slippage_bps: float = 25.0
    max_fill_quality_issue_errors: int = 0
    watch_total_r_drift: float = 0.25
    watch_avg_abs_slippage_bps: float = 15.0
    watch_fill_rate: float = 0.98
    require_daily_reconciliation_report: bool = True
    require_fill_quality_report: bool = True
    require_drawdown_source_validation: bool = True
    drawdown_calculation_tolerance_pct: float = 0.05
    watch_drawdown_pct: float = 7.5
    max_drawdown_pct: float = 10.0


@dataclass(frozen=True)
class DrawdownSourceValidation:
    source_name: str
    source_type: DrawdownSourceType
    account_equity: float
    peak_equity: float
    drawdown_pct: float
    is_reconciled: bool
    evidence_artifact: str
    validated_at: str = ""
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["source_type"] = self.source_type.value
        payload["notes"] = list(self.notes)
        return payload


@dataclass(frozen=True)
class ManualRiskFlag:
    code: str
    message: str
    severity: ExecutionKillSwitchSeverity = ExecutionKillSwitchSeverity.ERROR

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["severity"] = self.severity.value
        return payload


@dataclass(frozen=True)
class ExecutionKillSwitchReason:
    severity: ExecutionKillSwitchSeverity
    code: str
    message: str
    source: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["severity"] = self.severity.value
        return payload


@dataclass(frozen=True)
class ExecutionKillSwitchDecision:
    status: ExecutionKillSwitchStatus
    blocked: bool
    reasons: list[ExecutionKillSwitchReason] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "blocked": self.blocked,
            "reasons": [reason.to_dict() for reason in self.reasons],
            "notes": list(self.notes),
        }


def evaluate_execution_kill_switch(
    *,
    daily_reconciliation_report: dict[str, Any] | Any | None = None,
    fill_quality_report: dict[str, Any] | Any | None = None,
    drawdown_source_validation: dict[str, Any] | DrawdownSourceValidation | None = None,
    manual_risk_flags: Iterable[ManualRiskFlag | dict[str, Any]] | None = None,
    config: ExecutionKillSwitchConfig = ExecutionKillSwitchConfig(),
) -> ExecutionKillSwitchDecision:
    reasons: list[ExecutionKillSwitchReason] = []
    manual_flags = [_manual_flag_from(flag) for flag in (manual_risk_flags or [])]

    daily_payload = _to_payload(daily_reconciliation_report)
    fill_payload = _to_payload(fill_quality_report)
    drawdown_validation = _drawdown_validation_from(drawdown_source_validation)

    if daily_payload is None and config.require_daily_reconciliation_report:
        reasons.append(_error("missing_daily_reconciliation_report", "daily execution reconciliation report is required", "daily_reconciliation"))
    if fill_payload is None and config.require_fill_quality_report:
        reasons.append(_error("missing_fill_quality_report", "fill-quality report is required", "fill_quality"))
    if drawdown_validation is None and config.require_drawdown_source_validation:
        reasons.append(_error("missing_drawdown_source_validation", "validated drawdown source is required before kill-switch drawdown governance can be considered active", "drawdown_source"))

    if daily_payload is not None:
        _evaluate_daily_reconciliation(daily_payload, reasons, config)
    if fill_payload is not None:
        _evaluate_fill_quality(fill_payload, reasons, config)
    if drawdown_validation is not None:
        _evaluate_drawdown_source(drawdown_validation, reasons, config)

    for flag in manual_flags:
        severity = flag.severity
        reasons.append(ExecutionKillSwitchReason(severity, flag.code, flag.message, "manual_risk_flag"))

    has_blocker = any(reason.severity == ExecutionKillSwitchSeverity.ERROR for reason in reasons)
    has_warning = any(reason.severity == ExecutionKillSwitchSeverity.WARNING for reason in reasons)
    status = ExecutionKillSwitchStatus.BLOCK if has_blocker else ExecutionKillSwitchStatus.WATCH if has_warning else ExecutionKillSwitchStatus.ALLOW

    notes = [
        "execution_kill_switch_governance_only",
        "fail_closed_when_required_evidence_is_missing_or_failed",
        "does_not_submit_orders",
        "does_not_authorize_live_trading",
    ]
    if drawdown_validation is not None and not any(reason.source == "drawdown_source" and reason.severity == ExecutionKillSwitchSeverity.ERROR for reason in reasons):
        notes.append("drawdown_source_validated")
    if drawdown_validation is not None and not any(reason.source == "drawdown_source" and reason.code == "drawdown_block_threshold_exceeded" for reason in reasons):
        notes.append("drawdown_magnitude_checked")

    return ExecutionKillSwitchDecision(
        status=status,
        blocked=status == ExecutionKillSwitchStatus.BLOCK,
        reasons=reasons,
        notes=notes,
    )


def load_kill_switch_input(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("kill-switch input must be a JSON object")
    return payload


def write_execution_kill_switch_decision(decision: ExecutionKillSwitchDecision, *, json_path: Path, markdown_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(decision.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_execution_kill_switch_markdown(decision), encoding="utf-8")


def render_execution_kill_switch_markdown(decision: ExecutionKillSwitchDecision) -> str:
    lines = [
        "# C7 Execution Kill Switch Decision",
        "",
        f"Status: **{decision.status.value}**",
        f"Blocked: **{str(decision.blocked).lower()}**",
        "",
        "## Reasons",
        "",
    ]
    if decision.reasons:
        for reason in decision.reasons:
            lines.append(f"- **{reason.severity.value.upper()}** `{reason.code}` from `{reason.source}` — {reason.message}")
    else:
        lines.append("- None")
    lines.extend(["", "## Safety Notes", ""])
    lines.extend(f"- {note}" for note in decision.notes)
    return "\n".join(lines).rstrip() + "\n"


def _evaluate_daily_reconciliation(payload: dict[str, Any], reasons: list[ExecutionKillSwitchReason], config: ExecutionKillSwitchConfig) -> None:
    status = str(payload.get("status", "")).upper()
    passed = bool(payload.get("passed", False))
    metrics = payload.get("metrics", {}) if isinstance(payload.get("metrics", {}), dict) else {}
    total_r_drift = abs(float(metrics.get("total_r_drift", 0.0)))

    if config.block_on_failed_daily_reconciliation and (status == "FAIL" or not passed):
        reasons.append(_error("daily_reconciliation_failed", "daily expected-vs-observed reconciliation failed", "daily_reconciliation"))
    elif status == "WARN":
        reasons.append(_warning("daily_reconciliation_warning", "daily expected-vs-observed reconciliation is in warning state", "daily_reconciliation"))

    if total_r_drift > config.max_total_r_drift:
        reasons.append(_error("total_r_drift_block_threshold_exceeded", "total R drift exceeds block threshold", "daily_reconciliation"))
    elif total_r_drift > config.watch_total_r_drift:
        reasons.append(_warning("total_r_drift_watch_threshold_exceeded", "total R drift exceeds watch threshold", "daily_reconciliation"))


def _evaluate_fill_quality(payload: dict[str, Any], reasons: list[ExecutionKillSwitchReason], config: ExecutionKillSwitchConfig) -> None:
    status = str(payload.get("status", "")).upper()
    passed = bool(payload.get("passed", False))
    metrics = payload.get("metrics", {}) if isinstance(payload.get("metrics", {}), dict) else {}
    issues = payload.get("issues", []) if isinstance(payload.get("issues", []), list) else []

    avg_abs_slippage = abs(float(metrics.get("avg_abs_slippage_bps", 0.0)))
    fill_rate = float(metrics.get("fill_rate", 1.0))
    error_count = sum(1 for issue in issues if isinstance(issue, dict) and str(issue.get("severity", "")).lower() == "error")

    if config.block_on_failed_fill_quality and (status == "FAIL" or not passed):
        reasons.append(_error("fill_quality_failed", "fill-quality report failed", "fill_quality"))
    elif status == "WARN":
        reasons.append(_warning("fill_quality_warning", "fill-quality report is in warning state", "fill_quality"))

    if avg_abs_slippage > config.max_avg_abs_slippage_bps:
        reasons.append(_error("avg_abs_slippage_block_threshold_exceeded", "average absolute slippage exceeds block threshold", "fill_quality"))
    elif avg_abs_slippage > config.watch_avg_abs_slippage_bps:
        reasons.append(_warning("avg_abs_slippage_watch_threshold_exceeded", "average absolute slippage exceeds watch threshold", "fill_quality"))

    if fill_rate < config.watch_fill_rate:
        reasons.append(_warning("fill_rate_watch_threshold_breached", "fill rate is below watch threshold", "fill_quality"))

    if error_count > config.max_fill_quality_issue_errors:
        reasons.append(_error("fill_quality_error_count_exceeded", "fill-quality error issue count exceeds configured maximum", "fill_quality"))


def _evaluate_drawdown_source(validation: DrawdownSourceValidation, reasons: list[ExecutionKillSwitchReason], config: ExecutionKillSwitchConfig) -> None:
    source = "drawdown_source"

    if validation.source_type in {DrawdownSourceType.BACKTEST_ONLY, DrawdownSourceType.UNKNOWN}:
        reasons.append(_error("invalid_drawdown_source_type", "drawdown source must be broker equity or reconciled paper equity, not backtest-only or unknown", source))

    if not validation.is_reconciled:
        reasons.append(_error("unreconciled_drawdown_source", "drawdown source must be reconciled before kill-switch drawdown governance is active", source))

    if validation.account_equity <= 0 or validation.peak_equity <= 0:
        reasons.append(_error("invalid_drawdown_equity_values", "drawdown source equity and peak equity must be positive", source))
        return

    if validation.account_equity > validation.peak_equity:
        reasons.append(_error("current_equity_above_peak_equity", "drawdown source current equity cannot exceed peak equity", source))
        return

    if not validation.evidence_artifact.strip():
        reasons.append(_error("missing_drawdown_evidence_artifact", "drawdown source validation must reference an evidence artifact", source))

    calculated_drawdown_pct = round(((validation.peak_equity - validation.account_equity) / validation.peak_equity) * 100, 6)
    if abs(calculated_drawdown_pct - validation.drawdown_pct) > config.drawdown_calculation_tolerance_pct:
        reasons.append(_error("drawdown_calculation_mismatch", "reported drawdown percentage does not match current and peak equity", source))
        return

    if validation.drawdown_pct > config.max_drawdown_pct:
        reasons.append(_error("drawdown_block_threshold_exceeded", "validated drawdown percentage exceeds block threshold", source))
    elif validation.drawdown_pct > config.watch_drawdown_pct:
        reasons.append(_warning("drawdown_watch_threshold_exceeded", "validated drawdown percentage exceeds watch threshold", source))


def _to_payload(report: dict[str, Any] | Any | None) -> dict[str, Any] | None:
    if report is None:
        return None
    if isinstance(report, dict):
        return report
    if hasattr(report, "to_dict"):
        payload = report.to_dict()
        if isinstance(payload, dict):
            return payload
    raise TypeError("report must be a dict, object with to_dict(), or None")


def _drawdown_validation_from(validation: dict[str, Any] | DrawdownSourceValidation | None) -> DrawdownSourceValidation | None:
    if validation is None:
        return None
    if isinstance(validation, DrawdownSourceValidation):
        return validation
    if not isinstance(validation, dict):
        raise TypeError("drawdown_source_validation must be a dict, DrawdownSourceValidation, or None")

    return DrawdownSourceValidation(
        source_name=str(validation.get("source_name", "")).strip(),
        source_type=DrawdownSourceType(str(validation.get("source_type", DrawdownSourceType.UNKNOWN.value)).lower()),
        account_equity=float(validation.get("account_equity", 0.0)),
        peak_equity=float(validation.get("peak_equity", 0.0)),
        drawdown_pct=float(validation.get("drawdown_pct", 0.0)),
        is_reconciled=bool(validation.get("is_reconciled", False)),
        evidence_artifact=str(validation.get("evidence_artifact", "")).strip(),
        validated_at=str(validation.get("validated_at", "")).strip(),
        notes=tuple(str(note) for note in validation.get("notes", ()) if str(note).strip()),
    )


def _manual_flag_from(flag: ManualRiskFlag | dict[str, Any]) -> ManualRiskFlag:
    if isinstance(flag, ManualRiskFlag):
        return flag
    severity = ExecutionKillSwitchSeverity(str(flag.get("severity", "error")).lower())
    return ManualRiskFlag(
        code=str(flag.get("code", "manual_risk_flag")).strip() or "manual_risk_flag",
        message=str(flag.get("message", "manual risk flag raised")).strip() or "manual risk flag raised",
        severity=severity,
    )


def _error(code: str, message: str, source: str) -> ExecutionKillSwitchReason:
    return ExecutionKillSwitchReason(ExecutionKillSwitchSeverity.ERROR, code, message, source)


def _warning(code: str, message: str, source: str) -> ExecutionKillSwitchReason:
    return ExecutionKillSwitchReason(ExecutionKillSwitchSeverity.WARNING, code, message, source)
