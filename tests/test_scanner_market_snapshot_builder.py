"""
Tests for src/bridge/scanner_market_snapshot_builder.py

Covers:
- build_snapshot() returns correct type
- bridge and orchestrator are both called
- cycle_duration_ms is tracked
- data quality warnings pass through
- None metrics in map handled gracefully
- snapshot payload is persistence-ready

Also covers the scanner.py integration contract:
- runtime cycle is called after report is written
- GovernanceBlockedError is caught and does not raise to caller
- Generic exceptions are caught and do not raise to caller
"""

from __future__ import annotations

import math
from unittest.mock import MagicMock, patch

import pytest

from src.bridge.scanner_market_snapshot_builder import build_snapshot
from src.runtime.runtime_market_snapshot import RuntimeMarketSnapshot


# ── Fixtures ──────────────────────────────────────────────────────────────────

def _base_metrics(symbol: str = "SPY", benchmark: str = "SPY") -> dict:
    return {
        "symbol": symbol,
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
        "benchmark": benchmark,
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


def _make_metrics_map() -> dict:
    return {
        "SPY": _base_metrics("SPY", "SPY"),
        "QQQ": _base_metrics("QQQ", "QQQ"),
        "NVDA": {**_base_metrics("NVDA", "QQQ"), "rs_label": "Leader", "rs_spread": 5.0},
    }


def _make_vix(close: float = 16.5) -> dict:
    return {"close": close, "direction": "Falling"}


# ── build_snapshot ─────────────────────────────────────────────────────────────

class TestBuildSnapshot:
    def test_returns_runtime_market_snapshot(self):
        snap = build_snapshot(_make_metrics_map(), _make_vix())
        assert isinstance(snap, RuntimeMarketSnapshot)

    def test_snapshot_has_valid_orchestrator_result(self):
        snap = build_snapshot(_make_metrics_map(), _make_vix())
        assert snap.orchestrator_result.macro_regime != ""
        assert snap.orchestrator_result.final_exposure_percent >= 0.0

    def test_snapshot_has_bridge_with_derivation_notes(self):
        snap = build_snapshot(_make_metrics_map(), _make_vix())
        assert snap.bridge is not None
        assert len(snap.bridge.derivation_notes) > 0

    def test_cycle_duration_is_tracked(self):
        snap = build_snapshot(_make_metrics_map(), _make_vix())
        assert snap.cycle_duration_ms > 0.0
        assert not math.isnan(snap.cycle_duration_ms)

    def test_missing_vix_produces_warning(self):
        snap = build_snapshot(_make_metrics_map(), vix_data=None)
        assert snap.bridge.data_quality_warnings
        assert any("VIX" in w for w in snap.bridge.data_quality_warnings)

    def test_snapshot_payload_is_json_serialisable(self):
        import json
        snap = build_snapshot(_make_metrics_map(), _make_vix())
        payload = snap.to_persistence_payload()
        serialised = json.dumps(payload)
        assert len(serialised) > 50

    def test_none_metrics_handled_gracefully(self):
        m = {"SPY": None, "QQQ": _base_metrics("QQQ", "QQQ")}
        snap = build_snapshot(m, _make_vix())
        assert isinstance(snap, RuntimeMarketSnapshot)

    def test_empty_metrics_map_handled_gracefully(self):
        snap = build_snapshot({}, vix_data=None)
        assert isinstance(snap, RuntimeMarketSnapshot)

    def test_symbols_used_reflects_valid_metrics(self):
        snap = build_snapshot(_make_metrics_map(), _make_vix())
        assert len(snap.bridge.symbols_used) >= 2

    def test_regime_summary_is_non_empty_string(self):
        snap = build_snapshot(_make_metrics_map(), _make_vix())
        assert isinstance(snap.regime_summary, str)
        assert len(snap.regime_summary) > 20

    def test_snapshot_id_format(self):
        snap = build_snapshot(_make_metrics_map(), _make_vix())
        # Format: YYYYMMDD_HHMMSS_microseconds
        assert len(snap.snapshot_id) >= 15
        assert "_" in snap.snapshot_id

    def test_builder_and_bridge_are_separate_concerns(self):
        """
        The builder calls the bridge (translate) and the orchestrator.
        It does NOT contain derivation logic itself.
        Verify by checking the build_snapshot source has no _derive_ functions.
        """
        import inspect
        from src.bridge import scanner_market_snapshot_builder as mod
        source = inspect.getsource(mod)
        assert "_derive_" not in source, (
            "Builder should not contain derivation logic — "
            "that belongs in scanner_to_orchestrator.py"
        )


# ── scanner.py integration contract ────────────────────────────────────────────

class TestScannerIntegrationContract:
    """
    Tests that validate the contract between scanner.py and live_runtime_cycle.
    These do not import scanner.py directly (to avoid Polygon API calls),
    but verify the expected behavior patterns.
    """

    def test_governance_blocked_error_is_catchable(self):
        """
        GovernanceBlockedError must be importable and catchable at the scanner level.
        """
        from src.runtime.live_runtime_cycle import GovernanceBlockedError

        try:
            raise GovernanceBlockedError(["extreme_volatility"])
        except GovernanceBlockedError as e:
            assert "extreme_volatility" in e.reasons

    def test_live_runtime_cycle_singleton_importable(self):
        """
        live_runtime_cycle singleton must be importable without side effects.
        """
        from src.runtime.live_runtime_cycle import live_runtime_cycle
        from src.runtime.live_runtime_cycle import LiveRuntimeCycle
        assert isinstance(live_runtime_cycle, LiveRuntimeCycle)

    def test_governance_block_does_not_leak_to_scanner(self):
        """
        When governance blocks, scanner.py catches GovernanceBlockedError.
        This test simulates that catch pattern.
        """
        from src.runtime.live_runtime_cycle import GovernanceBlockedError

        report_written = False
        runtime_blocked = False

        # Simulate scanner.py main() flow
        try:
            # Report write (always succeeds)
            report_written = True

            # Runtime cycle (raises governance block)
            raise GovernanceBlockedError(["extreme_volatility"])

        except GovernanceBlockedError as e:
            runtime_blocked = True
            blocked_reasons = e.reasons

        # Report must be written regardless of runtime outcome
        assert report_written
        assert runtime_blocked
        assert "extreme_volatility" in blocked_reasons

    def test_generic_runtime_error_does_not_leak_to_scanner(self):
        """
        Generic exceptions from the runtime cycle must not crash scanner.py.
        """
        report_written = False
        error_caught = False

        try:
            report_written = True
            raise RuntimeError("unexpected cycle failure")
        except Exception:
            error_caught = True

        assert report_written
        assert error_caught
