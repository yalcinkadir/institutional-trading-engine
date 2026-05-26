from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from src.validation.daily_evidence_input_validation import validate_daily_evidence_inputs

SOURCE_FILES: dict[str, str] = {
    "paper_observations": "paper_observations.json",
    "backtest_results": "backtest_results.json",
    "forward_results": "forward_results.json",
    "regime_observations": "regime_observations.json",
    "position_snapshots": "position_snapshots.json",
}

OUTPUT_FILES: dict[str, str] = {
    "paper_records": "paper_observation_records.json",
    "backtest_records": "backtest_records.json",
    "forward_records": "forward_records.json",
    "regime_records": "regime_records.json",
    "position_records": "position_records.json",
}


@dataclass(frozen=True)
class BuiltInputFile:
    name: str
    path: str
    records: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DailyEvidenceInputBuildReport:
    passed: bool
    source_dir: str
    output_dir: str
    files: list[BuiltInputFile] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "source_dir": self.source_dir,
            "output_dir": self.output_dir,
            "files": [item.to_dict() for item in self.files],
            "errors": list(self.errors),
        }


def build_daily_evidence_inputs(source_dir: Path, output_dir: Path) -> DailyEvidenceInputBuildReport:
    errors: list[str] = []
    loaded: dict[str, list[dict[str, Any]]] = {}

    for key, filename in SOURCE_FILES.items():
        path = source_dir / filename
        if not path.exists():
            errors.append(f"missing source file: {filename}")
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid json in {filename}: {exc.msg}")
            continue
        if not isinstance(payload, list):
            errors.append(f"source file {filename} must contain a list")
            continue
        loaded[key] = [record for record in payload if isinstance(record, dict)]

    if errors:
        return DailyEvidenceInputBuildReport(False, str(source_dir), str(output_dir), [], errors)

    outputs = {
        "paper_records": [_normalize_paper_observation(record) for record in loaded["paper_observations"]],
        "backtest_records": [_normalize_result_record(record) for record in loaded["backtest_results"]],
        "forward_records": [_normalize_result_record(record) for record in loaded["forward_results"]],
        "regime_records": [_normalize_regime_observation(record) for record in loaded["regime_observations"]],
        "position_records": [_normalize_position_snapshot(record) for record in loaded["position_snapshots"]],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    built_files: list[BuiltInputFile] = []
    for key, records in outputs.items():
        output_path = output_dir / OUTPUT_FILES[key]
        output_path.write_text(json.dumps(records, indent=2), encoding="utf-8")
        built_files.append(BuiltInputFile(key, str(output_path), len(records)))

    validation = validate_daily_evidence_inputs(output_dir)
    validation_errors = [] if validation.passed else [
        f"{item.filename}: {'; '.join(item.errors)}" for item in validation.files if item.errors
    ]
    return DailyEvidenceInputBuildReport(
        passed=validation.passed,
        source_dir=str(source_dir),
        output_dir=str(output_dir),
        files=built_files,
        errors=validation_errors,
    )


def render_daily_evidence_input_build_markdown(report: DailyEvidenceInputBuildReport) -> str:
    lines = [
        "# Daily Evidence Input Build Report",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        f"Source dir: `{report.source_dir}`",
        f"Output dir: `{report.output_dir}`",
        "",
        "## Built Files",
        "",
        "| Name | Path | Records |",
        "|---|---|---:|",
    ]
    for item in report.files:
        lines.append(f"| {item.name} | `{item.path}` | {item.records} |")
    lines.extend(["", "## Errors", ""])
    if report.errors:
        for error in report.errors:
            lines.append(f"- {error}")
    else:
        lines.append("- none")
    return "\n".join(lines).rstrip() + "\n"


def write_daily_evidence_input_build_report(
    report: DailyEvidenceInputBuildReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_daily_evidence_input_build_markdown(report), encoding="utf-8")


def _normalize_paper_observation(record: dict[str, Any]) -> dict[str, Any]:
    expected_action = _string_value(record, "expected_action", default="HOLD")
    paper_action = _string_value(record, "paper_action", default=expected_action)
    expected_r = _float_value(record, "expected_r", fallback_fields=("expected_result_r", "result_r"))
    paper_r = _float_value(record, "paper_r", fallback_fields=("paper_result_r", "result_r"))
    return {
        "observation_date": _string_value(record, "observation_date", fallback_fields=("date", "signal_date")),
        "expected_action": expected_action,
        "paper_action": paper_action,
        "expected_r": expected_r,
        "paper_r": paper_r,
        "resolved": bool(record.get("resolved", True)),
    }


def _normalize_result_record(record: dict[str, Any]) -> dict[str, Any]:
    return {"result_r": _float_value(record, "result_r", fallback_fields=("paper_r", "r", "pnl_r"))}


def _normalize_regime_observation(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "regime": _string_value(record, "regime", fallback_fields=("regime_label",), default="unknown"),
        "volatility": _float_value(record, "volatility", fallback_fields=("volatility_pct", "vol")),
        "correlation": _float_value(record, "correlation", fallback_fields=("cross_asset_correlation", "corr")),
        "drawdown": _float_value(record, "drawdown", fallback_fields=("drawdown_pct", "max_drawdown")),
    }


def _normalize_position_snapshot(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "symbol": _string_value(record, "symbol"),
        "sector": _string_value(record, "sector", default="unknown"),
        "weight": _float_value(record, "weight", fallback_fields=("portfolio_weight",)),
        "result_r": _float_value(record, "result_r", fallback_fields=("paper_r", "r", "pnl_r")),
        "beta": _float_value(record, "beta", default=1.0),
        "market_return_r": _float_value(record, "market_return_r", fallback_fields=("market_r",), default=0.0),
        "factor_exposures": _dict_value(record, "factor_exposures"),
        "factor_returns": _dict_value(record, "factor_returns"),
    }


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


def _dict_value(record: dict[str, Any], field: str) -> dict[str, float]:
    value = record.get(field)
    if not isinstance(value, dict):
        return {}
    normalized: dict[str, float] = {}
    for key, raw in value.items():
        if isinstance(raw, bool):
            continue
        if isinstance(raw, (int, float)):
            normalized[str(key)] = float(raw)
        elif isinstance(raw, str):
            try:
                normalized[str(key)] = float(raw)
            except ValueError:
                continue
    return normalized
