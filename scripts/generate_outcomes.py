#!/usr/bin/env python3
"""
Generate outcome reports from committed signal JSON files.

Replaces the previous mock-based implementation with real Polygon EOD lookbacks.

For each signal in reports/signals/YYYY-MM-DD-signals.json:
  1. Fetches EOD price bars for the symbol.
  2. Finds the bar on signal date (= price_at_signal).
  3. Calculates 1d, 5d, 20d performance vs signal close.
  4. Classifies: WIN (>+1%), LOSS (<-1%), NEUTRAL.
  5. Writes outcome to reports/outcomes/YYYY-MM-DD-outcomes.{json,md}.

Usage:
    python scripts/generate_outcomes.py [--days 7]
"""

from __future__ import annotations

import json
import os
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.outcomes.outcome_summary import summarize_outcomes

REPORTS_DIR = Path("reports")
SIGNALS_DIR = REPORTS_DIR / "signals"
OUTCOMES_DIR = REPORTS_DIR / "outcomes"

WIN_THRESHOLD = 1.0    # % gain to classify as WIN
LOSS_THRESHOLD = -1.0  # % loss to classify as LOSS


def _pct(entry: float, exit_price: float) -> float:
    if entry <= 0:
        return 0.0
    return round((exit_price - entry) / entry * 100, 2)


def _find_bar_index(bars: list[dict], target_date: str) -> int | None:
    """Find the index of the bar on or after target_date."""
    for i, bar in enumerate(bars):
        # Polygon returns timestamps in ms
        ts = bar.get("t", 0)
        bar_date = datetime.utcfromtimestamp(ts / 1000).strftime("%Y-%m-%d")
        if bar_date >= target_date:
            return i
    return None


def fetch_real_outcomes(
    signal_date: str,
    symbol: str,
    close_at_signal: float,
    client,
) -> dict:
    """
    Fetch real EOD outcomes for a signal.

    Returns dict with result_1d, result_5d, result_20d, classification.
    """
    try:
        bars = client.get_daily_bars(symbol, days=30)
    except Exception as exc:
        return {
            "result_1d": None,
            "result_5d": None,
            "result_20d": None,
            "classification": "PENDING",
            "error": str(exc),
        }

    if not bars:
        return {
            "result_1d": None,
            "result_5d": None,
            "result_20d": None,
            "classification": "PENDING",
            "error": "no_bars_returned",
        }

    idx = _find_bar_index(bars, signal_date)
    if idx is None:
        return {
            "result_1d": None,
            "result_5d": None,
            "result_20d": None,
            "classification": "PENDING",
            "error": "signal_date_not_found_in_bars",
        }

    def _close_at(offset: int) -> float | None:
        target_idx = idx + offset
        if target_idx < len(bars):
            return float(bars[target_idx].get("c", 0))
        return None

    result_1d = None
    result_5d = None
    result_20d = None

    close_1d = _close_at(1)
    close_5d = _close_at(5)
    close_20d = _close_at(20)

    if close_1d:
        result_1d = _pct(close_at_signal, close_1d)
    if close_5d:
        result_5d = _pct(close_at_signal, close_5d)
    if close_20d:
        result_20d = _pct(close_at_signal, close_20d)

    # Primary classification on 5d result (first meaningful outcome window)
    primary = result_5d if result_5d is not None else result_1d
    if primary is None:
        classification = "PENDING"
    elif primary >= WIN_THRESHOLD:
        classification = "WIN"
    elif primary <= LOSS_THRESHOLD:
        classification = "LOSS"
    else:
        classification = "NEUTRAL"

    return {
        "result_1d": result_1d,
        "result_5d": result_5d,
        "result_20d": result_20d,
        "classification": classification,
    }


def load_signal_files(days: int = 7) -> list[tuple[str, list[dict]]]:
    """
    Load signal JSON files from the last N days.

    Returns: list of (date_str, signals_list)
    """
    cutoff = (datetime.now(UTC).date() - timedelta(days=days)).isoformat()
    result = []

    for json_file in sorted(SIGNALS_DIR.glob("*-signals.json")):
        # Skip latest-signals.json
        if json_file.stem == "latest-signals":
            continue
        date_str = json_file.stem.replace("-signals", "")
        if date_str < cutoff:
            continue
        try:
            payload = json.loads(json_file.read_text(encoding="utf-8"))
            signals = payload.get("signals", [])
            # Only actionable signals have outcomes to track
            actionable = [s for s in signals if s.get("action") == "BUY_WATCH"]
            if actionable:
                result.append((date_str, actionable))
        except Exception:
            continue

    return result


