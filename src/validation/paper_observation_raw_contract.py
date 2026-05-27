from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

RAW_CONTRACT_VERSION = "2026.05.27-v1"
OBSERVATION_ONLY_SOURCE_TYPES = {
    "broker_paper_account",
    "manual_paper_journal",
    "paper_reconciliation_log",
    "simulated_paper_observation",
}
PROHIBITED_SOURCE_TYPES = {"observation_only_bootstrap"}

REQUIRED_FILES = {
    "paper_observations": "paper_observations.json",
    "backtest_results": "backtest_results.json",
    "regime_observations": "regime_observations.json",
    "position_snapshots": "position_snapshots.json",
}

REQUIRED_FIELDS = {
    "paper_observations": (
        "observation_date",
        "symbol",
        "strategy_id",
        "signal_id",
        "expected_action",
        "paper_action",
        "expected_r",
        "paper_r",
        "source_type",
    ),
    "backtest_results": ("observation_date", "strategy_id", "signal_id", "result_r", "source_type"),
    "regime_observations": ("observation_date", "regime_label", "volatility_pct", "corr", "drawdown_pct", "source_type"),
    "position_snapshots": ("observation_date", "symbol", "strategy_id", "portfolio_weight", "paper_r", "source_type"),
}

NUMERIC_FIELDS = {
    "paper_observations": ("expected_r", "paper_r"),
    "backtest_results": ("result_r",),
    "regime_observations": ("volatility_pct", "corr", "drawdown_pct"),
    "position_snapshots": ("portfolio_weight", "paper_r"),
}


@dataclass(frozen=True)
class RawContractIssue:
    file_name: str
    record_index: int | None
    field: str | None
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RawContractFileSummary:
    name: str
    path: str
    records: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RawContractReport:
    passed: bool
    contract_version: str
    observation_only: bool
    source_dir: str
    files: list[RawContractFileSummary] = field(default_factory=list)
    issues: list[RawContractIssue] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "contract_version": self.contract_version,
            "observation_only": self.observation_only,
            "source_dir": self.source_dir,
            "files": [item.to_dict() for item in self.files],
            "issues": [issue.to_dict() for issue in self.issues],
            "warnings": list(self.warnings),
        }


def validate_raw_observation_contract(source_dir: Path) -> RawContractReport:
    issues: list[RawContractIssue] = []
    summaries: list[RawContractFileSummary] = []

    for name, filename in REQUIRED_FILES.items():
        path = source_dir / filename
        if not path.exists():
            issues.append(RawContractIssue(filename, None, None, "required raw source file is missing"))
            continue
        records = _read_records(path, filename, issues)
        if records is None:
            continue
        summaries.append(RawContractFileSummary(name=name, path=str(path), records=len(records)))
        _validate_records(name, filename, records, issues)

    warnings = [
        "Raw paper observation records are observation-only and do not authorize live trading.",
        "This contract validates capture quality, not statistical edge.",
    ]
    return RawContractReport(
        passed=not issues,
        contract_version=RAW_CONTRACT_VERSION,
        observation_only=True,
        source_dir=str(source_dir),
        files=summaries,
        issues=issues,
        warnings=warnings,
    )


def write_raw_contract_template(output_dir: Path, *, report_date: str) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    templates = {
        "paper_observations.json": [
            {
                "observation_date": report_date,
                "symbol": "AAPL",
                "strategy_id": "rule_based_core_v1",
                "signal_id": "example-signal-001",
                "expected_action": "enter_long",
                "paper_action": "enter_long",
                "expected_r": 0.25,
                "paper_r": 0.2,
                "resolved": True,
                "source_type": "manual_paper_journal",
                "notes": "replace this template record with real paper observation data",
            }
        ],
        "backtest_results.json": [
            {
                "observation_date": report_date,
                "strategy_id": "rule_based_core_v1",
                "signal_id": "example-signal-001",
                "result_r": 0.25,
                "source_type": "paper_reconciliation_log",
            }
        ],
        "regime_observations.json": [
            {
                "observation_date": report_date,
                "regime_label": "neutral",
                "volatility_pct": 0.18,
                "corr": 0.4,
                "drawdown_pct": 0.02,
                "source_type": "manual_paper_journal",
            }
        ],
        "position_snapshots.json": [
            {
                "observation_date": report_date,
                "symbol": "AAPL",
                "strategy_id": "rule_based_core_v1",
                "portfolio_weight": 0.5,
                "paper_r": 0.2,
                "source_type": "manual_paper_journal",
            }
        ],
    }
    paths: list[Path] = []
    for filename, payload in templates.items():
        path = output_dir / filename
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        paths.append(path)
    return paths


