"""Generate deterministic historical trade plans from daily OHLCV bars.

The generator creates simple pullback-continuation BUY_WATCH plans from existing
historical bar CSV files. It is intentionally deterministic and conservative:
plans are generated only after enough history exists, with stop and targets based
on recent volatility.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean
from typing import Any


@dataclass(frozen=True)
class GeneratedTradePlan:
    signal_id: str
    symbol: str
    signal_date: str
    action: str
    entry_trigger: float
    stop_loss: float
    target_1: float
    target_2: float
    valid_until: str
    entry_type: str
    setup_type: str
    stop_model: str
    exit_model: str


@dataclass(frozen=True)
class GenerationSummary:
    bars_root: str
    output: str
    scanned_symbols: int
    symbols_with_plans: int
    generated_plans: int
    max_plans: int
    max_plans_per_symbol: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate historical trade plans from OHLCV bars")
    parser.add_argument("--bars-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("data/trade_plans/historical_trade_plans.json"))
    parser.add_argument("--min-history", type=int, default=60)
    parser.add_argument("--lookahead-days", type=int, default=20)
    parser.add_argument("--max-plans", type=int, default=5000)
    parser.add_argument("--max-plans-per-symbol", type=int, default=3)
    parser.add_argument("--min-dollar-volume", type=float, default=1_000_000.0)
    return parser.parse_args()


def _float(value: Any) -> float | None:
    try:
        converted = float(value)
        return converted if converted == converted else None
    except (TypeError, ValueError):
        return None


def load_bars(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    clean: list[dict[str, Any]] = []
    for row in rows:
        parsed = {
            "date": str(row.get("date") or "")[:10],
            "open": _float(row.get("open")),
            "high": _float(row.get("high")),
            "low": _float(row.get("low")),
            "close": _float(row.get("close")),
            "volume": _float(row.get("volume")),
        }
        if parsed["date"] and all(parsed[key] is not None for key in ["open", "high", "low", "close", "volume"]):
            clean.append(parsed)
    return sorted(clean, key=lambda item: item["date"])


def _sma(values: list[float]) -> float:
    return round(mean(values), 4)


def _atr14(rows: list[dict[str, Any]]) -> float:
    ranges = [float(row["high"]) - float(row["low"]) for row in rows[-14:]]
    return round(mean(ranges), 4) if ranges else 0.0


def _signal_id(symbol: str, signal_date: str, entry: float, stop: float, target_1: float) -> str:
    seed = f"{symbol}|{signal_date}|{entry:.4f}|{stop:.4f}|{target_1:.4f}"
    digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()[:16]
    return f"hist_{symbol}_{digest}"


def build_plan(symbol: str, rows: list[dict[str, Any]], index: int, *, lookahead_days: int) -> GeneratedTradePlan | None:
    history = rows[: index + 1]
    current = history[-1]
    close = float(current["close"])
    volume = float(current["volume"])
    if close <= 0 or volume <= 0:
        return None
    sma20 = _sma([float(row["close"]) for row in history[-20:]])
    sma50 = _sma([float(row["close"]) for row in history[-50:]])
    recent_low = min(float(row["low"]) for row in history[-10:])
    atr = _atr14(history)
    dollar_volume = close * volume
    if close <= sma50:
        return None
    if recent_low > sma20:
        return None
    if dollar_volume < 1_000_000:
        return None
    entry = round(close * 1.01, 4)
    risk = max(round(atr * 1.25, 4), round(close * 0.02, 4))
    stop = round(entry - risk, 4)
    target_1 = round(entry + 2 * risk, 4)
    target_2 = round(entry + 3 * risk, 4)
    if not stop < entry < target_1 < target_2:
        return None
    valid_index = min(index + lookahead_days, len(rows) - 1)
    return GeneratedTradePlan(
        signal_id=_signal_id(symbol, str(current["date"]), entry, stop, target_1),
        symbol=symbol,
        signal_date=str(current["date"]),
        action="BUY_WATCH",
        entry_trigger=entry,
        stop_loss=stop,
        target_1=target_1,
        target_2=target_2,
        valid_until=str(rows[valid_index]["date"]),
        entry_type="breakout_trigger",
        setup_type="historical_pullback_continuation",
        stop_model="atr_1_25_or_2pct",
        exit_model="target_2_or_stop",
    )


def generate_for_symbol(path: Path, *, min_history: int, lookahead_days: int, max_plans_per_symbol: int, min_dollar_volume: float) -> list[GeneratedTradePlan]:
    symbol = path.stem.upper()
    rows = load_bars(path)
    if len(rows) <= min_history + lookahead_days:
        return []
    plans: list[GeneratedTradePlan] = []
    step = max(1, (len(rows) - min_history - lookahead_days) // max(max_plans_per_symbol * 3, 1))
    for index in range(min_history, len(rows) - lookahead_days, step):
        plan = build_plan(symbol, rows, index, lookahead_days=lookahead_days)
        if plan is None:
            continue
        if plan.entry_trigger * float(rows[index]["volume"]) < min_dollar_volume:
            continue
        plans.append(plan)
        if len(plans) >= max_plans_per_symbol:
            break
    return plans


def generate_plans(args: argparse.Namespace) -> tuple[list[GeneratedTradePlan], GenerationSummary]:
    files = sorted(args.bars_root.glob("*.csv"))
    plans: list[GeneratedTradePlan] = []
    symbols_with_plans = 0
    for path in files:
        symbol_plans = generate_for_symbol(
            path,
            min_history=args.min_history,
            lookahead_days=args.lookahead_days,
            max_plans_per_symbol=args.max_plans_per_symbol,
            min_dollar_volume=args.min_dollar_volume,
        )
        if symbol_plans:
            symbols_with_plans += 1
        plans.extend(symbol_plans)
        if len(plans) >= args.max_plans:
            plans = plans[: args.max_plans]
            break
    summary = GenerationSummary(
        bars_root=str(args.bars_root),
        output=str(args.output),
        scanned_symbols=len(files),
        symbols_with_plans=symbols_with_plans,
        generated_plans=len(plans),
        max_plans=args.max_plans,
        max_plans_per_symbol=args.max_plans_per_symbol,
    )
    return plans, summary


def write_output(plans: list[GeneratedTradePlan], summary: GenerationSummary, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "metadata": asdict(summary),
        "plans": [asdict(plan) for plan in plans],
    }
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    args = parse_args()
    plans, summary = generate_plans(args)
    write_output(plans, summary, args.output)
    print(json.dumps(asdict(summary), indent=2))
    if not plans:
        raise SystemExit("No historical trade plans generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
