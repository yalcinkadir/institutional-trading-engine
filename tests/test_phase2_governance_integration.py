"""
Tests for Phase 2 — Governance Integration.

Covers:
- kill_switch with VIX=None (Free Polygon tier safety)
- kill_switch with live VIX values
- risk_limits breach and pass
- live_runtime_cycle governance pre-check integration
"""

from __future__ import annotations

import pytest

from src.governance.kill_switch import evaluate_kill_switch
from src.governance.risk_limits import validate_risk_limits


class TestKillSwitchVixNoneSafety:
    """VIX=None must never trigger extreme_volatility."""

    def test_vix_none_does_not_activate(self):
        result = evaluate_kill_switch(vix=None, drawdown_percent=0, severe_anomaly_count=0)
        assert result["kill_switch"] is False
        assert "extreme_volatility" not in result["reasons"]

    def test_vix_none_marks_unavailable(self):
        result = evaluate_kill_switch(vix=None, drawdown_percent=0, severe_anomaly_count=0)
        assert result["vix_available"] is False

    def test_vix_none_with_drawdown_breach_still_activates(self):
        result = evaluate_kill_switch(vix=None, drawdown_percent=25.0, severe_anomaly_count=0)
        assert result["kill_switch"] is True
        assert "portfolio_drawdown_limit" in result["reasons"]
        assert "extreme_volatility" not in result["reasons"]

    def test_vix_zero_does_not_activate(self):
        # 0.0 should NOT trigger — only >= 40 triggers
        result = evaluate_kill_switch(vix=0.0, drawdown_percent=0, severe_anomaly_count=0)
        assert result["kill_switch"] is False

    def test_vix_available_when_provided(self):
        result = evaluate_kill_switch(vix=18.5, drawdown_percent=0, severe_anomaly_count=0)
        assert result["vix_available"] is True


class TestKillSwitchActivation:
    def test_extreme_vix_activates(self):
        result = evaluate_kill_switch(vix=42.0, drawdown_percent=0, severe_anomaly_count=0)
        assert result["kill_switch"] is True
        assert "extreme_volatility" in result["reasons"]

    def test_vix_exactly_40_activates(self):
        result = evaluate_kill_switch(vix=40.0, drawdown_percent=0, severe_anomaly_count=0)
        assert result["kill_switch"] is True

    def test_vix_39_does_not_activate(self):
        result = evaluate_kill_switch(vix=39.9, drawdown_percent=0, severe_anomaly_count=0)
        assert result["kill_switch"] is False

    def test_drawdown_20_activates(self):
        result = evaluate_kill_switch(vix=15.0, drawdown_percent=20.0, severe_anomaly_count=0)
        assert result["kill_switch"] is True
        assert "portfolio_drawdown_limit" in result["reasons"]

    def test_drawdown_19_does_not_activate(self):
        result = evaluate_kill_switch(vix=15.0, drawdown_percent=19.9, severe_anomaly_count=0)
        assert result["kill_switch"] is False

    def test_anomaly_count_5_activates(self):
        result = evaluate_kill_switch(vix=15.0, drawdown_percent=0, severe_anomaly_count=5)
        assert result["kill_switch"] is True
        assert "market_instability" in result["reasons"]

    def test_multiple_reasons_all_captured(self):
        result = evaluate_kill_switch(vix=45.0, drawdown_percent=25.0, severe_anomaly_count=6)
        assert len(result["reasons"]) == 3

    def test_normal_conditions_no_activation(self):
        result = evaluate_kill_switch(vix=18.0, drawdown_percent=5.0, severe_anomaly_count=1)
        assert result["kill_switch"] is False
        assert result["reasons"] == []


class TestRiskLimits:
    def test_pass_when_within_limits(self):
        result = validate_risk_limits(
            portfolio_drawdown_percent=10.0,
            max_drawdown_percent=15.0,
            daily_loss_percent=2.0,
            max_daily_loss_percent=5.0,
        )
        assert result["status"] == "PASS"
        assert result["breaches"] == []

    def test_breach_on_drawdown(self):
        result = validate_risk_limits(
            portfolio_drawdown_percent=15.0,
            max_drawdown_percent=15.0,
            daily_loss_percent=0.0,
            max_daily_loss_percent=5.0,
        )
        assert result["status"] == "BREACH"
        assert "max_drawdown_breached" in result["breaches"]

    def test_breach_on_daily_loss(self):
        result = validate_risk_limits(
            portfolio_drawdown_percent=0.0,
            max_drawdown_percent=15.0,
            daily_loss_percent=5.0,
            max_daily_loss_percent=5.0,
        )
        assert result["status"] == "BREACH"
        assert "max_daily_loss_breached" in result["breaches"]

    def test_both_breached(self):
        result = validate_risk_limits(
            portfolio_drawdown_percent=20.0,
            max_drawdown_percent=15.0,
            daily_loss_percent=8.0,
            max_daily_loss_percent=5.0,
        )
        assert result["status"] == "BREACH"
        assert len(result["breaches"]) == 2

    def test_zero_values_pass(self):
        result = validate_risk_limits(
            portfolio_drawdown_percent=0.0,
            max_drawdown_percent=15.0,
            daily_loss_percent=0.0,
            max_daily_loss_percent=5.0,
        )
        assert result["status"] == "PASS"


