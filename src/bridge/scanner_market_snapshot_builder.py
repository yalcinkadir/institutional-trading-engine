"""
Scanner Market Snapshot Builder.

Single responsibility:
  raw scanner metrics + vix_data
  → RuntimeMarketSnapshot

This module sits between the scanner and the bridge.
It does NOT produce InstitutionalDecisionInputs directly.
That is the bridge's job.

Responsibility split (mandatory, never merge these):

  scanner_market_snapshot_builder.py  (THIS FILE)
      raw scanner metrics
      → calls bridge (translate)
      → calls orchestrator (evaluate)
      → wraps result in RuntimeMarketSnapshot

  scanner_to_orchestrator.py  (BRIDGE)
      raw scanner metrics + vix_data
      → InstitutionalDecisionInputs
      → BridgeTranslation (with derivation_notes, warnings)

Why this file exists separately:
  The bridge is a pure, stateless transformation function.
  Building a snapshot requires calling the orchestrator and
  measuring cycle duration — those are runtime concerns, not
  transformation concerns. Keeping them separate makes both
  individually testable without mocking the other.

Usage:
    from src.bridge.scanner_market_snapshot_builder import (
        build_snapshot,
    )

    snapshot = build_snapshot(metrics_map, vix_data)
    # snapshot is a RuntimeMarketSnapshot, ready for persistence.
"""

from __future__ import annotations

import time
from typing import Any

from src.bridge.scanner_to_orchestrator import translate
from src.orchestration.institutional_decision_orchestrator import (
    institutional_decision_orchestrator,
)
from src.runtime.runtime_market_snapshot import RuntimeMarketSnapshot


def build_snapshot(
    metrics_map: dict[str, Any],
    vix_data: dict[str, Any] | None,
) -> RuntimeMarketSnapshot:
    """
    Build a complete RuntimeMarketSnapshot from live scanner data.

    Steps:
      1. Translate scanner metrics to InstitutionalDecisionInputs (bridge).
      2. Run the institutional orchestrator to produce a decision.
      3. Wrap everything in an immutable RuntimeMarketSnapshot.

    Args:
        metrics_map: Output of scanner.build_symbol_metrics() for all symbols.
                     Keys are ticker symbols. Values are metric dicts or None.
        vix_data:    Output of scanner.get_vix_value(). May be None.

    Returns:
        RuntimeMarketSnapshot — immutable, timestamped, audit-ready.
    """
    start = time.monotonic()

    bridge = translate(metrics_map, vix_data)
    orchestrator_result = institutional_decision_orchestrator.evaluate(bridge.inputs)

    cycle_duration_ms = (time.monotonic() - start) * 1000

    return RuntimeMarketSnapshot.create(
        metrics_map=metrics_map,
        vix_data=vix_data,
        bridge=bridge,
        orchestrator_result=orchestrator_result,
        cycle_duration_ms=cycle_duration_ms,
    )
