import json
from pathlib import Path

import pytest

from scripts.analyze_bt139_bt131_sample_expansion import (
    INSUFFICIENT_SAMPLE,
    PROMOTION_CANDIDATE_SAMPLE,
    REVIEWABLE_SAMPLE,
    analyze,
    write_report,
)


def _row(index: int, *, symbol: str = "AAPL", signal_date: str | None = None, setup: str = "breakout", regime: str = "bull", asset_group: str = "mega_cap_tech") -> dict:
    day = signal_date or f"2024-01-{(index % 28) + 1:02d}"
    return {
        "signal_id": f"sig_{index}",
        "symbol": symbol,
        "signal_date": day,
        "outcome": "TARGET_1_HIT" if index % 3 else "STOP_HIT",
        "setup_type": setup,
        "entry_price": 100.0,
        "initial_stop_loss": 95.0,
        "target_1": 110.0,
        "target_2": 120.0,
        "max_adverse_excursion_r": -0.5,
        "max_favorable_excursion_r": 1.5,
        "same_bar_ambiguous": False,
        "signal_day_cluster_size": 1,
        "market_regime": regime,
        "asset_group": asset_group,
        "atr14_at_signal": 2.0,
        "volume": 1000000,
        "avg_volume_20": 900000,
    }


def _payload(rows: list[dict]) -> dict:
    return {
        "run_id": "bt131-real-data-test",
        "data_source": "real_data",
        "is_demo": False,
        "input_pack_gate_status": "PASSED",
        "input_completeness_status": "OK",
        "run_health_status": "OK",
        "broker_execution_mode": "paper_only",
        "live_trading_authorized": False,
        "results": rows,
    }


def _write_payload(tmp_path: Path, payload: dict) -> Path:
    path = tmp_path / "evidence.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_bt139_blocks_promotion_for_small_bt131_sample(tmp_path: Path) -> None:
    path = _write_payload(tmp_path, _payload([_row(i) for i in range(24)]))

    report = analyze(path)

    assert report.evidence_quality == INSUFFICIENT_SAMPLE
    assert report.promotion_allowed is False
    assert report.production_rule_change_allowed is False
    assert report.broker_execution_mode == "paper_only"
    assert report.live_trading_authorized is False
    assert "sample quality below REVIEWABLE_SAMPLE" in report.promotion_block_reasons


def test_bt139_detects_signal_day_clusters(tmp_path: Path) -> None:
    rows = [
        _row(1, symbol="AAPL", signal_date="2024-01-02"),
        _row(2, symbol="MSFT", signal_date="2024-01-02"),
        _row(3, symbol="QQQ", signal_date="2024-01-03"),
    ]
    path = _write_payload(tmp_path, _payload(rows))

    report = analyze(path)

    assert report.signal_day_count == 2
    assert report.signal_day_cluster_count == 1
    assert report.max_signal_day_cluster_size == 2
    assert report.concentrated_signal_days[0]["signal_date"] == "2024-01-02"
    assert sorted(report.concentrated_signal_days[0]["symbols"]) == ["AAPL", "MSFT"]


def test_bt139_records_missing_fields_explicitly(tmp_path: Path) -> None:
    row = _row(1)
    row.pop("atr14_at_signal")
    row.pop("volume")
    row.pop("avg_volume_20")
    path = _write_payload(tmp_path, _payload([row]))

    report = analyze(path)

    assert "atr14_at_signal" in report.missing_field_reasons
    assert "volume" in report.missing_field_reasons
    assert "avg_volume_20" in report.missing_field_reasons
    assert report.missing_field_reasons["atr14_at_signal"] == ["sig_1"]


def test_bt139_separates_real_no_trade_from_missing_input_paths(tmp_path: Path) -> None:
    evaluated = _row(1)
    real_no_trade = _row(2)
    real_no_trade["outcome"] = "EXPIRED"
    missing_input = _row(3)
    missing_input["outcome"] = "MISSING_INPUT"
    missing_input["missing_input_reason"] = "source_bar_missing"
    unknown = _row(4)
    unknown["outcome"] = "UNMAPPED_STATE"

    report = analyze(_write_payload(tmp_path, _payload([evaluated, real_no_trade, missing_input, unknown])))

    assert report.outcome_path_summary == {
        "evaluated_trade_count": 1,
        "real_no_trade_count": 1,
        "skipped_or_missing_input_count": 1,
        "unknown_outcome_count": 1,
    }


