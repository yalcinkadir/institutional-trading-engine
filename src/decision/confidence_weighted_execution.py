from __future__ import annotations

from dataclasses import dataclass

from src.decision.probabilistic_decision_engine import ProbabilisticDecision


@dataclass(frozen=True)
class ExecutionPlan:
    exposure_percent: float
    execution_aggressiveness: str
    reasoning: str


class ConfidenceWeightedExecution:
    def generate(
        self,
        decision: ProbabilisticDecision,
    ) -> ExecutionPlan:
        confidence = decision.confidence_score

        if confidence >= 80:
            return ExecutionPlan(
                exposure_percent=100,
                execution_aggressiveness="high",
                reasoning="high_confidence_environment",
            )

        if confidence >= 60:
            return ExecutionPlan(
                exposure_percent=70,
                execution_aggressiveness="moderate",
                reasoning="moderate_confidence_environment",
            )

        return ExecutionPlan(
            exposure_percent=40,
            execution_aggressiveness="low",
            reasoning="uncertain_environment",
        )


confidence_weighted_execution = ConfidenceWeightedExecution()
