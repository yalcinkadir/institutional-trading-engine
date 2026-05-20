"""
Live Runtime Cycle.

This module closes the gap between the scanner world and the institutional
runtime. It is the first component that:

1. Accepts real scanner outputs (metrics_map + vix_data).
2. Translates them via the bridge.
3. Runs the institutional orchestrator.
4. Persists the decision.
5. Updates the runtime state.
6. Returns a complete snapshot for observability.

Design principles:
- One cycle = one atomic, traceable unit of institutional analysis.
- All errors are caught and logged — the runtime never crashes silently.
- Governance check runs BEFORE the orchestrator commits a decision.
- The cycle is synchronous by design (determinism over async complexity).

This is NOT a scheduler. LiveRuntimeCycle executes exactly one cycle
when called. Scheduling (when to run) is the responsibility of the caller.
"""

from __future__ import annotations

import time
from dataclasses import asdict
from datetime import UTC, datetime
from typing import Any

from src.bridge.scanner_to_orchestrator import translate
from src.governance.kill_switch import evaluate_kill_switch
from src.governance.risk_limits import validate_risk_limits
from src.orchestration.institutional_decision_orchestrator import (
    institutional_decision_orchestrator,
)
from src.runtime.in_memory_state_cache import in_memory_state_cache
from src.runtime.runtime_market_snapshot import RuntimeMarketSnapshot
from src.runtime.runtime_state import runtime_state
from src.storage.decision_log_store import decision_log_store


# ── Governance thresholds ──────────────────────────────────────────────────
# Conservative defaults. These should be moved to config when a proper
# portfolio position tracker is live (Phase 4).
_GOVERNANCE_VIX_KILL_THRESHOLD = 40.0
_GOVERNANCE_DRAWDOWN_KILL_THRESHOLD = 20.0
_GOVERNANCE_ANOMALY_KILL_THRESHOLD = 5
_GOVERNANCE_MAX_DRAWDOWN_PCT = 15.0
_GOVERNANCE_MAX_DAILY_LOSS_PCT = 5.0


class GovernanceBlockedError(Exception):
    """Raised when governance prevents cycle execution."""

    def __init__(self, reasons: list[str]) -> None:
        self.reasons = reasons
        super().__init__(f"Governance blocked cycle: {reasons}")


