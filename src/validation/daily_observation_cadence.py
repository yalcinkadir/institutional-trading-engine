from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

CADENCE_VERSION = "2026.05.27-v1"

RAW_SOURCE_FILES = (
    "paper_observations.json",
    "backtest_results.json",
    "regime_observations.json",
    "position_snapshots.json",
)

COMPONENT_REPORT_FILES = (
    "paper_observation_reconciliation.json",
    "performance_drift_detection.json",
    "sequential_edge_decay.json",
    "regime_change_detection.json",
    "position_risk_attribution.json",
    "monte_carlo_robustness.json",
)


@dataclass(frozen=True)
class CadenceGate:
    name: str
    passed: bool
    value: str | int | bool | None
    threshold: str | int | bool | None
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CadenceReport:
    passed: bool
    report_date: str
    cadence_version: str
    observation_only: bool
    raw_source_dir: str
    artifact_root: str
    gates: list[CadenceGate] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "report_date": self.report_date,
            "cadence_version": self.cadence_version,
            "observation_only": self.observation_only,
            "raw_source_dir": self.raw_source_dir,
            "artifact_root": self.artifact_root,
            "gates": [gate.to_dict() for gate in self.gates],
            "warnings": list(self.warnings),
        }


def review_daily_observation_cadence(
    *,
    report_date: str,
    raw_source_dir: Path,
    artifact_root: Path,
) -> CadenceReport:
    raw_files_present = [name for name in RAW_SOURCE_FILES if (raw_source_dir / name).exists()]
    raw_records = _count_records(raw_source_dir, RAW_SOURCE_FILES)
    component_dir = artifact_root / "daily_evidence_components"
    evidence_dir = artifact_root / "daily_evidence"
    source_feed_dir = artifact_root / "daily_observation_feed"
    input_validation_dir = artifact_root / "daily_evidence_input_validation"

    component_files_present = [name for name in COMPONENT_REPORT_FILES if (component_dir / name).exists()]
    evidence_report_json = evidence_dir / f"daily_evidence_report_{report_date}.json"
    evidence_report_md = evidence_dir / f"daily_evidence_report_{report_date}.md"
    component_exit_code = component_dir / "component_exit_code.txt"
    report_exit_code = evidence_dir / "report_exit_code.txt"

    gates = [
        CadenceGate(
            name="raw_source_files_complete",
            passed=len(raw_files_present) == len(RAW_SOURCE_FILES),
            value=f"{len(raw_files_present)}/{len(RAW_SOURCE_FILES)}",
            threshold=f"{len(RAW_SOURCE_FILES)}/{len(RAW_SOURCE_FILES)}",
            message="Every daily raw paper observation source file must be captured before review.",
        ),
        CadenceGate(
            name="raw_source_records_present",
            passed=raw_records > 0,
            value=raw_records,
            threshold=1,
            message="Raw paper observation files must contain at least one object record in total.",
        ),
        CadenceGate(
            name="persisted_feed_present",
            passed=source_feed_dir.exists(),
            value=source_feed_dir.exists(),
            threshold=True,
            message="Daily observation feed artifact must be present for audit continuity.",
        ),
        CadenceGate(
            name="input_validation_present",
            passed=input_validation_dir.exists(),
            value=input_validation_dir.exists(),
            threshold=True,
            message="Daily evidence input validation artifact must be present.",
        ),
        CadenceGate(
            name="component_reports_complete",
            passed=len(component_files_present) == len(COMPONENT_REPORT_FILES),
            value=f"{len(component_files_present)}/{len(COMPONENT_REPORT_FILES)}",
            threshold=f"{len(COMPONENT_REPORT_FILES)}/{len(COMPONENT_REPORT_FILES)}",
            message="All B1-B6 component JSON reports should be present in the artifact.",
        ),
        CadenceGate(
            name="daily_evidence_report_present",
            passed=evidence_report_json.exists() and evidence_report_md.exists(),
            value=evidence_report_json.exists() and evidence_report_md.exists(),
            threshold=True,
            message="Daily evidence JSON and Markdown reports must be present for review.",
        ),
        CadenceGate(
            name="diagnostic_exit_codes_present",
            passed=component_exit_code.exists() and report_exit_code.exists(),
            value=component_exit_code.exists() and report_exit_code.exists(),
            threshold=True,
            message="Component and report exit-code diagnostics must be included in the artifact.",
        ),
    ]
    warnings = [
        "Daily paper observation remains observation-only.",
        "A green cadence review proves capture discipline, not live trading readiness.",
        "Live capital remains blocked until the full forward evidence window is complete and reviewed.",
    ]
    return CadenceReport(
        passed=all(gate.passed for gate in gates),
        report_date=report_date,
        cadence_version=CADENCE_VERSION,
        observation_only=True,
        raw_source_dir=str(raw_source_dir),
        artifact_root=str(artifact_root),
        gates=gates,
        warnings=warnings,
    )


def render_cadence_report_markdown(report: CadenceReport) -> str:
    lines = [
        "# Daily Paper Observation Cadence Review",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        f"Report date: `{report.report_date}`",
        f"Cadence version: `{report.cadence_version}`",
        f"Observation-only: **{str(report.observation_only).lower()}**",
        f"Raw source dir: `{report.raw_source_dir}`",
        f"Artifact root: `{report.artifact_root}`",
        "",
        "## Gates",
        "",
        "| Gate | Status | Value | Threshold | Message |",
        "|---|---:|---:|---:|---|",
    ]
    for gate in report.gates:
        lines.append(
            f"| {gate.name} | {'PASS' if gate.passed else 'FAIL'} | "
            f"{gate.value} | {gate.threshold} | {gate.message} |"
        )
    lines.extend(["", "## Warnings", ""])
    for warning in report.warnings:
        lines.append(f"- {warning}")
    return "\n".join(lines).rstrip() + "\n"


def write_cadence_report(report: CadenceReport, *, json_path: Path, markdown_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_cadence_report_markdown(report), encoding="utf-8")


def _count_records(source_dir: Path, filenames: tuple[str, ...]) -> int:
    total = 0
    for filename in filenames:
        path = source_dir / filename
        if not path.exists():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if isinstance(payload, list):
            total += sum(1 for item in payload if isinstance(item, dict))
    return total