def test_bt139_classifies_reviewable_sample_when_diverse_enough(tmp_path: Path) -> None:
    symbols = ["AAPL", "MSFT", "META", "NVDA", "MU", "QQQ", "GLD", "SLV"]
    setups = ["breakout", "pullback"]
    groups = {
        "AAPL": "mega_cap_tech",
        "MSFT": "mega_cap_tech",
        "META": "mega_cap_tech",
        "NVDA": "semiconductor_or_hardware",
        "MU": "semiconductor_or_hardware",
        "QQQ": "index_etf",
        "GLD": "metals_etf",
        "SLV": "metals_etf",
    }
    rows = [
        _row(
            i,
            symbol=symbols[i % len(symbols)],
            signal_date=f"2024-{(i // 28) + 1:02d}-{(i % 28) + 1:02d}",
            setup=setups[i % len(setups)],
            regime="bull" if i % 2 else "neutral",
            asset_group=groups[symbols[i % len(symbols)]],
        )
        for i in range(120)
    ]
    path = _write_payload(tmp_path, _payload(rows))

    report = analyze(path)

    assert report.evidence_quality == REVIEWABLE_SAMPLE
    assert report.promotion_allowed is True
    assert report.symbol_count == 8
    assert report.setup_count == 2
    assert len(report.asset_group_coverage) == 4


def test_bt139_classifies_promotion_candidate_sample_when_broad_and_large(tmp_path: Path) -> None:
    symbols = ["AAPL", "MSFT", "META", "NVDA", "MU", "QQQ", "GLD", "SLV", "SPY", "AMD", "GOOGL", "AMZN"]
    setups = ["breakout", "pullback", "regime_gate"]
    groups = ["mega_cap_tech", "semiconductor_or_hardware", "index_etf", "metals_etf"]
    rows = [
        _row(
            i,
            symbol=symbols[i % len(symbols)],
            signal_date=f"2024-{(i // 28) + 1:02d}-{(i % 28) + 1:02d}",
            setup=setups[i % len(setups)],
            regime="bull" if i % 3 else "risk_off",
            asset_group=groups[i % len(groups)],
        )
        for i in range(240)
    ]
    path = _write_payload(tmp_path, _payload(rows))

    report = analyze(path)

    assert report.evidence_quality == PROMOTION_CANDIDATE_SAMPLE
    assert report.promotion_allowed is True


def test_bt139_refuses_demo_or_live_authorized_evidence(tmp_path: Path) -> None:
    demo_payload = _payload([_row(1)])
    demo_payload["is_demo"] = True

    with pytest.raises(SystemExit, match="refuses demo evidence"):
        analyze(_write_payload(tmp_path, demo_payload))

    live_payload = _payload([_row(2)])
    live_payload["live_trading_authorized"] = True

    with pytest.raises(SystemExit, match="live_trading_authorized=false"):
        analyze(_write_payload(tmp_path, live_payload))


def test_bt139_writes_json_and_markdown_reports(tmp_path: Path) -> None:
    report = analyze(_write_payload(tmp_path, _payload([_row(i) for i in range(24)])))
    output_json = tmp_path / "bt139.json"
    output_md = tmp_path / "bt139.md"

    write_report(report, output_json=output_json, output_md=output_md)

    parsed = json.loads(output_json.read_text(encoding="utf-8"))
    markdown = output_md.read_text(encoding="utf-8")

    assert parsed["report_version"] == "bt139.v2"
    assert parsed["promotion_allowed"] is False
    assert "outcome_path_summary" in parsed
    assert "# BT139 BT131 Sample Expansion Report" in markdown
    assert "Evidence quality" in markdown
    assert "Outcome Path Summary" in markdown
