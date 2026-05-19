from __future__ import annotations

from dataclasses import dataclass

from src.outcomes.signal_decay_detection import SignalDecayResult


@dataclass(frozen=True)
class AdaptiveWeight:
    module: str
    original_weight: float
    adjusted_weight: float
    reason: str


class AdaptiveWeightingEngine:
    def adjust(
        self,
        original_weight: float,
        decay_result: SignalDecayResult,
    ) -> AdaptiveWeight:
        adjusted_weight = original_weight
        reason = "stable"

        if decay_result.severity == "warning":
            adjusted_weight *= 0.75
            reason = "moderate_decay"

        elif decay_result.severity == "critical":
            adjusted_weight *= 0.5
            reason = "severe_decay"

        return AdaptiveWeight(
            module=decay_result.module,
            original_weight=round(original_weight, 4),
            adjusted_weight=round(adjusted_weight, 4),
            reason=reason,
        )


adaptive_weighting_engine = AdaptiveWeightingEngine()
