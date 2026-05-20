"""
Runtime Market Snapshot.

A snapshot is an immutable, timestamped record of one complete scanner cycle.
It carries both the raw scanner output and the translated institutional inputs,
so the full derivation chain is preserved for auditability and replay.

Design principles:
- Immutable after construction (frozen dataclass).
- Always timestamped in UTC.
- Carries warnings so the runtime can log or react to data quality issues.
- No business logic — pure data container.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from src.bridge.scanner_to_orchestrator import BridgeTranslation
from src.orchestration.institutional_decision_orchestrator import (
    InstitutionalDecisionResult,
)


@dataclass(frozen=True)
class RuntimeMarketSnapshot:
    """
    One complete institutional analysis cycle.

    Fields:
        snapshot_id:         Unique identifier (UTC timestamp string).
        captured_at:         ISO 8601 UTC timestamp.
        metrics_map:         Raw scanner metrics for all symbols.
        vix_data:            Raw VIX data from scanner (or None).
        bridge:              Full bridge translation including derivation notes.
        orchestrator_result: Final institutional decision result.
        cycle_duration_ms:   How long the cycle took to compute (ms).
    """

    snapshot_id: str
    captured_at: str
    metrics_map: dict[str, Any]
    vix_data: dict[str, Any] | None
    bridge: BridgeTranslation
    orchestrator_result: InstitutionalDecisionResult
    cycle_duration_ms: float

    @classmethod
    def create(
        cls,
        metrics_map: dict[str, Any],
        vix_data: dict[str, Any] | None,
        bridge: BridgeTranslation,
        orchestrator_result: InstitutionalDecisionResult,
        cycle_duration_ms: float,
    ) -> RuntimeMarketSnapshot:
        """Factory method ensures consistent ID and timestamp generation."""
        now = datetime.now(UTC)
        snapshot_id = now.strftime("%Y%m%d_%H%M%S_%f")
        return cls(
            snapshot_id=snapshot_id,
            captured_at=now.isoformat(),
            metrics_map=metrics_map,
            vix_data=vix_data,
            bridge=bridge,
            orchestrator_result=orchestrator_result,
            cycle_duration_ms=round(cycle_duration_ms, 2),
        )

    def to_persistence_payload(self) -> dict[str, Any]:
        """
        Serialise to a flat dict suitable for DecisionLogStore.

        Does NOT include the full metrics_map (too large for JSONL).
        Includes: institutional result, bridge inputs, derivation notes,
        and data quality warnings.
        """
        result = self.orchestrator_result
        inputs = self.bridge.inputs

        return {
            "snapshot_id": self.snapshot_id,
            "captured_at": self.captured_at,
            "cycle_duration_ms": self.cycle_duration_ms,
            "data_quality_warnings": self.bridge.data_quality_warnings,
            "symbols_used": self.bridge.symbols_used,
            "symbol_count": len(self.bridge.symbols_used),

            # Institutional result
            "macro_regime": result.macro_regime,
            "cross_asset_regime": result.cross_asset_regime,
            "tail_risk_regime": result.tail_risk_regime,
            "liquidity_risk": result.liquidity_risk,
            "fusion_classification": result.fusion_classification,
            "probabilistic_classification": result.probabilistic_classification,
            "execution_aggressiveness": result.execution_aggressiveness,
            "final_exposure_percent": result.final_exposure_percent,
            "explanation": result.explanation,

            # Key derived inputs (for reproducibility)
            "inputs": {
                "market_regime_score": inputs.market_regime_score,
                "equity_strength": inputs.equity_strength,
                "bond_strength": inputs.bond_strength,
                "dollar_strength": inputs.dollar_strength,
                "gold_strength": inputs.gold_strength,
                "volatility_level": inputs.volatility_level,
                "gap_risk_percent": inputs.gap_risk_percent,
                "liquidity_stress_percent": inputs.liquidity_stress_percent,
                "feature_alpha_score": inputs.feature_alpha_score,
            },

            # Derivation audit trail
            "derivation_notes": self.bridge.derivation_notes,
        }

    @property
    def has_data_quality_issues(self) -> bool:
        return len(self.bridge.data_quality_warnings) > 0

    @property
    def regime_summary(self) -> str:
        r = self.orchestrator_result
        return (
            f"macro={r.macro_regime} | "
            f"cross_asset={r.cross_asset_regime} | "
            f"tail={r.tail_risk_regime} | "
            f"fusion={r.fusion_classification} | "
            f"exposure={r.final_exposure_percent:.1f}%"
        )
