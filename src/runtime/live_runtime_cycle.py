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
from src.governance.governance_thresholds import (
    DEFAULT_GOVERNANCE_THRESHOLDS,
    GovernanceThresholds,
)
from src.governance.kill_switch import evaluate_kill_switch
from src.governance.risk_limits import validate_risk_limits
from src.orchestration.institutional_decision_orchestrator import (
    institutional_decision_orchestrator,
)
from src.runtime.anomaly_state import AnomalyState, AnomalyStateStore
from src.runtime.in_memory_state_cache import in_memory_state_cache
from src.runtime.portfolio_state import PortfolioState, PortfolioStateStore
from src.runtime.runtime_market_snapshot import RuntimeMarketSnapshot
from src.runtime.runtime_state import runtime_state
from src.storage.decision_log_store import decision_log_store
from src.structured_logging import emit_structured_log


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

    def __init__(
        self,
        portfolio_state_store: PortfolioStateStore | None = None,
        anomaly_state_store: AnomalyStateStore | None = None,
    ) -> None:
        self.portfolio_state_store = portfolio_state_store or PortfolioStateStore()
        self.anomaly_state_store = anomaly_state_store or AnomalyStateStore()

    def _log(
        self,
        *,
        level: str,
        event_type: str,
        message: str,
        cycle_id: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        emit_structured_log(
            level=level,
            event_type=event_type,
            component="live_runtime_cycle",
            message=message,
            cycle_id=cycle_id,
            context=context or {},
        )

    def run(
        self,
        metrics_map: dict[str, Any],
        vix_data: dict[str, Any] | None,
        portfolio_drawdown_percent: float | None = None,
        daily_loss_percent: float | None = None,
    ) -> RuntimeMarketSnapshot:
        """
        Execute one full institutional decision cycle.

        Args:
            metrics_map:                Live scanner metrics (symbol → metric dict).
            vix_data:                   Live VIX data or None.
            portfolio_drawdown_percent: Deprecated runtime argument. Supplying it is
                                        treated as untrusted and governance fails closed.
            daily_loss_percent:         Deprecated runtime argument. Supplying it is
                                        treated as untrusted and governance fails closed.

        Returns:
            RuntimeMarketSnapshot — full auditable record of this cycle.

        Raises:
            GovernanceBlockedError — if governance halts execution.
        """
        cycle_start = time.monotonic()
        preliminary_cycle_id = f"live-runtime-cycle-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}"
        self._log(
            level="INFO",
            event_type="live_runtime_cycle_started",
            message="Live runtime cycle started.",
            cycle_id=preliminary_cycle_id,
            context={
                "symbols": len(metrics_map),
                "has_vix_data": vix_data is not None,
                "portfolio_override": portfolio_drawdown_percent is not None or daily_loss_percent is not None,
            },
        )

        portfolio_state = self._resolve_portfolio_state(
            portfolio_drawdown_percent=portfolio_drawdown_percent,
            daily_loss_percent=daily_loss_percent,
        )

        if not portfolio_state.governance_valid:
            self._log_governance_block(
                reason="portfolio_state_invalid",
                details=["portfolio_state_invalid_or_missing"],
                vix_level=None,
                portfolio_state=portfolio_state,
                cycle_id=preliminary_cycle_id,
            )
            raise GovernanceBlockedError(["portfolio_state_invalid_or_missing"])

        portfolio_drawdown_for_governance = portfolio_state.drawdown_percent
        daily_loss_for_governance = portfolio_state.daily_loss_percent
        anomaly_state = self._resolve_anomaly_state()
        severe_anomaly_count = anomaly_state.severe_anomaly_count

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
            drawdown_percent=portfolio_drawdown_for_governance,
            severe_anomaly_count=severe_anomaly_count,
        )

        if kill_result["kill_switch"]:
            self._log_governance_block(
                reason="kill_switch",
                details=kill_result["reasons"],
                vix_level=vix_level,
                portfolio_state=portfolio_state,
                cycle_id=preliminary_cycle_id,
            )
            raise GovernanceBlockedError(kill_result["reasons"])

        risk_result = validate_risk_limits(
            portfolio_drawdown_percent=portfolio_drawdown_for_governance,
            max_drawdown_percent=_GOVERNANCE_MAX_DRAWDOWN_PCT,
            daily_loss_percent=daily_loss_for_governance,
            max_daily_loss_percent=_GOVERNANCE_MAX_DAILY_LOSS_PCT,
        )

        if risk_result["status"] == "BREACH":
            self._log_governance_block(
                reason="risk_limits",
                details=risk_result["breaches"],
                vix_level=vix_level,
                portfolio_state=portfolio_state,
                cycle_id=preliminary_cycle_id,
            )
            raise GovernanceBlockedError(risk_result["breaches"])

        self._log(
            level="INFO",
            event_type="live_runtime_governance_passed",
            message="Live runtime governance checks passed.",
            cycle_id=preliminary_cycle_id,
            context={
                "vix_level": vix_level,
                "portfolio_drawdown_percent": portfolio_state.drawdown_percent,
                "daily_loss_percent": portfolio_state.daily_loss_percent,
                "severe_anomaly_count": severe_anomaly_count,
                "anomaly_state_source": anomaly_state.source,
                "anomaly_state_warnings": anomaly_state.warnings,
            },
        )

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
        cycle_id = snapshot.snapshot_id

        # ── Step 5: Persist decision ───────────────────────────────────────
        payload = snapshot.to_persistence_payload()
        payload["portfolio_state"] = portfolio_state.to_dict()
        payload["anomaly_state"] = anomaly_state.to_dict()
        payload["severe_anomaly_count"] = severe_anomaly_count
        decision_log_store.append(
            decision_id=snapshot.snapshot_id,
            payload=payload,
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
            "portfolio_state_warnings": portfolio_state.warnings,
            "anomaly_state_warnings": anomaly_state.warnings,
            "anomaly_state_source": anomaly_state.source,
            "severe_anomaly_count": severe_anomaly_count,
            "cycle_duration_ms": snapshot.cycle_duration_ms,
        }
        runtime_state.update(state_update)

        # ── Step 7: Update in-memory state cache ───────────────────────────
        in_memory_state_cache.set("latest_snapshot_id", snapshot.snapshot_id)
        in_memory_state_cache.set("latest_regime", orchestrator_result.macro_regime)
        in_memory_state_cache.set("latest_exposure", orchestrator_result.final_exposure_percent)
        in_memory_state_cache.set("latest_cycle_at", snapshot.captured_at)
        in_memory_state_cache.set("latest_portfolio_drawdown_percent", portfolio_state.drawdown_percent)
        in_memory_state_cache.set("latest_daily_loss_percent", portfolio_state.daily_loss_percent)
        in_memory_state_cache.set("latest_severe_anomaly_count", severe_anomaly_count)
        in_memory_state_cache.set("latest_anomaly_state_source", anomaly_state.source)

        if bridge.data_quality_warnings:
            for warning in bridge.data_quality_warnings:
                print(f"[LiveRuntimeCycle] DATA WARNING: {warning}")
            self._log(
                level="WARNING",
                event_type="live_runtime_data_quality_warning",
                message="Live runtime bridge produced data quality warnings.",
                cycle_id=cycle_id,
                context={"warnings": bridge.data_quality_warnings},
            )

        if portfolio_state.warnings:
            for warning in portfolio_state.warnings:
                print(f"[LiveRuntimeCycle] PORTFOLIO STATE WARNING: {warning}")
            self._log(
                level="WARNING",
                event_type="live_runtime_portfolio_state_warning",
                message="Live runtime portfolio state warning.",
                cycle_id=cycle_id,
                context={"warnings": portfolio_state.warnings, "source": portfolio_state.source},
            )

        if anomaly_state.warnings:
            for warning in anomaly_state.warnings:
                print(f"[LiveRuntimeCycle] ANOMALY STATE WARNING: {warning}")
            self._log(
                level="WARNING",
                event_type="live_runtime_anomaly_state_warning",
                message="Live runtime anomaly state warning.",
                cycle_id=cycle_id,
                context={"warnings": anomaly_state.warnings, "source": anomaly_state.source},
            )

        print(
            f"[LiveRuntimeCycle] cycle={snapshot.snapshot_id} | "
            f"{snapshot.regime_summary} | "
            f"portfolio_drawdown={portfolio_state.drawdown_percent:.2f}% | "
            f"daily_loss={portfolio_state.daily_loss_percent:.2f}% | "
            f"severe_anomalies={severe_anomaly_count} | "
            f"anomaly_source={anomaly_state.source} | "
            f"duration={snapshot.cycle_duration_ms:.1f}ms"
        )
        self._log(
            level="INFO",
            event_type="live_runtime_cycle_completed",
            message="Live runtime cycle completed.",
            cycle_id=cycle_id,
            context={
                "macro_regime": orchestrator_result.macro_regime,
                "fusion_classification": orchestrator_result.fusion_classification,
                "final_exposure_percent": orchestrator_result.final_exposure_percent,
                "cycle_duration_ms": snapshot.cycle_duration_ms,
            },
        )

        return snapshot

    def _resolve_portfolio_state(
        self,
        portfolio_drawdown_percent: float | None,
        daily_loss_percent: float | None,
    ) -> PortfolioState:
        """Load portfolio state and fail closed for untrusted runtime overrides."""

        if portfolio_drawdown_percent is not None or daily_loss_percent is not None:
            return PortfolioState(
                equity_start=0.0,
                equity_current=0.0,
                drawdown_percent=float(portfolio_drawdown_percent or 0.0),
                daily_loss_percent=float(daily_loss_percent or 0.0),
                open_positions=[],
                source="runtime_argument_override_rejected",
                warnings=[
                    "Portfolio state supplied via runtime arguments is not a trusted governance source.",
                    "Provide data/portfolio_state.json or an injected PortfolioStateStore before runtime governance can pass.",
                ],
                governance_valid=False,
            )

        return self.portfolio_state_store.load()

    def _resolve_anomaly_state(self) -> AnomalyState:
        """Read anomaly state from persistent storage, with cache as fallback only."""

        persistent_state = self.anomaly_state_store.load()
        if persistent_state.source == "anomaly_state_json":
            return persistent_state

        cached_count = self._resolve_cached_severe_anomaly_count()
        if cached_count is not None:
            return AnomalyState(
                severe_anomaly_count=cached_count,
                anomaly_count=cached_count,
                classification=(
                    "Extreme Instability" if cached_count >= 5 else
                    "Elevated Instability" if cached_count >= 3 else
                    "Watchlist Environment" if cached_count >= 1 else
                    "Stable"
                ),
                source="runtime_cache_fallback",
                warnings=[
                    *persistent_state.warnings,
                    "Using process-local anomaly cache because persistent anomaly state is unavailable.",
                ],
            )

        return persistent_state

    def _resolve_cached_severe_anomaly_count(self) -> int | None:
        """Legacy cache fallback for tests/dev; not the primary governance source."""

        raw_value = in_memory_state_cache.get("severe_anomaly_count")
        if raw_value is None:
            raw_value = in_memory_state_cache.get("latest_severe_anomaly_count")
        if raw_value is None:
            return None
        if not isinstance(raw_value, (int, float, str)):
            return None
        try:
            return max(0, int(float(raw_value)))
        except (TypeError, ValueError):
            return None

    def _log_governance_block(
        self,
        reason: str,
        details: list[str],
        vix_level: float | None,
        portfolio_state: PortfolioState,
        cycle_id: str | None = None,
    ) -> None:
        """Persist governance block event for audit trail."""
        block_payload = {
            "type": "governance_block",
            "reason": reason,
            "details": details,
            "vix_level": vix_level,
            "portfolio_state": portfolio_state.to_dict(),
            "blocked_at": datetime.now(UTC).isoformat(),
        }
        block_id = f"BLOCK_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S_%f')}"
        decision_log_store.append(
            decision_id=block_id,
            payload=block_payload,
        )
        self._log(
            level="ERROR",
            event_type="live_runtime_governance_blocked",
            message="Live runtime cycle blocked by governance.",
            cycle_id=cycle_id or block_id,
            context={
                "reason": reason,
                "details": details,
                "vix_level": vix_level,
                "portfolio_source": portfolio_state.source,
                "portfolio_drawdown_percent": portfolio_state.drawdown_percent,
                "daily_loss_percent": portfolio_state.daily_loss_percent,
                "portfolio_governance_valid": portfolio_state.governance_valid,
            },
        )
        print(f"[LiveRuntimeCycle] GOVERNANCE BLOCK: {reason} — {details}")


live_runtime_cycle = LiveRuntimeCycle()