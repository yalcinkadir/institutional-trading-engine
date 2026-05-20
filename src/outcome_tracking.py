"""
Outcome Tracking for Decision Engine v3.

The Decision Engine only becomes useful when decisions are tracked and later
measured. This module records both approved and rejected opportunities so the
system can learn whether its gates, overrides and no-trade decisions improve
expectancy.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass, fields
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class DecisionRecord:
    timestamp_utc: str
    symbol: str
    market_state: str
    setup_type: str
    decision: str
    risk_tier: str
    position_size_multiplier: float
    setup_score: float
    regime_alignment: float
    asymmetry_score: float
    data_confidence: float
    blocked_reasons: str = ""
    notes: str = ""
    price_at_decision: float | None = None
    result_1d: float | None = None
    result_5d: float | None = None
    result_20d: float | None = None
    mfe: float | None = None
    mae: float | None = None


FIELDNAMES = [field.name for field in fields(DecisionRecord)]


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _stringify_list(values: list[str] | tuple[str, ...] | str | None) -> str:
    if values is None:
        return ""
    if isinstance(values, str):
        return values
    return "|".join(values)


def build_decision_record(
    *,
    symbol: str,
    market_state: str,
    setup_type: str,
    decision: str,
    risk_tier: str,
    position_size_multiplier: float,
    setup_score: float,
    regime_alignment: float,
    asymmetry_score: float,
    data_confidence: float,
    blocked_reasons: list[str] | tuple[str, ...] | str | None = None,
    notes: list[str] | tuple[str, ...] | str | None = None,
    price_at_decision: float | None = None,
    timestamp_utc: str | None = None,
) -> DecisionRecord:
    return DecisionRecord(
        timestamp_utc=timestamp_utc or utc_now_iso(),
        symbol=symbol,
        market_state=market_state,
        setup_type=setup_type,
        decision=decision,
        risk_tier=risk_tier,
        position_size_multiplier=position_size_multiplier,
        setup_score=setup_score,
        regime_alignment=regime_alignment,
        asymmetry_score=asymmetry_score,
        data_confidence=data_confidence,
        blocked_reasons=_stringify_list(blocked_reasons),
        notes=_stringify_list(notes),
        price_at_decision=price_at_decision,
    )


def append_decision_record(path: str | Path, record: DecisionRecord) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    file_exists = output_path.exists() and output_path.stat().st_size > 0

    with output_path.open("a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(asdict(record))

    return output_path


def _read_csv_records(input_path: Path) -> list[dict[str, Any]]:
    with input_path.open("r", newline="", encoding="utf-8") as csvfile:
        return list(csv.DictReader(csvfile))


def _read_jsonl_records(input_path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    with input_path.open("r", encoding="utf-8") as jsonlfile:
        for line in jsonlfile:
            line = line.strip()
            if not line:
                continue

            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue

            # Runtime snapshots may wrap the actual decision payload.
            if isinstance(payload, dict):
                if "decision" in payload and isinstance(payload["decision"], dict):
                    payload = payload["decision"]

                records.append(payload)

    return records


def read_decision_records(path: str | Path) -> list[dict[str, Any]]:
    """
    Read decision records from CSV or JSONL.

    Supported:
    - decision_log.csv
    - decision_log.jsonl
    - runtime snapshot JSONL streams
    """
    input_path = Path(path)
    if not input_path.exists():
        return []

    suffix = input_path.suffix.lower()

    try:
        if suffix == ".jsonl":
            return _read_jsonl_records(input_path)

        return _read_csv_records(input_path)

    except Exception:
        return []


def calculate_basic_expectancy(records: list[dict[str, Any]], result_field: str = "result_5d") -> dict[str, float | int]:
    """Calculate simple expectancy stats for a chosen result horizon."""
    numeric_results: list[float] = []

    for record in records:
        value = record.get(result_field)
        if value in {None, "", "None"}:
            continue
        try:
            numeric_results.append(float(value))
        except (TypeError, ValueError):
            continue

    if not numeric_results:
        return {
            "count": 0,
            "win_rate": 0.0,
            "average_result": 0.0,
            "expectancy": 0.0,
        }

    wins = [value for value in numeric_results if value > 0]
    losses = [value for value in numeric_results if value <= 0]
    win_rate = len(wins) / len(numeric_results)
    average_win = sum(wins) / len(wins) if wins else 0.0
    average_loss = sum(losses) / len(losses) if losses else 0.0
    expectancy = (win_rate * average_win) + ((1 - win_rate) * average_loss)

    return {
        "count": len(numeric_results),
        "win_rate": round(win_rate, 4),
        "average_result": round(sum(numeric_results) / len(numeric_results), 4),
        "expectancy": round(expectancy, 4),
    }
