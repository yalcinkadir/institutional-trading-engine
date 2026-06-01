from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from src.validation.backtesting_evidence_report import load_backtesting_evidence_report_from_contracts_json

ROOT = Path(__file__).resolve().parents[1]
DEMO_CONTRACTS = ROOT / "examples" / "backtesting" / "bt8_demo_contracts.json"


def test_bt8_demo_contracts_build_green_report() -> None:
    report = load_backtesting_evidence_report_from_contracts_json(
        DEMO_CONTRACTS,
        generated_at="2026-06-01T12:30:00Z",
    )

    assert report.summary.overall_status == "PASS"
    assert report.summary.run_count == 2
    assert report.summary.trade_count == 79
    assert report.live_trading_authorized is False


def test_bt8_demo_contracts_are_public_safe_and_research_only() -> None:
    payload = json.loads(DEMO_CONTRACTS.read_text(encoding="utf-8"))

    assert len(payload["contracts"]) == 2
    for contract in payload["contracts"]:
        tags = set(contract["tags"])
        assert {"demo", "public_safe", "research_only"}.issubset(tags)
        assert "production" not in tags
        assert "live" not in tags
        assert contract["footer"] == "Research / Paper Observation Only. Execution is not authorized by this report."


def test_bt8_cli_generates_demo_report_from_versioned_example(tmp_path) -> None:
    output_json = tmp_path / "bt8_demo_report.json"
    output_md = tmp_path / "bt8_demo_report.md"

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "generate_backtesting_evidence_report.py"),
            "--contracts-json",
            str(DEMO_CONTRACTS),
            "--output-json",
            str(output_json),
            "--output-md",
            str(output_md),
            "--generated-at",
            "2026-06-01T12:30:00Z",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(output_json.read_text(encoding="utf-8"))["overall_status"] == "PASS"
    assert "BT8 Backtesting Evidence Report" in output_md.read_text(encoding="utf-8")
