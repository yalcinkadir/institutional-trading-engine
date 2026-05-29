import json

from src.validation.execution_kill_switch import (
    DrawdownSourceType,
    DrawdownSourceValidation,
    ExecutionKillSwitchConfig,
    ExecutionKillSwitchSeverity,
    ExecutionKillSwitchStatus,
    ManualRiskFlag,
    evaluate_execution_kill_switch,
    load_kill_switch_input,
    write_execution_kill_switch_decision,
)


def _daily_report(**overrides):
    payload = {
        "passed": True,
        "status": "PASS",
        "metrics": {
            "total_r_drift": 0.0,
            "matched_count": 1,
        },
        "issues": [],
    }
    payload.update(overrides)
    return payload


def _fill_report(**overrides):
    payload = {
        "passed": True,
        "status": "PASS",
        "metrics": {
            "avg_abs_slippage_bps": 5.0,
            "fill_rate": 1.0,
        },
        "issues": [],
    }
    payload.update(overrides)
    return payload


def _drawdown_source(**overrides):
    payload = {
        "source_name": "paper_account_equity",
        "source_type": "reconciled_paper_equity",
        "account_equity": 95000.0,
        "peak_equity": 100000.0,
        "drawdown_pct": 5.0,
        "is_reconciled": True,
        "evidence_artifact": "reports/paper_equity/reconciled_equity.json",
        "validated_at": "2026-05-29T10:00:00Z",
    }
    payload.update(overrides)
    return payload


def test_kill_switch_allows_clean_daily_fill_quality_and_drawdown_source_reports():
    decision = evaluate_execution_kill_switch(
        daily_reconciliation_report=_daily_report(),
        fill_quality_report=_fill_report(),
        drawdown_source_validation=_drawdown_source(),
    )

    assert decision.status == ExecutionKillSwitchStatus.ALLOW
    assert not decision.blocked
    assert decision.reasons == []
    assert "does_not_submit_orders" in decision.notes
    assert "drawdown_source_validated" in decision.notes


def test_kill_switch_blocks_when_required_reports_are_missing():
    decision = evaluate_execution_kill_switch()

    codes = {reason.code for reason in decision.reasons}
    assert decision.status == ExecutionKillSwitchStatus.BLOCK
    assert decision.blocked
    assert "missing_daily_reconciliation_report" in codes
    assert "missing_fill_quality_report" in codes
    assert "missing_drawdown_source_validation" in codes


def test_kill_switch_blocks_failed_daily_reconciliation():
    decision = evaluate_execution_kill_switch(
        daily_reconciliation_report=_daily_report(passed=False, status="FAIL"),
        fill_quality_report=_fill_report(),
        drawdown_source_validation=_drawdown_source(),
    )

    assert decision.status == ExecutionKillSwitchStatus.BLOCK
    assert any(reason.code == "daily_reconciliation_failed" for reason in decision.reasons)


def test_kill_switch_blocks_failed_fill_quality():
    decision = evaluate_execution_kill_switch(
        daily_reconciliation_report=_daily_report(),
        fill_quality_report=_fill_report(passed=False, status="FAIL"),
        drawdown_source_validation=_drawdown_source(),
    )

    assert decision.status == ExecutionKillSwitchStatus.BLOCK
    assert any(reason.code == "fill_quality_failed" for reason in decision.reasons)


def test_kill_switch_blocks_total_r_drift_above_block_threshold():
    decision = evaluate_execution_kill_switch(
        daily_reconciliation_report=_daily_report(metrics={"total_r_drift": -0.8}),
        fill_quality_report=_fill_report(),
        drawdown_source_validation=_drawdown_source(),
    )

    assert decision.status == ExecutionKillSwitchStatus.BLOCK
    assert any(reason.code == "total_r_drift_block_threshold_exceeded" for reason in decision.reasons)


def test_kill_switch_watches_total_r_drift_between_watch_and_block_threshold():
    decision = evaluate_execution_kill_switch(
        daily_reconciliation_report=_daily_report(metrics={"total_r_drift": 0.3}),
        fill_quality_report=_fill_report(),
        drawdown_source_validation=_drawdown_source(),
    )

    assert decision.status == ExecutionKillSwitchStatus.WATCH
    assert not decision.blocked
    assert any(reason.code == "total_r_drift_watch_threshold_exceeded" for reason in decision.reasons)


def test_kill_switch_blocks_avg_slippage_above_block_threshold():
    decision = evaluate_execution_kill_switch(
        daily_reconciliation_report=_daily_report(),
        fill_quality_report=_fill_report(metrics={"avg_abs_slippage_bps": 30.0, "fill_rate": 1.0}),
        drawdown_source_validation=_drawdown_source(),
    )

    assert decision.status == ExecutionKillSwitchStatus.BLOCK
    assert any(reason.code == "avg_abs_slippage_block_threshold_exceeded" for reason in decision.reasons)


