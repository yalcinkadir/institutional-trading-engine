#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = [
    "run_id",
    "data_source",
    "is_demo",
    "symbol_universe",
    "date_range",
    "strategy_version",
    "input_pack_gate_status",
    "input_completeness_status",
    "run_health_status",
    "coverage_manifest_path",
    "survivorship_universe_path",
    "trade_plans_path",
    "input_plan_count",
    "accepted_plan_count",
    "rejected_plan_count",
    "rejection_reasons",
    "metrics",
    "results",
    "live_trading_authorized",
    "broker_execution_mode",
]

DEMO_MARKERS = {"demo", "synthetic", "public_safe", "historical_demo"}
REAL_DATA_SOURCE = "real_data"
BROKER_EXECUTION_MODE = "paper_only"
VALID_INPUT_COMPLETENESS_STATUSES = {"OK", "DEGRADED_DATA"}
VALID_RUN_HEALTH_STATUSES = {"OK", "NO_TRADE_VALID", "DEGRADED_DATA"}
MIN_REAL_DATA_TRADE_COUNT = 30
INSUFFICIENT_SAMPLE_STATUS = "INSUFFICIENT_SAMPLE"
REVIEWABLE_SAMPLE_STATUS = "REVIEWABLE_SAMPLE"
REVIEW_READY_STATUSES = {
    "READY_FOR_REVIEW",
    "REVIEW_READY",
    "REVIEWABLE_SAMPLE",
    "PROMOTION_CANDIDATE_SAMPLE",
}
REVIEW_STATUS_FIELDS = (
    "readiness_status",
    "review_status",
    "evidence_status",
    "validation_status",
    "promotion_status",
)


