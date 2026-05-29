from __future__ import annotations

import json

from src.validation.walk_forward_robustness_gate import (
    RESEARCH_ONLY_FOOTER,
    build_walk_forward_robustness_report,
    demo_walk_forward_folds,
    load_walk_forward_folds_json,
    render_walk_forward_robustness_markdown,
    write_walk_forward_robustness_report,
)


def _payloads():
    return [fold.to_dict() for fold in demo_walk_forward_folds()]


def _gate(report, name: str):
    return next(gate for gate in report.gates if gate.name == name)


def test_demo_folds_pass_all_gates():
    report = build_walk_forward_robustness_report(demo_walk_forward_folds(), generated_at="2026-05-29T00:00:00Z")

    assert report.passed is True
    assert report.metrics.fold_count == 3
    assert report.metrics.strategy_count == 2
    assert report.metrics.oos_pass_rate_pct == 100.0
    assert report.metrics.positive_oos_metric_rate_pct == 100.0
    assert report.metrics.average_primary_degradation_pct <= 50.0
    assert all(gate.passed for gate in report.gates)


def test_missing_required_identity_field_fails_gate():
    payloads = _payloads()
    payloads[0]["parameter_version"] = ""

    report = build_walk_forward_robustness_report(payloads)

    gate = _gate(report, "required_fields_complete")
    assert report.passed is False
    assert gate.passed is False
    assert "parameter_version" in gate.failures[0]


def test_too_few_folds_fail_gate():
    report = build_walk_forward_robustness_report(_payloads()[:2])

    gate = _gate(report, "minimum_fold_count")
    assert gate.passed is False
    assert "below required minimum" in gate.failures[0]


def test_overlapping_train_and_oos_window_fails_gate():
    payloads = _payloads()
    payloads[0]["train_end"] = "2024-04-01"

    report = build_walk_forward_robustness_report(payloads)

    gate = _gate(report, "chronological_walk_forward_windows")
    assert gate.passed is False
    assert "overlaps or touches OOS" in gate.failures[0]


def test_overlapping_oos_folds_fail_gate():
    payloads = _payloads()
    payloads[1]["oos_start"] = "2024-04-15"

    report = build_walk_forward_robustness_report(payloads)

    gate = _gate(report, "chronological_walk_forward_windows")
    assert gate.passed is False
    assert "OOS window overlaps previous fold" in "; ".join(gate.failures)


def test_missing_oos_metric_fails_gate():
    payloads = _payloads()
    del payloads[0]["oos_metrics"]["sharpe"]

    report = build_walk_forward_robustness_report(payloads)

    gate = _gate(report, "required_metrics_present")
    assert gate.passed is False
    assert "missing oos metric sharpe" in gate.failures[0]


def test_non_numeric_train_metric_fails_gate():
    payloads = _payloads()
    payloads[0]["train_metrics"]["expectancy_r"] = "strong"

    report = build_walk_forward_robustness_report(payloads)

    gate = _gate(report, "required_metrics_present")
    assert gate.passed is False
    assert "non-numeric train metric expectancy_r" in gate.failures[0]


def test_low_oos_trade_count_fails_gate():
    payloads = _payloads()
    payloads[0]["oos_metrics"]["trade_count"] = 2

    report = build_walk_forward_robustness_report(payloads)

    gate = _gate(report, "minimum_oos_trade_count")
    assert gate.passed is False
    assert "below minimum" in gate.failures[0]


def test_oos_drawdown_above_limit_fails_gate():
    payloads = _payloads()
    payloads[0]["oos_metrics"]["max_drawdown_pct"] = 25.0

    report = build_walk_forward_robustness_report(payloads)

    gate = _gate(report, "oos_drawdown_within_limit")
    assert gate.passed is False
    assert "exceeds limit" in gate.failures[0]


def test_low_oos_pass_rate_fails_gate():
    payloads = _payloads()
    payloads[0]["oos_metrics"]["expectancy_r"] = -0.10
    payloads[1]["oos_metrics"]["expectancy_r"] = -0.05

    report = build_walk_forward_robustness_report(payloads)

    assert _gate(report, "minimum_oos_pass_rate").passed is False
    assert _gate(report, "positive_oos_primary_metric_rate").passed is False


def test_excessive_train_to_oos_degradation_fails_gate():
    payloads = _payloads()
    for payload in payloads:
        payload["train_metrics"]["expectancy_r"] = 1.0
        payload["oos_metrics"]["expectancy_r"] = 0.2

    report = build_walk_forward_robustness_report(payloads)

    gate = _gate(report, "train_to_oos_degradation_limit")
    assert gate.passed is False
    assert "degradation" in gate.failures[0]


def test_missing_public_safe_tags_fail_gate():
    payloads = _payloads()
    payloads[0]["tags"] = ["demo"]

    report = build_walk_forward_robustness_report(payloads)

    assert _gate(report, "public_safe_demo_tags").passed is False


def test_missing_research_footer_fails_gate():
    payloads = _payloads()
    payloads[0]["footer"] = "Different footer"

    report = build_walk_forward_robustness_report(payloads)

    assert _gate(report, "research_footer_present").passed is False


def test_loader_accepts_folds_payload(tmp_path):
    path = tmp_path / "folds.json"
    path.write_text(json.dumps({"folds": _payloads()}), encoding="utf-8")

    folds = load_walk_forward_folds_json(path)

    assert len(folds) == 3
    assert folds[0].fold_id == "bt5-demo-fold-001"


def test_markdown_contains_summary_and_footer():
    report = build_walk_forward_robustness_report(demo_walk_forward_folds(), generated_at="2026-05-29T00:00:00Z")
    markdown = render_walk_forward_robustness_markdown(report)

    assert "# BT5 Walk-Forward / Out-of-Sample Robustness Gate Report" in markdown
    assert "Overall status: `PASS`" in markdown
    assert "bt5-demo-fold-001" in markdown
    assert RESEARCH_ONLY_FOOTER in markdown


def test_writer_outputs_json_and_markdown(tmp_path):
    report = build_walk_forward_robustness_report(demo_walk_forward_folds())
    output_json = tmp_path / "report.json"
    output_md = tmp_path / "report.md"

    write_walk_forward_robustness_report(report, output_json=output_json, output_md=output_md)

    assert json.loads(output_json.read_text(encoding="utf-8"))["passed"] is True
    assert "BT5 Walk-Forward" in output_md.read_text(encoding="utf-8")
