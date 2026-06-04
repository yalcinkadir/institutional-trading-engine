from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
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

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "total_signals": self.total_signals,
            "actionable_count": self.actionable_count,
            "valid_close_count": self.valid_close_count,
            "valid_core_close_count": self.valid_core_close_count,
            "market_regime": self.market_regime,
            "data_quality_status": self.data_quality_status,
            "issues": [issue.to_dict() for issue in self.issues],
            "warnings": list(self.warnings),
        }


def validate_paper_observation_health(payload: dict[str, Any]) -> PaperObservationHealthReport:
    signals = payload.get("signals")
    if not isinstance(signals, list):
        signals = []

    total_signals = _as_int(payload.get("total_signals"), len(signals))
    actionable_count = _as_int(payload.get("actionable_count"), 0)
    market_regime = str(payload.get("market_regime") or "Unknown")
    data_quality = payload.get("data_quality") if isinstance(payload.get("data_quality"), dict) else {}
    data_quality_status = str(data_quality.get("data_quality_status") or "UNKNOWN")

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

    if actionable_count == 0 and not issues:
        warnings.append("No actionable signals, but market data health is valid; treat as normal no-trade day, not infrastructure failure.")

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
    )


def validate_paper_observation_health_file(path: Path) -> PaperObservationHealthReport:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        payload = {}
    return validate_paper_observation_health(payload)


def render_paper_observation_health_markdown(report: PaperObservationHealthReport) -> str:
    lines = [
        "# Paper Observation Health Gate",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        f"Market regime: `{report.market_regime}`",
        f"Data quality status: `{report.data_quality_status}`",
        f"Total signals: {report.total_signals}",
        f"Actionable signals: {report.actionable_count}",
        f"Valid close values: {report.valid_close_count}",
        f"Valid core close values: {report.valid_core_close_count}",
        "",
        "## Issues",
        "",
    ]
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
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_paper_observation_health_markdown(report), encoding="utf-8")


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
