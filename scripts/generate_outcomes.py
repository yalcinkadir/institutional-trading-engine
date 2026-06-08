#!/usr/bin/env python3
"""
Generate outcome reports from committed signal JSON files.

For each signal in reports/signals/YYYY-MM-DD-signals.json:
  1. Reads lifecycle status from the signal file.
  2. Separates TRIGGERED / EXPIRED / UNTRIGGERED / PENDING states.
  3. Fetches EOD price bars only for triggered/actionable signals.
  4. Calculates 1d, 5d, 20d performance from actual entry price when available.
  5. Writes outcome to reports/outcomes/YYYY-MM-DD-outcomes.{json,md}.

Important:
Untriggered or expired signals are not counted as trading losses. They are
tracked separately as signal-quality information.

Usage:
    python scripts/generate_outcomes.py [--days 7]
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.outcomes.outcome_summary import summarize_outcomes

REPORTS_DIR = Path("reports")
SIGNALS_DIR = REPORTS_DIR / "signals"
OUTCOMES_DIR = REPORTS_DIR / "outcomes"

WIN_THRESHOLD = 1.0    # % gain to classify as WIN
LOSS_THRESHOLD = -1.0  # % loss to classify as LOSS
TRIGGERED_STATUSES = {"TRIGGERED", "TARGET_1_HIT", "TARGET_2_HIT", "STOP_HIT"}
NON_TRADE_STATUSES = {"EXPIRED", "UNTRIGGERED"}


def extract_signals(text: str) -> list[str]:
    """
    Extract uppercase ticker-like symbols from free text.

    The function preserves first-seen order and removes duplicates.
    """
    if not text:
        return []

    matches = re.findall(r"\b[A-Z]{1,5}\b", text)
    return list(dict.fromkeys(matches))


def _pct(entry: float, exit_price: float) -> float:
    if entry <= 0:
        return 0.0
    return round((exit_price - entry) / entry * 100, 2)


def _safe_float(value: Any) -> float | None:
    if value in {None, "", "None"}:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _find_bar_index(bars: list[dict], target_date: str) -> int | None:
    """Find the index of the bar on or after target_date."""
    for i, bar in enumerate(bars):
        ts = bar.get("t", 0)
        bar_date = datetime.utcfromtimestamp(ts / 1000).strftime("%Y-%m-%d")
        if bar_date >= target_date:
            return i
    return None


def _signal_lifecycle_status(signal: dict) -> str:
    return str(signal.get("status") or "PENDING").upper()


def _signal_entry_date(signal_date: str, signal: dict) -> str:
    entry_at = str(signal.get("entry_triggered_at") or "")
    if entry_at:
        return entry_at[:10]
    return signal_date


def _entry_price(signal: dict) -> float:
    return (
        _safe_float(signal.get("entry_price"))
        or _safe_float(signal.get("entry_trigger"))
        or _safe_float(signal.get("close"))
        or 0.0
    )


def fetch_real_outcomes(
    signal_date: str,
    symbol: str,
    entry_price: float,
    client,
) -> dict:
    """
    Fetch real EOD outcomes for a triggered signal.

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
        result_1d = _pct(entry_price, close_1d)
    if close_5d:
        result_5d = _pct(entry_price, close_5d)
    if close_20d:
        result_20d = _pct(entry_price, close_20d)

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
        "performance_percent": result_5d if result_5d is not None else result_1d,
        "classification": classification,
    }


def load_signal_files(days: int = 7, signals_dir: Path | None = None) -> list[tuple[str, list[dict]]]:
    """
    Load signal JSON files from the last N days.

    Returns: list of (date_str, signals_list)
    """
    src = signals_dir or SIGNALS_DIR
    cutoff = (datetime.now(UTC).date() - timedelta(days=days)).isoformat()
    result = []

    for json_file in sorted(src.glob("*-signals.json")):
        if json_file.stem == "latest-signals":
            continue
        date_str = json_file.stem.replace("-signals", "")
        if date_str < cutoff:
            continue
        try:
            payload = json.loads(json_file.read_text(encoding="utf-8"))
            signals = payload.get("signals", [])
            actionable = [s for s in signals if s.get("action") == "BUY_WATCH"]
            if actionable:
                result.append((date_str, actionable))
        except Exception:
            continue

    return result


