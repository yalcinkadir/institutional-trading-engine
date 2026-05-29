from src.validation.atr_governance import (
    AtrBar,
    AtrMethod,
    calculate_atr,
    evaluate_atr_migration_governance,
    true_ranges,
    wilder_atr_from_true_ranges,
)
from src.config.thresholds import ATR_CALCULATION_VERSION, THRESHOLDS_VERSION


def _bars():
    return [
        AtrBar(high=10.0, low=9.0, close=9.5),
        AtrBar(high=11.0, low=9.25, close=10.5),
        AtrBar(high=12.0, low=10.0, close=11.0),
        AtrBar(high=11.5, low=10.5, close=11.25),
        AtrBar(high=13.0, low=11.0, close=12.5),
        AtrBar(high=12.75, low=11.75, close=12.0),
    ]


def test_true_range_uses_previous_close_gap_risk():
    ranges = true_ranges(_bars())

    assert ranges[0] == 1.0
    assert ranges[1] == 1.75
    assert ranges[2] == 2.0


def test_wilder_atr_is_seeded_by_first_simple_average_then_smoothed():
    ranges = [1.0, 2.0, 3.0, 5.0]

    values = wilder_atr_from_true_ranges(ranges, period=3)

    assert values == [None, None, 2.0, 3.0]


def test_calculate_atr_requires_explicit_supported_method():
    simple_values = calculate_atr(_bars(), period=3, method=AtrMethod.SIMPLE)
    wilder_values = calculate_atr(_bars(), period=3, method=AtrMethod.WILDER)

    assert simple_values[:2] == [None, None]
    assert wilder_values[:2] == [None, None]
    assert simple_values[-1] != wilder_values[-1]


def test_atr_migration_governance_requires_evidence_invalidation_on_method_change():
    report = evaluate_atr_migration_governance(
        _bars(),
        period=3,
        current_method=AtrMethod.SIMPLE,
        candidate_method=AtrMethod.WILDER,
    )

    assert report.threshold_version == THRESHOLDS_VERSION
    assert report.atr_calculation_version == ATR_CALCULATION_VERSION
    assert report.evidence_invalidation_required
    assert not report.migration_allowed
    assert "atr_method_changed" in report.reasons
    assert "invalidate_prior_atr_dependent_evidence" in report.notes


def test_atr_governance_blocks_migration_until_enough_history_exists():
    report = evaluate_atr_migration_governance(
        _bars()[:2],
        period=3,
        current_method=AtrMethod.SIMPLE,
        candidate_method=AtrMethod.WILDER,
    )

    assert not report.migration_allowed
    assert not report.evidence_invalidation_required
    assert report.latest_current_atr is None
    assert "insufficient_atr_history" in report.reasons
