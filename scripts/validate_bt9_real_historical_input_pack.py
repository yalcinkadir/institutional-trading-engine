#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.validate_survivorship_universe import validate_survivorship_universe

DEMO_MARKERS = {"demo", "synthetic", "public_safe", "historical_demo", "placeholder"}
REQUIRED_BAR_COLUMNS = {"date", "open", "high", "low", "close", "volume"}
REQUIRED_TRADE_PLAN_FIELDS = {"signal_id", "symbol", "signal_date", "entry_trigger", "stop_loss", "target_1"}
REQUIRED_RUNTIME_GATES = [
    "scanner",
    "signal_generator",
    "quality_fusion",
    "trade_plan_validator",
]
ACCEPTED_PIPELINE_GENERATION_SOURCES = {
    "runtime_pipeline_adapter",
    "scanner_signal_quality_validator",
}
FORBIDDEN_PIPELINE_GENERATION_SOURCES = {
    "validated_paper_observation_export",
    "deterministic_historical_generator",
    "historical_demo_generator",
}
PIPELINE_SOURCES_REQUIRING_EXECUTION_PROOF = {"scanner_signal_quality_validator"}
REQUIRED_PIPELINE_EXECUTION_ENTRYPOINTS = {
    "src.signals.signal_generator.build_signals",
    "scripts.export_historical_trade_plans._signal_to_plan",
}


@dataclass(frozen=True)
class BT9RealHistoricalInputPackReport:
    passed: bool
    universe_path: str
    bars_root: str
    trade_plans_path: str
    coverage_manifest_path: str = ""
    symbols: list[str] = field(default_factory=list)
    date_range: dict[str, str] = field(default_factory=dict)
    input_checksums: dict[str, str] = field(default_factory=dict)
    failures: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _checksum_existing_file(path: Path | None) -> dict[str, str]:
    if path is None or not path.exists() or not path.is_file():
        return {}
    return {path.as_posix(): sha256_file(path)}


def _has_demo_marker(value: Any) -> bool:
    if isinstance(value, str):
        lower = value.lower()
        return any(marker in lower for marker in DEMO_MARKERS)
    if isinstance(value, list):
        return any(_has_demo_marker(item) for item in value)
    if isinstance(value, dict):
        return any(_has_demo_marker(item) for item in value.values())
    return False


def _metadata_runtime_gates(metadata: dict[str, Any]) -> list[str]:
    raw = metadata.get("runtime_gates_applied") or []
    if isinstance(raw, list):
        return [str(item) for item in raw]
    return []


def _proof_runtime_gates(proof: dict[str, Any]) -> list[str]:
    raw = proof.get("runtime_gates_applied") or []
    if isinstance(raw, list):
        return [str(item) for item in raw]
    return []


def _proof_entrypoints(proof: dict[str, Any]) -> set[str]:
    raw = proof.get("executed_runtime_entrypoints") or []
    if isinstance(raw, list):
        return {str(item) for item in raw}
    return set()


def _validate_pipeline_execution_proof(metadata: dict[str, Any], generation_source: str) -> list[str]:
    """Require machine-checkable proof for #177 scanner/signal/quality/validator exports.

    Plain metadata such as `pipeline_coupled=true` and `runtime_gates_applied=[...]` is not
    enough for strategy evidence. For the concrete #177 scanner/signal/quality/validator path,
    the exporter must also write a bounded execution proof that identifies the adapter, payload
    checksum and runtime entrypoints used to derive the trade plans.
    """

    if generation_source not in PIPELINE_SOURCES_REQUIRING_EXECUTION_PROOF:
        return []

    proof = metadata.get("pipeline_execution_proof")
    if not isinstance(proof, dict) or not proof:
        return ["trade_plans_missing_pipeline_execution_proof"]

    failures: list[str] = []
    if str(proof.get("proof_version") or "") != "2026.06.13-v1":
        failures.append(f"trade_plans_invalid_pipeline_execution_proof_version:{proof.get('proof_version')}")
    if str(proof.get("adapter") or "") != "historical_scanner_signal_quality_validator_export":
        failures.append(f"trade_plans_invalid_pipeline_execution_adapter:{proof.get('adapter')}")

    source_payload_sha256 = str(proof.get("source_payload_sha256") or "")
    if len(source_payload_sha256) != 64 or any(char not in "0123456789abcdef" for char in source_payload_sha256.lower()):
        failures.append("trade_plans_invalid_pipeline_execution_source_payload_sha256")

    missing_entrypoints = sorted(REQUIRED_PIPELINE_EXECUTION_ENTRYPOINTS - _proof_entrypoints(proof))
    if missing_entrypoints:
        failures.append(f"trade_plans_missing_pipeline_execution_entrypoints:{','.join(missing_entrypoints)}")

    missing_proof_gates = sorted(set(REQUIRED_RUNTIME_GATES) - set(_proof_runtime_gates(proof)))
    if missing_proof_gates:
        failures.append(f"trade_plans_missing_pipeline_execution_gates:{','.join(missing_proof_gates)}")

    if str(proof.get("proof_boundary") or "") != "generated_by_exporter_runtime_path":
        failures.append(f"trade_plans_invalid_pipeline_execution_proof_boundary:{proof.get('proof_boundary')}")

    return failures


