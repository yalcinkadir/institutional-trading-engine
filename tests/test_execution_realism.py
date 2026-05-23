import json

import pytest

from src.validation.execution_realism import (
    DEFAULT_NORMAL_SLIPPAGE_PCT,
    DEFAULT_SPREAD_COST_PCT,
    DEFAULT_VOLATILE_SLIPPAGE_PCT,
    ExecutionRealismConfig,
    adjust_execution_record,
    apply_execution_realism,
    render_execution_realism_markdown,
    write_execution_realism_report,
)


def test_normal_regime_execution_cost_is_subtracted_from_r_multiple() -> None:
    record = {
        "symbol": "SPY",
        "result_r": 1.0,
        "entry_price": 100.0,
        "stop_loss": 95.0,
        "volatility_regime": "normal",
    }

    adjusted = adjust_execution_record(record)

    expected_cost_r = (100.0 * (DEFAULT_SPREAD_COST_PCT + DEFAULT_NORMAL_SLIPPAGE_PCT)) / 5.0
    assert adjusted.valid is True
    assert adjusted.execution_cost_r == pytest.approx(expected_cost_r)
    assert adjusted.adjusted_r == pytest.approx(1.0 - expected_cost_r)
    assert adjusted.adjusted_record["execution_realism_applied"] is True
    assert adjusted.adjusted_record["no_lookahead_execution_adjustment"] is True


def test_volatile_regime_uses_higher_slippage() -> None:
    normal_record = {
        "result_r": 1.0,
        "entry_price": 100.0,
        "stop_loss": 95.0,
        "volatility_regime": "normal",
    }
    volatile_record = {
        "result_r": 1.0,
        "entry_price": 100.0,
        "stop_loss": 95.0,
        "volatility_regime": "panic",
    }

    normal = adjust_execution_record(normal_record)
    volatile = adjust_execution_record(volatile_record)

    assert volatile.slippage_pct == DEFAULT_VOLATILE_SLIPPAGE_PCT
    assert normal.slippage_pct == DEFAULT_NORMAL_SLIPPAGE_PCT
    assert volatile.execution_cost_r > normal.execution_cost_r
    assert volatile.adjusted_r < normal.adjusted_r


def test_spread_cost_has_minimum_floor() -> None:
    config = ExecutionRealismConfig(spread_cost_pct=0.0)
    record = {
        "result_r": 1.0,
        "entry_price": 100.0,
        "stop_loss": 95.0,
        "volatility_regime": "normal",
    }

    adjusted = adjust_execution_record(record, config=config)

    assert adjusted.spread_cost_pct == DEFAULT_SPREAD_COST_PCT


def test_missing_required_fields_are_flagged() -> None:
    adjusted = adjust_execution_record({"symbol": "SPY", "result_r": 1.0})

    assert adjusted.valid is False
    assert "missing_entry_price" in adjusted.warnings
    assert "missing_stop_loss" in adjusted.warnings


def test_invalid_initial_risk_is_flagged() -> None:
    adjusted = adjust_execution_record(
        {
            "result_r": 1.0,
            "entry_price": 100.0,
            "stop_loss": 100.0,
        }
    )

    assert adjusted.valid is False
    assert "invalid_initial_risk" in adjusted.warnings


def test_entry_trigger_and_r_multiple_fallbacks_are_supported() -> None:
    adjusted = adjust_execution_record(
        {
            "r_multiple": 1.0,
            "entry_trigger": 100.0,
            "stop_loss": 95.0,
        }
    )

    assert adjusted.valid is True
    assert adjusted.original_r == 1.0
    assert adjusted.adjusted_r < 1.0


def test_apply_execution_realism_summary() -> None:
    records = [
        {"result_r": 1.0, "entry_price": 100.0, "stop_loss": 95.0, "symbol": "SPY"},
        {"result_r": -1.0, "entry_price": 50.0, "stop_loss": 48.0, "symbol": "QQQ"},
        {"result_r": 1.0, "symbol": "BAD"},
    ]

    report = apply_execution_realism(records)

    assert report.summary.total_records == 3
    assert report.summary.adjusted_records == 2
    assert report.summary.invalid_records == 1
    assert report.summary.total_execution_cost_r > 0
    assert len(report.records) == 3


def test_render_execution_realism_markdown() -> None:
    report = apply_execution_realism(
        [{"symbol": "SPY", "result_r": 1.0, "entry_price": 100.0, "stop_loss": 95.0}]
    )

    markdown = render_execution_realism_markdown(report)

    assert "# Execution Realism Report" in markdown
    assert "Total adjusted R" in markdown
    assert "SPY" in markdown


def test_write_execution_realism_report(tmp_path) -> None:
    report = apply_execution_realism(
        [{"symbol": "SPY", "result_r": 1.0, "entry_price": 100.0, "stop_loss": 95.0}]
    )
    json_path = tmp_path / "execution-realism.json"
    markdown_path = tmp_path / "execution-realism.md"

    write_execution_realism_report(report, json_path=json_path, markdown_path=markdown_path)

    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert data["summary"]["total_records"] == 1
    assert markdown_path.read_text(encoding="utf-8").startswith("# Execution Realism Report")