class TestGovernanceLiveRuntimeIntegration:
    """Verify governance is wired into live_runtime_cycle correctly."""

    def test_kill_switch_blocks_cycle_on_extreme_vix(self, tmp_path):
        from unittest.mock import patch
        from src.runtime.live_runtime_cycle import GovernanceBlockedError, LiveRuntimeCycle

        cycle = LiveRuntimeCycle()
        metrics = {
            "SPY": {"close": 500, "rsi14": 58, "trend": "Strong Uptrend",
                    "atr_pct": 1.2, "rvol": 1.1, "ret_20d": 4.0, "vol20": 75e6,
                    "rs_spread": 0.0, "rs_label": "Neutral", "warnings": [],
                    "sma20": 490, "sma50": 470, "sma200": 450, "benchmark": "SPY",
                    "benchmark_ret_20d": 4.0, "momentum": "Strong",
                    "volatility": "Normal", "rvol_label": "Normal",
                    "setup_readiness": "OK", "symbol": "SPY",
                    "high": 502, "low": 498, "volume": 80e6,
                    "entry": None, "stop_loss": None, "exit_1": None, "exit_2": None},
        }

        with patch("src.runtime.live_runtime_cycle.decision_log_store") as store, \
             patch("src.runtime.live_runtime_cycle.runtime_state"), \
             patch("src.runtime.live_runtime_cycle.in_memory_state_cache"):
            store.append.return_value = None

            with pytest.raises(GovernanceBlockedError) as exc_info:
                cycle.run(metrics_map=metrics, vix_data={"close": 45.0})

        assert "extreme_volatility" in exc_info.value.reasons

    def test_vix_none_does_not_block_cycle(self, tmp_path):
        from unittest.mock import patch
        from src.runtime.live_runtime_cycle import LiveRuntimeCycle
        from src.runtime.runtime_market_snapshot import RuntimeMarketSnapshot

        cycle = LiveRuntimeCycle()
        metrics = {
            "SPY": {"close": 500, "rsi14": 58, "trend": "Strong Uptrend",
                    "atr_pct": 1.2, "rvol": 1.1, "ret_20d": 4.0, "vol20": 75e6,
                    "rs_spread": 0.0, "rs_label": "Neutral", "warnings": [],
                    "sma20": 490, "sma50": 470, "sma200": 450, "benchmark": "SPY",
                    "benchmark_ret_20d": 4.0, "momentum": "Strong",
                    "volatility": "Normal", "rvol_label": "Normal",
                    "setup_readiness": "OK", "symbol": "SPY",
                    "high": 502, "low": 498, "volume": 80e6,
                    "entry": None, "stop_loss": None, "exit_1": None, "exit_2": None},
            "QQQ": {"close": 420, "rsi14": 60, "trend": "Uptrend",
                    "atr_pct": 1.3, "rvol": 1.0, "ret_20d": 3.5, "vol20": 60e6,
                    "rs_spread": 0.0, "rs_label": "Neutral", "warnings": [],
                    "sma20": 410, "sma50": 395, "sma200": 380, "benchmark": "QQQ",
                    "benchmark_ret_20d": 3.5, "momentum": "Moderate",
                    "volatility": "Normal", "rvol_label": "Normal",
                    "setup_readiness": "OK", "symbol": "QQQ",
                    "high": 422, "low": 418, "volume": 65e6,
                    "entry": None, "stop_loss": None, "exit_1": None, "exit_2": None},
        }

        with patch("src.runtime.live_runtime_cycle.decision_log_store") as store, \
             patch("src.runtime.live_runtime_cycle.runtime_state"), \
             patch("src.runtime.live_runtime_cycle.in_memory_state_cache"):
            store.append.return_value = None
            # vix_data=None must NOT raise
            snapshot = cycle.run(metrics_map=metrics, vix_data=None)

        assert isinstance(snapshot, RuntimeMarketSnapshot)
        # VIX warning must be present
        assert snapshot.bridge.data_quality_warnings
