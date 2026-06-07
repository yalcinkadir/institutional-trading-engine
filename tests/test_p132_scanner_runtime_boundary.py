from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.validation.scanner_runtime_boundary import (
    DYNAMIC_SCANNER,
    STATIC_WATCHLIST,
    attach_selection_metadata,
    build_selection_metadata,
    validate_scanner_runtime_boundary,
)


def test_p132_accepts_static_watchlist_when_boundary_is_explicit() -> None:
    payload = build_selection_metadata(
        selection_mode=STATIC_WATCHLIST,
        selected_symbols=["SPY", "QQQ", "AAPL"],
        selection_reason="Seed universe for paper-observation research.",
    )

    result = validate_scanner_runtime_boundary(payload, artifact_kind="paper_observation_evidence")

    assert result.valid is True
    assert result.errors == ()
    assert result.summary["scanner_runtime_boundary_status"] == "PASS"
    assert result.summary["selection_mode"] == STATIC_WATCHLIST
    assert result.summary["selected_symbol_count"] == 3
    assert "paper_observation_evidence:static_watchlist_is_research_setup_not_dynamic_scanner" in result.warnings
    assert result.summary["live_trading_authorized"] is False
    assert result.summary["broker_execution_mode"] == "paper_only"


def test_p132_blocks_missing_selection_mode_in_runtime_report() -> None:
    payload = {
        "selected_symbols": ["SPY", "QQQ"],
        "selection_reason": "Missing mode must fail closed.",
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }

    result = validate_scanner_runtime_boundary(payload, artifact_kind="runtime_report")

    assert result.valid is False
    assert "runtime_report:missing_or_invalid_selection_mode" in result.errors
    assert result.summary["scanner_runtime_boundary_status"] == "BLOCKED"


def test_p132_blocks_static_watchlist_dynamic_scanner_or_edge_claims() -> None:
    payload = build_selection_metadata(
        selection_mode=STATIC_WATCHLIST,
        selected_symbols=["SPY", "QQQ"],
        selection_reason="Static watchlist only.",
    )
    payload["dynamic_scanner_claimed"] = True
    payload["trading_edge_claimed"] = True

    result = validate_scanner_runtime_boundary(payload, artifact_kind="runtime_report")

    assert result.valid is False
    assert "runtime_report:static_watchlist_must_not_claim_dynamic_scanner" in result.errors
    assert "runtime_report:static_watchlist_must_not_claim_trading_edge" in result.errors


def test_p132_requires_dynamic_scanner_contract_ref() -> None:
    payload = build_selection_metadata(
        selection_mode=DYNAMIC_SCANNER,
        selected_symbols=["SPY", "QQQ", "NVDA"],
        selection_reason="Dynamic scanner selected liquid symbols.",
    )

    result = validate_scanner_runtime_boundary(payload, artifact_kind="runtime_report")

    assert result.valid is False
    assert "runtime_report:dynamic_scanner_requires_contract_ref" in result.errors


def test_p132_accepts_dynamic_scanner_with_contract_ref() -> None:
    payload = build_selection_metadata(
        selection_mode=DYNAMIC_SCANNER,
        selected_symbols=["SPY", "QQQ", "NVDA"],
        selection_reason="Dynamic scanner selected liquid symbols.",
        scanner_contract_ref="docs/operations/p132_scanner_runtime_boundary.md#dynamic-scanner-contract",
    )

    result = validate_scanner_runtime_boundary(payload, artifact_kind="runtime_report")

    assert result.valid is True
    assert result.errors == ()
    assert result.summary["selection_mode"] == DYNAMIC_SCANNER
    assert result.summary["scanner_contract_ref"]


def test_p132_attach_selection_metadata_enriches_existing_payload() -> None:
    payload = attach_selection_metadata(
        {"run_id": "daily-observation-001", "run_health_status": "OK"},
        selection_mode=STATIC_WATCHLIST,
        selected_symbols=["spy", " qqq "],
        selection_reason="Static research universe.",
    )

    assert payload["run_id"] == "daily-observation-001"
    assert payload["run_health_status"] == "OK"
    assert payload["selection_mode"] == STATIC_WATCHLIST
    assert payload["selected_symbols"] == ["SPY", "QQQ"]

    result = validate_scanner_runtime_boundary(payload, artifact_kind="paper_observation_evidence")
    assert result.valid is True


def test_p132_preserves_paper_only_boundary() -> None:
    payload = build_selection_metadata(
        selection_mode=STATIC_WATCHLIST,
        selected_symbols=["SPY"],
        selection_reason="Static watchlist only.",
    )
    payload["live_trading_authorized"] = True
    payload["broker_execution_mode"] = "live"

    result = validate_scanner_runtime_boundary(payload, artifact_kind="runtime_report")

    assert result.valid is False
    assert "runtime_report:live_trading_must_remain_false" in result.errors
    assert "runtime_report:broker_execution_mode_must_be_paper_only" in result.errors
    assert result.summary["live_trading_authorized"] is False
    assert result.summary["broker_execution_mode"] == "paper_only"