def test_kill_switch_watches_slippage_and_fill_rate_degradation():
    decision = evaluate_execution_kill_switch(
        daily_reconciliation_report=_daily_report(),
        fill_quality_report=_fill_report(metrics={"avg_abs_slippage_bps": 17.0, "fill_rate": 0.9}),
        drawdown_source_validation=_drawdown_source(),
    )

    codes = {reason.code for reason in decision.reasons}
    assert decision.status == ExecutionKillSwitchStatus.WATCH
    assert not decision.blocked
    assert "avg_abs_slippage_watch_threshold_exceeded" in codes
    assert "fill_rate_watch_threshold_breached" in codes


def test_kill_switch_blocks_manual_error_flags_and_watches_manual_warning_flags():
    block_decision = evaluate_execution_kill_switch(
        daily_reconciliation_report=_daily_report(),
        fill_quality_report=_fill_report(),
        drawdown_source_validation=_drawdown_source(),
        manual_risk_flags=[ManualRiskFlag(code="broker_incident", message="broker incident")],
    )
    watch_decision = evaluate_execution_kill_switch(
        daily_reconciliation_report=_daily_report(),
        fill_quality_report=_fill_report(),
        drawdown_source_validation=_drawdown_source(),
        manual_risk_flags=[{"code": "latency_watch", "message": "latency elevated", "severity": "warning"}],
    )

    assert block_decision.status == ExecutionKillSwitchStatus.BLOCK
    assert any(reason.code == "broker_incident" for reason in block_decision.reasons)
    assert watch_decision.status == ExecutionKillSwitchStatus.WATCH
    assert any(reason.severity == ExecutionKillSwitchSeverity.WARNING for reason in watch_decision.reasons)


def test_kill_switch_can_run_with_optional_reports_disabled():
    decision = evaluate_execution_kill_switch(
        config=ExecutionKillSwitchConfig(
            require_daily_reconciliation_report=False,
            require_fill_quality_report=False,
            require_drawdown_source_validation=False,
        )
    )

    assert decision.status == ExecutionKillSwitchStatus.ALLOW
    assert not decision.blocked


def test_kill_switch_blocks_backtest_only_drawdown_source():
    decision = evaluate_execution_kill_switch(
        daily_reconciliation_report=_daily_report(),
        fill_quality_report=_fill_report(),
        drawdown_source_validation=_drawdown_source(source_type="backtest_only"),
    )

    assert decision.status == ExecutionKillSwitchStatus.BLOCK
    assert any(reason.code == "invalid_drawdown_source_type" for reason in decision.reasons)


def test_kill_switch_blocks_unreconciled_drawdown_source():
    decision = evaluate_execution_kill_switch(
        daily_reconciliation_report=_daily_report(),
        fill_quality_report=_fill_report(),
        drawdown_source_validation=_drawdown_source(is_reconciled=False),
    )

    assert decision.status == ExecutionKillSwitchStatus.BLOCK
    assert any(reason.code == "unreconciled_drawdown_source" for reason in decision.reasons)


def test_kill_switch_blocks_drawdown_calculation_mismatch():
    decision = evaluate_execution_kill_switch(
        daily_reconciliation_report=_daily_report(),
        fill_quality_report=_fill_report(),
        drawdown_source_validation=_drawdown_source(drawdown_pct=1.0),
    )

    assert decision.status == ExecutionKillSwitchStatus.BLOCK
    assert any(reason.code == "drawdown_calculation_mismatch" for reason in decision.reasons)


def test_kill_switch_accepts_drawdown_source_validation_dataclass():
    validation = DrawdownSourceValidation(
        source_name="broker_equity",
        source_type=DrawdownSourceType.BROKER_EQUITY,
        account_equity=99000.0,
        peak_equity=100000.0,
        drawdown_pct=1.0,
        is_reconciled=True,
        evidence_artifact="reports/broker/reconciled_equity.json",
    )

    decision = evaluate_execution_kill_switch(
        daily_reconciliation_report=_daily_report(),
        fill_quality_report=_fill_report(),
        drawdown_source_validation=validation,
    )

    assert decision.status == ExecutionKillSwitchStatus.ALLOW
    assert "drawdown_source_validated" in decision.notes


def test_kill_switch_loads_input_and_writes_decision(tmp_path):
    input_file = tmp_path / "kill_switch_input.json"
    output_dir = tmp_path / "out"
    input_file.write_text(
        json.dumps(
            {
                "daily_reconciliation_report": _daily_report(),
                "fill_quality_report": _fill_report(),
                "drawdown_source_validation": _drawdown_source(),
                "manual_risk_flags": [],
            }
        ),
        encoding="utf-8",
    )

    payload = load_kill_switch_input(input_file)
    decision = evaluate_execution_kill_switch(
        daily_reconciliation_report=payload["daily_reconciliation_report"],
        fill_quality_report=payload["fill_quality_report"],
        drawdown_source_validation=payload["drawdown_source_validation"],
        manual_risk_flags=payload["manual_risk_flags"],
    )
    write_execution_kill_switch_decision(
        decision,
        json_path=output_dir / "execution_kill_switch_decision.json",
        markdown_path=output_dir / "execution_kill_switch_decision.md",
    )

    assert decision.status == ExecutionKillSwitchStatus.ALLOW
    assert (output_dir / "execution_kill_switch_decision.json").exists()
    assert "# C7 Execution Kill Switch Decision" in (output_dir / "execution_kill_switch_decision.md").read_text(encoding="utf-8")
