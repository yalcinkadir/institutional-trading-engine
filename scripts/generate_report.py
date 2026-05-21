#!/usr/bin/env python3
"""Generate Institutional Trading Engine reports + signals.

Usage:
    python scripts/generate_report.py --type premarket --output reports/premarket-report.md
    python scripts/generate_report.py --type intraday --output reports/intraday-report.md
    python scripts/generate_report.py --type postmarket --output reports/postmarket-report.md
    python scripts/generate_report.py --type weekly --output reports/weekly-report.md

After each premarket/intraday/postmarket report, a signal JSON and Markdown file
is written to reports/signals/YYYY-MM-DD-signals.{json,md}.

Signal levels are also merged back into the decision payload before rendering,
so Entry/Stop/Target/R:R, quality reasons and signal_id are visible to downstream report logic.

Expectation-based scoring adjustments are persisted to:

data/scoring_adjustment_history.json
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.reporting.cross_asset_report import build_cross_asset_report
from src.reporting.decision_report import build_decision_report
from src.reporting.market_regime import build_market_regime_summary
from src.reporting.report_formatter import format_report
from src.reporting.screener_engine import build_screener_snapshot
from src.reporting.weekly_summary import build_weekly_summary

VALID_REPORT_TYPES = {"premarket", "intraday", "postmarket", "weekly"}
MARKET_REPORT_TYPES = {"premarket", "intraday", "postmarket"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a market report.")
    parser.add_argument(
        "--type",
        required=True,
        choices=sorted(VALID_REPORT_TYPES),
        help="Report type to generate.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional output markdown path. Printed to stdout if omitted.",
    )
    return parser.parse_args()


def _load_scanner_metrics(decision_report: dict) -> dict[str, Any] | None:
    """
    Best-effort scanner metric loading for Entry/Stop/Target levels.

    This is intentionally non-fatal. If scanner metrics are unavailable, the
    report still renders and signal generation falls back to no explicit levels.
    """
    try:
        from src.scanner import build_symbol_metrics, calculate_20d_return, get_daily_bars
        import time

        benchmark_returns: dict[str, Any] = {}
        for bench in ["QQQ", "SPY", "GLD"]:
            df = get_daily_bars(bench)
            if df is not None and not df.empty:
                benchmark_returns[bench] = calculate_20d_return(df["close"])
            time.sleep(2)

        watchlist_symbols = [
            item["symbol"]
            for item in decision_report.get("decisions", [])
            if item.get("symbol")
        ]

        scanner_metrics_map: dict[str, Any] = {}
        for symbol in watchlist_symbols:
            try:
                scanner_metrics_map[symbol] = build_symbol_metrics(
                    symbol,
                    benchmark_returns,
                )
                time.sleep(2)
            except Exception:
                scanner_metrics_map[symbol] = None

        return scanner_metrics_map

    except Exception:
        return None


def _merge_signal_levels_into_decisions(
    decision_report: dict,
    signals: list[Any],
) -> None:
    """
    Merge generated signal levels into decision_report in-place.

    report_formatter.py already knows how to render entry_trigger, stop_loss,
    target_1, target_2 and risk_reward from decision items. This function makes
    those fields and the quality explanations available before the main report
    is formatted.
    """
    signals_by_symbol = {signal.symbol: signal for signal in signals}

    for item in decision_report.get("decisions", []):
        signal = signals_by_symbol.get(item.get("symbol"))
        if not signal:
            continue

        signal_payload = asdict(signal)
        for key in (
            "signal_id",
            "action",
            "close",
            "entry_trigger",
            "entry_type",
            "entry_reason",
            "stop_loss",
            "stop_model",
            "stop_reason",
            "target_1",
            "target_2",
            "risk_reward",
            "atr_pct",
            "valid_until",
        ):
            item[key] = signal_payload.get(key)


def _build_market_payload(report_type: str) -> tuple[dict, dict | None]:
    market_regime = build_market_regime_summary(report_type)
    screener = build_screener_snapshot(report_type)
    cross_asset = build_cross_asset_report()
    decision_report = build_decision_report(
        market_regime=market_regime,
        screener=screener,
    )

    decision_payload = {
        "decision_report": decision_report,
        "market_regime": market_regime.get("regime", "Unknown"),
    }

    scanner_metrics_map = _load_scanner_metrics(decision_report)

    try:
        from src.signals.signal_generator import build_signals

        signals = build_signals(
            decision_report=decision_report,
            scanner_metrics_map=scanner_metrics_map,
            market_regime=decision_payload["market_regime"],
        )
        _merge_signal_levels_into_decisions(decision_report, signals)
        decision_payload["signals"] = signals
    except Exception as exc:
        print(f"WARNING: Signal level preparation failed (non-fatal): {type(exc).__name__}: {exc}")
        decision_payload["signals"] = []

    payload = {
        "report_type": report_type,
        "market_regime": market_regime,
        "cross_asset": cross_asset,
        "screener": screener,
        "decision_report": decision_report,
    }

    return payload, decision_payload


def build_report(report_type: str) -> tuple[str, dict | None]:
    """
    Build report content.

    Returns: (report_markdown, decision_payload | None)
    The decision_payload is used to generate signal files.
    """
    if report_type == "weekly":
        payload = {
            "report_type": report_type,
            "weekly_summary": build_weekly_summary(),
        }
        return format_report(payload), None

    payload, decision_payload = _build_market_payload(report_type)
    return format_report(payload), decision_payload


def persist_scoring_adjustments(report_type: str, decision_payload: dict) -> None:
    """Persist expectancy-based scoring adjustments for auditability."""
    try:
        from src.scoring.adjustment_history import append_scoring_adjustments

        decision_report = decision_payload["decision_report"]
        run_id = f"{report_type}-{datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')}"
        path = append_scoring_adjustments(
            decision_report=decision_report,
            report_type=report_type,
            run_id=run_id,
        )
        print(f"Scoring adjustment history updated: {path}")
    except Exception as exc:
        print(f"WARNING: Scoring adjustment history failed (non-fatal): {type(exc).__name__}: {exc}")


def generate_signals(decision_payload: dict) -> None:
    """
    Save signal JSON and Markdown from the decision payload.
    Non-fatal: if signal generation fails, the report is still saved.
    """
    try:
        from src.signals.signal_generator import build_signals, save_signals

        decision_report = decision_payload["decision_report"]
        market_regime = decision_payload["market_regime"]
        date_str = datetime.now(UTC).strftime("%Y-%m-%d")

        signals = decision_payload.get("signals")
        if signals is None:
            signals = build_signals(
                decision_report=decision_report,
                scanner_metrics_map=None,
                market_regime=market_regime,
            )

        json_path, md_path = save_signals(signals, date_str=date_str)
        print(f"Signals written: {json_path}, {md_path}")
        print(
            f"  {sum(1 for signal in signals if signal.action == 'BUY_WATCH')} actionable, "
            f"{sum(1 for signal in signals if signal.action != 'BUY_WATCH')} no-trade"
        )

    except Exception as exc:
        print(f"WARNING: Signal generation failed (non-fatal): {type(exc).__name__}: {exc}")


def main() -> int:
    args = parse_args()
    report, decision_payload = build_report(args.type)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        print(f"Report written to {output_path}")
    else:
        print(report)

    if args.type in MARKET_REPORT_TYPES and decision_payload is not None:
        persist_scoring_adjustments(args.type, decision_payload)
        generate_signals(decision_payload)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())