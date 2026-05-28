from __future__ import annotations

import json

from src.validation.backtest_run_contract import (
    RESEARCH_ONLY_FOOTER,
    build_backtest_run_contract_report,
    demo_backtest_run_contracts,
    load_backtest_run_contracts_json,
    render_backtest_run_contract_markdown,
    write_backtest_run_contract_report,
)


def _payloads():
    return [contract.to_dict() for contract in demo_backtest_run_contracts()]


def _gate(report, name: str):
    return next(gate for gate in report.gates if gate.name == name)


def test_demo_contracts_pass_all_gates():
    report = build_backtest_run_contract_report(demo_backtest_run_contracts(), generated_at="2026-05-28T00:00:00Z")

    assert report.passed is True
    assert report.metrics.run_count == 2
    assert report.metrics.strategy_count == 2
    assert report.metrics.metric_coverage_pct == 100.0
    assert report.metrics.artifact_coverage_pct == 100.0
    assert all(gate.passed for gate in report.gates)


def test_missing_required_fields_fail_gate():
    payloads = _payloads()
    payloads[0]["parameter_version"] = ""

    report = build_backtest_run_contract_report(payloads)

    gate = _gate(report, "required_fields_complete")
    assert report.passed is False
    assert gate.passed is False
    assert "parameter_version" in gate.failures[0]


def test_invalid_date_window_fails_gate():
    payloads = _payloads()
    payloads[0]["start_date"] = "2024-12-31"
    payloads[0]["end_date"] = "2024-01-01"

    report = build_backtest_run_contract_report(payloads)

    gate = _gate(report, "valid_backtest_date_windows")
    assert gate.passed is False
    assert "start_date after end_date" in gate.failures[0]


def test_invalid_commit_sha_fails_gate():
    payloads = _payloads()
    payloads[0]["code_commit_sha"] = "not-a-sha"

    report = build_backtest_run_contract_report(payloads)

    assert _gate(report, "commit_sha_present").passed is False


def test_missing_seed_fails_gate():
    payloads = _payloads()
    payloads[0]["seed"] = None

    report = build_backtest_run_contract_report(payloads)

    assert _gate(report, "seed_recorded").passed is False


def test_non_deterministic_contract_fails_gate():
    payloads = _payloads()
    payloads[0]["deterministic"] = False

    report = build_backtest_run_contract_report(payloads)

    assert _gate(report, "determinism_required").passed is False


def test_missing_metrics_fail_gate():
    payloads = _payloads()
    del payloads[0]["metrics"]["sharpe"]

    report = build_backtest_run_contract_report(payloads)

    gate = _gate(report, "required_metrics_present")
    assert gate.passed is False
    assert "sharpe" in gate.failures[0]


def test_non_numeric_metric_fails_gate():
    payloads = _payloads()
    payloads[0]["metrics"]["sharpe"] = "high"

    report = build_backtest_run_contract_report(payloads)

    gate = _gate(report, "required_metrics_present")
    assert gate.passed is False
    assert "non-numeric" in gate.failures[0]


def test_missing_artifact_fails_gate():
    payloads = _payloads()
    payloads[0]["artifacts"] = payloads[0]["artifacts"][:1]

    report = build_backtest_run_contract_report(payloads)

    gate = _gate(report, "artifact_manifest_complete")
    assert gate.passed is False
    assert "result_summary" in gate.failures[0]


def test_invalid_artifact_hash_fails_gate():
    payloads = _payloads()
    payloads[0]["artifacts"][0]["sha256"] = "bad-hash"

    report = build_backtest_run_contract_report(payloads)

    gate = _gate(report, "artifact_manifest_complete")
    assert gate.passed is False
    assert "invalid artifact sha256" in gate.failures[0]


def test_missing_public_safe_tags_fail_gate():
    payloads = _payloads()
    payloads[0]["tags"] = ["research_only"]

    report = build_backtest_run_contract_report(payloads)

    assert _gate(report, "public_safe_demo_tags").passed is False


def test_missing_footer_fails_gate():
    payloads = _payloads()
    payloads[0]["footer"] = "Different footer"

    report = build_backtest_run_contract_report(payloads)

    assert _gate(report, "research_footer_present").passed is False


def test_loader_accepts_contracts_payload(tmp_path):
    path = tmp_path / "contracts.json"
    path.write_text(json.dumps({"contracts": _payloads()}), encoding="utf-8")

    contracts = load_backtest_run_contracts_json(path)

    assert len(contracts) == 2
    assert contracts[0].run_id == "bt3-demo-trend-001"


def test_markdown_contains_summary_and_footer():
    report = build_backtest_run_contract_report(demo_backtest_run_contracts(), generated_at="2026-05-28T00:00:00Z")
    markdown = render_backtest_run_contract_markdown(report)

    assert "# BT3 Backtest Run Contract Report" in markdown
    assert "Overall status: `PASS`" in markdown
    assert "bt3-demo-trend-001" in markdown
    assert RESEARCH_ONLY_FOOTER in markdown


def test_writer_outputs_json_and_markdown(tmp_path):
    report = build_backtest_run_contract_report(demo_backtest_run_contracts())
    output_json = tmp_path / "report.json"
    output_md = tmp_path / "report.md"

    write_backtest_run_contract_report(report, output_json=output_json, output_md=output_md)

    assert json.loads(output_json.read_text(encoding="utf-8"))["passed"] is True
    assert "BT3 Backtest Run Contract Report" in output_md.read_text(encoding="utf-8")
