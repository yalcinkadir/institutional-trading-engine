from __future__ import annotations

import argparse
from datetime import date, timedelta
from pathlib import Path

from scripts.generate_historical_trade_plans import generate_plans


def _write_bars(path: Path, *, days: int = 110) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = ["date,open,high,low,close,volume"]
    close = 100.0
    start = date(2024, 1, 1)
    for index in range(days):
        current_date = start + timedelta(days=index)
        if index % 15 == 0:
            close *= 0.97
        else:
            close *= 1.003
        open_price = close * 0.995
        high = close * 1.02
        low = close * 0.985
        rows.append(f"{current_date},{open_price:.2f},{high:.2f},{low:.2f},{close:.2f},100000")
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def test_bt131_generated_trade_plans_use_supported_simulator_models(tmp_path: Path) -> None:
    bars_root = tmp_path / "bars"
    _write_bars(bars_root / "TEST.csv")
    args = argparse.Namespace(
        bars_root=bars_root,
        output=tmp_path / "historical_trade_plans.json",
        min_history=60,
        lookahead_days=20,
        max_plans=10,
        max_plans_per_symbol=2,
        min_dollar_volume=1_000_000.0,
    )

    plans, summary = generate_plans(args)

    assert summary.generated_plans == len(plans)
    assert plans
    assert {plan.stop_model for plan in plans} == {"fixed"}
    assert {plan.exit_model for plan in plans} == {"t1_t2"}
    assert "atr_1_25_or_2pct" not in {plan.stop_model for plan in plans}
    assert "target_2_or_stop" not in {plan.exit_model for plan in plans}