def write_outcome_reports(outcomes: list[dict], date_str: str) -> None:
    OUTCOMES_DIR.mkdir(parents=True, exist_ok=True)

    summary = summarize_outcomes(
        [o for o in outcomes if o["classification"] != "PENDING"]
    )

    now_iso = datetime.now(UTC).isoformat()

    lines = [
        "# Institutional Outcome Report",
        "",
        f"Generated: {now_iso}",
        f"Signal date: {date_str}",
        "",
        "## Summary",
        "",
        f"- Total Signals: {len(outcomes)}",
        f"- Evaluated: {summary['total_outcomes']}",
        f"- Pending: {len(outcomes) - summary['total_outcomes']}",
        f"- Win Rate: {summary['win_rate']}%",
        f"- Average Performance (5d): {summary['average_performance']}%",
        "",
        "## Signal Outcomes",
        "",
    ]

    for o in outcomes:
        status = o["classification"]
        r1 = f"{o['result_1d']:+.2f}%" if o["result_1d"] is not None else "pending"
        r5 = f"{o['result_5d']:+.2f}%" if o["result_5d"] is not None else "pending"
        r20 = f"{o['result_20d']:+.2f}%" if o["result_20d"] is not None else "pending"
        lines.append(
            f"- **{o['symbol']}** [{status}] "
            f"Entry: {o.get('entry_trigger', 'N/A')} | "
            f"1d: {r1} | 5d: {r5} | 20d: {r20}"
        )

    markdown = "\n".join(lines)

    dated_md = OUTCOMES_DIR / f"{date_str}-outcomes.md"
    dated_json = OUTCOMES_DIR / f"{date_str}-outcomes.json"
    latest_md = OUTCOMES_DIR / "latest-outcomes.md"
    history_json = OUTCOMES_DIR / "outcome-history.json"

    dated_md.write_text(markdown, encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")
    dated_json.write_text(json.dumps(outcomes, indent=2), encoding="utf-8")

    # Append to rolling history
    history: list[dict] = []
    if history_json.exists():
        try:
            history = json.loads(history_json.read_text(encoding="utf-8"))
        except Exception:
            history = []

    # Remove existing entries for this date to avoid duplicates
    history = [h for h in history if h.get("signal_date") != date_str]
    history.append({"signal_date": date_str, "outcomes": outcomes})

    # Keep last 90 days
    history = sorted(history, key=lambda x: x.get("signal_date", ""), reverse=True)[:90]
    history_json.write_text(json.dumps(history, indent=2), encoding="utf-8")


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate real outcome reports from committed signal files."
    )
    parser.add_argument("--days", type=int, default=7,
                        help="Number of past days to evaluate signals for.")
    args = parser.parse_args()

    api_key = os.getenv("POLYGON_API_KEY")
    if not api_key:
        print("WARNING: POLYGON_API_KEY not set. Cannot fetch real outcomes.")
        print("Outcome files will contain PENDING status for all signals.")

    signal_batches = load_signal_files(days=args.days)

    if not signal_batches:
        print(f"No signal files found in the last {args.days} days.")
        return 0

    client = None
    if api_key:
        from src.data.polygon_client import PolygonClient
        client = PolygonClient(api_key=api_key)

    total_processed = 0

    for date_str, signals in signal_batches:
        print(f"Processing signals for {date_str} ({len(signals)} actionable)...")
        outcomes = []

        for sig in signals:
            symbol = sig["symbol"]
            close = sig.get("close") or 0.0

            if client and close > 0:
                result = fetch_real_outcomes(date_str, symbol, float(close), client)
            else:
                result = {
                    "result_1d": None,
                    "result_5d": None,
                    "result_20d": None,
                    "classification": "PENDING",
                    "error": "no_api_key_or_no_close",
                }

            outcomes.append({
                "signal_date": date_str,
                "symbol": symbol,
                "action": sig.get("action"),
                "setup_type": sig.get("setup_type"),
                "entry_trigger": sig.get("entry_trigger"),
                "close_at_signal": close,
                "market_regime": sig.get("market_regime"),
                **result,
            })
            total_processed += 1

        write_outcome_reports(outcomes, date_str)
        print(f"  → outcomes written for {date_str}")

    print(f"Done. Processed {total_processed} signals across {len(signal_batches)} days.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
