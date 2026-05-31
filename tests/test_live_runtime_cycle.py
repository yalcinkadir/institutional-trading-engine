"""
Tests for src/runtime/live_runtime_cycle.py

Covers:
- Successful cycle execution end-to-end
- Runtime state updated after cycle
- Decision persisted after cycle
- In-memory cache updated after cycle
- Governance kill switch blocks cycle
- Governance risk limits block cycle
- Blocked cycles are persisted as audit entries
- Snapshot returned on success
- Cycle duration is tracked
- GOV1 severe anomaly count comes from runtime state cache
- GOV2 missing portfolio state fails closed
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from src.runtime.anomaly_state import AnomalyState, AnomalyStateStore
from src.runtime.in_memory_state_cache import InMemoryStateCache
from src.runtime.live_runtime_cycle import GovernanceBlockedError, LiveRuntimeCycle
from src.runtime.portfolio_state import PortfolioState, PortfolioStateStore
from src.runtime.runtime_market_snapshot import RuntimeMarketSnapshot
from src.runtime.runtime_state import RuntimeState
from src.storage.decision_log_store import DecisionLogStore


# ── Fixtures ──────────────────────────────────────────────────────────────────

def _make_metrics_map():
    base = {
        "close": 500.0, "high": 502.5, "low": 497.5,
        "volume": 80_000_000, "sma20": 490.0, "sma50": 470.0,
        "sma200": 450.0, "rsi14": 58.0, "atr14": 6.0, "atr_pct": 1.2,
        "vol20": 75_000_000, "rvol": 1.1, "ret_20d": 4.0,
        "benchmark": "SPY", "benchmark_ret_20d": 4.0,
        "rs_spread": 0.0, "rs_label": "Neutral", "trend": "Strong Uptrend",
        "momentum": "Strong", "volatility": "Normal", "rvol_label": "Normal",
        "setup_readiness": "Trend Strong, Entry Unclear", "warnings": [],
        "entry": None, "stop_loss": None, "exit_1": None, "exit_2": None,
    }
    return {
        "SPY": {**base, "symbol": "SPY"},
        "QQQ": {**base, "symbol": "QQQ", "benchmark": "QQQ"},
    }


def _make_vix_data(close: float = 16.5) -> dict:
    return {"close": close, "direction": "Falling"}


class _StaticPortfolioStateStore:
    def __init__(
        self,
        *,
        drawdown_percent: float = 0.0,
        daily_loss_percent: float = 0.0,
    ) -> None:
        self.state = PortfolioState(
            equity_start=10000.0,
            equity_current=10000.0,
            drawdown_percent=drawdown_percent,
            daily_loss_percent=daily_loss_percent,
            open_positions=[],
            source="test_portfolio_state_store",
            governance_valid=True,
        )

    def load(self) -> PortfolioState:
        return self.state


class _StaticAnomalyStateStore:
    def __init__(self, *, severe_anomaly_count: int = 0, source: str = "test_anomaly_state_store") -> None:
        self.state = AnomalyState(
            severe_anomaly_count=severe_anomaly_count,
            anomaly_count=severe_anomaly_count,
            classification="Extreme Instability" if severe_anomaly_count >= 5 else "Stable",
            source=source,
        )

    def load(self) -> AnomalyState:
        return self.state


def _run_with_valid_portfolio(cycle: LiveRuntimeCycle, **kwargs):
    cycle.portfolio_state_store = _StaticPortfolioStateStore(
        drawdown_percent=kwargs.pop("portfolio_drawdown_percent", 0.0),
        daily_loss_percent=kwargs.pop("daily_loss_percent", 0.0),
    )
    return cycle.run(**kwargs)


# ── Success path ──────────────────────────────────────────────────────────────

class TestLiveRuntimeCycleSuccess:
    def test_returns_snapshot(self, tmp_path):
        cycle = LiveRuntimeCycle()
        with patch("src.runtime.live_runtime_cycle.decision_log_store") as mock_store:
            mock_store.append.return_value = None
            with patch("src.runtime.live_runtime_cycle.runtime_state"):
                with patch("src.runtime.live_runtime_cycle.in_memory_state_cache"):
                    snapshot = _run_with_valid_portfolio(
                        cycle,
                        metrics_map=_make_metrics_map(),
                        vix_data=_make_vix_data(),
                    )
        assert isinstance(snapshot, RuntimeMarketSnapshot)

    def test_snapshot_has_valid_orchestrator_result(self, tmp_path):
        cycle = LiveRuntimeCycle()
        with patch("src.runtime.live_runtime_cycle.decision_log_store") as mock_store, \
             patch("src.runtime.live_runtime_cycle.runtime_state"), \
             patch("src.runtime.live_runtime_cycle.in_memory_state_cache"):
            mock_store.append.return_value = None
            snapshot = _run_with_valid_portfolio(
                cycle,
                metrics_map=_make_metrics_map(),
                vix_data=_make_vix_data(),
            )
        assert snapshot.orchestrator_result.macro_regime != ""
        assert snapshot.orchestrator_result.final_exposure_percent >= 0.0

    def test_decision_is_persisted(self, tmp_path):
        store = DecisionLogStore(path=tmp_path / "log.jsonl")
        cycle = LiveRuntimeCycle()

        with patch("src.runtime.live_runtime_cycle.decision_log_store", store), \
             patch("src.runtime.live_runtime_cycle.runtime_state"), \
             patch("src.runtime.live_runtime_cycle.in_memory_state_cache"):
            _run_with_valid_portfolio(
                cycle,
                metrics_map=_make_metrics_map(),
                vix_data=_make_vix_data(),
            )

        entries = store.load_all()
        assert len(entries) == 1
        assert "macro_regime" in entries[0].payload
        assert entries[0].payload["severe_anomaly_count"] == 0
        assert entries[0].payload["anomaly_state"]["source"] == "anomaly_state_missing"

    def test_runtime_state_updated(self, tmp_path):
        state = RuntimeState()
        cycle = LiveRuntimeCycle()

        with patch("src.runtime.live_runtime_cycle.decision_log_store") as mock_store, \
             patch("src.runtime.live_runtime_cycle.runtime_state", state), \
             patch("src.runtime.live_runtime_cycle.in_memory_state_cache"):
            mock_store.append.return_value = None
            _run_with_valid_portfolio(
                cycle,
                metrics_map=_make_metrics_map(),
                vix_data=_make_vix_data(),
            )

        assert state.cycle_count == 1
        assert state.latest_decision is not None
        assert "macro_regime" in state.latest_decision
        assert state.latest_decision["severe_anomaly_count"] == 0
        assert state.latest_decision["anomaly_state_source"] == "anomaly_state_missing"

    def test_in_memory_cache_updated(self, tmp_path):
        cache = InMemoryStateCache()
        cycle = LiveRuntimeCycle()

        with patch("src.runtime.live_runtime_cycle.decision_log_store") as mock_store, \
             patch("src.runtime.live_runtime_cycle.runtime_state"), \
             patch("src.runtime.live_runtime_cycle.in_memory_state_cache", cache):
            mock_store.append.return_value = None
            _run_with_valid_portfolio(
                cycle,
                metrics_map=_make_metrics_map(),
                vix_data=_make_vix_data(),
            )

        assert cache.get("latest_regime") is not None
        assert cache.get("latest_exposure") is not None
        assert cache.get("latest_snapshot_id") is not None
        assert cache.get("latest_cycle_at") is not None
        assert cache.get("latest_severe_anomaly_count") == 0
        assert cache.get("latest_anomaly_state_source") == "anomaly_state_missing"

    def test_snapshot_cycle_duration_is_tracked(self, tmp_path):
        cycle = LiveRuntimeCycle()
        with patch("src.runtime.live_runtime_cycle.decision_log_store") as mock_store, \
             patch("src.runtime.live_runtime_cycle.runtime_state"), \
             patch("src.runtime.live_runtime_cycle.in_memory_state_cache"):
            mock_store.append.return_value = None
            snapshot = _run_with_valid_portfolio(
                cycle,
                metrics_map=_make_metrics_map(),
                vix_data=_make_vix_data(),
            )
        assert snapshot.cycle_duration_ms > 0.0

    def test_multiple_cycles_accumulate_state(self, tmp_path):
        store = DecisionLogStore(path=tmp_path / "log.jsonl")
        state = RuntimeState()
        cycle = LiveRuntimeCycle()

        with patch("src.runtime.live_runtime_cycle.decision_log_store", store), \
             patch("src.runtime.live_runtime_cycle.runtime_state", state), \
             patch("src.runtime.live_runtime_cycle.in_memory_state_cache"):
            for _ in range(3):
                _run_with_valid_portfolio(
                    cycle,
                    metrics_map=_make_metrics_map(),
                    vix_data=_make_vix_data(),
                )

        assert state.cycle_count == 3
        entries = store.load_all()
        assert len(entries) == 3


# ── Governance paths ──────────────────────────────────────────────────────────

class TestLiveRuntimeCycleGovernance:
    def test_kill_switch_on_extreme_vix_raises(self, tmp_path):
        store = DecisionLogStore(path=tmp_path / "log.jsonl")
        cycle = LiveRuntimeCycle()

        with patch("src.runtime.live_runtime_cycle.decision_log_store", store), \
             patch("src.runtime.live_runtime_cycle.runtime_state"), \
             patch("src.runtime.live_runtime_cycle.in_memory_state_cache"):
            with pytest.raises(GovernanceBlockedError) as exc_info:
                _run_with_valid_portfolio(
                    cycle,
                    metrics_map=_make_metrics_map(),
                    vix_data=_make_vix_data(close=45.0),  # >= 40 triggers kill
                )

        assert "extreme_volatility" in exc_info.value.reasons

    def test_kill_switch_persists_block_entry(self, tmp_path):
        store = DecisionLogStore(path=tmp_path / "log.jsonl")
        cycle = LiveRuntimeCycle()

        with patch("src.runtime.live_runtime_cycle.decision_log_store", store), \
             patch("src.runtime.live_runtime_cycle.runtime_state"), \
             patch("src.runtime.live_runtime_cycle.in_memory_state_cache"):
            with pytest.raises(GovernanceBlockedError):
                _run_with_valid_portfolio(
                    cycle,
                    metrics_map=_make_metrics_map(),
                    vix_data=_make_vix_data(close=45.0),
                )

        entries = store.load_all()
        assert len(entries) == 1
        assert entries[0].payload["type"] == "governance_block"
        assert entries[0].payload["reason"] == "kill_switch"

    def test_drawdown_breach_raises(self, tmp_path):
        store = DecisionLogStore(path=tmp_path / "log.jsonl")
        cycle = LiveRuntimeCycle()

        with patch("src.runtime.live_runtime_cycle.decision_log_store", store), \
             patch("src.runtime.live_runtime_cycle.runtime_state"), \
             patch("src.runtime.live_runtime_cycle.in_memory_state_cache"):
            with pytest.raises(GovernanceBlockedError) as exc_info:
                _run_with_valid_portfolio(
                    cycle,
                    metrics_map=_make_metrics_map(),
                    vix_data=_make_vix_data(close=18.0),
                    portfolio_drawdown_percent=20.0,  # >= 20 → kill switch fires
                    daily_loss_percent=0.0,
                )

        assert "portfolio_drawdown_limit" in exc_info.value.reasons

    def test_persistent_severe_anomaly_count_triggers_market_instability(self, tmp_path):
        store = DecisionLogStore(path=tmp_path / "log.jsonl")
        anomaly_path = tmp_path / "anomaly_state.json"
        anomaly_path.write_text(
            '{"severe_anomaly_count": 5, "anomaly_count": 7, "classification": "Extreme Instability"}',
            encoding="utf-8",
        )
        cycle = LiveRuntimeCycle(anomaly_state_store=AnomalyStateStore(anomaly_path))

        with patch("src.runtime.live_runtime_cycle.decision_log_store", store), \
             patch("src.runtime.live_runtime_cycle.runtime_state"), \
             patch("src.runtime.live_runtime_cycle.in_memory_state_cache"):
            with pytest.raises(GovernanceBlockedError) as exc_info:
                _run_with_valid_portfolio(
                    cycle,
                    metrics_map=_make_metrics_map(),
                    vix_data=_make_vix_data(close=18.0),
                )

        assert "market_instability" in exc_info.value.reasons
        entries = store.load_all()
        assert entries[0].payload["reason"] == "kill_switch"

    def test_cache_is_only_fallback_when_persistent_anomaly_state_missing(self, tmp_path):
        store = DecisionLogStore(path=tmp_path / "log.jsonl")
        cache = InMemoryStateCache()
        cache.set("severe_anomaly_count", 5)
        cycle = LiveRuntimeCycle(anomaly_state_store=AnomalyStateStore(tmp_path / "missing_anomaly_state.json"))

        with patch("src.runtime.live_runtime_cycle.decision_log_store", store), \
             patch("src.runtime.live_runtime_cycle.runtime_state"), \
             patch("src.runtime.live_runtime_cycle.in_memory_state_cache", cache):
            with pytest.raises(GovernanceBlockedError) as exc_info:
                _run_with_valid_portfolio(
                    cycle,
                    metrics_map=_make_metrics_map(),
                    vix_data=_make_vix_data(close=18.0),
                )

        assert "market_instability" in exc_info.value.reasons
        entries = store.load_all()
        assert entries[0].payload["reason"] == "kill_switch"
        assert entries[0].payload["details"] == ["market_instability"]

    def test_missing_portfolio_state_fails_closed(self, tmp_path):
        store = DecisionLogStore(path=tmp_path / "log.jsonl")
        missing_portfolio_store = PortfolioStateStore(tmp_path / "missing_portfolio_state.json")
        cycle = LiveRuntimeCycle(portfolio_state_store=missing_portfolio_store)

        with patch("src.runtime.live_runtime_cycle.decision_log_store", store), \
             patch("src.runtime.live_runtime_cycle.runtime_state"), \
             patch("src.runtime.live_runtime_cycle.in_memory_state_cache"):
            with pytest.raises(GovernanceBlockedError) as exc_info:
                cycle.run(
                    metrics_map=_make_metrics_map(),
                    vix_data=_make_vix_data(close=18.0),
                )

        assert exc_info.value.reasons == ["portfolio_state_invalid_or_missing"]
        entries = store.load_all()
        assert entries[0].payload["reason"] == "portfolio_state_invalid"
        assert entries[0].payload["portfolio_state"]["governance_valid"] is False

    def test_normal_conditions_do_not_raise(self, tmp_path):
        cycle = LiveRuntimeCycle()
        with patch("src.runtime.live_runtime_cycle.decision_log_store") as mock_store, \
             patch("src.runtime.live_runtime_cycle.runtime_state"), \
             patch("src.runtime.live_runtime_cycle.in_memory_state_cache"):
            mock_store.append.return_value = None
            # Should not raise when portfolio state comes from a trusted store.
            snapshot = _run_with_valid_portfolio(
                cycle,
                metrics_map=_make_metrics_map(),
                vix_data=_make_vix_data(close=18.0),
                portfolio_drawdown_percent=5.0,
                daily_loss_percent=1.0,
            )
        assert snapshot is not None

    def test_runtime_portfolio_argument_override_fails_closed(self, tmp_path):
        store = DecisionLogStore(path=tmp_path / "log.jsonl")
        cycle = LiveRuntimeCycle()

        with patch("src.runtime.live_runtime_cycle.decision_log_store", store), \
             patch("src.runtime.live_runtime_cycle.runtime_state"), \
             patch("src.runtime.live_runtime_cycle.in_memory_state_cache"):
            with pytest.raises(GovernanceBlockedError) as exc_info:
                cycle.run(
                    metrics_map=_make_metrics_map(),
                    vix_data=_make_vix_data(close=18.0),
                    portfolio_drawdown_percent=0.0,
                    daily_loss_percent=0.0,
                )

        assert exc_info.value.reasons == ["portfolio_state_invalid_or_missing"]
        entries = store.load_all()
        assert entries[0].payload["portfolio_state"]["source"] == "runtime_argument_override_rejected"
        assert entries[0].payload["portfolio_state"]["governance_valid"] is False

    def test_governance_block_error_carries_reasons(self):
        err = GovernanceBlockedError(["extreme_volatility", "market_instability"])
        assert "extreme_volatility" in err.reasons
        assert "market_instability" in err.reasons
        assert "extreme_volatility" in str(err)