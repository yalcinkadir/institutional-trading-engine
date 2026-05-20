"""
Tests for src/runtime/runtime_market_snapshot.py

Covers:
- Snapshot creation and field population
- Serialisation to persistence payload
- Payload completeness and type correctness
- has_data_quality_issues flag
- regime_summary property
- snapshot_id uniqueness
"""

from __future__ import annotations

import time

import pytest

from src.bridge.scanner_to_orchestrator import translate
from src.orchestration.institutional_decision_orchestrator import (
    InstitutionalDecisionInputs,
    institutional_decision_orchestrator,
)
from src.runtime.runtime_market_snapshot import RuntimeMarketSnapshot


# ── Helpers ──────────────────────────────────────────────────────────────────

def _make_metrics_map():
    base = {
        "close": 500.0,
        "high": 502.5,
        "low": 497.5,
        "volume": 80_000_000,
        "sma20": 490.0,
        "sma50": 470.0,
        "sma200": 450.0,
        "rsi14": 58.0,
        "atr14": 6.0,
        "atr_pct": 1.2,
        "vol20": 75_000_000,
        "rvol": 1.1,
        "ret_20d": 4.0,
        "benchmark": "SPY",
        "benchmark_ret_20d": 4.0,
        "rs_spread": 0.0,
        "rs_label": "Neutral",
        "trend": "Strong Uptrend",
        "momentum": "Strong",
        "volatility": "Normal",
        "rvol_label": "Normal",
        "setup_readiness": "Trend Strong, Entry Unclear",
        "warnings": [],
        "entry": None,
        "stop_loss": None,
        "exit_1": None,
        "exit_2": None,
    }
    spy = {**base, "symbol": "SPY"}
    qqq = {**base, "symbol": "QQQ", "benchmark": "QQQ"}
    return {"SPY": spy, "QQQ": qqq}


def _make_snapshot(with_warnings: bool = False) -> RuntimeMarketSnapshot:
    metrics_map = _make_metrics_map()
    vix_data = {"close": 16.5, "direction": "Falling"} if not with_warnings else None

    bridge = translate(metrics_map, vix_data)

    result = institutional_decision_orchestrator.evaluate(bridge.inputs)

    return RuntimeMarketSnapshot.create(
        metrics_map=metrics_map,
        vix_data=vix_data,
        bridge=bridge,
        orchestrator_result=result,
        cycle_duration_ms=42.5,
    )


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestRuntimeMarketSnapshotCreation:
    def test_snapshot_has_valid_id(self):
        snap = _make_snapshot()
        assert len(snap.snapshot_id) > 10
        assert "_" in snap.snapshot_id

    def test_snapshot_ids_are_unique(self):
        snap1 = _make_snapshot()
        time.sleep(0.01)
        snap2 = _make_snapshot()
        assert snap1.snapshot_id != snap2.snapshot_id

    def test_captured_at_is_iso_string(self):
        snap = _make_snapshot()
        assert "T" in snap.captured_at
        assert snap.captured_at.endswith("+00:00")

    def test_cycle_duration_ms_is_positive(self):
        snap = _make_snapshot()
        assert snap.cycle_duration_ms > 0.0

    def test_orchestrator_result_is_populated(self):
        snap = _make_snapshot()
        assert snap.orchestrator_result is not None
        assert snap.orchestrator_result.macro_regime != ""
        assert snap.orchestrator_result.final_exposure_percent >= 0.0

    def test_bridge_is_stored(self):
        snap = _make_snapshot()
        assert snap.bridge is not None
        assert snap.bridge.inputs is not None


class TestDataQualityFlags:
    def test_no_warnings_when_vix_available(self):
        snap = _make_snapshot(with_warnings=False)
        assert not snap.has_data_quality_issues

    def test_warnings_present_when_vix_missing(self):
        snap = _make_snapshot(with_warnings=True)
        assert snap.has_data_quality_issues
        assert len(snap.bridge.data_quality_warnings) >= 1


class TestRegimeSummary:
    def test_regime_summary_contains_key_fields(self):
        snap = _make_snapshot()
        summary = snap.regime_summary
        assert "macro=" in summary
        assert "cross_asset=" in summary
        assert "tail=" in summary
        assert "fusion=" in summary
        assert "exposure=" in summary

    def test_regime_summary_is_string(self):
        snap = _make_snapshot()
        assert isinstance(snap.regime_summary, str)


class TestPersistencePayload:
    def test_payload_is_dict(self):
        snap = _make_snapshot()
        payload = snap.to_persistence_payload()
        assert isinstance(payload, dict)

    def test_required_keys_present(self):
        snap = _make_snapshot()
        payload = snap.to_persistence_payload()

        required = {
            "snapshot_id",
            "captured_at",
            "cycle_duration_ms",
            "data_quality_warnings",
            "symbols_used",
            "symbol_count",
            "macro_regime",
            "cross_asset_regime",
            "tail_risk_regime",
            "liquidity_risk",
            "fusion_classification",
            "probabilistic_classification",
            "execution_aggressiveness",
            "final_exposure_percent",
            "explanation",
            "inputs",
            "derivation_notes",
        }
        for key in required:
            assert key in payload, f"Missing key in payload: {key}"

    def test_inputs_sub_dict_has_key_fields(self):
        snap = _make_snapshot()
        inputs_dict = snap.to_persistence_payload()["inputs"]
        required = {
            "market_regime_score",
            "equity_strength",
            "bond_strength",
            "dollar_strength",
            "gold_strength",
            "volatility_level",
            "gap_risk_percent",
            "liquidity_stress_percent",
            "feature_alpha_score",
        }
        for key in required:
            assert key in inputs_dict, f"Missing input key: {key}"

    def test_all_numeric_fields_are_finite(self):
        import math
        snap = _make_snapshot()
        payload = snap.to_persistence_payload()
        for key in ["cycle_duration_ms", "final_exposure_percent", "symbol_count"]:
            val = payload[key]
            assert isinstance(val, (int, float))
            assert not math.isnan(float(val))
            assert not math.isinf(float(val))

    def test_snapshot_id_in_payload_matches(self):
        snap = _make_snapshot()
        assert snap.to_persistence_payload()["snapshot_id"] == snap.snapshot_id

    def test_payload_is_json_serialisable(self):
        import json
        snap = _make_snapshot()
        payload = snap.to_persistence_payload()
        # Should not raise
        serialised = json.dumps(payload)
        assert len(serialised) > 100
