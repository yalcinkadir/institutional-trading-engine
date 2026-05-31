from __future__ import annotations

from pathlib import Path

from src.operations.drift_regime_evidence import (
    SCHEMA_VERSION,
    build_drift_metric,
    build_drift_regime_evidence,
    build_regime_change_evidence,
    load_drift_regime_evidence,
    validate_drift_regime_evidence,
    write_drift_regime_evidence,
)


def test_build_drift_metric_pass_warn_fail_thresholds() -> None:
    passing = build_drift_metric(
        name="decision_score_mean",
        observed_value=0.61,
        expected_value=0.60,
        warn_threshold=0.05,
        fail_threshold=0.15,
    )
    warning = build_drift_metric(
        name="decision_score_mean",
        observed_value=0.68,
        expected_value=0.60,
        warn_threshold=0.05,
        fail_threshold=0.15,
    )
    failing = build_drift_metric(
        name="decision_score_mean",
        observed_value=0.80,
        expected_value=0.60,
        warn_threshold=0.05,
        fail_threshold=0.15,
    )

    assert passing.status == "PASS"
    assert warning.status == "WARN"
    assert failing.status == "FAIL"


def test_regime_change_stable_transition_passes() -> None:
    evidence = build_regime_change_evidence(
        previous_regime="BULL",
        current_regime="BULL",
    )

    assert evidence.status == "PASS"
    assert evidence.transition == "BULL->BULL"
    assert evidence.warnings == []


def test_regime_change_minor_transition_warns() -> None:
    evidence = build_regime_change_evidence(
        previous_regime="BULL",
        current_regime="NEUTRAL",
    )

    assert evidence.status == "WARN"
    assert "minor_regime_transition" in evidence.warnings


def test_regime_change_major_transition_fails() -> None:
    evidence = build_regime_change_evidence(
        previous_regime="RISK_ON",
        current_regime="RISK_OFF",
    )

    assert evidence.status == "FAIL"
    assert "major_regime_transition" in evidence.warnings


def test_unknown_regime_warns() -> None:
    evidence = build_regime_change_evidence(
        previous_regime=None,
        current_regime="BULL",
    )

    assert evidence.status == "WARN"
    assert "regime_unknown" in evidence.warnings


def test_drift_regime_evidence_passes_for_clean_day() -> None:
    metric = build_drift_metric(
        name="decision_score_mean",
        observed_value=0.61,
        expected_value=0.60,
        warn_threshold=0.05,
        fail_threshold=0.15,
    )

    evidence = build_drift_regime_evidence(
        trading_date="2026-05-31",
        drift_metrics=[metric],
        previous_regime="BULL",
        current_regime="BULL",
        cumulative_drift_value=0.02,
        created_at="2026-05-31T20:00:00+00:00",
    )

    assert evidence.schema_version == SCHEMA_VERSION
    assert evidence.status == "PASS"
    assert evidence.cumulative_drift_status == "PASS"
    assert evidence.live_trading_authorized is False
    assert validate_drift_regime_evidence(evidence) == {
        "status": "PASS",
        "errors": [],
    }


def test_drift_regime_evidence_warns_for_minor_regime_change() -> None:
    metric = build_drift_metric(
        name="decision_score_mean",
        observed_value=0.61,
        expected_value=0.60,
    )

    evidence = build_drift_regime_evidence(
        trading_date="2026-05-31",
        drift_metrics=[metric],
        previous_regime="BULL",
        current_regime="NEUTRAL",
        cumulative_drift_value=0.02,
        created_at="2026-05-31T20:00:00+00:00",
    )

    assert evidence.status == "WARN"
    assert evidence.regime_change.status == "WARN"


def test_drift_regime_evidence_fails_for_metric_fail() -> None:
    metric = build_drift_metric(
        name="decision_score_mean",
        observed_value=0.90,
        expected_value=0.60,
        warn_threshold=0.05,
        fail_threshold=0.15,
    )

    evidence = build_drift_regime_evidence(
        trading_date="2026-05-31",
        drift_metrics=[metric],
        previous_regime="BULL",
        current_regime="BULL",
        cumulative_drift_value=0.02,
        created_at="2026-05-31T20:00:00+00:00",
    )

    assert evidence.status == "FAIL"


def test_drift_regime_evidence_fails_for_cumulative_drift() -> None:
    metric = build_drift_metric(
        name="decision_score_mean",
        observed_value=0.61,
        expected_value=0.60,
    )

    evidence = build_drift_regime_evidence(
        trading_date="2026-05-31",
        drift_metrics=[metric],
        previous_regime="BULL",
        current_regime="BULL",
        cumulative_drift_value=0.35,
        cumulative_drift_warn_threshold=0.10,
        cumulative_drift_fail_threshold=0.30,
        created_at="2026-05-31T20:00:00+00:00",
    )

    assert evidence.status == "FAIL"
    assert evidence.cumulative_drift_status == "FAIL"


def test_write_and_load_drift_regime_evidence_round_trip(tmp_path: Path) -> None:
    metric = build_drift_metric(
        name="decision_score_mean",
        observed_value=0.61,
        expected_value=0.60,
    )
    evidence = build_drift_regime_evidence(
        trading_date="2026-05-31",
        drift_metrics=[metric],
        previous_regime="BULL",
        current_regime="BULL",
        created_at="2026-05-31T20:00:00+00:00",
        notes=["paper observation only"],
    )

    output_path = write_drift_regime_evidence(evidence, output_dir=tmp_path)
    latest_path = tmp_path / "latest-drift-regime-evidence.json"

    assert output_path.exists()
    assert latest_path.exists()

    loaded = load_drift_regime_evidence(output_path)

    assert loaded == evidence


def test_validation_rejects_live_trading_authorization_mutation() -> None:
    metric = build_drift_metric(
        name="decision_score_mean",
        observed_value=0.61,
        expected_value=0.60,
    )
    evidence = build_drift_regime_evidence(
        trading_date="2026-05-31",
        drift_metrics=[metric],
        previous_regime="BULL",
        current_regime="BULL",
        created_at="2026-05-31T20:00:00+00:00",
    )

    mutated = evidence.__class__(
        schema_version=evidence.schema_version,
        trading_date=evidence.trading_date,
        created_at=evidence.created_at,
        status=evidence.status,
        drift_metrics=evidence.drift_metrics,
        regime_change=evidence.regime_change,
        cumulative_drift_value=evidence.cumulative_drift_value,
        cumulative_drift_warn_threshold=evidence.cumulative_drift_warn_threshold,
        cumulative_drift_fail_threshold=evidence.cumulative_drift_fail_threshold,
        cumulative_drift_status=evidence.cumulative_drift_status,
        notes=evidence.notes,
        live_trading_authorized=True,
    )

    validation = validate_drift_regime_evidence(mutated)

    assert validation["status"] == "FAIL"
    assert "live_trading_authorized_must_be_false" in validation["errors"]