from __future__ import annotations

from collections import defaultdict


class RegimeOutcomeAnalysis:
    def summarize(
        self,
        historical_outcomes: list[dict],
    ) -> dict[str, dict[str, float]]:
        grouped: dict[str, list[float]] = defaultdict(list)

        for item in historical_outcomes:
            regime = item["regime"]
            performance = item["outcome"]["performance_percent"]

            grouped[regime].append(performance)

        summary: dict[str, dict[str, float]] = {}

        for regime, performances in grouped.items():
            avg_return = sum(performances) / len(performances)

            summary[regime] = {
                "average_return_percent": round(avg_return, 2),
                "sample_size": len(performances),
            }

        return summary


regime_outcome_analysis = RegimeOutcomeAnalysis()
