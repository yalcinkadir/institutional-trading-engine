from __future__ import annotations

from dataclasses import dataclass

from src.outcomes.feature_attribution import FeatureAttributionResult


@dataclass(frozen=True)
class ConfidenceCalibration:
    feature: str
    original_confidence: float
    calibrated_confidence: float
    adjustment_reason: str


class ConfidenceCalibrationEngine:
    def calibrate(
        self,
        original_confidence: float,
        attribution: FeatureAttributionResult,
    ) -> ConfidenceCalibration:
        calibrated = original_confidence
        reason = "stable"

        if attribution.classification == "alpha":
            calibrated *= 1.1
            reason = "positive_attribution"

        elif attribution.classification == "noise":
            calibrated *= 0.7
            reason = "negative_attribution"

        calibrated = min(max(calibrated, 0), 100)

        return ConfidenceCalibration(
            feature=attribution.feature,
            original_confidence=round(original_confidence, 2),
            calibrated_confidence=round(calibrated, 2),
            adjustment_reason=reason,
        )


confidence_calibration_engine = ConfidenceCalibrationEngine()