def render_raw_contract_report_markdown(report: RawContractReport) -> str:
    lines = [
        "# Real Paper Observation Raw Data Contract",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        f"Contract version: `{report.contract_version}`",
        f"Observation-only: **{str(report.observation_only).lower()}**",
        f"Source dir: `{report.source_dir}`",
        "",
        "## Files",
        "",
        "| Name | Records | Path |",
        "|---|---:|---|",
    ]
    for item in report.files:
        lines.append(f"| {item.name} | {item.records} | `{item.path}` |")
    lines.extend(["", "## Issues", ""])
    if report.issues:
        for issue in report.issues:
            location = issue.file_name
            if issue.record_index is not None:
                location += f"[{issue.record_index}]"
            if issue.field:
                location += f".{issue.field}"
            lines.append(f"- `{location}`: {issue.message}")
    else:
        lines.append("- none")
    lines.extend(["", "## Warnings", ""])
    for warning in report.warnings:
        lines.append(f"- {warning}")
    return "\n".join(lines).rstrip() + "\n"


def write_raw_contract_report(report: RawContractReport, *, json_path: Path, markdown_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_raw_contract_report_markdown(report), encoding="utf-8")


def _read_records(path: Path, filename: str, issues: list[RawContractIssue]) -> list[dict[str, Any]] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        issues.append(RawContractIssue(filename, None, None, f"invalid JSON: {exc.msg}"))
        return None
    if not isinstance(payload, list):
        issues.append(RawContractIssue(filename, None, None, "file must contain a JSON list"))
        return None
    if not payload:
        issues.append(RawContractIssue(filename, None, None, "file must not be empty"))
        return None
    records = [record for record in payload if isinstance(record, dict)]
    if len(records) != len(payload):
        issues.append(RawContractIssue(filename, None, None, "file must contain only object records"))
        return None
    return records


def _validate_records(name: str, filename: str, records: list[dict[str, Any]], issues: list[RawContractIssue]) -> None:
    seen_keys: set[tuple[str, ...]] = set()
    for index, record in enumerate(records):
        for field_name in REQUIRED_FIELDS[name]:
            if _is_missing(record.get(field_name)):
                issues.append(RawContractIssue(filename, index, field_name, "required field is missing or blank"))
        if "observation_date" in record and not _is_valid_date(record.get("observation_date")):
            issues.append(RawContractIssue(filename, index, "observation_date", "must be YYYY-MM-DD"))
        for field_name in NUMERIC_FIELDS[name]:
            if field_name in record and not _is_number(record.get(field_name)):
                issues.append(RawContractIssue(filename, index, field_name, "must be numeric"))
        source_type = str(record.get("source_type", "")).strip()
        if source_type in PROHIBITED_SOURCE_TYPES:
            issues.append(RawContractIssue(filename, index, "source_type", "bootstrap source is prohibited for real raw paper observations"))
        elif source_type and source_type not in OBSERVATION_ONLY_SOURCE_TYPES:
            issues.append(RawContractIssue(filename, index, "source_type", "unknown observation-only source type"))
        key = _duplicate_key(name, record)
        if key:
            if key in seen_keys:
                issues.append(RawContractIssue(filename, index, None, "duplicate logical record key"))
            seen_keys.add(key)


def _duplicate_key(name: str, record: dict[str, Any]) -> tuple[str, ...] | None:
    if name in {"paper_observations", "backtest_results"}:
        fields = ("observation_date", "strategy_id", "signal_id")
    elif name == "position_snapshots":
        fields = ("observation_date", "strategy_id", "symbol")
    elif name == "regime_observations":
        fields = ("observation_date", "regime_label")
    else:
        return None
    values = tuple(str(record.get(field_name, "")).strip() for field_name in fields)
    return values if all(values) else None


def _is_missing(value: Any) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_valid_date(value: Any) -> bool:
    if isinstance(value, date) and not isinstance(value, datetime):
        return True
    if not isinstance(value, str):
        return False
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False
