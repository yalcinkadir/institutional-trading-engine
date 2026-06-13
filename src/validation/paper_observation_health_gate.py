from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


CORE_SYMBOLS = {"SPY", "QQQ"}
UNKNOWN_REGIMES = {"", "unknown", "n/a", "none", "null"}
DATA_MISSING_REASONS = (
    "missing_close",
    "missing_atr",
    "missing_source",
    "missing_source_timestamp",
    "missing_fallback_level",
    "scanner_metrics_missing",
)
HEALTH_STATUS_OK = "OK"
HEALTH_STATUS_NO_TRADE_VALID = "NO_TRADE_VALID"
HEALTH_STATUS_DEGRADED = "DEGRADED"
HEALTH_STATUS_BLOCKED = "BLOCKED"
HEALTH_STATUS_FAILED = "FAILED"


@dataclass(frozen=True)
class PaperObservationHealthIssue:
    code: str
    message: str
    severity: str = "error"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PaperObservationHealthReport:
    passed: bool
    total_signals: int
    actionable_count: int
    valid_close_count: int
    valid_core_close_count: int
    market_regime: str
    data_quality_status: str
    issues: list[PaperObservationHealthIssue] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    observation_health_status: str = HEALTH_STATUS_OK
    run_timestamp: str = "UNKNOWN"
    workflow_name: str = "UNKNOWN"
    commit_sha: str = "UNKNOWN"
    data_provenance: dict[str, Any] = field(default_factory=dict)
    degradation_reasons: list[str] = field(default_factory=list)
    governance_state: dict[str, Any] = field(default_factory=dict)
    readiness_evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "observation_health_status": self.observation_health_status,
            "run_timestamp": self.run_timestamp,
            "workflow_name": self.workflow_name,
            "commit_sha": self.commit_sha,
            "total_signals": self.total_signals,
            "actionable_count": self.actionable_count,
            "valid_close_count": self.valid_close_count,
            "valid_core_close_count": self.valid_core_close_count,
            "market_regime": self.market_regime,
            "data_quality_status": self.data_quality_status,
            "data_provenance": dict(self.data_provenance),
            "degradation_reasons": list(self.degradation_reasons),
            "governance_state": dict(self.governance_state),
            "readiness_evidence": dict(self.readiness_evidence),
            "issues": [issue.to_dict() for issue in self.issues],
            "warnings": list(self.warnings),
        }


