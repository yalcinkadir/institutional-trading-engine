#!/usr/bin/env python3
"""One-shot script: classify all pipeline-relevant modules for issue #160.

Run once, then discard. Reads the existing classification JSON, merges in
all new pipeline-module entries, writes the file back, and regenerates the
module inventory.

Does NOT touch already-classified modules.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLASSIFICATION_PATH = ROOT / "docs/architecture/module_classification.json"


NEW_ENTRIES: dict[str, dict] = {
    # -----------------------------------------------------------------------
    # src/signals/ — unclassified remainder
    # -----------------------------------------------------------------------
    "src/signals/__init__.py": {
        "classification": "experimental",
        "notes": "P160 pipeline triage: signals package init. Useful boundary; promote to connected_runtime when a runtime proof references it.",
    },
    "src/signals/intraday_vwap.py": {
        "classification": "experimental",
        "notes": "P160 pipeline triage: intraday VWAP helper for signal generation. Not marked connected_runtime until a live runtime execution proof exists.",
    },
    "src/signals/signal_status.py": {
        "classification": "experimental",
        "notes": "P160 pipeline triage: signal lifecycle status helper. Not marked connected_runtime until a live runtime execution proof exists.",
    },
    "src/signals/structure_levels.py": {
        "classification": "experimental",
        "notes": "P160 pipeline triage: market structure level detection helper. Not marked connected_runtime until a live runtime execution proof exists.",
    },
    # -----------------------------------------------------------------------
    # src/watchers/ — Watcher stage
    # -----------------------------------------------------------------------
    "src/watchers/__init__.py": {
        "classification": "experimental",
        "notes": "P160 pipeline triage: watchers package init. Promote to connected_runtime when watcher runtime proof exists.",
    },
    "src/watchers/entry_exit_watcher.py": {
        "classification": "experimental",
        "notes": "P160 pipeline triage: entry/exit watcher — Watcher stage of the pipeline. Useful and actively maintained; not marked connected_runtime until scripts/run_entry_exit_watcher.py execution proof is added.",
    },
    "src/watchers/regime_invalidation.py": {
        "classification": "experimental",
        "notes": "P160 pipeline triage: regime invalidation watcher helper. Not marked connected_runtime until a watcher runtime execution proof exists.",
    },
    "src/watchers/trailing_stop_manager.py": {
        "classification": "experimental",
        "notes": "P160 pipeline triage: trailing stop helper for watcher-stage trade management. Not marked connected_runtime until a watcher runtime execution proof exists.",
    },
    # -----------------------------------------------------------------------
    # src/backtesting/ — Backtesting runtime and support modules
    # -----------------------------------------------------------------------
    "src/backtesting/__init__.py": {
        "classification": "experimental",
        "notes": "P160 pipeline triage: backtesting package init. No standalone runtime proof required.",
    },
    "src/backtesting/cross_validation.py": {
        "classification": "experimental",
        "notes": "P160 pipeline triage: cross-validation research helper. Not marked connected_runtime until real-data runtime proof exists.",
    },
    "src/backtesting/historical_entry_exit_backtest.py": {
        "classification": "connected_runtime",
        "notes": "P160 pipeline triage: historical entry/exit backtest runtime core executed by scripts/run_historical_entry_exit_backtest.py and guarded by BT9/BT130 evidence tests.",
        "runtime_entrypoint": "scripts/run_historical_entry_exit_backtest.py",
        "runtime_execution_proof": "tests/test_bt130_real_historical_evidence_pack_gate.py",
    },
    "src/backtesting/historical_models.py": {
        "classification": "connected_runtime",
        "notes": "P160 pipeline triage: historical backtest model definitions consumed by the BT9/BT130 real-data backtest evidence path.",
        "runtime_entrypoint": "scripts/run_historical_entry_exit_backtest.py",
        "runtime_execution_proof": "tests/test_bt130_real_historical_evidence_pack_gate.py",
    },
    "src/backtesting/historical_report.py": {
        "classification": "connected_runtime",
        "notes": "P160 pipeline triage: historical backtest report builder writes BT130 evidence artifacts on the real-data path.",
        "runtime_entrypoint": "scripts/run_historical_entry_exit_backtest.py",
        "runtime_execution_proof": "tests/test_bt130_real_historical_evidence_pack_gate.py",
    },
    "src/backtesting/realistic_execution.py": {
        "classification": "experimental",
        "notes": "P160 pipeline triage: execution realism research helper. Promote only after direct runtime proof exists.",
    },
    "src/backtesting/signal_validation.py": {
        "classification": "experimental",
        "notes": "P160 pipeline triage: backtest signal validation helper without current runtime execution proof.",
    },
    "src/backtesting/walk_forward.py": {
        "classification": "experimental",
        "notes": "P160 pipeline triage: walk-forward research helper without current runtime execution proof.",
    },
    # -----------------------------------------------------------------------
    # src/operations/ — evidence and observation operations
    # -----------------------------------------------------------------------
    "src/operations/__init__.py": {
        "classification": "experimental",
        "notes": "P160 pipeline triage: operations package init. No standalone runtime proof.",
    },
    "src/operations/broker_compatibility.py": {"classification": "experimental", "notes": "P160 pipeline triage: broker compatibility helper; promote only with broker adapter runtime proof."},
    "src/operations/broker_failover.py": {"classification": "experimental", "notes": "P160 pipeline triage: broker failover helper; no current runtime proof."},
    "src/operations/broker_monitoring.py": {"classification": "experimental", "notes": "P160 pipeline triage: broker monitoring helper; no current runtime proof."},
    "src/operations/broker_reconciliation.py": {"classification": "experimental", "notes": "P160 pipeline triage: broker reconciliation helper; no current runtime proof."},
    "src/operations/daily_evidence_report.py": {"classification": "experimental", "notes": "P160 pipeline triage: daily evidence report helper. Valuable evidence tooling but not marked connected_runtime without entrypoint proof."},
    "src/operations/execution_adapter.py": {"classification": "experimental", "notes": "P160 pipeline triage: execution adapter boundary. Promote only after paper/live adapter runtime proof."},
    "src/operations/execution_journal.py": {"classification": "experimental", "notes": "P160 pipeline triage: execution journal helper; no current runtime proof."},
    "src/operations/execution_policies.py": {"classification": "experimental", "notes": "P160 pipeline triage: execution policy helper; no current runtime proof."},
    "src/operations/market_calendar.py": {"classification": "experimental", "notes": "P160 pipeline triage: market calendar helper; no current runtime proof."},
    "src/operations/market_state.py": {"classification": "experimental", "notes": "P160 pipeline triage: market state helper; no current runtime proof."},
    "src/operations/manual_portfolio_sync.py": {"classification": "quarantine", "notes": "P160 pipeline triage: manual portfolio mutation/sync helper is safety-sensitive and should remain isolated until reviewed and proven."},
    "src/operations/order_lifecycle.py": {"classification": "experimental", "notes": "P160 pipeline triage: order lifecycle helper; no current runtime proof."},
    "src/operations/order_router.py": {"classification": "experimental", "notes": "P160 pipeline triage: order router helper; promote only with broker adapter runtime proof."},
    "src/operations/paper_broker_adapter.py": {"classification": "experimental", "notes": "P160 pipeline triage: paper broker adapter. Promote after dedicated paper-runtime execution proof is linked."},
    "src/operations/paper_observation.py": {"classification": "experimental", "notes": "P160 pipeline triage: paper observation helper; evidence path exists but this module needs direct runtime proof before promotion."},
    "src/operations/paper_order_book.py": {"classification": "experimental", "notes": "P160 pipeline triage: paper order book helper; no current runtime proof."},
    "src/operations/paper_portfolio.py": {"classification": "experimental", "notes": "P160 pipeline triage: paper portfolio helper; no current runtime proof."},
    "src/operations/performance_monitor.py": {"classification": "experimental", "notes": "P160 pipeline triage: performance monitoring helper; no current runtime proof."},
    "src/operations/position_lifecycle.py": {"classification": "experimental", "notes": "P160 pipeline triage: position lifecycle helper; no current runtime proof."},
    "src/operations/risk_monitor.py": {"classification": "experimental", "notes": "P160 pipeline triage: risk monitoring helper; no current runtime proof."},
    "src/operations/runtime_state.py": {"classification": "experimental", "notes": "P160 pipeline triage: runtime state helper; no current runtime proof."},
    "src/operations/scheduler.py": {"classification": "experimental", "notes": "P160 pipeline triage: scheduler helper; no current runtime proof."},
    "src/operations/trade_audit.py": {"classification": "experimental", "notes": "P160 pipeline triage: trade audit helper; no current runtime proof."},
    "src/operations/trade_execution.py": {"classification": "experimental", "notes": "P160 pipeline triage: trade execution helper; no current runtime proof."},
    "src/operations/trade_reconciliation.py": {"classification": "experimental", "notes": "P160 pipeline triage: trade reconciliation helper; no current runtime proof."},
    "src/operations/trading_session.py": {"classification": "experimental", "notes": "P160 pipeline triage: trading session helper; no current runtime proof."},
    # -----------------------------------------------------------------------
    # src/outcomes/ — outcome tracking/evidence support
    # -----------------------------------------------------------------------
    "src/outcomes/__init__.py": {"classification": "experimental", "notes": "P160 pipeline triage: outcomes package init."},
    "src/outcomes/attribution.py": {"classification": "experimental", "notes": "P160 pipeline triage: outcome attribution helper without current runtime proof."},
    "src/outcomes/drift_detection.py": {"classification": "experimental", "notes": "P160 pipeline triage: outcome drift detection helper without current runtime proof."},
    "src/outcomes/edge_decay.py": {"classification": "experimental", "notes": "P160 pipeline triage: outcome edge-decay helper without current runtime proof."},
    "src/outcomes/evidence_export.py": {"classification": "experimental", "notes": "P160 pipeline triage: outcome evidence export helper without current runtime proof."},
    "src/outcomes/expectancy.py": {"classification": "experimental", "notes": "P160 pipeline triage: expectancy helper without current runtime proof."},
    "src/outcomes/outcome_history.py": {"classification": "experimental", "notes": "P160 pipeline triage: outcome history helper without current runtime proof."},
    "src/outcomes/outcome_models.py": {"classification": "experimental", "notes": "P160 pipeline triage: outcome model definitions without current runtime proof."},
    "src/outcomes/outcome_summary.py": {"classification": "experimental", "notes": "P160 pipeline triage: outcome summary helper used by outcome tooling; not marked connected_runtime without dedicated proof."},
    "src/outcomes/regime_outcomes.py": {"classification": "experimental", "notes": "P160 pipeline triage: regime outcome helper without current runtime proof."},
    "src/outcomes/replay.py": {"classification": "experimental", "notes": "P160 pipeline triage: outcome replay helper without current runtime proof."},
    "src/outcomes/statistics.py": {"classification": "experimental", "notes": "P160 pipeline triage: outcome statistics helper without current runtime proof."},
    "src/outcomes/trade_outcome.py": {"classification": "experimental", "notes": "P160 pipeline triage: trade outcome helper without current runtime proof."},
    # -----------------------------------------------------------------------
    # src/quality/ and src/data/
    # -----------------------------------------------------------------------
    "src/quality/liquidity_filter.py": {"classification": "experimental", "notes": "P160 pipeline triage: liquidity quality helper; promote only after signal/runtime proof exists."},
    "src/data/__init__.py": {"classification": "experimental", "notes": "P160 pipeline triage: data package init."},
    "src/data/cache.py": {"classification": "experimental", "notes": "P160 pipeline triage: data cache helper without current runtime proof."},
    "src/data/data_quality.py": {"classification": "experimental", "notes": "P160 pipeline triage: data quality helper without direct runtime proof."},
    "src/data/market_data.py": {"classification": "experimental", "notes": "P160 pipeline triage: market data abstraction without direct runtime proof."},
    "src/data/polygon_client.py": {"classification": "experimental", "notes": "P160 pipeline triage: Polygon client helper; promote when direct report/backtest data-runtime proof is linked."},
    # -----------------------------------------------------------------------
    # src/validation/ — gate layer, mostly experimental until direct entrypoint proof
    # -----------------------------------------------------------------------
    "src/validation/__init__.py": {"classification": "experimental", "notes": "P160 pipeline triage: validation package init."},
    "src/validation/circuit_breakers.py": {"classification": "experimental", "notes": "P160 pipeline triage: circuit breaker helper without current runtime proof."},
    "src/validation/data_contracts.py": {"classification": "experimental", "notes": "P160 pipeline triage: data contract helper without current runtime proof."},
    "src/validation/data_freshness.py": {"classification": "experimental", "notes": "P160 pipeline triage: data freshness helper without current runtime proof."},
    "src/validation/data_quality_gate.py": {"classification": "experimental", "notes": "P160 pipeline triage: data quality gate without current runtime proof."},
    "src/validation/drawdown_guard.py": {"classification": "experimental", "notes": "P160 pipeline triage: drawdown guard without current runtime proof."},
    "src/validation/execution_kill_switch.py": {"classification": "quarantine", "notes": "P160 pipeline triage: kill-switch safety-sensitive logic. Keep quarantined until runtime proof and governance review."},
    "src/validation/fail_closed.py": {"classification": "experimental", "notes": "P160 pipeline triage: fail-closed helper without current runtime proof."},
    "src/validation/gate_result.py": {"classification": "experimental", "notes": "P160 pipeline triage: validation gate result model without current runtime proof."},
    "src/validation/governance.py": {"classification": "experimental", "notes": "P160 pipeline triage: governance helper without current runtime proof."},
    "src/validation/input_pack_gate.py": {"classification": "experimental", "notes": "P160 pipeline triage: input-pack gate helper without direct runtime proof."},
    "src/validation/market_regime_gate.py": {"classification": "experimental", "notes": "P160 pipeline triage: market regime gate without current runtime proof."},
    "src/validation/position_limits.py": {"classification": "experimental", "notes": "P160 pipeline triage: position limit helper without current runtime proof."},
    "src/validation/quality_gate.py": {"classification": "experimental", "notes": "P160 pipeline triage: quality gate without current runtime proof."},
    "src/validation/risk_limits.py": {"classification": "experimental", "notes": "P160 pipeline triage: risk limit helper without current runtime proof."},
    "src/validation/runtime_health.py": {"classification": "experimental", "notes": "P160 pipeline triage: runtime health helper without current runtime proof."},
    "src/validation/schema_validation.py": {"classification": "experimental", "notes": "P160 pipeline triage: schema validation helper without current runtime proof."},
    "src/validation/silent_failure.py": {"classification": "experimental", "notes": "P160 pipeline triage: silent failure detection helper without current runtime proof."},
    "src/validation/signal_gate.py": {"classification": "experimental", "notes": "P160 pipeline triage: signal gate without current runtime proof."},
    "src/validation/symbol_universe_gate.py": {"classification": "experimental", "notes": "P160 pipeline triage: symbol universe gate without current runtime proof."},
    "src/validation/trade_plan_gate.py": {"classification": "experimental", "notes": "P160 pipeline triage: trade-plan gate without current runtime proof."},
    "src/validation/validation_report.py": {"classification": "experimental", "notes": "P160 pipeline triage: validation report helper without current runtime proof."},
    "src/validation/volatility_gate.py": {"classification": "experimental", "notes": "P160 pipeline triage: volatility gate without current runtime proof."},
    "src/validation/warnings.py": {"classification": "experimental", "notes": "P160 pipeline triage: warning helper without current runtime proof."},
    "src/validation/weekly_review_gate.py": {"classification": "experimental", "notes": "P160 pipeline triage: weekly review gate without current runtime proof."},
    "src/validation/workflow_health.py": {"classification": "experimental", "notes": "P160 pipeline triage: workflow health helper without current runtime proof."},
}


EXPECTED_NEW_COUNT = 102
EXPECTED_RESULTING_UNCLASSIFIED_BASELINE = 182


def load_classification() -> dict:
    return json.loads(CLASSIFICATION_PATH.read_text(encoding="utf-8"))


def write_classification(payload: dict) -> None:
    CLASSIFICATION_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def merge_entries(payload: dict) -> tuple[int, list[str]]:
    classified = payload.setdefault("classified_modules", {})
    skipped: list[str] = []
    added = 0
    for path, record in NEW_ENTRIES.items():
        if path in classified:
            skipped.append(path)
            continue
        classified[path] = record
        added += 1
    payload["unclassified_legacy_baseline_limit"] = EXPECTED_RESULTING_UNCLASSIFIED_BASELINE
    return added, skipped


def main() -> int:
    if len(NEW_ENTRIES) != EXPECTED_NEW_COUNT:
        print(f"Expected {EXPECTED_NEW_COUNT} new entries, got {len(NEW_ENTRIES)}", file=sys.stderr)
        return 1

    payload = load_classification()
    added, skipped = merge_entries(payload)
    write_classification(payload)

    result = subprocess.run([sys.executable, "scripts/generate_module_inventory.py"], cwd=ROOT, check=False)
    if result.returncode != 0:
        return result.returncode

    print(f"P160 classification merge complete: added={added}, skipped_existing={len(skipped)}")
    print(f"Unclassified legacy baseline set to {EXPECTED_RESULTING_UNCLASSIFIED_BASELINE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
