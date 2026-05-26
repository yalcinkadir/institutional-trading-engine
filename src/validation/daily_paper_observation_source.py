from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

PAPER_SOURCE_VERSION = "2026.05.26-v1"
PAPER_SOURCE = "daily_paper_observation_source"
PROHIBITED_SOURCES = {"observation_only_bootstrap"}

INPUT_FILES: dict[str, str] = {
    "paper_observations": "paper_observations.json",
    "backtest_results": "backtest_results.json",
    "regime_observations": "regime_observations.json",
    "position_snapshots": "position_snapshots.json",
}

OUTPUT_FILES: dict[str, str] = {
    "paper_observations": "paper_observations.json",
    "backtest_results": "backtest_results.json",
    "forward_results": "forward_results.json",
    "regime_observations": "regime_observations.json",
    "position_snapshots": "position_snapshots.json",
}


@dataclass(frozen=True)
class BuiltPaperSourceFile:
    name: str
    path: str
    records: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DailyPaperObservationSourceReport:
    passed: bool
    source_version: str
    observation_only: bool
    source_dir: str
    output_dir: str
    files: list[BuiltPaperSourceFile] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "source_version": self.source_version,
            "observation_only": self.observation_only,
            "source_dir": self.source_dir,
            "output_dir": self.output_dir,
            "files": [item.to_dict() for item in self.files],
            "errors": list(self.errors),
            "warnings": list(self.warnings),
        }