def validate_paper_observation_health(
    payload: dict[str, Any],
    *,
    run_timestamp: str | None = None,
    workflow_name: str | None = None,
    commit_sha: str | None = None,
    scheduled_liveness: dict[str, Any] | None = None,
    watcher_lifecycle: dict[str, Any] | None = None,
) -> PaperObservationHealthReport:
    signals = payload.get("signals")
    if not isinstance(signals, list):
        signals = []

    total_signals = _as_int(payload.get("total_signals"), len(signals))
    actionable_count = _as_int(payload.get("actionable_count"), 0)
    market_regime = str(payload.get("market_regime") or "Unknown")
    data_quality = payload.get("data_quality") if isinstance(payload.get("data_quality"), dict) else {}
    data_quality_status = str(data_quality.get("data_quality_status") or "UNKNOWN").upper()

    valid_close_count = sum(1 for signal in signals if _is_number(signal.get("close")))
    valid_core_close_count = sum(
        1
        for signal in signals
        if signal.get("symbol") in CORE_SYMBOLS and _is_number(signal.get("close"))
    )
    missing_close_count = sum(1 for signal in signals if not _is_number(signal.get("close")))
    data_missing_reason_count = sum(1 for signal in signals if _has_data_missing_reason(signal))

    issues: list[PaperObservationHealthIssue] = []
    warnings: list[str] = []

    if total_signals <= 0:
        issues.append(PaperObservationHealthIssue("no_signals", "paper observation payload contains no signal records"))

    if signals and valid_close_count == 0:
        issues.append(PaperObservationHealthIssue("all_close_values_missing", "all signal close values are null or non-numeric"))
    elif signals and valid_close_count < max(1, len(signals) // 2):
        issues.append(PaperObservationHealthIssue("majority_close_values_missing", "most signal close values are null or non-numeric"))

    if CORE_SYMBOLS.intersection({str(signal.get("symbol")) for signal in signals}) and valid_core_close_count == 0:
        issues.append(PaperObservationHealthIssue("core_market_close_missing", "core market symbols are present but have no valid close values"))

    if _is_unknown_regime(market_regime) and valid_close_count > 0:
        issues.append(PaperObservationHealthIssue("unknown_regime_with_market_data", "market_regime is Unknown despite available close data"))
    elif _is_unknown_regime(market_regime) and valid_close_count == 0:
        issues.append(PaperObservationHealthIssue("unknown_regime_and_no_close_data", "market_regime is Unknown and no close data is available"))

    if signals and missing_close_count == len(signals) and actionable_count == 0:
        issues.append(PaperObservationHealthIssue("zero_actionable_due_to_missing_data", "actionable_count is zero because required market data is missing"))

    if data_missing_reason_count >= max(1, len(signals) // 2):
        issues.append(PaperObservationHealthIssue("scanner_metrics_missing_or_unusable", "scanner metrics appear missing or unusable for most signals"))

    if data_quality_status in {"BLOCKED", "FAILED", "UNKNOWN"} and not issues:
        issues.append(
            PaperObservationHealthIssue(
                f"data_quality_{data_quality_status.lower()}",
                f"paper observation data quality status is {data_quality_status}",
            )
        )
    elif data_quality_status == "DEGRADED":
        warnings.append("Data quality is degraded; run is evidence-producing but not GO-quality.")

    if actionable_count == 0 and not issues:
        warnings.append("No actionable signals, but market data health is valid; treat as normal no-trade day, not infrastructure failure.")

    readiness_evidence = _derive_readiness_evidence(
        scheduled_liveness=scheduled_liveness,
        watcher_lifecycle=watcher_lifecycle,
    )
    issues.extend(_derive_readiness_issues(readiness_evidence))

    data_provenance = _derive_data_provenance(payload, signals, data_quality)
    degradation_reasons = _derive_degradation_reasons(
        issues=issues,
        warnings=warnings,
        payload=payload,
        data_quality_status=data_quality_status,
        data_provenance=data_provenance,
    )
    observation_health_status = _derive_observation_health_status(
        passed=not issues,
        actionable_count=actionable_count,
        degradation_reasons=degradation_reasons,
    )

    return PaperObservationHealthReport(
        passed=not issues,
        total_signals=total_signals,
        actionable_count=actionable_count,
        valid_close_count=valid_close_count,
        valid_core_close_count=valid_core_close_count,
        market_regime=market_regime,
        data_quality_status=data_quality_status,
        issues=issues,
        warnings=warnings,
        observation_health_status=observation_health_status,
        run_timestamp=run_timestamp or str(payload.get("run_timestamp") or _now_iso()),
        workflow_name=workflow_name or str(payload.get("workflow_name") or "UNKNOWN"),
        commit_sha=commit_sha or str(payload.get("commit_sha") or "UNKNOWN"),
        data_provenance=data_provenance,
        degradation_reasons=degradation_reasons,
        governance_state=_derive_governance_state(payload),
        readiness_evidence=readiness_evidence,
    )


def validate_paper_observation_health_file(
    path: Path,
    *,
    run_timestamp: str | None = None,
    workflow_name: str | None = None,
    commit_sha: str | None = None,
    scheduled_liveness_file: Path | None = None,
    watcher_lifecycle_file: Path | None = None,
) -> PaperObservationHealthReport:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        payload = {}
    return validate_paper_observation_health(
        payload,
        run_timestamp=run_timestamp,
        workflow_name=workflow_name,
        commit_sha=commit_sha,
        scheduled_liveness=_read_optional_json(scheduled_liveness_file),
        watcher_lifecycle=_read_optional_json(watcher_lifecycle_file),
    )


def render_paper_observation_health_markdown(report: PaperObservationHealthReport) -> str:
    lines = [
        "# Paper Observation Health Gate",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        f"Observation health: `{report.observation_health_status}`",
        f"Run timestamp: `{report.run_timestamp}`",
        f"Workflow: `{report.workflow_name}`",
        f"Commit SHA: `{report.commit_sha}`",
        f"Market regime: `{report.market_regime}`",
        f"Data quality status: `{report.data_quality_status}`",
        f"Total signals: {report.total_signals}",
        f"Actionable signals: {report.actionable_count}",
        f"Valid close values: {report.valid_close_count}",
        f"Valid core close values: {report.valid_core_close_count}",
        "",
        "## Data provenance",
        "",
        f"- Sources: `{', '.join(report.data_provenance.get('sources', [])) or 'UNKNOWN'}`",
        f"- Fallback levels: `{', '.join(report.data_provenance.get('fallback_levels', [])) or 'UNKNOWN'}`",
        f"- Market-data failures: {len(report.data_provenance.get('market_data_failures', {}))}",
        "",
        "## Governance state",
        "",
        f"- Live trading authorized: `{report.governance_state.get('live_trading_authorized')}`",
        f"- Broker execution mode: `{report.governance_state.get('broker_execution_mode')}`",
        f"- Governance status: `{report.governance_state.get('governance_status')}`",
        "",
        "## Readiness evidence",
        "",
        f"- Scheduled liveness status: `{report.readiness_evidence.get('scheduled_liveness', {}).get('scheduled_report_status', 'NOT_PROVIDED')}`",
        f"- Report liveness status: `{report.readiness_evidence.get('scheduled_liveness', {}).get('report_liveness_status', 'NOT_PROVIDED')}`",
        f"- Productive report cycle: `{report.readiness_evidence.get('scheduled_liveness', {}).get('productive_report_cycle', 'NOT_PROVIDED')}`",
        f"- Watcher evaluated plans: `{report.readiness_evidence.get('watcher_lifecycle', {}).get('evaluated_plan_count', 'NOT_PROVIDED')}`",
        f"- Watcher lifecycle events: `{report.readiness_evidence.get('watcher_lifecycle', {}).get('lifecycle_event_count', 'NOT_PROVIDED')}`",
        "",
        "## Degradation reasons",
        "",
    ]
    if report.degradation_reasons:
        for reason in report.degradation_reasons:
            lines.append(f"- `{reason}`")
    else:
        lines.append("- none")
    lines.extend(["", "## Issues", ""])
    if report.issues:
        for issue in report.issues:
            lines.append(f"- `{issue.code}` ({issue.severity}): {issue.message}")
    else:
        lines.append("- none")
    lines.extend(["", "## Warnings", ""])
    if report.warnings:
        for warning in report.warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("- none")
    return "\n".join(lines).rstrip() + "\n"


def write_paper_observation_health_report(
    report: PaperObservationHealthReport,
    *,
    json_path: Path,
    markdown_path: Path,
    latest_json_path: Path | None = None,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    payload = report.to_dict()
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(render_paper_observation_health_markdown(report), encoding="utf-8")
    if latest_json_path is not None:
        latest_json_path.parent.mkdir(parents=True, exist_ok=True)
        latest_json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _derive_data_provenance(
    payload: dict[str, Any],
    signals: list[dict[str, Any]],
    data_quality: dict[str, Any],
) -> dict[str, Any]:
    sources = sorted({str(signal.get("source")) for signal in signals if signal.get("source")})
    fallback_levels = sorted({str(signal.get("fallback_level")) for signal in signals if signal.get("fallback_level")})
    data_statuses = sorted({str(signal.get("data_status")) for signal in signals if signal.get("data_status")})
    source_timestamps = sorted({str(signal.get("source_timestamp")) for signal in signals if signal.get("source_timestamp")})
    market_data_failures = data_quality.get("market_data_failures") if isinstance(data_quality.get("market_data_failures"), dict) else {}
    return {
        "data_quality_status": str(data_quality.get("data_quality_status") or "UNKNOWN").upper(),
        "sources": sources,
        "fallback_levels": fallback_levels,
        "data_statuses": data_statuses,
        "source_timestamps": source_timestamps,
        "market_data_failures": market_data_failures,
        "signal_payload_version": payload.get("schema_version") or payload.get("signals_schema_version") or "UNKNOWN",
    }


def _derive_readiness_evidence(
    *,
    scheduled_liveness: dict[str, Any] | None,
    watcher_lifecycle: dict[str, Any] | None,
) -> dict[str, Any]:
    evidence: dict[str, Any] = {}
    if isinstance(scheduled_liveness, dict):
        evidence["scheduled_liveness"] = {
            "scheduled_report_status": scheduled_liveness.get("scheduled_report_status"),
            "report_liveness_status": scheduled_liveness.get("report_liveness_status") or scheduled_liveness.get("liveness_status"),
            "productive_report_cycle": scheduled_liveness.get("productive_report_cycle"),
            "current_run_state": scheduled_liveness.get("current_run_state"),
            "errors": list(scheduled_liveness.get("errors", [])) if isinstance(scheduled_liveness.get("errors"), list) else [],
            "warnings": list(scheduled_liveness.get("warnings", [])) if isinstance(scheduled_liveness.get("warnings"), list) else [],
        }
    if isinstance(watcher_lifecycle, dict):
        evidence["watcher_lifecycle"] = {
            "schema_version": watcher_lifecycle.get("schema_version"),
            "evaluated_plan_count": _as_int(watcher_lifecycle.get("evaluated_plan_count"), 0),
            "lifecycle_event_count": _as_int(watcher_lifecycle.get("lifecycle_event_count"), 0),
            "terminal_signal_count": _as_int(watcher_lifecycle.get("terminal_signal_count"), 0),
            "live_trading_authorized": watcher_lifecycle.get("live_trading_authorized", False),
            "broker_execution_mode": watcher_lifecycle.get("broker_execution_mode", "paper_only"),
        }
    return evidence


def _derive_readiness_issues(readiness_evidence: dict[str, Any]) -> list[PaperObservationHealthIssue]:
    issues: list[PaperObservationHealthIssue] = []
    scheduled_liveness = readiness_evidence.get("scheduled_liveness")
    if isinstance(scheduled_liveness, dict):
        scheduled_status = str(scheduled_liveness.get("scheduled_report_status") or "UNKNOWN")
        liveness_status = str(scheduled_liveness.get("report_liveness_status") or "UNKNOWN")
        productive_cycle = scheduled_liveness.get("productive_report_cycle") is True
        current_run_state = str(scheduled_liveness.get("current_run_state") or "UNKNOWN")
        if scheduled_status != "PASSED" or liveness_status != "REPORT_LIVENESS_OK" or not productive_cycle:
            issues.append(
                PaperObservationHealthIssue(
                    "scheduled_report_liveness_not_ready",
                    "scheduled report liveness is not green for the current Paper Observation readiness decision",
                )
            )
        elif current_run_state not in {"UNKNOWN", "WORKFLOW_RAN_VALIDATED"}:
            issues.append(
                PaperObservationHealthIssue(
                    "scheduled_report_current_run_not_validated",
                    "scheduled report liveness exists but the current run was not validated",
                )
            )

    watcher_lifecycle = readiness_evidence.get("watcher_lifecycle")
    if isinstance(watcher_lifecycle, dict):
        evaluated_plan_count = _as_int(watcher_lifecycle.get("evaluated_plan_count"), 0)
        lifecycle_event_count = _as_int(watcher_lifecycle.get("lifecycle_event_count"), 0)
        terminal_signal_count = _as_int(watcher_lifecycle.get("terminal_signal_count"), 0)
        if evaluated_plan_count <= 0 or lifecycle_event_count <= 0 or terminal_signal_count <= 0:
            issues.append(
                PaperObservationHealthIssue(
                    "watcher_lifecycle_evidence_missing",
                    "watcher lifecycle evidence is empty or incomplete for the current Paper Observation readiness decision",
                )
            )
        if watcher_lifecycle.get("live_trading_authorized") is True:
            issues.append(
                PaperObservationHealthIssue(
                    "watcher_lifecycle_live_trading_authorized",
                    "watcher lifecycle evidence must remain paper-only",
                )
            )
    return issues


def _derive_degradation_reasons(
    *,
    issues: list[PaperObservationHealthIssue],
    warnings: list[str],
    payload: dict[str, Any],
    data_quality_status: str,
    data_provenance: dict[str, Any],
) -> list[str]:
    reasons: set[str] = {issue.code for issue in issues}
    if data_quality_status not in {"OK", ""}:
        reasons.add(f"data_quality_{data_quality_status.lower()}")
    for fallback in data_provenance.get("fallback_levels", []):
        if str(fallback).lower() not in {"", "primary"}:
            reasons.add("non_primary_fallback_active")
    if data_provenance.get("market_data_failures"):
        reasons.add("market_data_failures_present")
    run_health = payload.get("run_health") if isinstance(payload.get("run_health"), dict) else {}
    for reason in run_health.get("reasons", []) if isinstance(run_health.get("reasons"), list) else []:
        reasons.add(str(reason))
    for warning in warnings:
        if warning.startswith("Data quality is degraded"):
            reasons.add("data_quality_degraded")
    return sorted(reason for reason in reasons if reason)


def _derive_observation_health_status(
    *,
    passed: bool,
    actionable_count: int,
    degradation_reasons: list[str],
) -> str:
    if not passed:
        if any("failed" in reason or "no_signals" in reason for reason in degradation_reasons):
            return HEALTH_STATUS_FAILED
        return HEALTH_STATUS_BLOCKED
    if degradation_reasons:
        return HEALTH_STATUS_DEGRADED
    if actionable_count == 0:
        return HEALTH_STATUS_NO_TRADE_VALID
    return HEALTH_STATUS_OK


def _derive_governance_state(payload: dict[str, Any]) -> dict[str, Any]:
    governance = payload.get("governance_state") or payload.get("governance") or payload.get("governance_status")
    if isinstance(governance, dict):
        result = dict(governance)
    else:
        result = {"governance_status": str(governance or "NOT_EVALUATED")}
    result.setdefault("live_trading_authorized", False)
    result.setdefault("broker_execution_mode", "paper_only")
    result.setdefault("governance_status", "NOT_EVALUATED")
    return result


def _read_optional_json(path: Path | None) -> dict[str, Any] | None:
    if path is None or not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else None


def _has_data_missing_reason(signal: dict[str, Any]) -> bool:
    text_parts = [
        str(signal.get("entry_reason") or ""),
        str(signal.get("stop_reason") or ""),
        str(signal.get("exit_reason") or ""),
        str(signal.get("notes") or ""),
    ]
    joined = " ".join(text_parts).lower()
    return any(reason in joined for reason in DATA_MISSING_REASONS)


def _is_number(value: Any) -> bool:
    if isinstance(value, bool) or value is None:
        return False
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return number == number and number not in {float("inf"), float("-inf")}


def _as_int(value: Any, fallback: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def _is_unknown_regime(value: str) -> bool:
    return value.strip().lower() in UNKNOWN_REGIMES


def _now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
