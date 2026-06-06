#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

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


def _read_records(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    if not path.exists():
        return [], ["missing_source_observations_file"]
    if path.suffix.lower() == ".csv":
        with path.open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle)), []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [], [f"source_observations_invalid_json:{exc}"]
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


def _convert(record: dict[str, Any], index: int) -> tuple[dict[str, Any] | None, list[str]]:
    failures: list[str] = []
    missing = sorted(field for field in REQUIRED_FIELDS if record.get(field) in (None, ""))
    if missing:
        failures.append(f"record_{index}_missing:{','.join(missing)}")
    if _has_marker(record):
        failures.append(f"record_{index}_demo_marker")
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


def export_historical_trade_plans(*, source_path: Path, output_path: Path, manifest_path: Path) -> HistoricalTradePlanExportReport:
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
    if not failures:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"plans": plans}
        raw = _json_bytes(payload)
        output_sha = hashlib.sha256(raw).hexdigest()
        output_path.write_bytes(raw)

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
        failures=failures,
    )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_bytes(_json_bytes(report.to_dict()))
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export Paper Observation records to historical trade plans.")
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", default="data/trade_plans/historical_trade_plans.json")
    parser.add_argument("--manifest", default="data/trade_plans/historical_trade_plans_manifest.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = export_historical_trade_plans(source_path=Path(args.source), output_path=Path(args.output), manifest_path=Path(args.manifest))
    print(f"HTP1 historical trade-plan export status: {'PASS' if report.passed else 'FAIL'}")
    if report.failures:
        print("Failures:")
        for failure in report.failures:
            print(f"- {failure}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