def _validate_trade_plan_metadata(metadata: Any) -> list[str]:
    """Fail closed when real-data backtest plans do not prove runtime-pipeline origin."""

    if not isinstance(metadata, dict) or not metadata:
        return ["trade_plans_missing_pipeline_metadata"]

    failures: list[str] = []
    if metadata.get("pipeline_coupled") is not True:
        failures.append("trade_plans_not_pipeline_coupled")

    runtime_gates = _metadata_runtime_gates(metadata)
    missing_gates = sorted(set(REQUIRED_RUNTIME_GATES) - set(runtime_gates))
    if missing_gates:
        failures.append(f"trade_plans_missing_runtime_gates:{','.join(missing_gates)}")

    generation_source = str(metadata.get("pipeline_generation_source") or "UNKNOWN")
    if generation_source not in ACCEPTED_PIPELINE_GENERATION_SOURCES:
        failures.append(f"trade_plans_invalid_pipeline_generation_source:{generation_source}")
    if generation_source in FORBIDDEN_PIPELINE_GENERATION_SOURCES:
        failures.append(f"trade_plans_forbidden_pipeline_generation_source:{generation_source}")

    generated_signal_count = metadata.get("generated_signal_count")
    validated_trade_plan_count = metadata.get("validated_trade_plan_count")
    if generated_signal_count in (None, ""):
        failures.append("trade_plans_missing_generated_signal_count")
    if validated_trade_plan_count in (None, ""):
        failures.append("trade_plans_missing_validated_trade_plan_count")

    failures.extend(_validate_pipeline_execution_proof(metadata, generation_source))

    return failures


