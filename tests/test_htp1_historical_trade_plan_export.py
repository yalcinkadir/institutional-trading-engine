from __future__ import annotations

import json
from pathlib import Path

from scripts.export_historical_trade_plans import export_historical_trade_plans
from scripts.validate_bt9_real_historical_input_pack import validate_bt9_input_pack


def _valid_record(**overrides):
    record = {
        "signal_id": "sig_SPY_001",
        "symbol": "SPY",
        "timestamp": "2026-06-01T14:30:00Z",
        "close": 100.0,
        "entry_trigger": 101.0,
        "stop_loss": 99.0,
        "target_1": 104.0,
        "target_2": 106.0,
        "valid_until": "2026-06-05",
        "entry_type": "breakout",
        "setup_type": "momentum_breakout",
        "data_source": "polygon",
        "data_status": "ok",
        "provenance": {"vendor": "polygon", "as_of": "2026-06-01T14:30:00Z"},
    }
    record.update(overrides)
    return record


def _write_source(path: Path, records: list[dict]) -> None:
    path.write_text(json.dumps({"observations": records}), encoding="utf-8")


def test_htp1_missing_close_blocks_export(tmp_path: Path) -> None:
    source = tmp_path / "observations.json"
    _write_source(source, [_valid_record(close=None)])

    report = export_historical_trade_plans(
        source_path=source,
        output_path=tmp_path / "historical_trade_plans.json",
        manifest_path=tmp_path / "manifest.json",
    )

    assert report.passed is False
    assert "record_0_missing:close" in report.failures
    assert "record_0_missing_close" in report.failures
    assert not (tmp_path / "historical_trade_plans.json").exists()


def test_htp1_missing_entry_stop_target_blocks_export(tmp_path: Path) -> None:
    source = tmp_path / "observations.json"
    _write_source(source, [_valid_record(entry_trigger=None, stop_loss=None, target_1=None)])

    report = export_historical_trade_plans(
        source_path=source,
        output_path=tmp_path / "historical_trade_plans.json",
        manifest_path=tmp_path / "manifest.json",
    )

    assert report.passed is False
    assert "record_0_missing:entry_trigger,stop_loss,target_1" in report.failures
    assert "record_0_missing_entry_trigger" in report.failures
    assert "record_0_missing_stop_loss" in report.failures
    assert "record_0_missing_target_1" in report.failures


def test_htp1_rejects_demo_synthetic_public_safe_records(tmp_path: Path) -> None:
    source = tmp_path / "observations.json"
    _write_source(source, [_valid_record(data_source="synthetic_demo", provenance={"vendor": "public_safe"})])

    report = export_historical_trade_plans(
        source_path=source,
        output_path=tmp_path / "historical_trade_plans.json",
        manifest_path=tmp_path / "manifest.json",
    )

    assert report.passed is False
    assert "record_0_demo_marker" in report.failures


def test_htp1_valid_observations_export_deterministic_trade_plans(tmp_path: Path) -> None:
    source = tmp_path / "observations.json"
    output = tmp_path / "historical_trade_plans.json"
    manifest = tmp_path / "manifest.json"
    _write_source(
        source,
        [
            _valid_record(signal_id="sig_QQQ_001", symbol="QQQ", timestamp="2026-06-02T14:30:00Z"),
            _valid_record(signal_id="sig_SPY_001", symbol="SPY", timestamp="2026-06-01T14:30:00Z"),
        ],
    )

    first = export_historical_trade_plans(source_path=source, output_path=output, manifest_path=manifest)
    first_bytes = output.read_bytes()
    second = export_historical_trade_plans(source_path=source, output_path=output, manifest_path=manifest)

    payload = json.loads(first_bytes.decode("utf-8"))
    manifest_payload = json.loads(manifest.read_text(encoding="utf-8"))

    assert first.passed is True
    assert second.passed is True
    assert output.read_bytes() == first_bytes
    assert [plan["signal_id"] for plan in payload["plans"]] == ["sig_SPY_001", "sig_QQQ_001"]
    assert manifest_payload["exported_count"] == 2
    assert manifest_payload["symbols"] == ["QQQ", "SPY"]
    assert manifest_payload["output_sha256"]
    assert manifest_payload["boundary"] == "paper_only_research_only"


def test_htp1_export_is_bt9_compatible(tmp_path: Path) -> None:
    source = tmp_path / "observations.json"
    output = tmp_path / "data/trade_plans/historical_trade_plans.json"
    manifest = tmp_path / "data/trade_plans/historical_trade_plans_manifest.json"
    universe = tmp_path / "data/universe/survivorship_universe.csv"
    bars_root = tmp_path / "data/historical/bars/1day"
    _write_source(source, [_valid_record()])
    export_report = export_historical_trade_plans(source_path=source, output_path=output, manifest_path=manifest)
    universe.parent.mkdir(parents=True, exist_ok=True)
    universe.write_text(
        "symbol,effective_from,effective_to,active,asset_class,exchange,source,status,reason\n"
        "SPY,2024-01-01,,true,etf,NYSEARCA,initial_universe,active,initial test universe\n",
        encoding="utf-8",
    )
    bars_root.mkdir(parents=True, exist_ok=True)
    (bars_root / "SPY.csv").write_text(
        "date,open,high,low,close,volume\n"
        "2026-06-01,100,101,99,100,1000000\n"
        "2026-06-02,101,105,100,104,1100000\n",
        encoding="utf-8",
    )

    bt9_report = validate_bt9_input_pack(universe_path=universe, bars_root=bars_root, trade_plans_path=output)

    assert export_report.passed is True
    assert bt9_report.passed is True
    assert bt9_report.symbols == ["SPY"]
