import json

import pytest

from src.config.thresholds import DEFAULT_THRESHOLDS
from src.validation.historical_edge_validation import HistoricalEdgeValidationConfig
from src.validation.out_of_sample_lockbox import (
    DEFAULT_OOS_SPLIT_DATE,
    VALIDATION_METHOD,
    VALIDATION_SCOPE_NOTE,
    OutOfSampleLockboxConfig,
    build_evidence_contract_hash,
    build_out_of_sample_lockbox,
    render_out_of_sample_lockbox_markdown,
    write_out_of_sample_lockbox_report,
)


def _records(date_value: str, result_r: float, count: int) -> list[dict[str, object]]:
    return [{"exit_date": date_value, "result_r": result_r} for _ in range(count)]


def _versioned_records(date_value: str, result_r: float, count: int, version: str) -> list[dict[str, object]]:
    return [
        {"exit_date": date_value, "result_r": result_r, "thresholds_version": version}
        for _ in range(count)
    ]


def _edge_config(
    *,
    min_total_trades: int = 2,
    min_expectancy_r: float = 0.1,
    min_profit_factor: float = 1.0,
    max_drawdown_limit: float = 10,
    min_sharpe_ratio: float = -10,
) -> HistoricalEdgeValidationConfig:
    return HistoricalEdgeValidationConfig(
        min_total_trades=min_total_trades,
        min_expectancy_r=min_expectancy_r,
        min_profit_factor=min_profit_factor,
        max_drawdown_limit=max_drawdown_limit,
        min_sharpe_ratio=min_sharpe_ratio,
        min_deflated_sharpe_probability=0.0,
        bootstrap_iterations=100,
    )


def _config() -> OutOfSampleLockboxConfig:
    return OutOfSampleLockboxConfig(
        split_date=DEFAULT_OOS_SPLIT_DATE,
        max_core_metric_degradation=0.20,
        edge_config=_edge_config(),
    )


def test_lockbox_splits_records_by_fixed_oos_date() -> None:
    records = _records("2023-12-31", 1.0, 2) + _records("2024-01-01", 1.0, 2)

    report = build_out_of_sample_lockbox(records, config=_config())

    assert report.split_date == "2024-01-01"
    assert report.validation_method == VALIDATION_METHOD
    assert report.validation_scope_note == VALIDATION_SCOPE_NOTE
    assert report.threshold_version == DEFAULT_THRESHOLDS.version
    assert report.evidence_contract_hash == build_evidence_contract_hash(_config())
    assert report.in_sample_count == 2
    assert report.out_of_sample_count == 2
    assert report.unassigned_records == 0


def test_lockbox_passes_when_oos_degradation_is_within_limit() -> None:
    records = _records("2023-06-01", 1.0, 4) + _records("2024-06-01", 0.9, 4)

    report = build_out_of_sample_lockbox(records, config=_config())

    assert report.passed is True
    assert report.invalidation_reasons == ()
    assert all(check.passed for check in report.degradation_checks)


def test_lockbox_fails_when_expectancy_degrades_too_much() -> None:
    records = _records("2023-06-01", 1.0, 4) + _records("2024-06-01", 0.5, 4)

    report = build_out_of_sample_lockbox(records, config=_config())

    expectancy = next(check for check in report.degradation_checks if check.metric == "expectancy_r")
    assert report.passed is False
    assert expectancy.passed is False
    assert expectancy.degradation == pytest.approx(0.5)


def test_lockbox_fails_closed_on_stale_threshold_version() -> None:
    config = OutOfSampleLockboxConfig(
        threshold_version="2026.05.01-old",
        edge_config=_edge_config(),
    )
    records = _records("2023-06-01", 1.0, 4) + _records("2024-06-01", 1.0, 4)

    report = build_out_of_sample_lockbox(records, config=config)

    assert report.passed is False
    assert report.threshold_version == "2026.05.01-old"
    assert report.invalidation_reasons == (
        f"stale_threshold_version:2026.05.01-old!={DEFAULT_THRESHOLDS.version}",
    )


def test_lockbox_can_require_matching_record_threshold_versions() -> None:
    config = OutOfSampleLockboxConfig(
        require_matching_record_threshold_version=True,
        edge_config=_edge_config(),
    )
    records = _versioned_records("2023-06-01", 1.0, 4, DEFAULT_THRESHOLDS.version) + _versioned_records(
        "2024-06-01", 1.0, 4, DEFAULT_THRESHOLDS.version
    )

    report = build_out_of_sample_lockbox(records, config=config)

    assert report.passed is True
    assert report.invalidation_reasons == ()


def test_lockbox_fails_closed_when_record_threshold_versions_are_missing() -> None:
    config = OutOfSampleLockboxConfig(
        require_matching_record_threshold_version=True,
        edge_config=_edge_config(),
    )
    records = _records("2023-06-01", 1.0, 4) + _records("2024-06-01", 1.0, 4)

    report = build_out_of_sample_lockbox(records, config=config)

    assert report.passed is False
    assert "missing_record_threshold_versions" in report.invalidation_reasons


def test_lockbox_fails_closed_when_record_threshold_versions_mismatch() -> None:
    config = OutOfSampleLockboxConfig(
        require_matching_record_threshold_version=True,
        edge_config=_edge_config(),
    )
    records = _versioned_records("2023-06-01", 1.0, 4, DEFAULT_THRESHOLDS.version) + _versioned_records(
        "2024-06-01", 1.0, 4, "old-version"
    )

    report = build_out_of_sample_lockbox(records, config=config)

    assert report.passed is False
    assert report.invalidation_reasons == (
        f"record_threshold_version_mismatch:old-version!={DEFAULT_THRESHOLDS.version}",
    )


