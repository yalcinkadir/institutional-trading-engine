#!/usr/bin/env python3
"""Produce a canonical paper-only daily observation evidence artifact for P166.

The producer is intentionally paper-only. It does not place orders, does not talk to
brokers, does not allocate capital, and does not commit runtime output back to the
repository. It writes the daily evidence JSON that PO11 validates and uploads as an
Actions artifact.
"""

from __future__ import annotations

import argparse
import json
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from src.operations.daily_observation_record_writer import build_daily_observation_record, write_daily_observation_record
from src.reporting.market_regime import build_market_regime_summary

OUTPUT_ROOT = Path("reports/daily_evidence")
DEFAULT_SELECTION_MODE = "configured_watchlist"
DEFAULT_SELECTED_SYMBOLS = ("MSFT", "NVDA", "META", "AAPL", "MU", "QQQ", "GLD", "SLV")
PRODUCTIVE_SOURCE = "p166_daily_observation_evidence_producer"
PAPER_ONLY_BOUNDARY = {
    "live_trading_authorized": False,
    "broker_execution_mode": "paper_only",
    "capital_allocation_authorized": False,
    "repository_mutation_authorized": False,
}


def _parse_symbols(value: str | None) -> list[str]:
    if not value:
        return list(DEFAULT_SELECTED_SYMBOLS)
    symbols = [part.strip().upper() for part in value.split(",") if part.strip()]
    return symbols or list(DEFAULT_SELECTED_SYMBOLS)


def _observation_date(value: str | None) -> str:
    if not value:
        return datetime.now(UTC).date().isoformat()
    date.fromisoformat(value)
    return value


def _evidence_path(observation_date: str, output_root: str | Path = OUTPUT_ROOT) -> Path:
    return Path(output_root) / f"{observation_date}.json"


def _market_regime_health(regime: dict[str, Any]) -> dict[str, Any]:
    validation_status = str(regime.get("regime_validation_status") or "UNKNOWN")
    data_status = str(regime.get("data_status") or "UNKNOWN")
    errors = list(regime.get("errors") or [])

    if data_status == "LIVE" and validation_status == "LIVE" and not errors:
        status = "PASSED"
        run_health_status = "OK"
        data_quality_status = "LIVE"
        missing_evidence: list[str] = []
    elif validation_status in {"DEGRADED", "LIVE"} and data_status in {"PARTIAL", "LIVE"}:
        status = "PASSED"
        run_health_status = "DEGRADED"
        data_quality_status = data_status
        missing_evidence = []
    else:
        status = "BLOCKED_DATA_QUALITY"
        run_health_status = "BLOCKED"
        data_quality_status = data_status
        missing_evidence = [f"regime_validation_status:{validation_status}"]

    return {
        "signal_generation_status": status,
        "run_health_status": run_health_status,
        "data_quality_status": data_quality_status,
        "missing_evidence": missing_evidence,
    }


def build_daily_evidence(
    *,
    observation_date: str,
    selected_symbols: list[str],
    selection_mode: str = DEFAULT_SELECTION_MODE,
    created_at: str | None = None,
    report_type: str = "postmarket",
) -> dict[str, Any]:
    created_at_value = created_at or datetime.now(UTC).isoformat()
    regime = build_market_regime_summary(report_type)
    health = _market_regime_health(regime)

    signal_health = {
        "stage": "signal_generation",
        "status": health["signal_generation_status"],
        "run_health_status": health["run_health_status"],
        "data_quality_status": health["data_quality_status"],
        "selection_mode": selection_mode,
        "selected_symbols": selected_symbols,
        "source": PRODUCTIVE_SOURCE,
        "source_provenance": {
            "producer": PRODUCTIVE_SOURCE,
            "market_regime_source": "src.reporting.market_regime.build_market_regime_summary",
            "regime_validation_status": regime.get("regime_validation_status"),
            "regime_data_status": regime.get("data_status"),
            "vix_input": (regime.get("regime_input") or {}).get("vix"),
        },
        **PAPER_ONLY_BOUNDARY,
    }

    record = build_daily_observation_record(
        observation_date=observation_date,
        missing_evidence=health["missing_evidence"],
        incidents=[] if health["run_health_status"] != "DEGRADED" else ["degraded_regime_evidence"],
        artifact_paths=[],
        review_notes="P166 productive paper-only daily observation evidence.",
        created_at=created_at_value,
        signal_generation_status=health["signal_generation_status"],
        signal_generation_health=signal_health,
    )

    record.update(
        {
            "schema_version": "p166.v1",
            "observation_date": observation_date,
            "source": PRODUCTIVE_SOURCE,
            "source_provenance": signal_health["source_provenance"],
            "run_health_status": health["run_health_status"],
            "data_quality_status": health["data_quality_status"],
            "selection_mode": selection_mode,
            "selected_symbols": selected_symbols,
            "market_regime": regime,
            "paper_only_safety_boundary": PAPER_ONLY_BOUNDARY,
            "productive_evidence": record["status"] == "ACCEPTED",
            "demo_or_synthetic": False,
        }
    )
    return record


def write_daily_evidence(record: dict[str, Any], output_root: str | Path = OUTPUT_ROOT) -> Path:
    path = _evidence_path(str(record["date"]), output_root)
    validation = write_daily_observation_record(record=record, output_path=path)
    if not validation.valid:
        raise SystemExit("daily observation evidence validation failed: " + ",".join(validation.errors))
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Produce P166 paper-only daily observation evidence")
    parser.add_argument("--observation-date", default=None)
    parser.add_argument("--selected-symbols", default=None)
    parser.add_argument("--selection-mode", default=DEFAULT_SELECTION_MODE)
    parser.add_argument("--output-root", default=str(OUTPUT_ROOT))
    parser.add_argument("--report-type", default="postmarket")
    args = parser.parse_args()

    observation_date = _observation_date(args.observation_date)
    selected_symbols = _parse_symbols(args.selected_symbols)
    record = build_daily_evidence(
        observation_date=observation_date,
        selected_symbols=selected_symbols,
        selection_mode=args.selection_mode,
        report_type=args.report_type,
    )
    path = write_daily_evidence(record, output_root=args.output_root)

    print(json.dumps({
        "observation_date": observation_date,
        "artifact_path": str(path),
        "status": record.get("status"),
        "run_health_status": record.get("run_health_status"),
        "data_quality_status": record.get("data_quality_status"),
        "regime_validation_status": record.get("market_regime", {}).get("regime_validation_status"),
        "productive_evidence": record.get("productive_evidence"),
        "demo_or_synthetic": record.get("demo_or_synthetic"),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
