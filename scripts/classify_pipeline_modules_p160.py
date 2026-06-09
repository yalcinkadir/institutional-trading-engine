#!/usr/bin/env python3
"""One-shot script: classify pipeline-relevant modules for issue #160.

Run once, then discard. Reads the existing classification JSON, merges in
P160 pipeline-module entries, writes the file back, and regenerates the module
inventory.

Does NOT touch already-classified modules.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLASSIFICATION_PATH = ROOT / "docs" / "architecture" / "module_classification.json"

CONNECTED_RUNTIME_PATHS = [
    "src/backtesting/historical_entry_exit_backtest.py",
    "src/backtesting/historical_models.py",
    "src/backtesting/historical_report.py",
]

QUARANTINE_PATHS = [
    "src/operations/manual_portfolio_sync.py",
    "src/validation/execution_kill_switch.py",
]

EXPERIMENTAL_PATHS = [
    "src/signals/__init__.py",
    "src/signals/intraday_vwap.py",
    "src/signals/signal_status.py",
    "src/signals/structure_levels.py",
    "src/watchers/__init__.py",
    "src/watchers/entry_exit_watcher.py",
    "src/watchers/regime_invalidation.py",
    "src/watchers/trailing_stop_manager.py",
    "src/backtesting/__init__.py",
    "src/backtesting/cross_validation.py",
    "src/backtesting/realistic_execution.py",
    "src/backtesting/signal_validation.py",
    "src/backtesting/walk_forward.py",
    "src/operations/__init__.py",
    "src/operations/broker_compatibility.py",
    "src/operations/broker_failover.py",
    "src/operations/broker_monitoring.py",
    "src/operations/broker_reconciliation.py",
    "src/operations/daily_evidence_report.py",
    "src/operations/execution_adapter.py",
    "src/operations/execution_journal.py",
    "src/operations/execution_policies.py",
    "src/operations/market_calendar.py",
    "src/operations/market_state.py",
    "src/operations/order_lifecycle.py",
    "src/operations/order_router.py",
    "src/operations/paper_broker_adapter.py",
    "src/operations/paper_observation.py",
    "src/operations/paper_order_book.py",
    "src/operations/paper_portfolio.py",
    "src/operations/performance_monitor.py",
    "src/operations/position_lifecycle.py",
    "src/operations/risk_monitor.py",
    "src/operations/runtime_state.py",
    "src/operations/scheduler.py",
    "src/operations/trade_audit.py",
    "src/operations/trade_execution.py",
    "src/operations/trade_reconciliation.py",
    "src/operations/trading_session.py",
    "src/outcomes/__init__.py",
    "src/outcomes/attribution.py",
    "src/outcomes/drift_detection.py",
    "src/outcomes/edge_decay.py",
    "src/outcomes/evidence_export.py",
    "src/outcomes/expectancy.py",
    "src/outcomes/outcome_history.py",
    "src/outcomes/outcome_models.py",
    "src/outcomes/outcome_summary.py",
    "src/outcomes/regime_outcomes.py",
    "src/outcomes/replay.py",
    "src/outcomes/statistics.py",
    "src/outcomes/trade_outcome.py",
    "src/quality/liquidity_filter.py",
    "src/data/__init__.py",
    "src/data/cache.py",
    "src/data/data_quality.py",
    "src/data/market_data.py",
    "src/data/polygon_client.py",
    "src/validation/__init__.py",
    "src/validation/circuit_breakers.py",
    "src/validation/data_contracts.py",
    "src/validation/data_freshness.py",
    "src/validation/data_quality_gate.py",
    "src/validation/drawdown_guard.py",
    "src/validation/fail_closed.py",
    "src/validation/gate_result.py",
    "src/validation/governance.py",
    "src/validation/input_pack_gate.py",
    "src/validation/market_regime_gate.py",
    "src/validation/position_limits.py",
    "src/validation/quality_gate.py",
    "src/validation/risk_limits.py",
    "src/validation/runtime_health.py",
    "src/validation/schema_validation.py",
    "src/validation/silent_failure.py",
    "src/validation/signal_gate.py",
    "src/validation/symbol_universe_gate.py",
    "src/validation/trade_plan_gate.py",
    "src/validation/validation_report.py",
    "src/validation/volatility_gate.py",
    "src/validation/warnings.py",
    "src/validation/weekly_review_gate.py",
    "src/validation/workflow_health.py",
]

EXPECTED_NEW_COUNT = 88
EXPECTED_RESULTING_UNCLASSIFIED_BASELINE = 196
RUNTIME_ENTRYPOINT = "scripts/run_historical_entry_exit_backtest.py"
RUNTIME_EXECUTION_PROOF = "tests/test_bt130_real_historical_evidence_pack_gate.py"


def _experimental_record(path: str) -> dict[str, str]:
    return {
        "classification": "experimental",
        "notes": (
            "P160 pipeline triage: pipeline-relevant module classified as "
            "experimental until a direct runtime execution proof exists. "
            f"Module: {path}"
        ),
    }


def _quarantine_record(path: str) -> dict[str, str | None]:
    return {
        "classification": "quarantine",
        "notes": (
            "P160 pipeline triage: safety-sensitive module kept isolated until "
            f"dedicated governance review and runtime proof exist. Module: {path}"
        ),
        "runtime_entrypoint": None,
        "runtime_execution_proof": None,
    }


def _connected_runtime_record(path: str) -> dict[str, str]:
    return {
        "classification": "connected_runtime",
        "notes": (
            "P160 pipeline triage: BT130-proven historical backtesting runtime "
            f"module. Module: {path}"
        ),
        "runtime_entrypoint": RUNTIME_ENTRYPOINT,
        "runtime_execution_proof": RUNTIME_EXECUTION_PROOF,
    }


def build_new_entries() -> dict[str, dict]:
    entries: dict[str, dict] = {}
    for path in EXPERIMENTAL_PATHS:
        entries[path] = _experimental_record(path)
    for path in QUARANTINE_PATHS:
        entries[path] = _quarantine_record(path)
    for path in CONNECTED_RUNTIME_PATHS:
        entries[path] = _connected_runtime_record(path)
    return entries


NEW_ENTRIES = build_new_entries()


def load_classification() -> dict:
    return json.loads(CLASSIFICATION_PATH.read_text(encoding="utf-8"))


def write_classification(payload: dict) -> None:
    CLASSIFICATION_PATH.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def merge_entries(payload: dict) -> tuple[int, list[str]]:
    classified = payload.setdefault("classified_modules", {})
    skipped: list[str] = []
    added = 0
    for path, record in sorted(NEW_ENTRIES.items()):
        if path in classified:
            skipped.append(path)
            continue
        classified[path] = record
        added += 1
    payload["unclassified_legacy_baseline_limit"] = EXPECTED_RESULTING_UNCLASSIFIED_BASELINE
    return added, skipped


def main() -> int:
    if len(NEW_ENTRIES) != EXPECTED_NEW_COUNT:
        print(
            f"Expected {EXPECTED_NEW_COUNT} new entries, got {len(NEW_ENTRIES)}",
            file=sys.stderr,
        )
        return 1

    payload = load_classification()
    added, skipped = merge_entries(payload)
    write_classification(payload)

    result = subprocess.run(
        [sys.executable, "scripts/generate_module_inventory.py"],
        cwd=ROOT,
        check=False,
    )
    if result.returncode != 0:
        return result.returncode

    print(f"P160 classification merge complete: added={added}, skipped_existing={len(skipped)}")
    print(f"Unclassified legacy baseline set to {EXPECTED_RESULTING_UNCLASSIFIED_BASELINE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
