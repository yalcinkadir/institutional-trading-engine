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

from src.signals.signal_generator import Signal, build_signals

DEMO_MARKERS = {"demo", "synthetic", "public_safe", "placeholder", "example", "historical_demo"}
REQUIRED_FIELDS = {
    "signal_id",
    "symbol",
    "timestamp",
    "close",
    "entry_trigger",
    "stop_loss",
    "target_1",
    "data_source",
    "data_status",
    "provenance",
}
PIPELINE_GATE_NAMES = [
    "scanner",
    "signal_generator",
    "quality_fusion",
    "trade_plan_validator",
]
PIPELINE_GENERATION_SOURCE = "scanner_signal_quality_validator"
OBSERVATION_GENERATION_SOURCE = "validated_paper_observation_export"


@dataclass(frozen=True)
class HistoricalTradePlanExportReport:
    passed: bool
    source_path: str
    output_path: str
    manifest_path: str
    source_window: dict[str, str] = field(default_factory=dict)
    record_count: int = 0
    exported_count: int = 0
    symbols: list[str] = field(default_factory=list)
    output_sha256: str | None = None
    boundary: str = "paper_only_research_only"
    pipeline_coupled: bool = False
    pipeline_generation_source: str = OBSERVATION_GENERATION_SOURCE
    runtime_gates_applied: list[str] = field(default_factory=list)
    generated_signal_count: int = 0
    validated_trade_plan_count: int = 0
    blocked_signal_count: int = 0
    failures: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _json_bytes(payload: Any) -> bytes:
    return json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n"


def _has_marker(value: Any) -> bool:
    if isinstance(value, str):
        lower = value.lower()
        return any(marker in lower for marker in DEMO_MARKERS)
    if isinstance(value, dict):
        return any(_has_marker(item) for item in value.values())
    if isinstance(value, list):
        return any(_has_marker(item) for item in value)
    return False


def _num(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _read_payload(path: Path) -> tuple[Any, list[str]]:
    if not path.exists():
        return None, ["missing_source_observations_file"]
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except json.JSONDecodeError as exc:
        return None, [f"source_observations_invalid_json:{exc}"]


def _read_records(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    if not path.exists():
        return [], ["missing_source_observations_file"]
    if path.suffix.lower() == ".csv":
        with path.open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle)), []
    payload, failures = _read_payload(path)
    if failures:
        return [], failures
    if isinstance(payload, list):
        return payload, []
    if isinstance(payload, dict):
        for key in ("observations", "signals", "records"):
            if isinstance(payload.get(key), list):
                return payload[key], []
    return [], ["source_observations_empty_or_invalid"]


def _provenance(value: Any) -> dict[str, Any] | None:
    if isinstance(value, dict) and value:
        return value
    if isinstance(value, str) and value.strip():
        return {"source": value.strip()}
    return None


def _runtime_gates(record: dict[str, Any]) -> list[str]:
    raw = record.get("runtime_gates_applied") or []
    if isinstance(raw, list):
        return [str(item) for item in raw]
    return []


def _pipeline_failures(record: dict[str, Any], index: int) -> list[str]:
    failures: list[str] = []
    if record.get("pipeline_coupled") is not True:
        failures.append(f"record_{index}_not_pipeline_coupled")
    gates = _runtime_gates(record)
    missing_gates = sorted(set(PIPELINE_GATE_NAMES) - set(gates))
    if missing_gates:
        failures.append(f"record_{index}_missing_runtime_gates:{','.join(missing_gates)}")
    return failures


