from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FeatureAttributionResult:
    feature: str
    average_return_percent: float
    win_rate_percent: float
    contribution_score: float
    classification: str


class FeatureAttributionEngine:
    def evaluate(
        self,
        feature: str,
        returns: list[float],
    ) -> FeatureAttributionResult:
        if not returns:
            raise ValueError("returns must not be empty")

        average_return = sum(returns) / len(returns)

        wins = sum(1 for value in returns if value > 0)
        win_rate = (wins / len(returns)) * 100

        contribution_score = (
            (average_return * 0.6)
            + ((win_rate / 100) * 40)
        )

        if contribution_score >= 20:
            classification = "alpha"
        elif contribution_score >= 5:
            classification = "neutral"
        else:
            classification = "noise"

        return FeatureAttributionResult(
            feature=feature,
            average_return_percent=round(average_return, 2),
            win_rate_percent=round(win_rate, 2),
            contribution_score=round(contribution_score, 2),
            classification=classification,
        )


feature_attribution_engine = FeatureAttributionEngine()
