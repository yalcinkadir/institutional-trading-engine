import json

from src.validation.fill_quality_report import (
    FillQualityConfig,
    FillQualitySeverity,
    FillQualityStatus,
    analyze_fill_quality,
    load_fill_quality_records,
    write_fill_quality_report,
)


def _record(**overrides):
    payload = {
        "order_id": "order-1",
        "symbol": "AAPL",
        "side": "buy",
        "requested_quantity": 100,
        "filled_quantity": 100,
        "arrival_price": 100,
        "average_fill_price": 100.05,
        "submitted_at": "2026-05-28T13:30:00+00:00",
        "first_fill_at": "2026-05-28T13:30:10+00:00",
        "bid_price": 99.99,
        "ask_price": 100.01,
        "strategy_id": "strategy-1",
        "signal_id": "signal-1",
    }
    payload.update(overrides)
    return payload


def test_fill_quality_passes_for_good_fill():
    report = analyze_fill_quality([_record()])

    assert report.passed
    assert report.status == FillQualityStatus.PASS
    assert report.metrics.record_count == 1
    assert report.metrics.fill_rate == 1.0
    assert report.metrics.full_fill_rate == 1.0
    assert report.metrics.avg_abs_slippage_bps == 5.0
    assert report.comparisons[0].delay_seconds == 10.0
    assert "no_order_submission_performed" in report.notes


def test_fill_quality_detects_bad_buy_slippage():
    report = analyze_fill_quality([
        _record(average_fill_price=100.50)
    ])

    codes = {issue.code for issue in report.issues}
    assert not report.passed
    assert report.status == FillQualityStatus.FAIL
    assert "max_abs_slippage_bps_exceeded" in codes
    assert "avg_abs_slippage_bps_exceeded" in codes
    assert report.comparisons[0].slippage_bps == 50.0


def test_fill_quality_sell_slippage_is_directional():
    report = analyze_fill_quality([
        _record(side="sell", arrival_price=100, average_fill_price=99.80)
    ])

    assert report.comparisons[0].slippage_bps == 20.0


def test_fill_quality_detects_partial_fill_and_fill_rate_gate():
    report = analyze_fill_quality([
        _record(requested_quantity=100, filled_quantity=50)
    ])

    codes = {issue.code for issue in report.issues}
    assert not report.passed
    assert report.metrics.partial_fill_count == 1
    assert report.metrics.fill_rate == 0.5
    assert "fill_rate_below_minimum" in codes
    assert "full_fill_rate_below_minimum" in codes


def test_fill_quality_warns_on_wide_spread_and_slow_average_delay():
    report = analyze_fill_quality(
        [
            _record(order_id="order-1", bid_price=99, ask_price=101, first_fill_at="2026-05-28T13:40:00+00:00"),
            _record(order_id="order-2", bid_price=99, ask_price=101, first_fill_at="2026-05-28T13:40:00+00:00"),
        ],
        config=FillQualityConfig(max_spread_bps=10, max_avg_delay_seconds=1000),
    )

    codes = {issue.code for issue in report.issues}
    assert report.passed
    assert report.status == FillQualityStatus.WARN
    assert "max_spread_bps_exceeded" in codes
    assert report.metrics.avg_delay_seconds == 600.0


def test_fill_quality_fails_on_missing_reference_price_by_default():
    report = analyze_fill_quality([_record(arrival_price=None)])

    assert not report.passed
    assert report.issues[0].severity == FillQualitySeverity.ERROR
    assert report.issues[0].code == "missing_arrival_price"


def test_fill_quality_can_warn_on_missing_reference_price():
    report = analyze_fill_quality(
        [_record(arrival_price=None)],
        config=FillQualityConfig(fail_on_missing_reference_price=False),
    )

    assert report.passed
    assert report.status == FillQualityStatus.WARN
    assert report.issues[0].severity == FillQualitySeverity.WARNING


def test_fill_quality_detects_duplicate_overfill_crossed_spread_and_negative_delay():
    report = analyze_fill_quality([
        _record(order_id="order-1", filled_quantity=120, bid_price=101, ask_price=100, first_fill_at="2026-05-28T13:29:59+00:00"),
        _record(order_id="order-1"),
    ])

    codes = {issue.code for issue in report.issues}
    assert not report.passed
    assert "overfilled_order" in codes
    assert "crossed_spread" in codes
    assert "negative_fill_delay" in codes
    assert "duplicate_order_id" in codes


def test_fill_quality_loads_json_and_writes_reports(tmp_path):
    input_file = tmp_path / "fills.json"
    output_dir = tmp_path / "out"
    input_file.write_text(json.dumps({"records": [_record()]}), encoding="utf-8")

    records = load_fill_quality_records(input_file)
    report = analyze_fill_quality(records)
    write_fill_quality_report(
        report,
        json_path=output_dir / "fill_quality_report.json",
        markdown_path=output_dir / "fill_quality_report.md",
    )

    assert report.passed
    assert (output_dir / "fill_quality_report.json").exists()
    assert "# C6 Fill Quality Report" in (output_dir / "fill_quality_report.md").read_text(encoding="utf-8")