def _outcome_for_non_trade_signal(date_str: str, sig: dict, lifecycle_status: str) -> dict:
    return {
        "signal_date": date_str,
        "symbol": sig.get("symbol"),
        "action": sig.get("action"),
        "setup_type": sig.get("setup_type"),
        "entry_type": sig.get("entry_type"),
        "entry_trigger": sig.get("entry_trigger"),
        "entry_price": sig.get("entry_price"),
        "close_at_signal": sig.get("close"),
        "market_regime": sig.get("market_regime"),
        "lifecycle_status": lifecycle_status,
        "result_1d": None,
        "result_5d": None,
        "result_20d": None,
        "performance_percent": None,
        "classification": lifecycle_status,
    }


def write_outcome_reports(outcomes: list[dict], date_str: str, *, outcomes_dir: Path | None = None) -> None:
    out = outcomes_dir or OUTCOMES_DIR
    out.mkdir(parents=True, exist_ok=True)

    evaluated = [
        outcome for outcome in outcomes
        if outcome.get("classification") in {"WIN", "LOSS", "NEUTRAL"}
    ]
    summary = summarize_outcomes(evaluated)

    lifecycle_counts: dict[str, int] = {}
    for outcome in outcomes:
        status = str(outcome.get("lifecycle_status") or outcome.get("classification") or "UNKNOWN")
        lifecycle_counts[status] = lifecycle_counts.get(status, 0) + 1

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
        f"- Evaluated Trades: {summary['total_outcomes']}",
        f"- Pending / Non-trade Signals: {len(outcomes) - summary['total_outcomes']}",
        f"- Win Rate: {summary['win_rate']}%",
        f"- Average Performance (5d): {summary['average_performance']}%",
        "",
        "## Lifecycle Counts",
        "",
    ]

    for status, count in sorted(lifecycle_counts.items()):
        lines.append(f"- {status}: {count}")

    lines += ["", "## Signal Outcomes", ""]

    for outcome in outcomes:
        status = outcome["classification"]
        lifecycle = outcome.get("lifecycle_status", status)
        r1 = f"{outcome['result_1d']:+.2f}%" if outcome["result_1d"] is not None else "n/a"
        r5 = f"{outcome['result_5d']:+.2f}%" if outcome["result_5d"] is not None else "n/a"
        r20 = f"{outcome['result_20d']:+.2f}%" if outcome["result_20d"] is not None else "n/a"
        lines.append(
            f"- **{outcome['symbol']}** [{status} / {lifecycle}] "
            f"Entry: {outcome.get('entry_trigger', 'N/A')} | "
            f"1d: {r1} | 5d: {r5} | 20d: {r20}"
        )

    markdown = "\n".join(lines)

    dated_md = out / f"{date_str}-outcomes.md"
    dated_json = out / f"{date_str}-outcomes.json"
    latest_md = out / "latest-outcomes.md"
    history_json = out / "outcome-history.json"

    dated_md.write_text(markdown, encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")
    dated_json.write_text(json.dumps(outcomes, indent=2), encoding="utf-8")

    history: list[dict] = []
    if history_json.exists():
        try:
            history = json.loads(history_json.read_text(encoding="utf-8"))
        except Exception:
            history = []

    history = [h for h in history if h.get("signal_date") != date_str]
    history.append({"signal_date": date_str, "outcomes": outcomes})
    history = sorted(history, key=lambda x: x.get("signal_date", ""), reverse=True)[:90]
    history_json.write_text(json.dumps(history, indent=2), encoding="utf-8")


def _write_run_manifest(
    *,
    run_status: str,
    days_evaluated: int,
    signal_batch_count: int,
    total_input_signals: int,
    total_evaluated: int,
    skip_reasons: list[str],
    outcomes_dir: Path | None = None,
) -> Path:
    """Write a run-level manifest so CI can distinguish empty/blocked runs from no-run."""
    out = outcomes_dir or OUTCOMES_DIR
    out.mkdir(parents=True, exist_ok=True)
    manifest = {
        "run_status": run_status,
        "run_timestamp_utc": datetime.now(UTC).isoformat(),
        "days_evaluated": days_evaluated,
        "signal_batch_count": signal_batch_count,
        "total_input_signals": total_input_signals,
        "total_evaluated": total_evaluated,
        "skip_reasons": skip_reasons,
    }
    path = out / "outcome-run-manifest.json"
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return path


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate real outcome reports from committed signal files."
    )
    parser.add_argument("--days", type=int, default=7,
                        help="Number of past days to evaluate signals for.")
    parser.add_argument("--signals-dir", type=Path, default=None,
                        help="Override signals input directory (default: reports/signals).")
    parser.add_argument("--outcomes-dir", type=Path, default=None,
                        help="Override outcomes output directory (default: reports/outcomes).")
    args = parser.parse_args()

    signals_dir = args.signals_dir or SIGNALS_DIR
    outcomes_dir = args.outcomes_dir or OUTCOMES_DIR

    api_key = os.getenv("POLYGON_API_KEY")
    if not api_key:
        print("WARNING: POLYGON_API_KEY not set. Cannot fetch real outcomes.")
        print("Outcome files will contain PENDING status for triggered signals.")

    if not signals_dir.exists():
        print(f"BLOCKED_MISSING_INPUTS: signals directory not found: {signals_dir}")
        _write_run_manifest(
            run_status="BLOCKED_MISSING_INPUTS",
            days_evaluated=args.days,
            signal_batch_count=0,
            total_input_signals=0,
            total_evaluated=0,
            skip_reasons=["signals_directory_missing"],
            outcomes_dir=outcomes_dir,
        )
        return 1

    signal_batches = load_signal_files(days=args.days, signals_dir=signals_dir)

    if not signal_batches:
        print(f"NO_ELIGIBLE_SIGNALS: no signal files found in the last {args.days} days.")
        _write_run_manifest(
            run_status="NO_ELIGIBLE_SIGNALS",
            days_evaluated=args.days,
            signal_batch_count=0,
            total_input_signals=0,
            total_evaluated=0,
            skip_reasons=["no_signal_files_in_window"],
            outcomes_dir=outcomes_dir,
        )
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
            lifecycle_status = _signal_lifecycle_status(sig)
            entry_price = _entry_price(sig)
            entry_date = _signal_entry_date(date_str, sig)

            if lifecycle_status in NON_TRADE_STATUSES:
                outcomes.append(_outcome_for_non_trade_signal(date_str, sig, lifecycle_status))
                total_processed += 1
                continue

            if lifecycle_status == "PENDING":
                outcomes.append(_outcome_for_non_trade_signal(date_str, sig, "PENDING"))
                total_processed += 1
                continue

            if client and entry_price > 0 and lifecycle_status in TRIGGERED_STATUSES:
                result = fetch_real_outcomes(entry_date, symbol, float(entry_price), client)
            else:
                result = {
                    "result_1d": None,
                    "result_5d": None,
                    "result_20d": None,
                    "performance_percent": None,
                    "classification": "PENDING",
                    "error": "no_api_key_or_no_entry_price_or_not_triggered",
                }

            outcomes.append({
                "signal_date": date_str,
                "symbol": symbol,
                "action": sig.get("action"),
                "setup_type": sig.get("setup_type"),
                "entry_type": sig.get("entry_type"),
                "entry_trigger": sig.get("entry_trigger"),
                "entry_price": entry_price,
                "close_at_signal": sig.get("close"),
                "market_regime": sig.get("market_regime"),
                "lifecycle_status": lifecycle_status,
                **result,
            })
            total_processed += 1

        write_outcome_reports(outcomes, date_str, outcomes_dir=outcomes_dir)
        print(f"  → outcomes written for {date_str}")

    total_input = sum(len(sigs) for _, sigs in signal_batches)
    print(f"Done. Processed {total_processed} signals across {len(signal_batches)} days.")
    _write_run_manifest(
        run_status="OK",
        days_evaluated=args.days,
        signal_batch_count=len(signal_batches),
        total_input_signals=total_input,
        total_evaluated=total_processed,
        skip_reasons=[],
        outcomes_dir=outcomes_dir,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
