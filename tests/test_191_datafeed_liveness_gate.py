from __future__ import annotations

import json
from pathlib import Path

from src.signals.signal_generator import build_signals, save_signals
from src.validation.datafeed_liveness import (
    DATAFEED_BLOCKED,
    PROVIDER_FAILURE_SCHEMA_MISMATCH,
    build_datafeed_liveness_record,
    write_datafeed_liveness_record,
)


def _decision_report() -> dict:
    return {
        "decisions": [
            {
                "symbol": "NVDA",
                "decision": "approved",
                "setup_type": "momentum_breakout",
                "risk_tier": "tier_2",
                "position_size_multiplier": 0.75,
                "setup_score": 88.0,
                "regime_alignment": 0.7,
                "blocked_reasons": [],
                "notes": [],
            },
            {
                "symbol": "MSFT",
                "decision": "approved",
                "setup_type": "pullback_continuation",
                "risk_tier": "tier_1",
                "position_size_multiplier": 1.0,
                "setup_score": 91.0,
                "regime_alignment": 0.8,
                "blocked_reasons": [],
                "notes": [],
            },
        ]
    }


def _all_null_scanner_metrics() -> dict:
    return {
        "NVDA": {
            "close": None,
            "atr14": None,
            "source": "polygon",
            "source_timestamp": "2026-06-11T14:30:00+00:00",
            "fallback_level": "primary",
            "data_status": "BLOCKED",
        },
        "MSFT": {
            "close": None,
            "atr14": None,
            "source": "polygon",
            "source_timestamp": "2026-06-11T14:30:00+00:00",
            "fallback_level": "primary",
            "data_status": "BLOCKED",
        },
    }


def _blocked_data_quality_summary() -> dict:
    return {
        "data_quality_status": "BLOCKED",
        "total_symbols": 2,
        "valid_symbols": 0,
        "missing_symbols": [],
        "missing_required_fields": {
            "NVDA": ["close", "atr14"],
            "MSFT": ["close", "atr14"],
        },
        "missing_provenance_fields": {},
        "stale_symbols": {},
        "market_data_failures": {},
    }


def test_191_all_null_scanner_prices_block_paper_observation_liveness() -> None:
    record = build_datafeed_liveness_record(
        scanner_metrics_map=_all_null_scanner_metrics(),
        scanner_data_quality=_blocked_data_quality_summary(),
        checked_at="2026-06-11T15:00:00+00:00",
    )

    assert record.datafeed_status == DATAFEED_BLOCKED
    assert record.provider_failure_reason == PROVIDER_FAILURE_SCHEMA_MISMATCH
    assert record.total_symbols == 2
    assert record.valid_close_count == 0
    assert record.all_close_missing is True
    assert record.blocked_symbols == ["MSFT", "NVDA"]


def test_191_all_null_close_signals_cannot_be_persisted_as_productive_observation(tmp_path: Path) -> None:
    signals = build_signals(
        decision_report=_decision_report(),
        scanner_metrics_map=_all_null_scanner_metrics(),
        market_regime="Bullish",
    )
    record = build_datafeed_liveness_record(
        scanner_metrics_map=_all_null_scanner_metrics(),
        scanner_data_quality=_blocked_data_quality_summary(),
        checked_at="2026-06-11T15:00:00+00:00",
    )
    save_signals(
        signals,
        date_str="2026-06-11",
        signals_dir=tmp_path,
        data_quality=_blocked_data_quality_summary(),
        datafeed_liveness=record.to_dict(),
    )

    payload = json.loads((tmp_path / "2026-06-11-signals.json").read_text(encoding="utf-8"))

    assert payload["actionable_count"] == 0
    assert payload["datafeed_liveness"]["datafeed_status"] == DATAFEED_BLOCKED
    assert payload["datafeed_liveness"]["provider_failure_reason"] == PROVIDER_FAILURE_SCHEMA_MISMATCH
    assert all(signal["action"] == "NO_TRADE" for signal in payload["signals"])
    assert all(signal["close"] is None for signal in payload["signals"])
    assert all(signal["decision"] != "approved" for signal in payload["signals"])
    assert all(signal["risk_tier"] == "NO_TRADE" for signal in payload["signals"])


def test_191_writes_repo_visible_liveness_record(tmp_path: Path) -> None:
    record = build_datafeed_liveness_record(
        scanner_metrics_map=_all_null_scanner_metrics(),
        scanner_data_quality=_blocked_data_quality_summary(),
        checked_at="2026-06-11T15:00:00+00:00",
    )

    dated_path, latest_path = write_datafeed_liveness_record(record, output_dir=tmp_path, date_str="2026-06-11")

    assert dated_path == tmp_path / "2026-06-11-datafeed-liveness.json"
    assert latest_path == tmp_path / "datafeed-liveness-latest.json"
    payload = json.loads(latest_path.read_text(encoding="utf-8"))
    assert payload["datafeed_status"] == DATAFEED_BLOCKED
    assert payload["provider_failure_reason"] == PROVIDER_FAILURE_SCHEMA_MISMATCH
    assert payload["all_close_missing"] is True