def _read_trade_plans(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    if not path.exists():
        return [], ["missing_trade_plans_file"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [], [f"trade_plans_invalid_json:{exc}"]

    metadata: Any = {}
    if isinstance(payload, dict):
        metadata = payload.get("metadata")
        raw = payload.get("plans") or payload.get("signals")
    elif isinstance(payload, list):
        raw = payload
    else:
        raw = None

    if not isinstance(raw, list) or not raw:
        return [], ["trade_plans_empty_or_invalid"]

    failures: list[str] = _validate_trade_plan_metadata(metadata)
    plans: list[dict[str, Any]] = []
    for index, plan in enumerate(raw):
        if not isinstance(plan, dict):
            failures.append(f"trade_plan_{index}_not_object")
            continue
        missing = sorted(field_name for field_name in REQUIRED_TRADE_PLAN_FIELDS if plan.get(field_name) in (None, ""))
        if missing:
            failures.append(f"trade_plan_{index}_missing:{','.join(missing)}")
        if _has_demo_marker(plan):
            failures.append(f"trade_plan_{index}_demo_marker")
        plans.append(plan)
    return plans, failures


def _load_coverage_manifest(path: Path | None) -> tuple[dict[str, Any], list[str]]:
    if path is None:
        return {}, ["missing_coverage_manifest_argument"]
    if not path.exists():
        return {}, ["missing_coverage_manifest"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {}, [f"coverage_manifest_invalid_json:{exc}"]
    if not isinstance(payload, dict):
        return {}, ["coverage_manifest_not_object"]
    return payload, []


def _manifest_records_by_symbol(manifest: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], list[str]]:
    raw_symbols = manifest.get("symbols")
    if not isinstance(raw_symbols, list) or not raw_symbols:
        return {}, ["coverage_manifest_symbols_empty_or_invalid"]
    failures: list[str] = []
    records: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(raw_symbols):
        if not isinstance(item, dict):
            failures.append(f"coverage_manifest_symbol_{index}_not_object")
            continue
        symbol = str(item.get("symbol") or "").upper()
        if not symbol:
            failures.append(f"coverage_manifest_symbol_{index}_missing_symbol")
            continue
        records[symbol] = item
    return records, failures


def _validate_bars(
    bars_root: Path,
    symbols: list[str],
    *,
    coverage_manifest_path: Path | None,
) -> tuple[dict[str, str], dict[str, str], list[str]]:
    if not bars_root.exists():
        return {}, {}, ["missing_bars_root"]
    manifest, manifest_failures = _load_coverage_manifest(coverage_manifest_path)
    manifest_records, record_failures = _manifest_records_by_symbol(manifest) if manifest else ({}, [])
    failures: list[str] = manifest_failures + record_failures
    input_checksums: dict[str, str] = {}
    all_dates: list[str] = []
    for symbol in symbols:
        path = bars_root / f"{symbol}.csv"
        if not path.exists():
            failures.append(f"missing_bars:{symbol}")
            continue
        actual_sha256 = sha256_file(path)
        input_checksums[path.as_posix()] = actual_sha256
        manifest_record = manifest_records.get(symbol)
        if manifest_record is None:
            failures.append(f"coverage_manifest_missing_symbol:{symbol}")
        else:
            expected_path = str(manifest_record.get("output_path") or "")
            expected_sha256 = str(manifest_record.get("output_sha256") or "")
            if not expected_path:
                failures.append(f"coverage_manifest_missing_output_path:{symbol}")
            elif Path(expected_path).as_posix() != path.as_posix():
                failures.append(f"coverage_manifest_output_path_mismatch:{symbol}:{expected_path}")
            if not expected_sha256:
                failures.append(f"coverage_manifest_missing_output_sha256:{symbol}")
            elif expected_sha256 != actual_sha256:
                failures.append(f"coverage_manifest_checksum_mismatch:{symbol}")
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            failures.append(f"empty_bars:{symbol}")
            continue
        columns = set(rows[0].keys())
        missing_columns = sorted(REQUIRED_BAR_COLUMNS - columns)
        if missing_columns:
            failures.append(f"bars_missing_columns:{symbol}:{','.join(missing_columns)}")
            continue
        if any(_has_demo_marker(row) for row in rows):
            failures.append(f"bars_demo_marker:{symbol}")
        for row_index, row in enumerate(rows, start=2):
            if any(row.get(column) in (None, "") for column in REQUIRED_BAR_COLUMNS):
                failures.append(f"bars_incomplete_row:{symbol}:{row_index}")
            all_dates.append(str(row.get("date")))
    all_dates = sorted(date for date in all_dates if date)
    return ({"start": all_dates[0], "end": all_dates[-1]} if all_dates else {}, input_checksums, failures)


def validate_bt9_input_pack(
    *,
    universe_path: Path,
    bars_root: Path,
    trade_plans_path: Path,
    coverage_manifest_path: Path | None = Path("data/historical/metadata/coverage_manifest.json"),
) -> BT9RealHistoricalInputPackReport:
    plans, trade_plan_failures = _read_trade_plans(trade_plans_path)
    plan_symbols = sorted({str(plan.get("symbol") or "").upper() for plan in plans if plan.get("symbol")})
    signal_dates = sorted(str(plan.get("signal_date")) for plan in plans if plan.get("signal_date"))
    requested_start = signal_dates[0] if signal_dates else None
    requested_end = signal_dates[-1] if signal_dates else None
    universe_report = validate_survivorship_universe(
        universe_path=universe_path,
        requested_symbols=plan_symbols,
        start_date=requested_start,
        end_date=requested_end,
    )
    requested_symbols = sorted(set(universe_report.active_symbols) | set(plan_symbols))
    date_range, bar_input_checksums, bar_failures = _validate_bars(
        bars_root,
        requested_symbols,
        coverage_manifest_path=coverage_manifest_path,
    )
    input_checksums = {
        **_checksum_existing_file(universe_path),
        **_checksum_existing_file(coverage_manifest_path),
        **_checksum_existing_file(trade_plans_path),
        **bar_input_checksums,
    }
    failures = universe_report.failures + trade_plan_failures + bar_failures
    return BT9RealHistoricalInputPackReport(
        passed=not failures,
        universe_path=universe_path.as_posix(),
        bars_root=bars_root.as_posix(),
        trade_plans_path=trade_plans_path.as_posix(),
        coverage_manifest_path=coverage_manifest_path.as_posix() if coverage_manifest_path else "",
        symbols=requested_symbols,
        date_range=date_range,
        input_checksums=input_checksums,
        failures=failures,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate BT9 real historical backtesting input pack.")
    parser.add_argument("--universe", default="data/universe/survivorship_universe.csv")
    parser.add_argument("--bars-root", default="data/historical/bars/1day")
    parser.add_argument("--trade-plans", default="data/trade_plans/historical_trade_plans.json")
    parser.add_argument("--coverage-manifest", default="data/historical/metadata/coverage_manifest.json")
    parser.add_argument("--report-output", default="reports/backtests/bt9-real-historical-input-pack-gate.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = validate_bt9_input_pack(
        universe_path=Path(args.universe),
        bars_root=Path(args.bars_root),
        trade_plans_path=Path(args.trade_plans),
        coverage_manifest_path=Path(args.coverage_manifest),
    )
    output = Path(args.report_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    status = "PASS" if report.passed else "FAIL"
    print(f"BT9 real historical input pack gate status: {status}")
    if report.failures:
        print("Failures:")
        for failure in report.failures:
            print(f"- {failure}")
    print(f"Gate report: {args.report_output}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