def _convert(record: dict[str, Any], index: int) -> tuple[dict[str, Any] | None, list[str]]:
    failures: list[str] = []
    missing = sorted(field for field in REQUIRED_FIELDS if record.get(field) in (None, ""))
    if missing:
        failures.append(f"record_{index}_missing:{','.join(missing)}")
    if _has_marker(record):
        failures.append(f"record_{index}_demo_marker")
    failures.extend(_pipeline_failures(record, index))
    if str(record.get("data_status") or "").lower() not in {"ok", "valid", "complete"}:
        failures.append(f"record_{index}_invalid_data_status:{record.get('data_status')}")

    close = _num(record.get("close"))
    entry = _num(record.get("entry_trigger"))
    stop = _num(record.get("stop_loss"))
    target_1 = _num(record.get("target_1"))
    target_2 = _num(record.get("target_2"))
    if close is None:
        failures.append(f"record_{index}_missing_close")
    if entry is None:
        failures.append(f"record_{index}_missing_entry_trigger")
    if stop is None:
        failures.append(f"record_{index}_missing_stop_loss")
    if target_1 is None:
        failures.append(f"record_{index}_missing_target_1")
    if entry is not None and stop is not None and target_1 is not None and not (stop < entry < target_1):
        failures.append(f"record_{index}_invalid_price_ladder")
    provenance = _provenance(record.get("provenance"))
    if provenance is None:
        failures.append(f"record_{index}_missing_provenance")
    if failures:
        return None, failures

    timestamp = str(record["timestamp"])
    plan: dict[str, Any] = {
        "signal_id": str(record["signal_id"]),
        "symbol": str(record["symbol"]).upper(),
        "signal_date": str(record.get("signal_date") or timestamp[:10])[:10],
        "entry_trigger": entry,
        "stop_loss": stop,
        "target_1": target_1,
        "source": "paper_observation_validated",
        "data_source": str(record["data_source"]),
        "data_status": str(record["data_status"]),
        "provenance": provenance,
        "close": close,
    }
    if target_2 is not None:
        plan["target_2"] = target_2
    for key in ("valid_until", "entry_type", "setup_type", "stop_model", "exit_model"):
        if record.get(key) not in (None, ""):
            plan[key] = record[key]
    return plan, []


def _metadata(
    *,
    plans: list[dict[str, Any]],
    records: list[dict[str, Any]],
    generation_source: str = OBSERVATION_GENERATION_SOURCE,
) -> dict[str, Any]:
    blocked = max(len(records) - len(plans), 0)
    return {
        "pipeline_coupled": True,
        "pipeline_generation_source": generation_source,
        "generated_signal_count": len(records),
        "validated_trade_plan_count": len(plans),
        "blocked_signal_count": blocked,
        "runtime_gates_applied": PIPELINE_GATE_NAMES,
    }


def _scanner_metrics_map_from_payload(payload: dict[str, Any]) -> dict[str, Any]:
    raw = payload.get("scanner_metrics_map") or payload.get("scanner_metrics") or {}
    if isinstance(raw, dict):
        if all(isinstance(value, dict) for value in raw.values()):
            return {str(symbol).upper(): value for symbol, value in raw.items()}
        if raw.get("symbol"):
            return {str(raw["symbol"]).upper(): raw}
    if isinstance(raw, list):
        mapped: dict[str, Any] = {}
        for item in raw:
            if isinstance(item, dict) and item.get("symbol"):
                mapped[str(item["symbol"]).upper()] = item
        return mapped
    return {}


def _is_scanner_signal_quality_validator_payload(payload: Any) -> bool:
    return isinstance(payload, dict) and isinstance(payload.get("decision_report"), dict) and bool(
        payload.get("scanner_metrics_map") or payload.get("scanner_metrics")
    )


def _signal_date(signal: Signal) -> str:
    return str(signal.generated_at or "")[:10]


