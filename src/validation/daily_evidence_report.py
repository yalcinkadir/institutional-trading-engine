from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class DailyEvidenceConfig:
    require_reconciliation: bool = True
    require_performance_drift: bool = True
    require_edge_decay: bool = True
    require_regime_change: bool = True
    require_risk_attribution: bool = True
    require_monte_carlo: bool = True
    max_failed_components: int = 0


@dataclass(frozen=True)
class EvidenceComponentSummary:
    name: str
    present: bool
    passed: bool
    status: str
    reason: str
    key_metrics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DailyEvidenceMetrics:
    report_date: str
    components_expected: int
    components_present: int
    components_passed: int
    components_failed: int
    components_missing: int
    overall_status: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DailyEvidenceGate:
    name: str
    passed: bool
    value: float | int | str | bool
    threshold: float | int | str | bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DailyEvidenceReport:
    passed: bool
    metrics: DailyEvidenceMetrics
    components: list[EvidenceComponentSummary] = field(default_factory=list)
    gates: list[DailyEvidenceGate] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "metrics": self.metrics.to_dict(),
            "components": [component.to_dict() for component in self.components],
            "gates": [gate.to_dict() for gate in self.gates],
        }


_COMPONENTS: tuple[tuple[str, str], ...] = (
    ("reconciliation", "require_reconciliation"),
    ("performance_drift", "require_performance_drift"),
    ("edge_decay", "require_edge_decay"),
    ("regime_change", "require_regime_change"),
    ("risk_attribution", "require_risk_attribution"),
    ("monte_carlo", "require_monte_carlo"),
)

_KEY_METRIC_ALLOWLIST: dict[str, tuple[str, ...]] = {
    "reconciliation": ("observation_days", "action_mismatch_rate", "max_abs_daily_drift_r", "unresolved_records"),
    "performance_drift": ("forward_expectancy_r", "expectancy_drift_r", "win_rate_drift", "z_score"),
    "edge_decay": ("observations", "win_rate", "expectancy_r", "decision"),
    "regime_change": ("latest_regime", "change_score", "state"),
    "risk_attribution": ("portfolio_r", "max_single_name_contribution_r", "max_sector_contribution_r", "unknown_sector_count"),
    "monte_carlo": ("observed_expectancy_r", "bootstrap_expectancy_lower_r", "permutation_p_value", "drawdown_p95_r"),
}


def build_daily_evidence_report(
    component_reports: dict[str, Any],
    *,
    report_date: str | date | None = None,
    config: DailyEvidenceConfig = DailyEvidenceConfig(),
) -> DailyEvidenceReport:
    normalized_date = _normalize_date(report_date)
    components = [_summarize_component(name, component_reports.get(name), required=getattr(config, attr)) for name, attr in _COMPONENTS]
    gates = _build_gates(components, config=config)
    passed = all(gate.passed for gate in gates)
    metrics = _build_metrics(normalized_date, components, passed=passed)
    return DailyEvidenceReport(passed=passed, metrics=metrics, components=components, gates=gates)


def render_daily_evidence_markdown(report: DailyEvidenceReport) -> str:
    metrics = report.metrics
    lines = [
        "# Daily Evidence Report",
        "",
        f"Date: **{metrics.report_date}**",
        f"Status: **{metrics.overall_status}**",
        "",
        "## Summary",
        "",
        f"- Components expected: {metrics.components_expected}",
        f"- Components present: {metrics.components_present}",
        f"- Components passed: {metrics.components_passed}",
        f"- Components failed: {metrics.components_failed}",
        f"- Components missing: {metrics.components_missing}",
        "",
        "## Components",
        "",
        "| Component | Present | Status | Reason |",
        "|---|---:|---:|---|",
    ]
    for component in report.components:
        lines.append(
            f"| {component.name} | {_format_bool(component.present)} | {component.status} | {component.reason} |"
        )
    lines.extend(["", "## Gates", "", "| Gate | Status | Value | Threshold |", "|---|---:|---:|---:|"])
    for gate in report.gates:
        lines.append(
            f"| {gate.name} | {'PASS' if gate.passed else 'FAIL'} | "
            f"{_format_value(gate.value)} | {_format_value(gate.threshold)} |"
        )
    lines.extend(["", "## Key Metrics", ""])
    for component in report.components:
        lines.append(f"### {component.name}")
        if component.key_metrics:
            for key, value in component.key_metrics.items():
                lines.append(f"- {key}: {_format_value(value)}")
        else:
            lines.append("- none")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_daily_evidence_report(
    report: DailyEvidenceReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_daily_evidence_markdown(report), encoding="utf-8")


