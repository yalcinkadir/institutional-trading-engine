import json
from datetime import date

from src.validation.historical_edge_validation import HistoricalEdgeValidationConfig
from src.validation.out_of_sample_lockbox import (
    DEFAULT_OOS_SPLIT_DATE,
    OutOfSampleLockboxConfig,
    build_out_of_sample_lockbox,
    build_evidence_contract_hash,
    render_out_of_sample_lockbox_markdown,
)


def _edge_config() -> HistoricalEdgeValidationConfig:
    return HistoricalEdgeValidationConfig(
        min_total_trades=1,
        min_expectancy_r=-10,
        min_profit_factor=0.0,
        max_drawdown_limit=10,
        min_sharpe_ratio=-10,
        min_deflated_sharpe_probability=0.0,
        bootstrap_iterations=100,
    )


def _config(**overrides) -> OutOfSampleLockboxConfig:
    payload = {
        "split_date": DEFAULT_OOS_SPLIT_DATE,
        "purge_days": 2,
        "embargo_days": 1,
        "edge_config": _edge_config(),
    }
    payload.update(overrides)
    return OutOfSampleLockboxConfig(**payload)


def test_er10_trade_spanning_split_is_purged_not_assigned_to_oos() -> None:
    records = [
        {"entry_date": "2023-12-30", "exit_date": "2024-01-03", "result_r": 5.0},
        {"entry_date": "2023-12-01", "exit_date": "2023-12-10", "result_r": 1.0},
        {"entry_date": "2024-01-10", "exit_date": "2024-01-12", "result_r": 1.0},
    ]

    report = build_out_of_sample_lockbox(records, config=_config())

    assert report.in_sample_count == 1
    assert report.out_of_sample_count == 1
    assert report.purged_records == 1
    assert report.embargoed_records == 0
    assert report.unassigned_records == 0
    assert "purged_overlap_records:1" in report.invalidation_reasons
    assert report.passed is False


def test_er10_entry_inside_embargo_window_is_embargoed() -> None:
    records = [
        {"entry_date": "2023-12-20", "exit_date": "2023-12-22", "result_r": 1.0},
        {"entry_date": "2024-01-01", "exit_date": "2024-01-02", "result_r": 1.0},
        {"entry_date": "2024-01-10", "exit_date": "2024-01-12", "result_r": 1.0},
    ]

    report = build_out_of_sample_lockbox(records, config=_config())

    assert report.in_sample_count == 1
    assert report.out_of_sample_count == 1
    assert report.purged_records == 0
    assert report.embargoed_records == 1
    assert "embargoed_records:1" in report.invalidation_reasons
    assert report.passed is False


def test_er10_contract_hash_and_serialization_include_purge_embargo() -> None:
    config = _config(split_date=date(2024, 1, 1), purge_days=3, embargo_days=2)
    report = build_out_of_sample_lockbox(
        [
            {"entry_date": "2023-12-01", "exit_date": "2023-12-10", "result_r": 1.0},
            {"entry_date": "2024-01-10", "exit_date": "2024-01-12", "result_r": 1.0},
        ],
        config=config,
    )

    data = report.to_dict()
    markdown = render_out_of_sample_lockbox_markdown(report)

    assert data["purge_days"] == 3
    assert data["embargo_days"] == 2
    assert data["purged_records"] == 0
    assert data["embargoed_records"] == 0
    assert build_evidence_contract_hash(config) == report.evidence_contract_hash
    assert "Purge days: **3**" in markdown
    assert "Embargo days: **2**" in markdown
    assert json.dumps(data, allow_nan=False)
