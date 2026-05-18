"""
Automated Outcome Pipeline.

This module connects generated decision reports with persistent outcome logs.
It supports three core operations:

1. record_decisions_from_report_payload
   Store every ranked opportunity from a generated report.

2. update_outcomes
   Resolve 1D/5D/20D returns plus MFE/MAE from historical bars.

3. build_expectancy_summary
   Convert the updated log into adaptive expectancy profiles.
"""

from __future__ import annotations

import csv
from dataclasses import asdict, replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from src.adaptive_expectancy import build_adaptive_expectancy_report
from src.outcome_tracking import (
    FIELDNAMES,
    DecisionRecord,
    append_decision_record,
    build_decision_record,
    read_decision_records,
)

DEFAULT_DECISION_LOG = Path("data/decision_log.csv")


def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _serialize_record(record: DecisionRecord) -> dict[str, Any]:
    return asdict(record)


def _safe_float(value: object) -> float | None:
    if value in {None, "", "None"}:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def record_decisions_from_report_payload(
    payload: dict,
    *,
    path: str | Path = DEFAULT_DECISION_LOG,
    price_lookup: dict[str, float] | None = None,
) -> Path:
    """Persist ranked opportunities from a report payload."""
    decision_report = payload.get("decision_report", {})
    decisions = decision_report.get("decisions", [])
    market_state = decision_report.get("market_state", "unknown")
    price_lookup = price_lookup or {}

    output_path = Path(path)

    for decision in decisions:
        symbol = decision["symbol"]
        record = build_decision_record(
            symbol=symbol,
            market_state=market_state,
            setup_type=decision.get("setup_type", "unknown"),
            decision=decision.get("decision", "unknown"),
            risk_tier=decision.get("risk_tier", "no_trade"),
            position_size_multiplier=float(decision.get("position_size_multiplier", 0.0)),
            setup_score=float(decision.get("setup_score", 0.0)),
            regime_alignment=float(decision.get("regime_alignment", 0.0)),
            asymmetry_score=float(decision.get("asymmetry_score", 0.0)),
            data_confidence=float(decision.get("data_confidence", 0.0)),
            blocked_reasons=decision.get("blocked_reasons", []),
            notes=decision.get("notes", []),
            price_at_decision=price_lookup.get(symbol),
        )
        append_decision_record(output_path, record)

    return output_path


def _bar_close_on_or_after(bars: list[dict], start_index: int, offset: int) -> float | None:
    target_index = start_index + offset
    if target_index >= len(bars):
        return None
    return float(bars[target_index]["c"])


def _find_decision_bar_index(bars: list[dict], timestamp_utc: str) -> int | None:
    decision_date = _parse_timestamp(timestamp_utc).date()

    for index, bar in enumerate(bars):
        raw_time = bar.get("t")
        if raw_time is None:
            continue
        bar_date = datetime.fromtimestamp(int(raw_time) / 1000, tz=UTC).date()
        if bar_date >= decision_date:
            return index

    if bars:
        return len(bars) - 1
    return None


def calculate_outcome_metrics(record: dict, bars: list[dict]) -> dict[str, float | None]:
    """Calculate return horizons and MFE/MAE for one decision record."""
    if not bars:
        return {
            "price_at_decision": None,
            "result_1d": None,
            "result_5d": None,
            "result_20d": None,
            "mfe": None,
            "mae": None,
        }

    start_index = _find_decision_bar_index(bars, str(record["timestamp_utc"]))
    if start_index is None:
        return {
            "price_at_decision": None,
            "result_1d": None,
            "result_5d": None,
            "result_20d": None,
            "mfe": None,
            "mae": None,
        }

    entry_price = _safe_float(record.get("price_at_decision")) or float(bars[start_index]["c"])

    def pct_return(close: float | None) -> float | None:
        if close is None or entry_price == 0:
            return None
        return round(((close / entry_price) - 1) * 100, 4)

    future_window = bars[start_index : min(len(bars), start_index + 21)]
    highs = [float(bar["h"]) for bar in future_window]
    lows = [float(bar["l"]) for bar in future_window]

    mfe = round(((max(highs) / entry_price) - 1) * 100, 4) if highs and entry_price else None
    mae = round(((min(lows) / entry_price) - 1) * 100, 4) if lows and entry_price else None

    return {
        "price_at_decision": round(entry_price, 4),
        "result_1d": pct_return(_bar_close_on_or_after(bars, start_index, 1)),
        "result_5d": pct_return(_bar_close_on_or_after(bars, start_index, 5)),
        "result_20d": pct_return(_bar_close_on_or_after(bars, start_index, 20)),
        "mfe": mfe,
        "mae": mae,
    }


def update_outcomes(
    *,
    path: str | Path = DEFAULT_DECISION_LOG,
    bars_by_symbol: dict[str, list[dict]],
) -> Path:
    """Update existing decision records with outcome metrics."""
    input_path = Path(path)
    rows = read_decision_records(input_path)
    updated_records: list[DecisionRecord] = []

    for row in rows:
        bars = bars_by_symbol.get(row["symbol"], [])
        metrics = calculate_outcome_metrics(row, bars)

        record = DecisionRecord(
            timestamp_utc=row["timestamp_utc"],
            symbol=row["symbol"],
            market_state=row["market_state"],
            setup_type=row["setup_type"],
            decision=row["decision"],
            risk_tier=row["risk_tier"],
            position_size_multiplier=float(row["position_size_multiplier"]),
            setup_score=float(row["setup_score"]),
            regime_alignment=float(row["regime_alignment"]),
            asymmetry_score=float(row["asymmetry_score"]),
            data_confidence=float(row["data_confidence"]),
            blocked_reasons=row.get("blocked_reasons", ""),
            notes=row.get("notes", ""),
            price_at_decision=metrics["price_at_decision"],
            result_1d=metrics["result_1d"],
            result_5d=metrics["result_5d"],
            result_20d=metrics["result_20d"],
            mfe=metrics["mfe"],
            mae=metrics["mae"],
        )
        updated_records.append(record)

    input_path.parent.mkdir(parents=True, exist_ok=True)
    with input_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        writer.writeheader()
        for record in updated_records:
            writer.writerow(_serialize_record(record))

    return input_path


def build_expectancy_summary(path: str | Path = DEFAULT_DECISION_LOG) -> dict[str, Any]:
    records = read_decision_records(path)
    report = build_adaptive_expectancy_report(records)

    return {
        "setup_profiles": [asdict(profile) for profile in report.setup_profiles],
        "regime_profiles": [asdict(profile) for profile in report.regime_profiles],
        "combined_profiles": [asdict(profile) for profile in report.combined_profiles],
        "strongest_edges": list(report.strongest_edges),
        "weakest_edges": list(report.weakest_edges),
    }