@dataclass(frozen=True)
class RealDataBacktestEvidenceGateReport:
    passed: bool
    artifact_path: str
    missing_fields: list[str] = field(default_factory=list)
    invalid_fields: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    observed_trade_count: int | None = None
    min_trade_count: int = MIN_REAL_DATA_TRADE_COUNT
    sample_quality_status: str = INSUFFICIENT_SAMPLE_STATUS

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _load_payload(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    if not path.exists():
        return None, ["artifact_missing"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [f"invalid_json: {exc}"]
    if not isinstance(payload, dict):
        return None, ["artifact_not_object"]
    return payload, []


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_symbol_universe(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(_non_empty_string(symbol) for symbol in value)


def _valid_date_range(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    return _non_empty_string(value.get("start")) and _non_empty_string(value.get("end"))


def _has_demo_marker(payload: dict[str, Any]) -> bool:
    tags = payload.get("tags", [])
    if isinstance(tags, list) and any(str(tag).lower() in DEMO_MARKERS for tag in tags):
        return True
    for field_name in ("data_source", "data_mode", "dataset_id"):
        value = str(payload.get(field_name, "")).lower()
        if any(marker in value for marker in DEMO_MARKERS):
            return True
    return bool(payload.get("is_demo"))


def _valid_non_negative_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _int_or_none(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return None


def _extract_trade_count(payload: dict[str, Any]) -> int | None:
    """Return the trade count used by the real-data sample-size gate.

    The preferred source is an explicit metric. Results length remains a
    backward-compatible fallback for existing BT130/P121 artifacts.
    """

    metrics = payload.get("metrics")
    if isinstance(metrics, dict):
        for key in ("trade_count", "executed_trade_count", "total_trades", "total"):
            count = _int_or_none(metrics.get(key))
            if count is not None:
                return count

    results = payload.get("results")
    if isinstance(results, list):
        return len(results)

    return _int_or_none(payload.get("accepted_plan_count"))


def _derive_sample_quality_status(trade_count: int | None) -> str:
    if trade_count is None or trade_count < MIN_REAL_DATA_TRADE_COUNT:
        return INSUFFICIENT_SAMPLE_STATUS
    return REVIEWABLE_SAMPLE_STATUS


def validate_real_data_backtest_evidence_artifact(path: Path) -> RealDataBacktestEvidenceGateReport:
    payload, errors = _load_payload(path)
    if payload is None:
        return RealDataBacktestEvidenceGateReport(passed=False, artifact_path=path.as_posix(), errors=errors)

    missing_fields = [field_name for field_name in REQUIRED_FIELDS if field_name not in payload]
    invalid_fields: list[str] = []

    if "run_id" in payload and not _non_empty_string(payload.get("run_id")):
        invalid_fields.append("run_id")
    if "data_source" in payload and payload.get("data_source") != REAL_DATA_SOURCE:
        invalid_fields.append("data_source")
    if "is_demo" in payload and payload.get("is_demo") is not False:
        invalid_fields.append("is_demo")
    if "symbol_universe" in payload and not _valid_symbol_universe(payload.get("symbol_universe")):
        invalid_fields.append("symbol_universe")
    if "date_range" in payload and not _valid_date_range(payload.get("date_range")):
        invalid_fields.append("date_range")
    if "strategy_version" in payload and not _non_empty_string(payload.get("strategy_version")):
        invalid_fields.append("strategy_version")
    if "input_pack_gate_status" in payload and payload.get("input_pack_gate_status") != "PASSED":
        invalid_fields.append("input_pack_gate_status")
    if "input_completeness_status" in payload and payload.get("input_completeness_status") not in VALID_INPUT_COMPLETENESS_STATUSES:
        invalid_fields.append("input_completeness_status")
    if "run_health_status" in payload and payload.get("run_health_status") not in VALID_RUN_HEALTH_STATUSES:
        invalid_fields.append("run_health_status")
    for field_name in ("coverage_manifest_path", "survivorship_universe_path", "trade_plans_path"):
        if field_name in payload and not _non_empty_string(payload.get(field_name)):
            invalid_fields.append(field_name)
    for field_name in ("input_plan_count", "accepted_plan_count", "rejected_plan_count"):
        if field_name in payload and not _valid_non_negative_int(payload.get(field_name)):
            invalid_fields.append(field_name)
    if "input_plan_count" in payload and "accepted_plan_count" in payload and "rejected_plan_count" in payload:
        if payload.get("input_plan_count") != payload.get("accepted_plan_count") + payload.get("rejected_plan_count"):
            invalid_fields.append("plan_count_mismatch")
        if payload.get("input_plan_count") <= 0:
            invalid_fields.append("input_plan_count_empty")
        if payload.get("accepted_plan_count") <= 0:
            invalid_fields.append("accepted_plan_count_empty")
    if "rejection_reasons" in payload and not isinstance(payload.get("rejection_reasons"), list):
        invalid_fields.append("rejection_reasons")
    if "rejected_plan_count" in payload and "rejection_reasons" in payload and isinstance(payload.get("rejection_reasons"), list):
        if payload.get("rejected_plan_count") != len(payload.get("rejection_reasons")):
            invalid_fields.append("rejection_reason_count_mismatch")
    if "metrics" in payload and not isinstance(payload.get("metrics"), dict):
        invalid_fields.append("metrics")
    if "results" in payload and not isinstance(payload.get("results"), list):
        invalid_fields.append("results")
    if "results" in payload and isinstance(payload.get("results"), list) and not payload.get("results"):
        invalid_fields.append("results_empty")

    observed_trade_count = _extract_trade_count(payload)
    sample_quality_status = _derive_sample_quality_status(observed_trade_count)
    if observed_trade_count is None:
        invalid_fields.append("trade_count")
    elif observed_trade_count < MIN_REAL_DATA_TRADE_COUNT:
        invalid_fields.append("insufficient_sample")
        declared_sample_status = payload.get("sample_quality_status")
        if declared_sample_status is not None and declared_sample_status != INSUFFICIENT_SAMPLE_STATUS:
            invalid_fields.append("sample_quality_status")
        for field_name in REVIEW_STATUS_FIELDS:
            if payload.get(field_name) in REVIEW_READY_STATUSES:
                invalid_fields.append(f"{field_name}_sample_size_mismatch")
    elif payload.get("sample_quality_status") not in (None, REVIEWABLE_SAMPLE_STATUS):
        invalid_fields.append("sample_quality_status")

    if payload.get("live_trading_authorized") is not False:
        invalid_fields.append("live_trading_authorized")
    if payload.get("broker_execution_mode") != BROKER_EXECUTION_MODE:
        invalid_fields.append("broker_execution_mode")
    if _has_demo_marker(payload):
        invalid_fields.append("demo_marker")

    return RealDataBacktestEvidenceGateReport(
        passed=not missing_fields and not invalid_fields and not errors,
        artifact_path=path.as_posix(),
        missing_fields=missing_fields,
        invalid_fields=invalid_fields,
        errors=errors,
        observed_trade_count=observed_trade_count,
        min_trade_count=MIN_REAL_DATA_TRADE_COUNT,
        sample_quality_status=sample_quality_status,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate real-data backtest evidence artifact schema.")
    parser.add_argument("--artifact", default="reports/backtests/real-data-backtest-evidence.json")
    parser.add_argument("--report-output", default="reports/backtests/real-data-backtest-evidence-gate.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = validate_real_data_backtest_evidence_artifact(Path(args.artifact))
    output = Path(args.report_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")

    status = "PASS" if report.passed else "FAIL"
    print(f"Real-data backtest evidence gate status: {status}")
    print(f"Artifact: {report.artifact_path}")
    print(f"Observed trade count: {report.observed_trade_count}")
    print(f"Minimum trade count: {report.min_trade_count}")
    print(f"Sample quality status: {report.sample_quality_status}")
    if report.missing_fields:
        print(f"Missing fields: {', '.join(report.missing_fields)}")
    if report.invalid_fields:
        print(f"Invalid fields: {', '.join(report.invalid_fields)}")
    if report.errors:
        print(f"Errors: {', '.join(report.errors)}")
    print(f"Gate report: {args.report_output}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
