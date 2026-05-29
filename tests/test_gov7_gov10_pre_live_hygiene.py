from src.validation.gov7_gov10_pre_live_hygiene import (
    DuplicateModuleMarker,
    classify_vix_term_structure,
    evaluate_cumulative_paper_observation_drift,
    normalize_public_weights_exact,
    validate_duplicate_module_markers,
)


def test_gov7_normalized_public_weights_sum_exactly_one_after_rounding() -> None:
    result = normalize_public_weights_exact(
        {
            "momentum": 1,
            "quality": 1,
            "risk": 1,
        },
        decimals=2,
    )

    assert result.is_valid
    assert result.sum_after_rounding == 1.0
    assert round(sum(result.weights.values()), 2) == 1.0
    assert result.adjusted_key in result.weights


def test_gov7_rejects_negative_weights() -> None:
    result = normalize_public_weights_exact({"a": 1, "b": -1})

    assert not result.is_valid
    assert "negative_weight:b" in result.issues


def test_gov8_direct_vix_term_structure_inversion_is_explicit() -> None:
    result = classify_vix_term_structure(front_month_vix=22.0, second_month_vix=21.5)

    assert result.is_valid
    assert result.mode == "DIRECT"
    assert result.is_inverted is True
    assert result.severity == "HIGH"


def test_gov8_partial_vix_term_structure_compression_is_not_direct_inversion() -> None:
    result = classify_vix_term_structure(front_month_vix=20.0, second_month_vix=20.25)

    assert result.is_valid
    assert result.mode == "PARTIAL"
    assert result.is_inverted is False
    assert result.severity == "MEDIUM"


def test_gov8_missing_vix_term_structure_is_unknown() -> None:
    result = classify_vix_term_structure(front_month_vix=None, second_month_vix=21.0)

    assert not result.is_valid
    assert result.mode == "UNKNOWN"
    assert result.issues == ["missing_vix_term_structure"]


def test_gov9_duplicate_module_markers_require_owner_replacement_and_rationale() -> None:
    result = validate_duplicate_module_markers(
        [
            DuplicateModuleMarker(
                module_path="src/legacy/risk_gate.py",
                status="DEPRECATED",
                owner_module="src/governance/risk_limits.py",
                replacement_module="src/governance/risk_limits.py",
                rationale="Legacy wrapper overlaps with authoritative governance risk limits.",
            )
        ]
    )

    assert result.is_valid
    assert result.issues == []


def test_gov9_duplicate_module_marker_validation_fails_closed() -> None:
    result = validate_duplicate_module_markers(
        [
            DuplicateModuleMarker(
                module_path="src/legacy/risk_gate.py",
                status="DEPRECATED",
                owner_module="",
                replacement_module=None,
                rationale="",
            )
        ]
    )

    assert not result.is_valid
    assert "missing_owner_module:src/legacy/risk_gate.py" in result.issues
    assert "missing_replacement_module:src/legacy/risk_gate.py" in result.issues
    assert "missing_rationale:src/legacy/risk_gate.py" in result.issues


def test_gov10_cumulative_drift_detects_small_persistent_daily_drift() -> None:
    result = evaluate_cumulative_paper_observation_drift(
        [0.04, 0.04, 0.04, 0.04],
        cumulative_threshold=0.10,
    )

    assert result.breached is True
    assert result.max_abs_daily_drift == 0.04
    assert round(result.cumulative_abs_drift, 2) == 0.16
    assert result.message == "cumulative_drift_breach"


def test_gov10_cumulative_drift_passes_clean_observation_series() -> None:
    result = evaluate_cumulative_paper_observation_drift(
        [0.01, -0.01, 0.0],
        cumulative_threshold=0.10,
    )

    assert result.breached is False
    assert result.observations == 3
    assert result.message == "cumulative_drift_within_threshold"