def test_evidence_contract_hash_changes_when_threshold_version_changes() -> None:
    current = build_evidence_contract_hash(OutOfSampleLockboxConfig())
    stale = build_evidence_contract_hash(OutOfSampleLockboxConfig(threshold_version="old-version"))

    assert current != stale


def test_lockbox_counts_unassigned_records() -> None:
    report = build_out_of_sample_lockbox(
        [{"exit_date": "invalid", "result_r": 1.0}, {"result_r": 1.0}],
        config=_config(),
    )

    assert report.unassigned_records == 2
    assert report.in_sample_count == 0
    assert report.out_of_sample_count == 0
    assert report.passed is False


def test_fallback_date_and_r_multiple_fields_are_supported() -> None:
    records = [
        {"signal_date": "2023-06-01", "r_multiple": 1.0},
        {"closed_at": "2024-06-01T12:00:00Z", "r_multiple": 1.0},
    ]
    config = OutOfSampleLockboxConfig(
        edge_config=_edge_config(min_total_trades=1, min_profit_factor=0.0)
    )

    report = build_out_of_sample_lockbox(records, config=config, result_field="result_r")

    assert report.in_sample_count == 1
    assert report.out_of_sample_count == 1
    assert report.unassigned_records == 0


def test_drawdown_check_is_lower_is_better() -> None:
    report = build_out_of_sample_lockbox(
        _records("2023-06-01", 1.0, 2) + _records("2024-06-01", 1.0, 2),
        config=OutOfSampleLockboxConfig(
            edge_config=_edge_config(min_total_trades=1, min_expectancy_r=-10, min_profit_factor=0.0)
        ),
    )

    drawdown = next(check for check in report.degradation_checks if check.metric == "max_drawdown")
    assert drawdown.higher_is_better is False


def test_ev8_report_declares_fixed_date_holdout_not_walk_forward_claim() -> None:
    report = build_out_of_sample_lockbox(
        _records("2023-06-01", 1.0, 2) + _records("2024-06-01", 1.0, 2),
        config=_config(),
    )

    markdown = render_out_of_sample_lockbox_markdown(report)
    report_dict = report.to_dict()

    assert report.validation_method == "fixed_date_holdout_degradation_check"
    assert "not walk-forward optimization" in report.validation_scope_note
    assert "not proof against overfitting" in report.validation_scope_note
    assert report_dict["validation_method"] == "fixed_date_holdout_degradation_check"
    assert "Fixed-Date Holdout Validation Lockbox" in markdown
    assert "Validation method: `fixed_date_holdout_degradation_check`" in markdown
    assert "not walk-forward optimization" in markdown
    assert "not proof against overfitting" in markdown
    assert "# Out-of-Sample Validation Lockbox" not in markdown


def test_ev8_json_report_contains_validation_scope_note(tmp_path) -> None:
    report = build_out_of_sample_lockbox(
        _records("2023-06-01", 1.0, 2) + _records("2024-06-01", 1.0, 2),
        config=_config(),
    )
    json_path = tmp_path / "oos-lockbox.json"
    markdown_path = tmp_path / "oos-lockbox.md"

    write_out_of_sample_lockbox_report(report, json_path=json_path, markdown_path=markdown_path)

    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert data["validation_method"] == "fixed_date_holdout_degradation_check"
    assert "not walk-forward optimization" in data["validation_scope_note"]
    assert "not proof against overfitting" in data["validation_scope_note"]


def test_render_markdown_contains_sections() -> None:
    report = build_out_of_sample_lockbox(
        _records("2023-06-01", 1.0, 2) + _records("2024-06-01", 1.0, 2),
        config=_config(),
    )

    markdown = render_out_of_sample_lockbox_markdown(report)

    assert "# Fixed-Date Holdout Validation Lockbox" in markdown
    assert "Threshold version" in markdown
    assert "Evidence contract hash" in markdown
    assert "Core Metrics" in markdown
    assert "Degradation Checks" in markdown


def test_render_markdown_contains_invalidation_reasons() -> None:
    report = build_out_of_sample_lockbox(
        _records("2023-06-01", 1.0, 2) + _records("2024-06-01", 1.0, 2),
        config=OutOfSampleLockboxConfig(
            threshold_version="old-version",
            edge_config=_edge_config(min_total_trades=1, min_expectancy_r=-10, min_profit_factor=0.0),
        ),
    )

    markdown = render_out_of_sample_lockbox_markdown(report)

    assert "Invalidation Reasons" in markdown
    assert "stale_threshold_version" in markdown


def test_write_out_of_sample_lockbox_report(tmp_path) -> None:
    report = build_out_of_sample_lockbox(
        _records("2023-06-01", 1.0, 2) + _records("2024-06-01", 1.0, 2),
        config=_config(),
    )
    json_path = tmp_path / "oos-lockbox.json"
    markdown_path = tmp_path / "oos-lockbox.md"

    write_out_of_sample_lockbox_report(report, json_path=json_path, markdown_path=markdown_path)

    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert data["split_date"] == "2024-01-01"
    assert data["validation_method"] == VALIDATION_METHOD
    assert data["threshold_version"] == DEFAULT_THRESHOLDS.version
    assert data["evidence_contract_hash"] == build_evidence_contract_hash(_config())
    assert data["invalidation_reasons"] == []
    assert markdown_path.read_text(encoding="utf-8").startswith("# Fixed-Date Holdout Validation Lockbox")