def _signal_to_plan(signal: Signal) -> tuple[dict[str, Any] | None, list[str]]:
    failures: list[str] = []
    if signal.action != "BUY_WATCH":
        return None, [f"signal_{signal.signal_id}_not_actionable:{signal.action}"]
    if signal.entry_trigger is None:
        failures.append(f"signal_{signal.signal_id}_missing_entry_trigger")
    if signal.stop_loss is None:
        failures.append(f"signal_{signal.signal_id}_missing_stop_loss")
    if signal.target_1 is None:
        failures.append(f"signal_{signal.signal_id}_missing_target_1")
    if signal.close is None:
        failures.append(f"signal_{signal.signal_id}_missing_close")
    if signal.atr14 is None:
        failures.append(f"signal_{signal.signal_id}_missing_atr14")
    if signal.source is None:
        failures.append(f"signal_{signal.signal_id}_missing_source")
    if signal.source_timestamp is None:
        failures.append(f"signal_{signal.signal_id}_missing_source_timestamp")
    if signal.data_status != "OK":
        failures.append(f"signal_{signal.signal_id}_invalid_data_status:{signal.data_status}")
    if signal.entry_trigger is not None and signal.stop_loss is not None and signal.target_1 is not None:
        if not (signal.stop_loss < signal.entry_trigger < signal.target_1):
            failures.append(f"signal_{signal.signal_id}_invalid_price_ladder")
    if _has_marker(asdict(signal)):
        failures.append(f"signal_{signal.signal_id}_demo_marker")
    if failures:
        return None, failures

    plan: dict[str, Any] = {
        "signal_id": signal.signal_id,
        "symbol": signal.symbol.upper(),
        "signal_date": _signal_date(signal),
        "entry_trigger": signal.entry_trigger,
        "stop_loss": signal.stop_loss,
        "target_1": signal.target_1,
        "source": PIPELINE_GENERATION_SOURCE,
        "data_source": signal.data_source,
        "data_status": signal.data_status,
        "provenance": {
            "source": signal.source,
            "source_timestamp": signal.source_timestamp,
            "fallback_level": signal.fallback_level,
            "score_source": signal.score_source,
            "thresholds_version": signal.thresholds_version,
            "runtime_gates_applied": PIPELINE_GATE_NAMES,
        },
        "close": signal.close,
        "atr14": signal.atr14,
        "valid_until": signal.valid_until,
        "entry_type": signal.entry_type,
        "setup_type": signal.setup_type,
        "stop_model": signal.stop_model,
        "exit_model": signal.exit_model,
    }
    if signal.target_2 is not None:
        plan["target_2"] = signal.target_2
    return plan, []


def _build_pipeline_plans(payload: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any], list[str]]:
    failures: list[str] = []
    decision_report = payload.get("decision_report")
    scanner_metrics_map = _scanner_metrics_map_from_payload(payload)
    if not isinstance(decision_report, dict):
        return [], {}, ["missing_decision_report"]
    if not scanner_metrics_map:
        return [], {}, ["missing_scanner_metrics_map"]
    if _has_marker(payload):
        failures.append("pipeline_payload_demo_marker")

    try:
        signals = build_signals(
            decision_report=decision_report,
            scanner_metrics_map=scanner_metrics_map,
            market_regime=str(payload.get("market_regime") or decision_report.get("market_regime") or "Unknown"),
        )
    except Exception as exc:  # defensive CLI boundary: report as fail-closed manifest instead of partial output
        return [], {}, [f"signal_generation_failed:{type(exc).__name__}:{exc}"]

    plans: list[dict[str, Any]] = []
    for signal in signals:
        plan, signal_failures = _signal_to_plan(signal)
        if plan is not None:
            plans.append(plan)
        else:
            failures.extend(signal_failures)

    actionable_input_count = sum(1 for signal in signals if signal.action == "BUY_WATCH")
    if actionable_input_count == 0:
        failures.append("no_validated_buy_watch_signals")
    if not plans:
        failures.append("no_validated_trade_plans")

    metadata = {
        "pipeline_coupled": True,
        "pipeline_generation_source": PIPELINE_GENERATION_SOURCE,
        "generated_signal_count": len(signals),
        "validated_trade_plan_count": len(plans),
        "blocked_signal_count": max(len(signals) - len(plans), 0),
        "runtime_gates_applied": PIPELINE_GATE_NAMES,
    }
    return plans, metadata, failures


def _write_export_payload(
    *,
    plans: list[dict[str, Any]],
    output_path: Path,
    metadata: dict[str, Any],
) -> str:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"metadata": metadata, "plans": plans}
    raw = _json_bytes(payload)
    output_sha = hashlib.sha256(raw).hexdigest()
    output_path.write_bytes(raw)
    return output_sha