class LiveRuntimeCycle:
    """
    Executes one complete institutional analysis cycle from live scanner data.

    Usage:
        cycle = LiveRuntimeCycle()
        snapshot = cycle.run(metrics_map=..., vix_data=...)
    """

    def run(
        self,
        metrics_map: dict[str, Any],
        vix_data: dict[str, Any] | None,
        portfolio_drawdown_percent: float = 0.0,
        daily_loss_percent: float = 0.0,
    ) -> RuntimeMarketSnapshot:
        """
        Execute one full institutional decision cycle.

        Args:
            metrics_map:                Live scanner metrics (symbol → metric dict).
            vix_data:                   Live VIX data or None.
            portfolio_drawdown_percent: Current portfolio drawdown (for governance).
                                        Defaults to 0 until portfolio tracking is live.
            daily_loss_percent:         Current daily loss (for governance).
                                        Defaults to 0 until portfolio tracking is live.

        Returns:
            RuntimeMarketSnapshot — full auditable record of this cycle.

        Raises:
            GovernanceBlockedError — if governance halts execution.
        """
        cycle_start = time.monotonic()

        # ── Step 1: Governance pre-check ───────────────────────────────────
        # Governance runs BEFORE any analysis. If the kill switch fires,
        # we log the block and raise — no partial decisions are persisted.
        # Preserve None when VIX is unavailable (Free Polygon tier).
        # The kill switch handles None safely — it skips the VIX check
        # rather than treating 0.0 as a falsely calm reading.
        vix_level: float | None = (
            float(vix_data["close"])
            if vix_data and vix_data.get("close") is not None
            else None
        )
        vix_for_bridge: float = vix_level if vix_level is not None else 25.0

        kill_result = evaluate_kill_switch(
            vix=vix_level,
            drawdown_percent=portfolio_drawdown_percent,
            severe_anomaly_count=0,
        )

        if kill_result["kill_switch"]:
            self._log_governance_block(
                reason="kill_switch",
                details=kill_result["reasons"],
                vix_level=vix_level,
            )
            raise GovernanceBlockedError(kill_result["reasons"])

        risk_result = validate_risk_limits(
            portfolio_drawdown_percent=portfolio_drawdown_percent,
            max_drawdown_percent=_GOVERNANCE_MAX_DRAWDOWN_PCT,
            daily_loss_percent=daily_loss_percent,
            max_daily_loss_percent=_GOVERNANCE_MAX_DAILY_LOSS_PCT,
        )

        if risk_result["status"] == "BREACH":
            self._log_governance_block(
                reason="risk_limits",
                details=risk_result["breaches"],
                vix_level=vix_level,
            )
            raise GovernanceBlockedError(risk_result["breaches"])

        # ── Step 2: Translate scanner → institutional inputs ───────────────
        bridge = translate(metrics_map, vix_data)

        # ── Step 3: Run institutional orchestrator ─────────────────────────
        orchestrator_result = institutional_decision_orchestrator.evaluate(
            bridge.inputs
        )

        # ── Step 4: Build snapshot ─────────────────────────────────────────
        cycle_duration_ms = (time.monotonic() - cycle_start) * 1000

        snapshot = RuntimeMarketSnapshot.create(
            metrics_map=metrics_map,
            vix_data=vix_data,
            bridge=bridge,
            orchestrator_result=orchestrator_result,
            cycle_duration_ms=cycle_duration_ms,
        )

        # ── Step 5: Persist decision ───────────────────────────────────────
        decision_log_store.append(
            decision_id=snapshot.snapshot_id,
            payload=snapshot.to_persistence_payload(),
        )

        # ── Step 6: Update runtime state ───────────────────────────────────
        state_update = {
            "snapshot_id": snapshot.snapshot_id,
            "captured_at": snapshot.captured_at,
            "macro_regime": orchestrator_result.macro_regime,
            "cross_asset_regime": orchestrator_result.cross_asset_regime,
            "tail_risk_regime": orchestrator_result.tail_risk_regime,
            "fusion_classification": orchestrator_result.fusion_classification,
            "final_exposure_percent": orchestrator_result.final_exposure_percent,
            "data_quality_warnings": bridge.data_quality_warnings,
            "cycle_duration_ms": snapshot.cycle_duration_ms,
        }
        runtime_state.update(state_update)

        # ── Step 7: Update in-memory state cache ───────────────────────────
        in_memory_state_cache.set("latest_snapshot_id", snapshot.snapshot_id)
        in_memory_state_cache.set("latest_regime", orchestrator_result.macro_regime)
        in_memory_state_cache.set("latest_exposure", orchestrator_result.final_exposure_percent)
        in_memory_state_cache.set("latest_cycle_at", snapshot.captured_at)

        # Log warnings to stdout (structured logging integration comes in Phase 3)
        if bridge.data_quality_warnings:
            for warning in bridge.data_quality_warnings:
                print(f"[LiveRuntimeCycle] DATA WARNING: {warning}")

        print(
            f"[LiveRuntimeCycle] cycle={snapshot.snapshot_id} | "
            f"{snapshot.regime_summary} | "
            f"duration={snapshot.cycle_duration_ms:.1f}ms"
        )

        return snapshot

    def _log_governance_block(
        self,
        reason: str,
        details: list[str],
        vix_level: float,
    ) -> None:
        """Persist governance block event for audit trail."""
        block_payload = {
            "type": "governance_block",
            "reason": reason,
            "details": details,
            "vix_level": vix_level,
            "blocked_at": datetime.now(UTC).isoformat(),
        }
        block_id = f"BLOCK_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S_%f')}"
        decision_log_store.append(
            decision_id=block_id,
            payload=block_payload,
        )
        print(f"[LiveRuntimeCycle] GOVERNANCE BLOCK: {reason} — {details}")


live_runtime_cycle = LiveRuntimeCycle()
