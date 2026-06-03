from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from src.runtime.live_runtime_cycle import GovernanceBlockedError, LiveRuntimeCycle
from src.runtime.portfolio_state import PortfolioStateStore


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
    return {
        "SPY": {**base, "symbol": "SPY"},
        "QQQ": {**base, "symbol": "QQQ", "benchmark": "QQQ"},
    }


def _make_vix_data(close: float = 16.5) -> dict:
    return {"close": close, "direction": "Falling"}


def _write_portfolio_state(
    path: Path,
    drawdown_percent: float,
    daily_loss_percent: float,
) -> None:
    path.write_text(
        json.dumps(
            {
                "equity_start": 10000.0,
                "equity_current": 9500.0,
                "drawdown_percent": drawdown_percent,
                "daily_loss_percent": daily_loss_percent,
                "open_positions": [],
                "updated_at": "2026-05-20T22:00:00+02:00",
                "governance_valid": True,
            }
        ),
        encoding="utf-8",
    )


def test_live_cycle_persists_loaded_portfolio_state(tmp_path: Path) -> None:
    portfolio_path = tmp_path / "portfolio_state.json"
    _write_portfolio_state(
        portfolio_path,
        drawdown_percent=-2.5,
        daily_loss_percent=-0.7,
    )
    cycle = LiveRuntimeCycle(portfolio_state_store=PortfolioStateStore(portfolio_path))

    with patch("src.runtime.live_runtime_cycle.decision_log_store") as mock_store, \
         patch("src.runtime.live_runtime_cycle.runtime_state"), \
         patch("src.runtime.live_runtime_cycle.in_memory_state_cache"):
        mock_store.append.return_value = None
        cycle.run(metrics_map=_make_metrics_map(), vix_data=_make_vix_data())

    payload = mock_store.append.call_args.kwargs["payload"]
    assert payload["portfolio_state"]["drawdown_percent"] == -2.5
    assert payload["portfolio_state"]["daily_loss_percent"] == -0.7
    assert payload["portfolio_state"]["source"] == "portfolio_state_json"


def test_live_cycle_emits_structured_logs_for_success(tmp_path: Path) -> None:
    portfolio_path = tmp_path / "portfolio_state.json"
    _write_portfolio_state(
        portfolio_path,
        drawdown_percent=-2.5,
        daily_loss_percent=-0.7,
    )
    cycle = LiveRuntimeCycle(portfolio_state_store=PortfolioStateStore(portfolio_path))
    events: list[dict] = []

    def fake_log(**kwargs):
        events.append(kwargs)

    with patch("src.runtime.live_runtime_cycle.decision_log_store") as mock_store, \
         patch("src.runtime.live_runtime_cycle.runtime_state"), \
         patch("src.runtime.live_runtime_cycle.in_memory_state_cache"), \
         patch("src.runtime.live_runtime_cycle.emit_structured_log", side_effect=fake_log):
        mock_store.append.return_value = None
        cycle.run(metrics_map=_make_metrics_map(), vix_data=_make_vix_data())

    event_types = [event["event_type"] for event in events]
    assert "live_runtime_cycle_started" in event_types
    assert "live_runtime_governance_passed" in event_types
    assert "live_runtime_cycle_completed" in event_types
    assert all(event["component"] == "live_runtime_cycle" for event in events)
    completed = [event for event in events if event["event_type"] == "live_runtime_cycle_completed"][0]
    assert "final_exposure_percent" in completed["context"]


def test_live_cycle_blocks_from_portfolio_state_drawdown(tmp_path: Path) -> None:
    portfolio_path = tmp_path / "portfolio_state.json"
    _write_portfolio_state(
        portfolio_path,
        drawdown_percent=20.0,
        daily_loss_percent=0.0,
    )
    cycle = LiveRuntimeCycle(portfolio_state_store=PortfolioStateStore(portfolio_path))

    with patch("src.runtime.live_runtime_cycle.decision_log_store") as mock_store, \
         patch("src.runtime.live_runtime_cycle.runtime_state"), \
         patch("src.runtime.live_runtime_cycle.in_memory_state_cache"):
        mock_store.append.return_value = None
        with pytest.raises(GovernanceBlockedError) as exc_info:
            cycle.run(metrics_map=_make_metrics_map(), vix_data=_make_vix_data())

    assert "portfolio_drawdown_limit" in exc_info.value.reasons
    block_payload = mock_store.append.call_args.kwargs["payload"]
    assert block_payload["type"] == "governance_block"
    assert block_payload["portfolio_state"]["drawdown_percent"] == 20.0