def export_historical_trade_plans(*, source_path: Path, output_path: Path, manifest_path: Path) -> HistoricalTradePlanExportReport:
    payload, payload_failures = _read_payload(source_path)
    if not payload_failures and _is_scanner_signal_quality_validator_payload(payload):
        plans, metadata, failures = _build_pipeline_plans(payload)
        plans = sorted(plans, key=lambda item: (item["signal_date"], item["symbol"], item["signal_id"]))
        dates = sorted({plan["signal_date"] for plan in plans})
        output_sha: str | None = None
        if not failures:
            output_sha = _write_export_payload(plans=plans, output_path=output_path, metadata=metadata)
        report = HistoricalTradePlanExportReport(
            passed=not failures,
            source_path=source_path.as_posix(),
            output_path=output_path.as_posix(),
            manifest_path=manifest_path.as_posix(),
            source_window={"start": dates[0], "end": dates[-1]} if dates else {},
            record_count=metadata.get("generated_signal_count", 0),
            exported_count=len(plans) if not failures else 0,
            symbols=sorted({plan["symbol"] for plan in plans}) if not failures else [],
            output_sha256=output_sha,
            pipeline_coupled=not failures,
            pipeline_generation_source=PIPELINE_GENERATION_SOURCE,
            runtime_gates_applied=PIPELINE_GATE_NAMES if not failures else [],
            generated_signal_count=metadata.get("generated_signal_count", 0),
            validated_trade_plan_count=metadata.get("validated_trade_plan_count", 0) if not failures else 0,
            blocked_signal_count=metadata.get("blocked_signal_count", 0) if not failures else metadata.get("generated_signal_count", 0),
            failures=failures,
        )
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_bytes(_json_bytes(report.to_dict()))
        return report

    records, failures = _read_records(source_path)
    plans: list[dict[str, Any]] = []
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            failures.append(f"record_{index}_not_object")
            continue
        plan, record_failures = _convert(record, index)
        failures.extend(record_failures)
        if plan:
            plans.append(plan)

    plans = sorted(plans, key=lambda item: (item["signal_date"], item["symbol"], item["signal_id"]))
    dates = sorted({plan["signal_date"] for plan in plans})
    output_sha: str | None = None
    metadata = _metadata(plans=plans, records=records)
    if not failures:
        output_sha = _write_export_payload(plans=plans, output_path=output_path, metadata=metadata)

    report = HistoricalTradePlanExportReport(
        passed=not failures,
        source_path=source_path.as_posix(),
        output_path=output_path.as_posix(),
        manifest_path=manifest_path.as_posix(),
        source_window={"start": dates[0], "end": dates[-1]} if dates else {},
        record_count=len(records),
        exported_count=len(plans) if not failures else 0,
        symbols=sorted({plan["symbol"] for plan in plans}) if not failures else [],
        output_sha256=output_sha,
        pipeline_coupled=not failures,
        pipeline_generation_source=OBSERVATION_GENERATION_SOURCE,
        runtime_gates_applied=PIPELINE_GATE_NAMES if not failures else [],
        generated_signal_count=metadata["generated_signal_count"] if not failures else len(records),
        validated_trade_plan_count=metadata["validated_trade_plan_count"] if not failures else 0,
        blocked_signal_count=metadata["blocked_signal_count"] if not failures else len(records),
        failures=failures,
    )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_bytes(_json_bytes(report.to_dict()))
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export validated observations or scanner/signal/quality/validator payloads to historical trade plans."
    )
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", default="data/trade_plans/historical_trade_plans.json")
    parser.add_argument("--manifest", default="data/trade_plans/historical_trade_plans_manifest.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = export_historical_trade_plans(source_path=Path(args.source), output_path=Path(args.output), manifest_path=Path(args.manifest))
    print(f"HTP1/#177 historical trade-plan export status: {'PASS' if report.passed else 'FAIL'}")
    print(f"Pipeline source: {report.pipeline_generation_source}")
    if report.failures:
        print("Failures:")
        for failure in report.failures:
            print(f"- {failure}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
