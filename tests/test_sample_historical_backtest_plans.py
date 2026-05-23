from __future__ import annotations

import json
from pathlib import Path

from scripts.create_sample_historical_backtest_plans import build_sample_plans, main


def test_build_sample_plans_creates_deterministic_buy_watch_plans() -> None:
    plans = build_sample_plans(["SPY", "QQQ"], signal_date="2017-01-03")

    assert len(plans) == 2
    assert plans[0]["signal_id"] == "sample_historical_SPY_2017-01-03"
    assert plans[0]["action"] == "BUY_WATCH"
    assert plans[0]["entry_trigger"] == 100.0
    assert plans[0]["stop_loss"] == 95.0
    assert plans[0]["target_1"] == 108.0
    assert plans[0]["target_2"] == 116.0
    assert plans[1]["entry_trigger"] == 101.0


def test_cli_writes_sample_plan_file(tmp_path: Path, monkeypatch) -> None:
    output = tmp_path / "plans.json"
    monkeypatch.setattr(
        "sys.argv",
        [
            "create_sample_historical_backtest_plans.py",
            "--symbols",
            "SPY,QQQ",
            "--signal-date",
            "2017-01-03",
            "--output",
            str(output),
        ],
    )

    assert main() == 0
    payload = json.loads(output.read_text(encoding="utf-8"))

    assert "plans" in payload
    assert len(payload["plans"]) == 2
    assert payload["plans"][0]["symbol"] == "SPY"
