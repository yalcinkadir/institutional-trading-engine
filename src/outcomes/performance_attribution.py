from __future__ import annotations

from collections import defaultdict

from src.outcomes.real_outcome_evaluator import OutcomeEvaluation


class PerformanceAttribution:
    def summarize(
        self,
        module_outcomes: dict[str, list[OutcomeEvaluation]],
    ) -> dict[str, dict[str, float]]:
        summary: dict[str, dict[str, float]] = {}

        for module, outcomes in module_outcomes.items():
            if not outcomes:
                continue

            total = len(outcomes)
            wins = sum(1 for outcome in outcomes if outcome.classification == "WIN")

            average_return = sum(
                outcome.performance_percent
                for outcome in outcomes
            ) / total

            summary[module] = {
                "win_rate_percent": round((wins / total) * 100, 2),
                "average_return_percent": round(average_return, 2),
                "sample_size": total,
            }

        return summary


performance_attribution = PerformanceAttribution()