def test_live_cycle_emits_structured_log_for_governance_block(tmp_path: Path) -> None:
    portfolio_path = tmp_path / "portfolio_state.json"
    _write_portfolio_state(
        portfolio_path,
        drawdown_percent=20.0,
        daily_loss_percent=0.0,
    )
    cycle = LiveRuntimeCycle(portfolio_state_store=PortfolioStateStore(portfolio_path))
    events: list[dict] = []

    def fake_log(**kwargs):
        events.append(kwargs)

    with patch("src.runtime.live_runtime_cycle.decision_log_store") as mock_store, \
         patch("src.runtime.live_runtime_cycle.runtime_state"), \
         patch("src.runtime.live_runtime_cycle.in_memory_state_cache"), \
         patch("src.runtime.live_runtime_cycle.emit_structured_log", side_effect=fake_log):
        mock_store.append.return_value = None
        with pytest.raises(GovernanceBlockedError):
            cycle.run(metrics_map=_make_metrics_map(), vix_data=_make_vix_data())

    event_types = [event["event_type"] for event in events]
    assert "live_runtime_cycle_started" in event_types
    assert "live_runtime_governance_blocked" in event_types
    blocked = [event for event in events if event["event_type"] == "live_runtime_governance_blocked"][0]
    assert blocked["level"] == "ERROR"
    assert blocked["context"]["reason"] == "kill_switch"
    assert blocked["context"]["portfolio_drawdown_percent"] == 20.0


def test_live_cycle_blocks_from_portfolio_state_daily_loss(tmp_path: Path) -> None:
    portfolio_path = tmp_path / "portfolio_state.json"
    _write_portfolio_state(
        portfolio_path,
        drawdown_percent=0.0,
        daily_loss_percent=5.0,
    )
    cycle = LiveRuntimeCycle(portfolio_state_store=PortfolioStateStore(portfolio_path))

    with patch("src.runtime.live_runtime_cycle.decision_log_store") as mock_store, \
         patch("src.runtime.live_runtime_cycle.runtime_state"), \
         patch("src.runtime.live_runtime_cycle.in_memory_state_cache"):
        mock_store.append.return_value = None
        with pytest.raises(GovernanceBlockedError) as exc_info:
            cycle.run(metrics_map=_make_metrics_map(), vix_data=_make_vix_data())

    assert "max_daily_loss_breached" in exc_info.value.reasons
    block_payload = mock_store.append.call_args.kwargs["payload"]
    assert block_payload["type"] == "governance_block"
    assert block_payload["portfolio_state"]["daily_loss_percent"] == 5.0


def test_live_cycle_runtime_arguments_are_rejected_as_untrusted_state(tmp_path: Path) -> None:
    portfolio_path = tmp_path / "portfolio_state.json"
    _write_portfolio_state(
        portfolio_path,
        drawdown_percent=0.0,
        daily_loss_percent=0.0,
    )
    cycle = LiveRuntimeCycle(portfolio_state_store=PortfolioStateStore(portfolio_path))

    with patch("src.runtime.live_runtime_cycle.decision_log_store") as mock_store, \
         patch("src.runtime.live_runtime_cycle.runtime_state"), \
         patch("src.runtime.live_runtime_cycle.in_memory_state_cache"):
        mock_store.append.return_value = None
        with pytest.raises(GovernanceBlockedError) as exc_info:
            cycle.run(
                metrics_map=_make_metrics_map(),
                vix_data=_make_vix_data(),
                portfolio_drawdown_percent=1.0,
                daily_loss_percent=0.5,
            )

    assert exc_info.value.reasons == ["portfolio_state_invalid_or_missing"]
    payload = mock_store.append.call_args.kwargs["payload"]
    assert payload["portfolio_state"]["drawdown_percent"] == 1.0
    assert payload["portfolio_state"]["daily_loss_percent"] == 0.5
    assert payload["portfolio_state"]["source"] == "runtime_argument_override_rejected"
    assert payload["portfolio_state"]["governance_valid"] is False
