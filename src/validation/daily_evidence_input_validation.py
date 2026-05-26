from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


REQUIRED_INPUT_FILES: dict[str, str] = {
    "paper_records": "paper_observation_records.json",
    "backtest_records": "backtest_records.json",
    "forward_records": "forward_records.json",
    "regime_records": "regime_records.json",
    "position_records": "position_records.json",
}

_REQUIRED_FIELDS: dict[str, tuple[str, ...]] = {
    "paper_records": ("observation_date", "expected_action", "paper_action", "expected_r", "paper_r", "resolved"),
    "backtest_records": ("result_r",),
    "forward_records": ("result_r",),
    "regime_records": ("regime", "volatility", "correlation", "drawdown"),
    "position_records": (
        "symbol",
        "sector",
        "weight",
        "result_r",
        "beta",
        "market_return_r",
        "factor_exposures",
        "factor_returns",
    ),
}

_NUMERIC_FIELDS: dict[str, tuple[str, ...]] = {
    "paper_records": ("expected_r", "paper_r"),
    "backtest_records": ("result_r",),
    "forward_records": ("result_r",),
    "regime_records": ("volatility", "correlation", "drawdown"),
    "position_records": ("weight", "result_r", "beta", "market_return_r"),
}

_DICT_FIELDS: dict[str, tuple[str, ...]] = {
    "position_records": ("factor_exposures", "factor_returns"),
}


@dataclass(frozen=True)
class InputFileValidation:
    component: str
    filename: str
    present: bool
    valid_json: bool
    records: int
    passed: bool
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DailyEvidenceInputValidationMetrics:
    files_expected: int
    files_present: int
    files_valid: int
    files_failed: int
    total_records: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DailyEvidenceInputValidationReport:
    passed: bool
    input_dir: str
    metrics: DailyEvidenceInputValidationMetrics
    files: list[InputFileValidation] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "input_dir": self.input_dir,
            "metrics": self.metrics.to_dict(),
            "files": [item.to_dict() for item in self.files],
        }


def validate_daily_evidence_inputs(input_dir: Path) -> DailyEvidenceInputValidationReport:
    validations = [_validate_input_file(input_dir, component, filename) for component, filename in REQUIRED_INPUT_FILES.items()]
    files_present = sum(1 for item in validations if item.present)
    files_valid = sum(1 for item in validations if item.passed)
    files_failed = len(validations) - files_valid
    total_records = sum(item.records for item in validations)
    metrics = DailyEvidenceInputValidationMetrics(
        files_expected=len(validations),
        files_present=files_present,
        files_valid=files_valid,
        files_failed=files_failed,
        total_records=total_records,
    )
    return DailyEvidenceInputValidationReport(
        passed=all(item.passed for item in validations),
        input_dir=str(input_dir),
        metrics=metrics,
        files=validations,
    )


def render_daily_evidence_input_validation_markdown(report: DailyEvidenceInputValidationReport) -> str:
    lines = [
        "# Daily Evidence Input Validation",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        f"Input dir: `{report.input_dir}`",
        "",
        "## Summary",
        "",
        f"- Files expected: {report.metrics.files_expected}",
        f"- Files present: {report.metrics.files_present}",
        f"- Files valid: {report.metrics.files_valid}",
        f"- Files failed: {report.metrics.files_failed}",
        f"- Total records: {report.metrics.total_records}",
        "",
        "## Files",
        "",
        "| Component | File | Present | Records | Status | Errors |",
        "|---|---|---:|---:|---:|---|",
    ]
    for item in report.files:
        errors = "; ".join(item.errors) if item.errors else "none"
        lines.append(
            f"| {item.component} | `{item.filename}` | {_format_bool(item.present)} | "
            f"{item.records} | {'PASS' if item.passed else 'FAIL'} | {errors} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def write_daily_evidence_input_validation_report(
    report: DailyEvidenceInputValidationReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_daily_evidence_input_validation_markdown(report), encoding="utf-8")


def _validate_input_file(input_dir: Path, component: str, filename: str) -> InputFileValidation:
    path = input_dir / filename
    errors: list[str] = []
    if not path.exists():
        return InputFileValidation(component, filename, False, False, 0, False, ["missing file"])

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return InputFileValidation(component, filename, True, False, 0, False, [f"invalid json: {exc.msg}"])

    if not isinstance(payload, list):
        return InputFileValidation(component, filename, True, True, 0, False, ["payload must be a list of records"])

    if not payload:
        errors.append("record list must not be empty")

    for index, record in enumerate(payload):
        if not isinstance(record, dict):
            errors.append(f"record {index} must be an object")
            continue
        errors.extend(_validate_record(component, record, index))

    return InputFileValidation(
        component=component,
        filename=filename,
        present=True,
        valid_json=True,
        records=len(payload),
        passed=not errors,
        errors=errors,
    )


def _validate_record(component: str, record: dict[str, Any], index: int) -> list[str]:
    errors: list[str] = []
    for field_name in _REQUIRED_FIELDS.get(component, ()):
        if field_name not in record:
            errors.append(f"record {index} missing {field_name}")
    for field_name in _NUMERIC_FIELDS.get(component, ()):
        if field_name in record and not _is_number(record[field_name]):
            errors.append(f"record {index} field {field_name} must be numeric")
    for field_name in _DICT_FIELDS.get(component, ()):
        if field_name in record and not isinstance(record[field_name], dict):
            errors.append(f"record {index} field {field_name} must be an object")
    if component == "paper_records" and "resolved" in record and not isinstance(record["resolved"], bool):
        errors.append(f"record {index} field resolved must be boolean")
    return errors


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _format_bool(value: bool) -> str:
    return "yes" if value else "no"
