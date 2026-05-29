from src.notifications.telegram_report_dispatcher import TelegramDispatchConfig, dispatch_telegram_report
from src.operations.evidence_operation_discipline import build_evidence_operation_record, render_evidence_operation_markdown
from src.reporting.tg2_tg3_report_templates import build_tg2_tg3_report_templates, build_telegram_message_from_template


def _daily_report(passed=True):
    return {
        "passed": passed,
        "metrics": {"overall_status": "PASS" if passed else "FAIL", "components_expected": 6, "components_present": 6, "components_failed": 0, "components_missing": 0},
        "components": [{"name": "reconciliation", "status": "PASS" if passed else "FAIL", "passed": passed}],
    }


def _payloads():
    return {
        "daily_evidence": _daily_report(),
        "fill_quality": {"passed": True, "status": "PASS", "metrics": {"record_count": 2, "fill_rate": 1.0, "avg_abs_slippage_bps": 3.2}},
        "kill_switch": {"status": "ALLOW", "blocked": False, "reasons": []},
        "backtest_summary": {"passed": True, "metrics": {"trade_count": 40, "expectancy_r": 0.22, "max_drawdown_r": 2.4, "oos_pass_rate": 0.7}},
    }


def test_tg2_tg3_templates_render_research_only_footer_and_safe_messages():
    templates = build_tg2_tg3_report_templates(_payloads(), report_date="2026-05-29")

    assert {template.report_type.value for template in templates} == {"daily_evidence", "fill_quality", "kill_switch", "backtest_summary"}
    for template in templates:
        message = build_telegram_message_from_template(template)
        result = dispatch_telegram_report(message, config=TelegramDispatchConfig(dry_run=True))
        assert result.status.value == "DRY_RUN"
        assert not result.findings
        assert "No live trading authorization" in result.message


def test_b11_operation_record_passes_with_daily_evidence_templates_and_tg2_dry_runs():
    templates = build_tg2_tg3_report_templates(_payloads(), report_date="2026-05-29")
    dispatches = [
        dispatch_telegram_report(build_telegram_message_from_template(template), config=TelegramDispatchConfig(dry_run=True)).to_dict()
        for template in templates
    ]

    record = build_evidence_operation_record(
        observation_date="2026-05-29",
        daily_evidence_report=_daily_report(),
        report_templates=templates,
        telegram_dispatch_results=dispatches,
    )

    assert record.passed is True
    assert record.status.value == "PASS"
    markdown = render_evidence_operation_markdown(record)
    assert "B1.1 Evidence Operation Discipline" in markdown
    assert "no_live_trading_authorization" in markdown


def test_b11_operation_record_fails_when_daily_reconciliation_fails():
    templates = build_tg2_tg3_report_templates(_payloads(), report_date="2026-05-29")

    record = build_evidence_operation_record(
        observation_date="2026-05-29",
        daily_evidence_report=_daily_report(passed=False),
        report_templates=templates,
    )

    assert record.passed is False
    failed_gate_names = {gate.name for gate in record.gates if not gate.passed}
    assert "daily_evidence_passed" in failed_gate_names
    assert "reconciliation_component_passed" in failed_gate_names


def test_b11_operation_record_rejects_live_mode():
    templates = build_tg2_tg3_report_templates(_payloads(), report_date="2026-05-29")

    record = build_evidence_operation_record(
        observation_date="2026-05-29",
        observation_mode="live_trading",
        daily_evidence_report=_daily_report(),
        report_templates=templates,
    )

    assert record.passed is False
    mode_gate = next(gate for gate in record.gates if gate.name == "observation_only_mode")
    assert mode_gate.passed is False
