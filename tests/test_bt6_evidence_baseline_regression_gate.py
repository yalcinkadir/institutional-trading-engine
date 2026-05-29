from __future__ import annotations

import json
from pathlib import Path

from src.validation.evidence_baseline_regression_gate import (
    RESEARCH_ONLY_FOOTER,
    EvidenceSnapshot,
    build_evidence_baseline_regression_report,
    demo_evidence_baseline_pair,
    load_evidence_baseline_regression_json,
    render_evidence_baseline_regression_markdown,
    write_evidence_baseline_regression_report,
)


def _pair():
    return demo_evidence_baseline_pair()


def _report_names(report):
    return {gate.name: gate for gate in report.gates}


def test_demo_pair_passes():
    baseline, current = _pair()
    report = build_evidence_baseline_regression_report(baseline, current, generated_at="2026-05-29T00:00:00Z")

    assert report.passed is True
    assert report.version == "BT6-v1"
    assert report.generated_at == "2026-05-29T00:00:00Z"
    assert report.footer == RESEARCH_ONLY_FOOTER
    assert {delta.metric for delta in report.deltas} == {"expectancy_r", "sharpe", "max_drawdown_pct", "oos_pass_rate_pct", "trade_count"}


def test_missing_required_field_fails_closed():
    baseline, current = _pair()
    broken = EvidenceSnapshot.from_mapping({**current.to_dict(), "run_id": ""})
    report = build_evidence_baseline_regression_report(baseline, broken)

    assert report.passed is False
    assert _report_names(report)["required_fields_complete"].passed is False


def test_strategy_mismatch_fails_closed():
    baseline, current = _pair()
    broken = EvidenceSnapshot.from_mapping({**current.to_dict(), "strategy_id": "other-strategy"})
    report = build_evidence_baseline_regression_report(baseline, broken)

    assert report.passed is False
    assert _report_names(report)["same_strategy_id"].passed is False


def test_dataset_mismatch_fails_closed():
    baseline, current = _pair()
    broken = EvidenceSnapshot.from_mapping({**current.to_dict(), "dataset_id": "other-dataset"})
    report = build_evidence_baseline_regression_report(baseline, broken)

    assert report.passed is False
    assert _report_names(report)["same_dataset_id"].passed is False


def test_missing_metric_fails_closed():
    baseline, current = _pair()
    metrics = dict(current.metrics)
    metrics.pop("sharpe")
    broken = EvidenceSnapshot.from_mapping({**current.to_dict(), "metrics": metrics})
    report = build_evidence_baseline_regression_report(baseline, broken)

    assert report.passed is False
    assert _report_names(report)["required_metrics_valid"].passed is False


def test_non_numeric_metric_fails_closed():
    baseline, current = _pair()
    metrics = dict(current.metrics)
    metrics["expectancy_r"] = "bad"
    broken = EvidenceSnapshot.from_mapping({**current.to_dict(), "metrics": metrics})
    report = build_evidence_baseline_regression_report(baseline, broken)

    assert report.passed is False
    assert _report_names(report)["required_metrics_valid"].passed is False


def test_missing_artifact_hashes_fail_closed():
    baseline, current = _pair()
    broken = EvidenceSnapshot.from_mapping({**current.to_dict(), "artifact_hashes": {}})
    report = build_evidence_baseline_regression_report(baseline, broken)

    assert report.passed is False
    assert _report_names(report)["artifact_hashes_present"].passed is False


def test_expectancy_regression_fails_closed():
    baseline, current = _pair()
    metrics = dict(current.metrics)
    metrics["expectancy_r"] = 0.25
    broken = EvidenceSnapshot.from_mapping({**current.to_dict(), "metrics": metrics})
    report = build_evidence_baseline_regression_report(baseline, broken)

    assert report.passed is False
    assert _report_names(report)["expectancy_regression"].passed is False


def test_sharpe_regression_fails_closed():
    baseline, current = _pair()
    metrics = dict(current.metrics)
    metrics["sharpe"] = 0.85
    broken = EvidenceSnapshot.from_mapping({**current.to_dict(), "metrics": metrics})
    report = build_evidence_baseline_regression_report(baseline, broken)

    assert report.passed is False
    assert _report_names(report)["sharpe_regression"].passed is False


def test_oos_pass_rate_regression_fails_closed():
    baseline, current = _pair()
    metrics = dict(current.metrics)
    metrics["oos_pass_rate_pct"] = 60.0
    broken = EvidenceSnapshot.from_mapping({**current.to_dict(), "metrics": metrics})
    report = build_evidence_baseline_regression_report(baseline, broken)

    assert report.passed is False
    assert _report_names(report)["oos_pass_rate_regression"].passed is False


def test_drawdown_regression_fails_closed():
    baseline, current = _pair()
    metrics = dict(current.metrics)
    metrics["max_drawdown_pct"] = 30.0
    broken = EvidenceSnapshot.from_mapping({**current.to_dict(), "metrics": metrics})
    report = build_evidence_baseline_regression_report(baseline, broken)

    assert report.passed is False
    assert _report_names(report)["drawdown_regression"].passed is False


def test_trade_count_regression_fails_closed():
    baseline, current = _pair()
    metrics = dict(current.metrics)
    metrics["trade_count"] = 40
    broken = EvidenceSnapshot.from_mapping({**current.to_dict(), "metrics": metrics})
    report = build_evidence_baseline_regression_report(baseline, broken)

    assert report.passed is False
    assert _report_names(report)["trade_count_regression"].passed is False


def test_public_safe_tag_required():
    baseline, current = _pair()
    broken = EvidenceSnapshot.from_mapping({**current.to_dict(), "tags": ["demo"]})
    report = build_evidence_baseline_regression_report(baseline, broken)

    assert report.passed is False
    assert _report_names(report)["public_safe_tags"].passed is False


def test_research_footer_required():
    baseline, current = _pair()
    broken = EvidenceSnapshot.from_mapping({**current.to_dict(), "footer": "Live trading approved"})
    report = build_evidence_baseline_regression_report(baseline, broken)

    assert report.passed is False
    assert _report_names(report)["research_only_footer"].passed is False


def test_json_loader_and_writer(tmp_path: Path):
    baseline, current = _pair()
    source = tmp_path / "input.json"
    source.write_text(json.dumps({"baseline": baseline.to_dict(), "current": current.to_dict()}), encoding="utf-8")

    loaded_baseline, loaded_current = load_evidence_baseline_regression_json(source)
    report = build_evidence_baseline_regression_report(loaded_baseline, loaded_current)
    output_json = tmp_path / "report.json"
    output_md = tmp_path / "report.md"
    write_evidence_baseline_regression_report(report, output_json=output_json, output_md=output_md)

    assert output_json.exists()
    assert output_md.exists()
    assert json.loads(output_json.read_text(encoding="utf-8"))["passed"] is True
    assert "BT6 Evidence Baseline Regression Gate Report" in output_md.read_text(encoding="utf-8")


def test_markdown_contains_research_only_footer():
    baseline, current = _pair()
    report = build_evidence_baseline_regression_report(baseline, current)
    markdown = render_evidence_baseline_regression_markdown(report)

    assert "Overall status: `PASS`" in markdown
    assert RESEARCH_ONLY_FOOTER in markdown
