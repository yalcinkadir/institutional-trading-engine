from src.validation.execution_kill_switch import (
    ExecutionKillSwitchConfig,
    ExecutionKillSwitchStatus,
    evaluate_execution_kill_switch,
)


def _daily_report():
    return {
        "passed": True,
        "status": "PASS",
        "metrics": {"total_r_drift": 0.0, "matched_count": 1},
        "issues": [],
    }


def _fill_report():
    return {
        "passed": True,
        "status": "PASS",
        "metrics": {"avg_abs_slippage_bps": 5.0, "fill_rate": 1.0},
        "issues": [],
    }


def _drawdown_source(account_equity: float, drawdown_pct: float):
    return {
        "source_name": "paper_account_equity",
        "source_type": "reconciled_paper_equity",
        "account_equity": account_equity,
        "peak_equity": 100000.0,
        "drawdown_pct": drawdown_pct,
        "is_reconciled": True,
        "evidence_artifact": "reports/paper_equity/reconciled_equity.json",
        "validated_at": "2026-05-29T10:00:00Z",
    }


def test_ev12_blocks_validated_drawdown_above_block_threshold():
    decision = evaluate_execution_kill_switch(
        daily_reconciliation_report=_daily_report(),
        fill_quality_report=_fill_report(),
        drawdown_source_validation=_drawdown_source(account_equity=89000.0, drawdown_pct=11.0),
        config=ExecutionKillSwitchConfig(max_drawdown_pct=10.0, watch_drawdown_pct=7.5),
    )

    assert decision.status == ExecutionKillSwitchStatus.BLOCK
    assert decision.blocked
    assert any(reason.code == "drawdown_block_threshold_exceeded" for reason in decision.reasons)


def test_ev12_watches_validated_drawdown_between_watch_and_block_threshold():
    decision = evaluate_execution_kill_switch(
        daily_reconciliation_report=_daily_report(),
        fill_quality_report=_fill_report(),
        drawdown_source_validation=_drawdown_source(account_equity=92000.0, drawdown_pct=8.0),
        config=ExecutionKillSwitchConfig(max_drawdown_pct=10.0, watch_drawdown_pct=7.5),
    )

    assert decision.status == ExecutionKillSwitchStatus.WATCH
    assert not decision.blocked
    assert any(reason.code == "drawdown_watch_threshold_exceeded" for reason in decision.reasons)
    assert "drawdown_magnitude_checked" in decision.notes


def test_ev12_does_not_apply_magnitude_gate_when_drawdown_calculation_is_invalid():
    decision = evaluate_execution_kill_switch(
        daily_reconciliation_report=_daily_report(),
        fill_quality_report=_fill_report(),
        drawdown_source_validation=_drawdown_source(account_equity=89000.0, drawdown_pct=5.0),
        config=ExecutionKillSwitchConfig(max_drawdown_pct=10.0, watch_drawdown_pct=7.5),
    )

    codes = {reason.code for reason in decision.reasons}
    assert decision.status == ExecutionKillSwitchStatus.BLOCK
    assert "drawdown_calculation_mismatch" in codes
    assert "drawdown_block_threshold_exceeded" not in codes
