from __future__ import annotations

import json
import subprocess
import sys

from src.validation.backtest_run_contract import demo_backtest_run_contracts
from src.validation.backtesting_evidence_report import (
    RESEARCH_ONLY_FOOTER,
    build_backtesting_evidence_report,
    render_backtesting_evidence_report_markdown,
    write_backtesting_evidence_report,
)


def _payloads():
    return [contract.to_dict() for contract in demo_backtest_run_contracts()]


def test_build_backtesting_evidence_report_summarizes_demo_contracts() -> None:
    report = build_backtesting_evidence_report(demo_backtest_run_contracts(), generated_at="2026-06-01T12:00:00Z")

    assert report.version == "BT8-v1"
    assert report.summary.overall_status == "PASS"
    assert report.summary.run_count == 2
    assert report.summary.strategy_count == 2
    assert report.summary.dataset_count == 2
    assert report.summary.symbol_count == 5
    assert report.summary.trade_count == 79
    assert report.summary.average_return_pct == 9.1
    assert report.summary.average_win_rate_pct == 52.6
    assert report.summary.average_sharpe == 1.045
    assert report.summary.worst_max_drawdown_pct == -7.1
    assert report.live_trading_authorized is False
    assert report.footer == RESEARCH_ONLY_FOOTER


def test_backtesting_evidence_report_fails_when_bt3_contract_gate_fails() -> None:
    payloads = _payloads()
    payloads[0]["seed"] = None

    report = build_backtesting_evidence_report(payloads, generated_at="2026-06-01T12:00:00Z")

    assert report.summary.overall_status == "FAIL"
    assert any(gate.name == "seed_recorded" and not gate.passed for gate in report.run_contract_report.gates)


def test_markdown_contains_required_audit_sections_and_disclaimer() -> None:
    report = build_backtesting_evidence_report(demo_backtest_run_contracts(), generated_at="2026-06-01T12:00:00Z")
    markdown = render_backtesting_evidence_report_markdown(report)

    assert "# BT8 Backtesting Evidence Report" in markdown
    assert "Overall status: `PASS`" in markdown
    assert "Live trading authorized: `False`" in markdown
    assert "## Summary" in markdown
    assert "## Gate Results" in markdown
    assert "## Runs" in markdown
    assert "## Limitations" in markdown
    assert "bt3-demo-trend-001" in markdown
    assert RESEARCH_ONLY_FOOTER in markdown


def test_writer_outputs_json_and_markdown(tmp_path) -> None:
    report = build_backtesting_evidence_report(demo_backtest_run_contracts(), generated_at="2026-06-01T12:00:00Z")
    output_json = tmp_path / "bt8.json"
    output_md = tmp_path / "bt8.md"

    write_backtesting_evidence_report(report, output_json=output_json, output_md=output_md)

    payload = json.loads(output_json.read_text(encoding="utf-8"))
    assert payload["overall_status"] == "PASS"
    assert payload["live_trading_authorized"] is False
    assert "BT8 Backtesting Evidence Report" in output_md.read_text(encoding="utf-8")


def test_cli_generates_report_outputs(tmp_path) -> None:
    contracts_json = tmp_path / "contracts.json"
    output_json = tmp_path / "report.json"
    output_md = tmp_path / "report.md"
    contracts_json.write_text(json.dumps({"contracts": _payloads()}), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/generate_backtesting_evidence_report.py",
            "--contracts-json",
            str(contracts_json),
            "--output-json",
            str(output_json),
            "--output-md",
            str(output_md),
            "--generated-at",
            "2026-06-01T12:00:00Z",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(output_json.read_text(encoding="utf-8"))["overall_status"] == "PASS"
    assert "BT8 Backtesting Evidence Report" in output_md.read_text(encoding="utf-8")
