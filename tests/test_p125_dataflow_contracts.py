from __future__ import annotations

from types import SimpleNamespace

import pytest

from scripts.validate_dataflow_contracts import (
    ContractViolation,
    validate_backtest_evidence_contract,
    validate_decision_report_contract,
    validate_paper_observation_contract,
    validate_signal_contract,
)


def test_p125_signal_contract_rejects_missing_symbol() -> None:
    signal = SimpleNamespace(
        signal_id="sig_1",
        symbol="",
        action="BUY_WATCH",
        setup_type="momentum",
        decision="approved",
        market_regime="Bullish",
        generated_at="2026-06-07T10:00:00Z",
        data_status="OK",
        source="polygon",
        source_timestamp="2026-06-07T09:59:00Z",
        fallback_level="primary",
        entry_trigger=101.0,
        stop_loss=99.0,
        target_1=104.0,
    )

    with pytest.raises(ContractViolation) as exc:
        validate_signal_contract(signal)

    assert "symbol" in exc.value.report.invalid_fields


def test_p125_signal_contract_rejects_buy_watch_without_entry() -> None:
    signal = SimpleNamespace(
        signal_id="sig_1",
        symbol="SPY",
        action="BUY_WATCH",
        setup_type="momentum",
        decision="approved",
        market_regime="Bullish",
        generated_at="2026-06-07T10:00:00Z",
        data_status="OK",
        source="polygon",
        source_timestamp="2026-06-07T09:59:00Z",
        fallback_level="primary",
        entry_trigger=None,
        stop_loss=99.0,
        target_1=104.0,
    )

    with pytest.raises(ContractViolation) as exc:
        validate_signal_contract(signal)

    assert "entry_trigger" in exc.value.report.invalid_fields


def test_p125_decision_report_requires_run_health() -> None:
    payload = {
        "market_state": "LOW_VOL_BULL",
        "summary": "ok",
        "scanner_data_quality": {"data_quality_status": "OK"},
        "signal_generation_status": "PASSED",
        "decisions": [],
    }

    with pytest.raises(ContractViolation) as exc:
        validate_decision_report_contract(payload)

    assert "run_health" in exc.value.report.missing_fields


def test_p125_paper_observation_requires_health_gate() -> None:
    payload = {
        "timestamp_utc": "2026-06-07T10:00:00Z",
        "ready_for_review": True,
        "universe": ["SPY"],
        "signal_ids": ["sig_1"],
        "decision_status": {"approved": 1},
        "data_quality_status": "OK",
        "provenance": [{"symbol": "SPY", "source": "polygon"}],
        "gates": [],
    }

    with pytest.raises(ContractViolation) as exc:
        validate_paper_observation_contract(payload)

    assert "paper_observation_health_gate" in exc.value.report.invalid_fields


def test_p125_backtest_evidence_requires_health_fields() -> None:
    payload = {
        "run_id": "bt_1",
        "data_source": "real_data",
        "symbol_universe": ["SPY"],
        "date_range": {"start": "2026-06-01", "end": "2026-06-02"},
        "strategy_version": "v1",
        "input_pack_gate_status": "PASSED",
        "input_plan_count": 1,
        "accepted_plan_count": 1,
        "rejected_plan_count": 0,
        "metrics": {"total": 1},
        "results": [{"signal_id": "sig_1"}],
    }

    with pytest.raises(ContractViolation) as exc:
        validate_backtest_evidence_contract(payload)

    assert "input_completeness_status" in exc.value.report.missing_fields
    assert "run_health_status" in exc.value.report.missing_fields
