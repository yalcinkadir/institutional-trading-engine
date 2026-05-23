from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

from src.backtesting.out_of_sample_validation import (
    reconstruct_breakout_plans_from_bars,
    reconstruct_plans_for_symbols,
    render_validation_markdown,
    validate_out_of_sample,
    write_reconstructed_plans,
    write_validation_report,
)


def _write_bars(path: Path, *, count: int = 80) -> None:
    lines = ["date,open,high,low,close,volume"]
    start_date = date(2020, 1, 1)
    for index in range(count):
        bar_date = start_date + timedelta(days=index)
        base = 100 + index
        lines.append(f"{bar_date.isoformat()},{base},{base + 2},{base - 2},{base + 1},1000")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_reconstruct_breakout_plans_from_bars(tmp_path: Path) -> None:
    bars = tmp_path / "TEST.csv"
    _write_bars(bars, count=50)

    plans = reconstruct_breakout_plans_from_bars(
        symbol="TEST",
        bars_path=bars,
        lookback_bars=10,
        every_nth_signal=10,
    )

    assert len(plans) == 4
    assert plans[0].symbol == "TEST"
    assert plans[0].entry_type == "historical_breakout_reconstruction"
    assert plans[0].setup_type == "p25_reconstructed_daily_breakout"
    assert plans[0].stop_loss < plans[0].entry_trigger < plans[0].target_1 < plans[0].target_2


def test_reconstruct_plans_for_symbols(tmp_path: Path) -> None:
    bars_root = tmp_path / "bars"
    bars_root.mkdir()
    _write_bars(bars_root / "AAA.csv", count=50)
    _write_bars(bars_root / "BBB.csv", count=50)

    plans = reconstruct_plans_for_symbols(
        symbols=["AAA", "BBB"],
        bars_root=bars_root,
        lookback_bars=10,
        every_nth_signal=10,
    )

    assert len(plans) == 8
    assert {plan.symbol for plan in plans} == {"AAA", "BBB"}


def test_validate_out_of_sample_splits_by_signal_date(tmp_path: Path) -> None:
    bars_root = tmp_path / "bars"
    bars_root.mkdir()
    _write_bars(bars_root / "TEST.csv", count=80)
    plans = reconstruct_plans_for_symbols(
        symbols=["TEST"],
        bars_root=bars_root,
        lookback_bars=10,
        every_nth_signal=10,
    )

    report = validate_out_of_sample(
        plans=plans,
        bars_root=bars_root,
        split_date="2020-02-01",
        max_bars=5,
    )

    assert report.reconstructed_plan_count == len(plans)
    assert report.in_sample_count > 0
    assert report.out_of_sample_count > 0
    assert report.all_metrics.total == len(plans)
    assert report.in_sample_metrics.total == report.in_sample_count
    assert report.out_of_sample_metrics.total == report.out_of_sample_count


def test_write_validation_report_and_plans(tmp_path: Path) -> None:
    bars_root = tmp_path / "bars"
    bars_root.mkdir()
    _write_bars(bars_root / "TEST.csv", count=80)
    plans = reconstruct_plans_for_symbols(
        symbols=["TEST"],
        bars_root=bars_root,
        lookback_bars=10,
        every_nth_signal=10,
    )
    report = validate_out_of_sample(
        plans=plans,
        bars_root=bars_root,
        split_date="2020-02-01",
        max_bars=5,
    )

    plans_path = tmp_path / "plans.json"
    json_path = tmp_path / "validation.json"
    markdown_path = tmp_path / "validation.md"
    write_reconstructed_plans(plans, plans_path)
    write_validation_report(report, json_path=json_path, markdown_path=markdown_path)

    assert len(json.loads(plans_path.read_text(encoding="utf-8"))["plans"]) == len(plans)
    assert json.loads(json_path.read_text(encoding="utf-8"))["split_date"] == "2020-02-01"
    markdown = markdown_path.read_text(encoding="utf-8")
    assert "Out-of-Sample Historical Validation" in markdown
    assert "out_of_sample" in markdown
    assert "validation evidence only" in render_validation_markdown(report)
