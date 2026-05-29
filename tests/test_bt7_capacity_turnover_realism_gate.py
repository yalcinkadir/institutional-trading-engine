from __future__ import annotations

import json
from pathlib import Path

from src.validation.capacity_turnover_realism_gate import (
    RESEARCH_ONLY_FOOTER,
    CapacityTurnoverSnapshot,
    build_capacity_turnover_realism_report,
    demo_capacity_turnover_snapshot,
    load_capacity_turnover_realism_json,
    render_capacity_turnover_realism_markdown,
    write_capacity_turnover_realism_report,
)


def _snapshot():
    return demo_capacity_turnover_snapshot()


def _report_names(report):
    return {gate.name: gate for gate in report.gates}


def _with_metric(snapshot, name, value):
    metrics = dict(snapshot.metrics)
    metrics[name] = value
    return CapacityTurnoverSnapshot.from_mapping({**snapshot.to_dict(), "metrics": metrics})


def test_demo_snapshot_passes():
    snapshot = _snapshot()
    report = build_capacity_turnover_realism_report(snapshot, generated_at="2026-05-29T00:00:00Z")

    assert report.passed is True
    assert report.version == "BT7-v1"
    assert report.generated_at == "2026-05-29T00:00:00Z"
    assert report.footer == RESEARCH_ONLY_FOOTER


def test_missing_required_field_fails_closed():
    snapshot = CapacityTurnoverSnapshot.from_mapping({**_snapshot().to_dict(), "run_id": ""})
    report = build_capacity_turnover_realism_report(snapshot)

    assert report.passed is False
    assert _report_names(report)["required_fields_complete"].passed is False


def test_missing_metric_fails_closed():
    snapshot = _snapshot()
    metrics = dict(snapshot.metrics)
    metrics.pop("median_adv_usd")
    broken = CapacityTurnoverSnapshot.from_mapping({**snapshot.to_dict(), "metrics": metrics})
    report = build_capacity_turnover_realism_report(broken)

    assert report.passed is False
    assert _report_names(report)["required_metrics_valid"].passed is False


def test_non_numeric_metric_fails_closed():
    broken = _with_metric(_snapshot(), "gross_expectancy_bps", "bad")
    report = build_capacity_turnover_realism_report(broken)

    assert report.passed is False
    assert _report_names(report)["required_metrics_valid"].passed is False


def test_non_positive_scale_fails_closed():
    broken = CapacityTurnoverSnapshot.from_mapping({**_snapshot().to_dict(), "proposed_capital_usd": 0, "symbol_count": 0})
    report = build_capacity_turnover_realism_report(broken)

    assert report.passed is False
    assert _report_names(report)["positive_scale"].passed is False


def test_max_position_adv_limit_fails_closed():
    broken = _with_metric(_snapshot(), "max_position_adv_pct", 7.0)
    report = build_capacity_turnover_realism_report(broken)

    assert report.passed is False
    assert _report_names(report)["capacity_liquidity_limits"].passed is False


def test_portfolio_adv_limit_fails_closed():
    broken = _with_metric(_snapshot(), "portfolio_adv_pct", 25.0)
    report = build_capacity_turnover_realism_report(broken)

    assert report.passed is False
    assert _report_names(report)["capacity_liquidity_limits"].passed is False


def test_average_daily_turnover_limit_fails_closed():
    broken = _with_metric(_snapshot(), "average_daily_turnover_pct", 45.0)
    report = build_capacity_turnover_realism_report(broken)

    assert report.passed is False
    assert _report_names(report)["turnover_limits"].passed is False


def test_annual_turnover_limit_fails_closed():
    broken = _with_metric(_snapshot(), "annual_turnover_pct", 1400.0)
    report = build_capacity_turnover_realism_report(broken)

    assert report.passed is False
    assert _report_names(report)["turnover_limits"].passed is False


def test_cost_drag_limit_fails_closed():
    broken = _with_metric(_snapshot(), "round_trip_cost_bps", 20.0)
    report = build_capacity_turnover_realism_report(broken)

    assert report.passed is False
    assert _report_names(report)["cost_drag_realism"].passed is False


def test_net_expectancy_floor_fails_closed():
    broken = _with_metric(_snapshot(), "net_expectancy_bps", 2.0)
    report = build_capacity_turnover_realism_report(broken)

    assert report.passed is False
    assert _report_names(report)["cost_drag_realism"].passed is False


def test_holding_period_floor_fails_closed():
    broken = _with_metric(_snapshot(), "average_holding_days", 0.5)
    report = build_capacity_turnover_realism_report(broken)

    assert report.passed is False
    assert _report_names(report)["holding_period_realism"].passed is False


def test_trade_count_floor_fails_closed():
    broken = _with_metric(_snapshot(), "trade_count", 10)
    report = build_capacity_turnover_realism_report(broken)

    assert report.passed is False
    assert _report_names(report)["trade_count_floor"].passed is False


def test_slippage_model_coverage_required():
    broken = _with_metric(_snapshot(), "slippage_model_coverage_pct", 95.0)
    report = build_capacity_turnover_realism_report(broken)

    assert report.passed is False
    assert _report_names(report)["slippage_model_coverage"].passed is False


def test_missing_artifact_hashes_fail_closed():
    broken = CapacityTurnoverSnapshot.from_mapping({**_snapshot().to_dict(), "artifact_hashes": {}})
    report = build_capacity_turnover_realism_report(broken)

    assert report.passed is False
    assert _report_names(report)["artifact_hashes_present"].passed is False


def test_public_safe_tag_required():
    broken = CapacityTurnoverSnapshot.from_mapping({**_snapshot().to_dict(), "tags": ["demo"]})
    report = build_capacity_turnover_realism_report(broken)

    assert report.passed is False
    assert _report_names(report)["public_safe_tags"].passed is False


def test_research_footer_required():
    broken = CapacityTurnoverSnapshot.from_mapping({**_snapshot().to_dict(), "footer": "Live trading approved"})
    report = build_capacity_turnover_realism_report(broken)

    assert report.passed is False
    assert _report_names(report)["research_only_footer"].passed is False


def test_json_loader_and_writer(tmp_path: Path):
    snapshot = _snapshot()
    source = tmp_path / "input.json"
    source.write_text(json.dumps({"snapshot": snapshot.to_dict()}), encoding="utf-8")

    loaded = load_capacity_turnover_realism_json(source)
    report = build_capacity_turnover_realism_report(loaded)
    output_json = tmp_path / "report.json"
    output_md = tmp_path / "report.md"
    write_capacity_turnover_realism_report(report, output_json=output_json, output_md=output_md)

    assert output_json.exists()
    assert output_md.exists()
    assert json.loads(output_json.read_text(encoding="utf-8"))["passed"] is True
    assert "BT7 Capacity / Turnover / Realism Gate Report" in output_md.read_text(encoding="utf-8")


def test_markdown_contains_research_only_footer():
    report = build_capacity_turnover_realism_report(_snapshot())
    markdown = render_capacity_turnover_realism_markdown(report)

    assert "Overall status: `PASS`" in markdown
    assert RESEARCH_ONLY_FOOTER in markdown
