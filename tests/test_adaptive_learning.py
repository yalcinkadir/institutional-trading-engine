from src.outcomes.adaptive_weighting import AdaptiveWeightingEngine
from src.outcomes.signal_decay_detection import SignalDecayDetector


def test_signal_decay_detection_warning():
    detector = SignalDecayDetector()

    result = detector.evaluate(
        module="relative_strength",
        returns=[-3, -2, -4],
    )

    assert result.degraded is True
    assert result.severity == "warning"


def test_adaptive_weight_reduction():
    detector = SignalDecayDetector()
    weighting = AdaptiveWeightingEngine()

    decay = detector.evaluate(
        module="momentum",
        returns=[-6, -7, -5],
    )

    adjusted = weighting.adjust(
        original_weight=1.0,
        decay_result=decay,
    )

    assert adjusted.adjusted_weight == 0.5
    assert adjusted.reason == "severe_decay"
