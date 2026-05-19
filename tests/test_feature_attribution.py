from src.outcomes.confidence_calibration import ConfidenceCalibrationEngine
from src.outcomes.feature_attribution import FeatureAttributionEngine


def test_feature_attribution_alpha_signal():
    engine = FeatureAttributionEngine()

    result = engine.evaluate(
        feature="relative_strength",
        returns=[5, 4, 6, -1, 3],
    )

    assert result.classification == "alpha"
    assert result.win_rate_percent > 50


def test_confidence_calibration_increases_for_alpha():
    attribution_engine = FeatureAttributionEngine()
    calibration_engine = ConfidenceCalibrationEngine()

    attribution = attribution_engine.evaluate(
        feature="momentum",
        returns=[6, 5, 4, 3],
    )

    calibration = calibration_engine.calibrate(
        original_confidence=70,
        attribution=attribution,
    )

    assert calibration.calibrated_confidence > 70
