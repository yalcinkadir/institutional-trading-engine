from __future__ import annotations

import json
from pathlib import Path

import scripts.generate_report as generate_report


def _decision(symbol: str = "SPY") -> dict:
    return {
        "symbol": symbol,
        "decision": "approved",
        "setup_type": "momentum_continuation",
        "risk_tier": "A",
        "position_size_multiplier": 1.0,
        "setup_score": 82.0,
        "base_setup_score": 82.0,
        "regime_alignment": 1.0,
        "asymmetry_score": 75.0,
        "data_confidence": "high",
        "blocked_reasons": [],
        "notes": [],
    }


def _decision_report() -> dict:
    return {
        "market_state": "bullish",
        "portfolio_heat_limit": 1.0,
        "approved_count": 1,
        "blocked_count": 0,
        "hard_overrides": [],
        "expectancy_adjustments_used": [],
        "allowed_setups": ["momentum_continuation"],
        "summary": "One approved opportunity before runtime governance.",
        "decisions": [_decision()],
    }


def _patch_report_dependencies(monkeypatch) -> None:
    monkeypatch.setattr(
        generate_report,
        "build_market_regime_summary",
        lambda report_type: {"regime": "Bullish", "data_status": "OK", "market_health_score": 80, "symbols": {}, "focus_areas": []},
    )
    monkeypatch.setattr(generate_report, "build_screener_snapshot", lambda report_type: {"title": "Test Screener", "watchlist": [], "objectives": [], "warnings": []})
    monkeypatch.setattr(generate_report, "build_cross_asset_report", lambda: {"data_status": "OK", "regime": "risk_on", "risk_score": 70, "risk_on_score": 70, "risk_off_score": 30})
    monkeypatch.setattr(generate_report, "build_decision_report", lambda *, market_regime, screener: _decision_report())


def test_p149_kill_switch_blocks_active_report_path_before_actionable_output(monkeypatch) -> None:
    monkeypatch.setenv("ITE_KILL_SWITCH_ACTIVE", "true")
    _patch_report_dependencies(monkeypatch)

    report, decision_payload = generate_report.build_report("premarket")

    assert decision_payload is not None
    governance = decision_payload["governance_state"]
    assert governance["governance_status"] == "BLOCKED"
    assert governance["kill_switch_active"] is True
    assert "kill_switch_active" in governance["reasons"]
    assert governance["active_path"] == "scripts/generate_report.py::_build_market_payload"
    assert decision_payload["signal_generation_status"] == "BLOCKED_GOVERNANCE"
    assert decision_payload["run_health"]["run_health_status"] == "GOVERNANCE_BLOCKED"
    assert all(item["decision"] == "blocked" for item in decision_payload["decision_report"]["decisions"])
    assert all(item["position_size_multiplier"] == 0.0 for item in decision_payload["decision_report"]["decisions"])
    assert "BUY_WATCH" not in report


def test_p149_governance_state_is_visible_in_report_artifact(monkeypatch) -> None:
    monkeypatch.setenv("ITE_KILL_SWITCH_ACTIVE", "true")
    _patch_report_dependencies(monkeypatch)

    report, _ = generate_report.build_report("premarket")

    assert "Governance Status: BLOCKED" in report
    assert "Governance Stage: active_report_path_governance" in report
    assert "Governance Active Path: scripts/generate_report.py::_build_market_payload" in report
    assert "Kill Switch Active: True" in report
    assert "Live Trading Authorized: False" in report
    assert "Broker Execution Mode: paper_only" in report
    assert "Governance Reasons: kill_switch_active" in report


def test_p149_governance_state_is_persisted_to_signal_artifact(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("ITE_KILL_SWITCH_ACTIVE", "true")
    _patch_report_dependencies(monkeypatch)

    _, decision_payload = generate_report.build_report("premarket")

    from src.signals.signal_generator import save_signals

    json_path, _ = save_signals(
        decision_payload["signals"],
        date_str="2026-06-08",
        signals_dir=tmp_path,
        governance_state=decision_payload["governance_state"],
    )
    latest_payload = json.loads((tmp_path / "latest-signals.json").read_text(encoding="utf-8"))
    dated_payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert latest_payload == dated_payload
    assert latest_payload["governance_state"]["governance_status"] == "BLOCKED"
    assert latest_payload["governance_state"]["kill_switch_active"] is True
    assert latest_payload["governance_state"]["live_trading_authorized"] is False
    assert latest_payload["actionable_count"] == 0
    assert latest_payload["signals"] == []
