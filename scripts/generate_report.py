#!/usr/bin/env python3
"""Generate Institutional Trading Engine reports + signals.

Usage:
    python scripts/generate_report.py --type premarket --output reports/premarket-report.md
    python scripts/generate_report.py --type intraday --output reports/intraday-report.md
    python scripts/generate_report.py --type postmarket --output reports/postmarket-report.md
    python scripts/generate_report.py --type weekly --output reports/weekly-report.md

After each premarket/intraday/postmarket report, a signal JSON and Markdown file
is written to reports/signals/YYYY-MM-DD-signals.{json,md}.
"""

from __future__ import annotations

import argparse
import sys
from datetime import UTC, datetime
from pathlib import Path

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

    market_regime = build_market_regime_summary(report_type)
    screener = build_screener_snapshot(report_type)
    cross_asset = build_cross_asset_report()
    decision_report = build_decision_report(
        market_regime=market_regime,
        screener=screener,
    )

    payload = {
        "report_type": report_type,
        "market_regime": market_regime,
        "cross_asset": cross_asset,
        "screener": screener,
        "decision_report": decision_report,
    }

    return format_report(payload), {
        "decision_report": decision_report,
        "market_regime": market_regime.get("regime", "Unknown"),
    }


def generate_signals(decision_payload: dict) -> None:
    """
    Generate signal JSON and Markdown from the decision report.
    Non-fatal: if signal generation fails, the report is still saved.
    """
    try:
        from src.signals.signal_generator import build_signals, save_signals

        decision_report = decision_payload["decision_report"]
        market_regime = decision_payload["market_regime"]
        date_str = datetime.now(UTC).strftime("%Y-%m-%d")

        # Try to load scanner metrics for Entry/Stop/Target levels
        scanner_metrics_map: dict | None = None
        try:
            from src.scanner import build_symbol_metrics, get_daily_bars, calculate_20d_return
            import time

            benchmark_returns: dict = {}
            for bench in ["QQQ", "SPY", "GLD"]:
                df = get_daily_bars(bench)
                if df is not None and not df.empty:
                    benchmark_returns[bench] = calculate_20d_return(df["close"])
                time.sleep(2)

            # Only fetch symbols in the watchlist to stay within rate limits
            watchlist = decision_report.get("decisions", [])
            watchlist_symbols = [d["symbol"] for d in watchlist]

            scanner_metrics_map = {}
            for sym in watchlist_symbols:
                try:
                    metrics = build_symbol_metrics(sym, benchmark_returns)
                    scanner_metrics_map[sym] = metrics
                    time.sleep(2)
                except Exception:
                    pass

        except Exception:
            # Scanner metrics unavailable — signals will be created without levels
            # unless the signal generator can derive them from available fields.
            pass

        signals = build_signals(
            decision_report=decision_report,
            scanner_metrics_map=scanner_metrics_map,
            market_regime=market_regime,
        )

        json_path, md_path = save_signals(signals, date_str=date_str)
        print(f"Signals written: {json_path}, {md_path}")
        print(
            f"  {sum(1 for s in signals if s.action == 'BUY_WATCH')} actionable, "
            f"{sum(1 for s in signals if s.action != 'BUY_WATCH')} no-trade"
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

    # Generate signals for market reports. Weekly is strategic-only.
    if args.type in {"premarket", "intraday", "postmarket"} and decision_payload is not None:
        generate_signals(decision_payload)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