def build_daily_paper_observation_sources(source_dir: Path, output_dir: Path) -> DailyPaperObservationSourceReport:
    errors: list[str] = []
    loaded: dict[str, list[dict[str, Any]]] = {}

    for name, filename in INPUT_FILES.items():
        path = source_dir / filename
        if not path.exists():
            errors.append(f"missing source file: {filename}")
            continue
        payload = _read_json_list(path, filename, errors)
        if payload is None:
            continue
        loaded[name] = payload

    if errors:
        return DailyPaperObservationSourceReport(
            passed=False,
            source_version=PAPER_SOURCE_VERSION,
            observation_only=True,
            source_dir=str(source_dir),
            output_dir=str(output_dir),
            errors=errors,
        )

    source_errors = _validate_no_bootstrap_source(loaded)
    if source_errors:
        return DailyPaperObservationSourceReport(
            passed=False,
            source_version=PAPER_SOURCE_VERSION,
            observation_only=True,
            source_dir=str(source_dir),
            output_dir=str(output_dir),
            errors=source_errors,
        )

    paper_observations = [_normalize_paper_observation(record) for record in loaded["paper_observations"]]
    forward_results = [_forward_result_from_paper(record) for record in paper_observations]
    backtest_results = [_normalize_result_record(record) for record in loaded["backtest_results"]]
    regime_observations = [_mark_record(record) for record in loaded["regime_observations"]]
    position_snapshots = [_mark_record(record) for record in loaded["position_snapshots"]]

    output_payloads = {
        "paper_observations": paper_observations,
        "backtest_results": backtest_results,
        "forward_results": forward_results,
        "regime_observations": regime_observations,
        "position_snapshots": position_snapshots,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    files: list[BuiltPaperSourceFile] = []
    for name, records in output_payloads.items():
        output_path = output_dir / OUTPUT_FILES[name]
        output_path.write_text(json.dumps(records, indent=2), encoding="utf-8")
        files.append(BuiltPaperSourceFile(name=name, path=str(output_path), records=len(records)))

    return DailyPaperObservationSourceReport(
        passed=True,
        source_version=PAPER_SOURCE_VERSION,
        observation_only=True,
        source_dir=str(source_dir),
        output_dir=str(output_dir),
        files=files,
        warnings=[
            "real paper observation source records are still observation-only",
            "this does not authorize live capital",
        ],
    )


def render_daily_paper_observation_source_markdown(report: DailyPaperObservationSourceReport) -> str:
    lines = [
        "# Daily Paper Observation Source Report",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        f"Source version: `{report.source_version}`",
        f"Observation-only: **{str(report.observation_only).lower()}**",
        f"Source dir: `{report.source_dir}`",
        f"Output dir: `{report.output_dir}`",
        "",
        "## Files",
        "",
        "| Name | Records | Path |",
        "|---|---:|---|",
    ]
    for item in report.files:
        lines.append(f"| {item.name} | {item.records} | `{item.path}` |")
    lines.extend(["", "## Errors", ""])
    if report.errors:
        for error in report.errors:
            lines.append(f"- {error}")
    else:
        lines.append("- none")
    lines.extend(["", "## Warnings", ""])
    if report.warnings:
        for warning in report.warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("- none")
    return "\n".join(lines).rstrip() + "\n"


def write_daily_paper_observation_source_report(
    report: DailyPaperObservationSourceReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_daily_paper_observation_source_markdown(report), encoding="utf-8")


def _read_json_list(path: Path, filename: str, errors: list[str]) -> list[dict[str, Any]] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid json in {filename}: {exc.msg}")
        return None
    if not isinstance(payload, list):
        errors.append(f"source file {filename} must contain a list")
        return None
    if not payload:
        errors.append(f"source file {filename} must not be empty")
        return None
    records = [record for record in payload if isinstance(record, dict)]
    if len(records) != len(payload):
        errors.append(f"source file {filename} must contain only object records")
        return None
    return records


def _validate_no_bootstrap_source(loaded: dict[str, list[dict[str, Any]]]) -> list[str]:
    errors: list[str] = []
    for name, records in loaded.items():
        for index, record in enumerate(records):
            source = str(record.get("source", "")).strip()
            if source in PROHIBITED_SOURCES:
                errors.append(f"{name}[{index}] uses prohibited bootstrap source: {source}")
    return errors


def _normalize_paper_observation(record: dict[str, Any]) -> dict[str, Any]:
    expected_action = _string_value(record, "expected_action", fallback_fields=("backtest_action",), default="hold")
    paper_action = _string_value(record, "paper_action", fallback_fields=("observed_action",), default=expected_action)
    return {
        "observation_date": _string_value(record, "observation_date", fallback_fields=("date", "signal_date")),
        "expected_action": expected_action,
        "paper_action": paper_action,
        "expected_result_r": _float_value(record, "expected_result_r", fallback_fields=("expected_r", "backtest_r", "result_r")),
        "paper_result_r": _float_value(record, "paper_result_r", fallback_fields=("paper_r", "observed_r", "result_r")),
        "resolved": bool(record.get("resolved", True)),
        "source": PAPER_SOURCE,
        "source_version": PAPER_SOURCE_VERSION,
    }


def _forward_result_from_paper(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "result_r": _float_value(record, "paper_result_r", fallback_fields=("paper_r", "observed_r")),
        "source": PAPER_SOURCE,
        "source_version": PAPER_SOURCE_VERSION,
    }


def _normalize_result_record(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "result_r": _float_value(record, "result_r", fallback_fields=("r", "pnl_r", "backtest_r")),
        "source": PAPER_SOURCE,
        "source_version": PAPER_SOURCE_VERSION,
    }


def _mark_record(record: dict[str, Any]) -> dict[str, Any]:
    marked = dict(record)
    marked["source"] = PAPER_SOURCE
    marked["source_version"] = PAPER_SOURCE_VERSION
    return marked


def _string_value(
    record: dict[str, Any],
    field: str,
    *,
    fallback_fields: tuple[str, ...] = (),
    default: str = "",
) -> str:
    for candidate in (field, *fallback_fields):
        value = record.get(candidate)
        if value is not None:
            return str(value)
    return default


def _float_value(
    record: dict[str, Any],
    field: str,
    *,
    fallback_fields: tuple[str, ...] = (),
    default: float = 0.0,
) -> float:
    for candidate in (field, *fallback_fields):
        value = record.get(candidate)
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                continue
    return default
