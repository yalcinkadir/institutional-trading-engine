from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SignalDecayResult:
    module: str
    average_return_percent: float
    degraded: bool
    severity: str


class SignalDecayDetector:
    def evaluate(
        self,
        module: str,
        returns: list[float],
        degradation_threshold: float = -2.0,
    ) -> SignalDecayResult:
        if not returns:
            raise ValueError("returns must not be empty")

        average_return = sum(returns) / len(returns)

        degraded = average_return <= degradation_threshold

        if average_return <= -5:
            severity = "critical"
        elif degraded:
            severity = "warning"
        else:
            severity = "healthy"

        return SignalDecayResult(
            module=module,
            average_return_percent=round(average_return, 2),
            degraded=degraded,
            severity=severity,
        )


signal_decay_detector = SignalDecayDetector()
