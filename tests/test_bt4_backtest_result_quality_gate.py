from __future__ import annotations

import json

from src.validation.backtest_result_quality_gate import (
    RESEARCH_ONLY_FOOTER,
    BacktestResultQualityConfig,
    build_backtest_result_quality_report,
    demo_backtest_result_quality_cases,
    load_backtest_result_quality_json,
    render_backtest_result_quality_markdown,
    write_backtest_result_quality_report,
)


def _payloads():
    return [case.to_dict() for case in demo_backtest_result_quality_cases()]


def _first_gate(report, name: str, *, passed: bool | None = None):
    for gate in report.gates:
        if gate.name == name and (passed is None or gate.passed is passed):
            return gate
    raise AssertionError(f"Gate not found: {name}")


def test_demo_quality_cases_pass_all_gates():
    report = build_backtest_result_quality_report(demo_backtest_result_quality_cases(), generated_at="2026-05-29T00:00:00Z")

    assert report.passed is True
    assert report.metrics.case_count == 2
    assert report.metrics.passing_case_count == 2
    assert report.metrics.failing_case_count == 0
    assert all(gate.passed for gate in report.gates)


def test_empty_case_set_fails_closed():
    report = build_backtest_result_quality_report([])

    assert report.passed is False
    assert _first_gate(report, "non_empty_quality_case_set", passed=False).passed is False


def test_missing_identity_field_fails_gate():
    payloads = _payloads()
    payloads[0]["contract_version"] = ""

    report = build_backtest_result_quality_report(payloads)

    gate = _first_gate(report, "required_fields_complete", passed=False)
    assert report.passed is False
    assert "contract_version" in gate.failures[0]


def test_minimum_trade_count_gate_fails():
    payloads = _payloads()
    payloads[0]["trade_count"] = 12

    report = build_backtest_result_quality_report(payloads)

    gate = _first_gate(report, "minimum_trade_count", passed=False)
    assert "trade_count" in gate.failures[0]


def test_drawdown_gate_fails_when_too_deep():
    payloads = _payloads()
    payloads[0]["max_drawdown_pct"] = -18.0

    report = build_backtest_result_quality_report(payloads)

    gate = _first_gate(report, "max_drawdown_limit", passed=False)
    assert "drawdown" in gate.failures[0]


def test_expectancy_gate_fails_when_too_small():
    payloads = _payloads()
    payloads[0]["expectancy_r"] = 0.01

    report = build_backtest_result_quality_report(payloads)

    gate = _first_gate(report, "positive_expectancy", passed=False)
    assert "expectancy" in gate.failures[0]


def test_profit_factor_gate_fails():
    payloads = _payloads()
    payloads[0]["profit_factor"] = 1.02

    report = build_backtest_result_quality_report(payloads)

    gate = _first_gate(report, "minimum_profit_factor", passed=False)
    assert "profit_factor" in gate.failures[0]


def test_sharpe_gate_fails():
    payloads = _payloads()
    payloads[0]["sharpe"] = 0.2

    report = build_backtest_result_quality_report(payloads)

    gate = _first_gate(report, "minimum_sharpe", passed=False)
    assert "sharpe" in gate.failures[0]


def test_loss_rate_gate_fails():
    payloads = _payloads()
    payloads[0]["loss_rate_pct"] = 61.0

    report = build_backtest_result_quality_report(payloads)

    gate = _first_gate(report, "max_loss_rate", passed=False)
    assert "loss_rate" in gate.failures[0]


def test_regime_split_gate_fails_when_missing():
    payloads = _payloads()
    payloads[0]["regime_slices"] = []

    report = build_backtest_result_quality_report(payloads)

    assert _first_gate(report, "regime_split_available", passed=False).passed is False
    assert _first_gate(report, "no_single_regime_overfit", passed=False).passed is False


def test_single_regime_concentration_fails():
    payloads = _payloads()
    payloads[0]["trade_count"] = 50
    payloads[0]["regime_slices"] = [
        {"regime": "risk_on", "trade_count": 46, "expectancy_r": 0.2, "max_drawdown_pct": -4.0, "profit_factor": 1.5},
        {"regime": "neutral", "trade_count": 4, "expectancy_r": 0.1, "max_drawdown_pct": -2.0, "profit_factor": 1.2},
    ]

    report = build_backtest_result_quality_report(payloads)

    gate = _first_gate(report, "no_single_regime_overfit", passed=False)
    assert "largest regime share" in gate.failures[0]


def test_public_safe_tags_gate_fails():
    payloads = _payloads()
    payloads[0]["tags"] = ["research_only"]

    report = build_backtest_result_quality_report(payloads)

    assert _first_gate(report, "public_safe_demo_tags", passed=False).passed is False


def test_research_footer_gate_fails():
    payloads = _payloads()
    payloads[0]["footer"] = "Different footer"

    report = build_backtest_result_quality_report(payloads)

    assert _first_gate(report, "research_footer_present", passed=False).passed is False


def test_config_can_relax_thresholds():
    payloads = _payloads()
    payloads[0]["trade_count"] = 12
    config = BacktestResultQualityConfig(min_trade_count=10)

    report = build_backtest_result_quality_report(payloads, config=config)

    assert _first_gate(report, "minimum_trade_count", passed=True).passed is True


def test_loader_accepts_cases_payload(tmp_path):
    path = tmp_path / "quality.json"
    path.write_text(json.dumps({"cases": _payloads()}), encoding="utf-8")

    cases = load_backtest_result_quality_json(path)

    assert len(cases) == 2
    assert cases[0].run_id == "bt4-demo-trend-quality-001"


def test_markdown_contains_summary_and_footer():
    report = build_backtest_result_quality_report(demo_backtest_result_quality_cases(), generated_at="2026-05-29T00:00:00Z")
    markdown = render_backtest_result_quality_markdown(report)

    assert "# BT4 Backtest Result Quality Report" in markdown
    assert "Overall status: `PASS`" in markdown
    assert "bt4-demo-trend-quality-001" in markdown
    assert RESEARCH_ONLY_FOOTER in markdown


def test_writer_outputs_json_and_markdown(tmp_path):
    report = build_backtest_result_quality_report(demo_backtest_result_quality_cases())
    output_json = tmp_path / "report.json"
    output_md = tmp_path / "report.md"

    write_backtest_result_quality_report(report, output_json=output_json, output_md=output_md)

    assert json.loads(output_json.read_text(encoding="utf-8"))["passed"] is True
    assert "BT4 Backtest Result Quality Report" in output_md.read_text(encoding="utf-8")
