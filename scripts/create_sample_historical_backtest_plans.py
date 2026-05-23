#!/usr/bin/env python3
"""Create deterministic sample plans for the historical backtest workflow.

The generated plans are only for smoke validation of the P24/P24B pipeline.
They are not trading recommendations.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def _parse_symbols(value: str) -> list[str]:
    return [symbol.strip().upper() for symbol in value.split(",") if symbol.strip()]


def build_sample_plans(symbols: list[str], *, signal_date: str) -> list[dict]:
    plans: list[dict] = []
    for index, symbol in enumerate(symbols):
        entry = 100.0 + index
        plans.append(
            {
                "signal_id": f"sample_historical_{symbol}_{signal_date}",
                "symbol": symbol,
                "signal_date": signal_date,
                "action": "BUY_WATCH",
                "entry_trigger": entry,
                "stop_loss": round(entry * 0.95, 4),
                "target_1": round(entry * 1.08, 4),
                "target_2": round(entry * 1.16, 4),
                "entry_type": "sample_breakout",
                "setup_type": "workflow_smoke",
                "stop_model": "sample_percentage_stop",
                "exit_model": "sample_r_targets",
            }
        )
    return plans


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create deterministic sample historical backtest plans.")
    parser.add_argument("--symbols", default="SPY,QQQ,NVDA,AAPL,MSFT,AMD,TSLA,META,GOOGL,AMZN")
    parser.add_argument("--signal-date", default="2017-01-03")
    parser.add_argument("--output", default="reports/backtests/sample-historical-plans.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    symbols = _parse_symbols(args.symbols)
    if not symbols:
        raise SystemExit("No symbols provided")
    plans = build_sample_plans(symbols, signal_date=args.signal_date)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"plans": plans}, indent=2), encoding="utf-8")
    print(f"Wrote {len(plans)} sample historical plans to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
