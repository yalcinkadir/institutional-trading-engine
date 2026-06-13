#!/usr/bin/env python3
"""Build BT139 sample-expansion evidence report for BT131 real-data backtests.

BT139 is an evidence-expansion gate. It does not change trading rules. It
classifies whether the BT131 sample is large and diverse enough to support
research recommendations from BT133/BT134/BT135/BT137/BT138.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any


INSUFFICIENT_SAMPLE = "INSUFFICIENT_SAMPLE"
EARLY_DIRECTIONAL_SAMPLE = "EARLY_DIRECTIONAL_SAMPLE"
REVIEWABLE_SAMPLE = "REVIEWABLE_SAMPLE"
PROMOTION_CANDIDATE_SAMPLE = "PROMOTION_CANDIDATE_SAMPLE"

QUALITY_ORDER = {
    INSUFFICIENT_SAMPLE: 0,
    EARLY_DIRECTIONAL_SAMPLE: 1,
    REVIEWABLE_SAMPLE: 2,
    PROMOTION_CANDIDATE_SAMPLE: 3,
}

REQUIRED_ROW_FIELDS = (
    "signal_id",
    "symbol",
    "signal_date",
    "setup_type",
    "entry_price",
    "initial_stop_loss",
    "target_1",
    "target_2",
    "max_adverse_excursion_r",
    "max_favorable_excursion_r",
    "same_bar_ambiguous",
    "signal_day_cluster_size",
)

OPTIONAL_ROW_FIELDS = (
    "atr14_at_signal",
    "volume",
    "avg_volume_20",
    "market_regime",
    "asset_group",
)

REAL_NO_TRADE_OUTCOMES = {"EXPIRED", "UNTRIGGERED", "PENDING", "NO_TRADE", "NO_ACTIONABLE_SIGNALS"}
MISSING_INPUT_OUTCOMES = {"MISSING_INPUT", "MISSING_INPUTS", "SKIPPED_MISSING_INPUT", "BLOCKED_MISSING_INPUTS"}
EVALUATED_OUTCOMES = {"TARGET_1_HIT", "TARGET_2_HIT", "STOP_HIT", "WIN", "LOSS", "NEUTRAL"}


@dataclass(frozen=True)
class SampleThresholds:
    early_min_trade_count: int = 50
    reviewable_min_trade_count: int = 100
    promotion_min_trade_count: int = 200
    reviewable_min_symbol_count: int = 8
    promotion_min_symbol_count: int = 12
    reviewable_min_signal_day_count: int = 30
    promotion_min_signal_day_count: int = 60
    reviewable_min_setup_count: int = 2
    promotion_min_setup_count: int = 3
    reviewable_min_asset_group_count: int = 3
    promotion_min_asset_group_count: int = 4


@dataclass(frozen=True)
class BT139Report:
    report_version: str
    source_evidence: str
    run_id: str
    data_source: str
    is_demo: bool
    input_pack_gate_status: str
    input_completeness_status: str
    run_health_status: str
    broker_execution_mode: str
    live_trading_authorized: bool
    production_rule_change_allowed: bool
    sample_start_date: str | None
    sample_end_date: str | None
    symbol_count: int
    setup_count: int
    trade_count: int
    signal_day_count: int
    signal_day_cluster_count: int
    max_signal_day_cluster_size: int
    market_regime_coverage: dict[str, int]
    asset_group_coverage: dict[str, int]
    setup_coverage: dict[str, int]
    per_symbol_trade_count: dict[str, int]
    per_setup_trade_count: dict[str, int]
    per_regime_trade_count: dict[str, int]
    concentrated_signal_days: list[dict[str, Any]]
    outcome_path_summary: dict[str, int]
    missing_field_reasons: dict[str, list[str]]
    evidence_quality: str
    promotion_allowed: bool
    promotion_block_reasons: list[str]
    thresholds: dict[str, int]
    safety_notes: list[str]


def _load_evidence(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(payload, dict):
        raise SystemExit("BT139 source evidence must be a JSON object")

    if payload.get("data_source") != "real_data":
        raise SystemExit("BT139 requires data_source=real_data")

    if payload.get("is_demo") is not False:
        raise SystemExit("BT139 refuses demo evidence")

    if payload.get("input_pack_gate_status") != "PASSED":
        raise SystemExit("BT139 requires input_pack_gate_status=PASSED")

    if payload.get("run_health_status") != "OK":
        raise SystemExit("BT139 requires run_health_status=OK")

    if payload.get("broker_execution_mode") != "paper_only":
        raise SystemExit("BT139 requires broker_execution_mode=paper_only")

    if payload.get("live_trading_authorized") is not False:
        raise SystemExit("BT139 requires live_trading_authorized=false")

    if not isinstance(payload.get("results"), list):
        raise SystemExit("BT139 requires results list")

    return payload


def _asset_group(symbol: str, row: dict[str, Any]) -> str:
    explicit = row.get("asset_group")
    if explicit:
        return str(explicit)

    symbol = symbol.upper()

    if symbol in {"QQQ", "SPY", "IWM", "DIA"}:
        return "index_etf"

    if symbol in {"GLD", "SLV", "PPLT", "IAU"}:
        return "metals_etf"

    if symbol in {"NVDA", "MU", "AMD", "AVGO", "INTC"}:
        return "semiconductor_or_hardware"

    if symbol in {"MSFT", "AAPL", "META", "GOOGL", "AMZN", "NFLX"}:
        return "mega_cap_tech"

    return "unknown"


def _regime(row: dict[str, Any]) -> str:
    return str(row.get("market_regime") or row.get("regime") or "UNKNOWN")


def _outcome(row: dict[str, Any]) -> str:
    return str(row.get("outcome") or row.get("classification") or row.get("lifecycle_status") or "UNKNOWN").upper()


def _valid_date(value: Any) -> str | None:
    if value is None:
        return None

    text = str(value)[:10]

    try:
        date.fromisoformat(text)
    except ValueError:
        return None

    return text


def _count_missing_fields(rows: list[dict[str, Any]]) -> dict[str, list[str]]:
    missing: dict[str, list[str]] = {}

    for field in REQUIRED_ROW_FIELDS + OPTIONAL_ROW_FIELDS:
        missing_ids = [
            str(row.get("signal_id") or f"row_{index}")
            for index, row in enumerate(rows)
            if row.get(field) is None
        ]

        if missing_ids:
            missing[field] = missing_ids[:25]

    return missing


def _outcome_path_summary(rows: list[dict[str, Any]]) -> dict[str, int]:
    summary = {
        "evaluated_trade_count": 0,
        "real_no_trade_count": 0,
        "skipped_or_missing_input_count": 0,
        "unknown_outcome_count": 0,
    }

    for row in rows:
        outcome = _outcome(row)
        if outcome in EVALUATED_OUTCOMES:
            summary["evaluated_trade_count"] += 1
        elif outcome in REAL_NO_TRADE_OUTCOMES:
            summary["real_no_trade_count"] += 1
        elif outcome in MISSING_INPUT_OUTCOMES or row.get("missing_input_reason") or row.get("skip_reason"):
            summary["skipped_or_missing_input_count"] += 1
        else:
            summary["unknown_outcome_count"] += 1

    return summary


def _cluster_days(rows: list[dict[str, Any]]) -> tuple[int, int, list[dict[str, Any]]]:
    by_day: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for row in rows:
        signal_date = _valid_date(row.get("signal_date")) or "UNKNOWN_DATE"
        by_day[signal_date].append(row)

    concentrated: list[dict[str, Any]] = []
    max_cluster_size = 0

    for signal_date, day_rows in sorted(by_day.items()):
        cluster_size = len(day_rows)
        max_cluster_size = max(max_cluster_size, cluster_size)

        if cluster_size < 2:
            continue

        outcomes = Counter(_outcome(row) for row in day_rows)
        symbols = sorted({str(row.get("symbol") or "UNKNOWN") for row in day_rows})

        concentrated.append(
            {
                "signal_date": signal_date,
                "cluster_size": cluster_size,
                "symbols": symbols,
                "outcome_concentration": dict(sorted(outcomes.items())),
            }
        )

    return len(by_day), max_cluster_size, concentrated


def _classify_sample(
    *,
    trade_count: int,
    symbol_count: int,
    setup_count: int,
    signal_day_count: int,
    asset_group_count: int,
    thresholds: SampleThresholds,
) -> tuple[str, list[str]]:
    reasons: list[str] = []

    if trade_count >= thresholds.promotion_min_trade_count:
        candidate = PROMOTION_CANDIDATE_SAMPLE
    elif trade_count >= thresholds.reviewable_min_trade_count:
        candidate = REVIEWABLE_SAMPLE
    elif trade_count >= thresholds.early_min_trade_count:
        candidate = EARLY_DIRECTIONAL_SAMPLE
    else:
        candidate = INSUFFICIENT_SAMPLE
        reasons.append(
            f"trade_count={trade_count} below early_min_trade_count={thresholds.early_min_trade_count}"
        )

    if candidate in {REVIEWABLE_SAMPLE, PROMOTION_CANDIDATE_SAMPLE}:
        if symbol_count < thresholds.reviewable_min_symbol_count:
            candidate = EARLY_DIRECTIONAL_SAMPLE
            reasons.append(
                f"symbol_count={symbol_count} below reviewable_min_symbol_count={thresholds.reviewable_min_symbol_count}"
            )

        if setup_count < thresholds.reviewable_min_setup_count:
            candidate = EARLY_DIRECTIONAL_SAMPLE
            reasons.append(
                f"setup_count={setup_count} below reviewable_min_setup_count={thresholds.reviewable_min_setup_count}"
            )

        if signal_day_count < thresholds.reviewable_min_signal_day_count:
            candidate = EARLY_DIRECTIONAL_SAMPLE
            reasons.append(
                f"signal_day_count={signal_day_count} below reviewable_min_signal_day_count={thresholds.reviewable_min_signal_day_count}"
            )

        if asset_group_count < thresholds.reviewable_min_asset_group_count:
            candidate = EARLY_DIRECTIONAL_SAMPLE
            reasons.append(
                f"asset_group_count={asset_group_count} below reviewable_min_asset_group_count={thresholds.reviewable_min_asset_group_count}"
            )

    if candidate == PROMOTION_CANDIDATE_SAMPLE:
        if symbol_count < thresholds.promotion_min_symbol_count:
            candidate = REVIEWABLE_SAMPLE
            reasons.append(
                f"symbol_count={symbol_count} below promotion_min_symbol_count={thresholds.promotion_min_symbol_count}"
            )

        if setup_count < thresholds.promotion_min_setup_count:
            candidate = REVIEWABLE_SAMPLE
            reasons.append(
                f"setup_count={setup_count} below promotion_min_setup_count={thresholds.promotion_min_setup_count}"
            )

        if signal_day_count < thresholds.promotion_min_signal_day_count:
            candidate = REVIEWABLE_SAMPLE
            reasons.append(
                f"signal_day_count={signal_day_count} below promotion_min_signal_day_count={thresholds.promotion_min_signal_day_count}"
            )

        if asset_group_count < thresholds.promotion_min_asset_group_count:
            candidate = REVIEWABLE_SAMPLE
            reasons.append(
                f"asset_group_count={asset_group_count} below promotion_min_asset_group_count={thresholds.promotion_min_asset_group_count}"
            )

    if QUALITY_ORDER[candidate] < QUALITY_ORDER[REVIEWABLE_SAMPLE] and not reasons:
        reasons.append("sample quality below REVIEWABLE_SAMPLE")

    return candidate, reasons


def analyze(evidence_path: Path) -> BT139Report:
    evidence = _load_evidence(evidence_path)
    rows = list(evidence.get("results") or [])
    thresholds = SampleThresholds()

    dates = sorted(
        date_text
        for row in rows
        if (date_text := _valid_date(row.get("signal_date")))
    )

    symbols = [str(row.get("symbol") or "UNKNOWN") for row in rows]
    setups = [str(row.get("setup_type") or "UNKNOWN_SETUP") for row in rows]
    regimes = [_regime(row) for row in rows]
    asset_groups = [
        _asset_group(str(row.get("symbol") or "UNKNOWN"), row)
        for row in rows
    ]

    signal_day_count, max_cluster_size, concentrated_signal_days = _cluster_days(rows)

    symbol_counts = Counter(symbols)
    setup_counts = Counter(setups)
    regime_counts = Counter(regimes)
    asset_group_counts = Counter(asset_groups)

    evidence_quality, block_reasons = _classify_sample(
        trade_count=len(rows),
        symbol_count=len(symbol_counts),
        setup_count=len(setup_counts),
        signal_day_count=signal_day_count,
        asset_group_count=len(asset_group_counts),
        thresholds=thresholds,
    )

    promotion_allowed = QUALITY_ORDER[evidence_quality] >= QUALITY_ORDER[REVIEWABLE_SAMPLE]

    if not promotion_allowed and "sample quality below REVIEWABLE_SAMPLE" not in block_reasons:
        block_reasons.append("sample quality below REVIEWABLE_SAMPLE")

    return BT139Report(
        report_version="bt139.v2",
        source_evidence=str(evidence_path),
        run_id=str(evidence.get("run_id")),
        data_source=str(evidence.get("data_source")),
        is_demo=bool(evidence.get("is_demo")),
        input_pack_gate_status=str(evidence.get("input_pack_gate_status")),
        input_completeness_status=str(evidence.get("input_completeness_status")),
        run_health_status=str(evidence.get("run_health_status")),
        broker_execution_mode=str(evidence.get("broker_execution_mode")),
        live_trading_authorized=bool(evidence.get("live_trading_authorized")),
        production_rule_change_allowed=False,
        sample_start_date=dates[0] if dates else None,
        sample_end_date=dates[-1] if dates else None,
        symbol_count=len(symbol_counts),
        setup_count=len(setup_counts),
        trade_count=len(rows),
        signal_day_count=signal_day_count,
        signal_day_cluster_count=len(concentrated_signal_days),
        max_signal_day_cluster_size=max_cluster_size,
        market_regime_coverage=dict(sorted(regime_counts.items())),
        asset_group_coverage=dict(sorted(asset_group_counts.items())),
        setup_coverage=dict(sorted(setup_counts.items())),
        per_symbol_trade_count=dict(sorted(symbol_counts.items())),
        per_setup_trade_count=dict(sorted(setup_counts.items())),
        per_regime_trade_count=dict(sorted(regime_counts.items())),
        concentrated_signal_days=concentrated_signal_days,
        outcome_path_summary=_outcome_path_summary(rows),
        missing_field_reasons=_count_missing_fields(rows),
        evidence_quality=evidence_quality,
        promotion_allowed=promotion_allowed,
        promotion_block_reasons=block_reasons,
        thresholds=asdict(thresholds),
        safety_notes=[
            "BT139 is evidence-expansion only and does not modify production trading rules.",
            "No live trading authorization.",
            "broker_execution_mode remains paper_only.",
            "Downstream strategy variants remain blocked below REVIEWABLE_SAMPLE.",
            "Real no-trade paths are counted separately from skipped or missing-input paths.",
        ],
    )


def _markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]

    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")

    return lines


def render_markdown(report: BT139Report) -> str:
    lines = [
        "# BT139 BT131 Sample Expansion Report",
        "",
        "## Executive Summary",
        "",
        f"- Evidence quality: {report.evidence_quality}",
        f"- Promotion allowed: {report.promotion_allowed}",
        f"- Trade count: {report.trade_count}",
        f"- Symbol count: {report.symbol_count}",
        f"- Setup count: {report.setup_count}",
        f"- Signal-day count: {report.signal_day_count}",
        f"- Signal-day cluster count: {report.signal_day_cluster_count}",
        f"- Max cluster size: {report.max_signal_day_cluster_size}",
        f"- Sample window: {report.sample_start_date} to {report.sample_end_date}",
        f"- Broker execution mode: {report.broker_execution_mode}",
        f"- Live trading authorized: {report.live_trading_authorized}",
        f"- Production rule change allowed: {report.production_rule_change_allowed}",
        "",
        "## Promotion Block Reasons",
        "",
    ]

    if report.promotion_block_reasons:
        lines.extend(f"- {reason}" for reason in report.promotion_block_reasons)
    else:
        lines.append("- none")

    lines.extend(["", "## Outcome Path Summary", ""])
    lines.extend(
        _markdown_table(
            ["Path", "Count"],
            [[key, value] for key, value in report.outcome_path_summary.items()],
        )
    )

    lines.extend(["", "## Symbol Coverage", ""])
    lines.extend(
        _markdown_table(
            ["Symbol", "Trade Count"],
            [[key, value] for key, value in report.per_symbol_trade_count.items()],
        )
    )

    lines.extend(["", "## Setup Coverage", ""])
    lines.extend(
        _markdown_table(
            ["Setup", "Trade Count"],
            [[key, value] for key, value in report.per_setup_trade_count.items()],
        )
    )

    lines.extend(["", "## Asset Group Coverage", ""])
    lines.extend(
        _markdown_table(
            ["Asset Group", "Trade Count"],
            [[key, value] for key, value in report.asset_group_coverage.items()],
        )
    )

    lines.extend(["", "## Market Regime Coverage", ""])
    lines.extend(
        _markdown_table(
            ["Regime", "Trade Count"],
            [[key, value] for key, value in report.market_regime_coverage.items()],
        )
    )

    lines.extend(["", "## Concentrated Signal Days", ""])

    if report.concentrated_signal_days:
        lines.extend(
            _markdown_table(
                ["Signal Date", "Cluster Size", "Symbols", "Outcomes"],
                [
                    [
                        item["signal_date"],
                        item["cluster_size"],
                        ", ".join(item["symbols"]),
                        json.dumps(item["outcome_concentration"], sort_keys=True),
                    ]
                    for item in report.concentrated_signal_days
                ],
            )
        )
    else:
        lines.append("No concentrated signal days detected.")

    lines.extend(["", "## Missing Field Reasons", ""])

    if report.missing_field_reasons:
        lines.extend(
            _markdown_table(
                ["Field", "Example Missing Signal IDs"],
                [
                    [field, ", ".join(ids)]
                    for field, ids in report.missing_field_reasons.items()
                ],
            )
        )
    else:
        lines.append("No missing fields detected for BT139 tracked fields.")

    lines.extend(["", "## Safety Notes", ""])

    for note in report.safety_notes:
        lines.append(f"- {note}")

    return "\n".join(lines).rstrip() + "\n"


def write_report(report: BT139Report, *, output_json: Path, output_md: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)

    output_json.write_text(
        json.dumps(asdict(report), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    output_md.write_text(render_markdown(report), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build BT139 sample-expansion report from BT131 evidence"
    )
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = analyze(args.evidence)
    write_report(report, output_json=args.output_json, output_md=args.output_md)

    print(
        json.dumps(
            {
                "evidence_quality": report.evidence_quality,
                "promotion_allowed": report.promotion_allowed,
            },
            indent=2,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