def load_component_report(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_component_reports(paths: Iterable[Path]) -> dict[str, Any]:
    reports: dict[str, Any] = {}
    for path in paths:
        component_name = _component_name_from_path(path)
        reports[component_name] = load_component_report(path)
    return reports


def _summarize_component(name: str, report: Any, *, required: bool) -> EvidenceComponentSummary:
    if not required:
        return EvidenceComponentSummary(
            name=name,
            present=True,
            passed=True,
            status="SKIPPED",
            reason="component not required by config",
            key_metrics={},
        )
    if report is None:
        return EvidenceComponentSummary(
            name=name,
            present=False,
            passed=False,
            status="MISSING",
            reason="required component report is missing",
            key_metrics={},
        )
    report_dict = _to_dict(report)
    passed = bool(report_dict.get("passed", False))
    status = "PASS" if passed else "FAIL"
    reason = "component passed" if passed else "component failed"
    metrics = report_dict.get("metrics", {}) if isinstance(report_dict.get("metrics", {}), dict) else {}
    return EvidenceComponentSummary(
        name=name,
        present=True,
        passed=passed,
        status=status,
        reason=reason,
        key_metrics=_extract_key_metrics(name, metrics),
    )


def _build_gates(components: list[EvidenceComponentSummary], *, config: DailyEvidenceConfig) -> list[DailyEvidenceGate]:
    failed = sum(1 for component in components if component.present and not component.passed)
    missing = sum(1 for component in components if not component.present)
    return [
        DailyEvidenceGate(
            name="required_components_present",
            passed=missing == 0,
            value=missing,
            threshold=0,
            message="All required evidence components must be present.",
        ),
        DailyEvidenceGate(
            name="failed_components",
            passed=failed <= config.max_failed_components,
            value=failed,
            threshold=config.max_failed_components,
            message="Failed evidence components must remain within tolerance.",
        ),
    ]


def _build_metrics(report_date: str, components: list[EvidenceComponentSummary], *, passed: bool) -> DailyEvidenceMetrics:
    expected = len(components)
    present = sum(1 for component in components if component.present)
    failed = sum(1 for component in components if component.present and not component.passed)
    missing = sum(1 for component in components if not component.present)
    passed_count = sum(1 for component in components if component.present and component.passed)
    return DailyEvidenceMetrics(
        report_date=report_date,
        components_expected=expected,
        components_present=present,
        components_passed=passed_count,
        components_failed=failed,
        components_missing=missing,
        overall_status="PASS" if passed else "FAIL",
    )


def _extract_key_metrics(name: str, metrics: dict[str, Any]) -> dict[str, Any]:
    allowed = _KEY_METRIC_ALLOWLIST.get(name, ())
    return {key: metrics[key] for key in allowed if key in metrics}


def _to_dict(report: Any) -> dict[str, Any]:
    if isinstance(report, dict):
        return report
    if hasattr(report, "to_dict"):
        return report.to_dict()
    return {}


def _component_name_from_path(path: Path) -> str:
    stem = path.stem.lower().replace("-", "_")
    aliases = {
        "paper_observation_reconciliation": "reconciliation",
        "performance_drift_detection": "performance_drift",
        "sequential_edge_decay": "edge_decay",
        "regime_change_detection": "regime_change",
        "position_risk_attribution": "risk_attribution",
        "monte_carlo_robustness": "monte_carlo",
    }
    return aliases.get(stem, stem)


def _normalize_date(value: str | date | None) -> str:
    if value is None:
        return date.today().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


def _format_bool(value: bool) -> str:
    return "yes" if value else "no"


def _format_value(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)
