import json

from src.validation.daily_execution_reconciliation import (
    DailyExecutionReconciliationConfig,
    DailyExecutionSeverity,
    DailyExecutionStatus,
    ExpectedExecutionRecord,
    ObservedExecutionRecord,
    load_expected_execution_records,
    load_observed_execution_records,
    reconcile_daily_execution,
    write_daily_execution_reconciliation_report,
)


def _expected(**overrides):
    payload = {
        "signal_id": "signal-1",
        "symbol": "AAPL",
        "side": "buy",
        "expected_quantity": 10,
        "expected_avg_price": 100,
        "expected_r": 1.0,
        "strategy_id": "strategy-1",
        "expected_order_id": "order-1",
    }
    payload.update(overrides)
    return ExpectedExecutionRecord(**payload)


def _observed(**overrides):
    payload = {
        "signal_id": "signal-1",
        "symbol": "AAPL",
        "side": "buy",
        "filled_quantity": 10,
        "average_fill_price": 100,
        "realized_r": 1.0,
        "status": "filled",
        "strategy_id": "strategy-1",
        "order_id": "order-1",
        "commission": 0,
    }
    payload.update(overrides)
    return ObservedExecutionRecord(**payload)


def test_daily_execution_reconciliation_passes_matching_records():
    report = reconcile_daily_execution(expected_records=[_expected()], observed_records=[_observed()])

    assert report.passed
    assert report.status == DailyExecutionStatus.PASS
    assert report.metrics.expected_count == 1
    assert report.metrics.observed_count == 1
    assert report.metrics.matched_count == 1
    assert report.metrics.total_r_drift == 0
    assert report.comparisons[0].status == DailyExecutionStatus.PASS
    assert "no_order_submission_performed" in report.notes


def test_daily_execution_reconciliation_fails_on_missing_observed_record():
    report = reconcile_daily_execution(expected_records=[_expected()], observed_records=[])

    assert not report.passed
    assert report.status == DailyExecutionStatus.FAIL
    assert report.metrics.missing_count == 1
    assert report.issues[0].severity == DailyExecutionSeverity.ERROR
    assert report.issues[0].code == "missing_observed_execution"


def test_daily_execution_reconciliation_can_warn_on_missing_observed_record():
    report = reconcile_daily_execution(
        expected_records=[_expected()],
        observed_records=[],
        config=DailyExecutionReconciliationConfig(require_observed_for_each_expected=False),
    )

    assert report.passed
    assert report.status == DailyExecutionStatus.WARN
    assert report.issues[0].severity == DailyExecutionSeverity.WARNING


def test_daily_execution_reconciliation_fails_on_unexpected_observed_record():
    report = reconcile_daily_execution(expected_records=[], observed_records=[_observed()])

    assert not report.passed
    assert report.metrics.unexpected_count == 1
    assert report.issues[0].code == "unexpected_observed_execution"


def test_daily_execution_reconciliation_detects_quantity_price_and_r_drift():
    report = reconcile_daily_execution(
        expected_records=[_expected(expected_quantity=10, expected_avg_price=100, expected_r=1.0)],
        observed_records=[_observed(filled_quantity=8, average_fill_price=103, realized_r=0.4)],
    )

    codes = {issue.code for issue in report.issues}
    assert not report.passed
    assert "quantity_drift_exceeded" in codes
    assert "price_drift_exceeded" in codes
    assert "r_drift_exceeded" in codes
    assert report.comparisons[0].quantity_drift == -2
    assert report.comparisons[0].price_drift_pct == 0.03
    assert report.comparisons[0].r_drift == -0.6


def test_daily_execution_reconciliation_detects_total_r_drift():
    report = reconcile_daily_execution(
        expected_records=[_expected(expected_r=1.0)],
        observed_records=[_observed(realized_r=0.7)],
        config=DailyExecutionReconciliationConfig(max_abs_r_drift=1.0, max_abs_total_r_drift=0.1),
    )

    assert not report.passed
    assert report.metrics.total_r_drift == -0.3
    assert report.issues[-1].code == "total_r_drift_exceeded"


def test_daily_execution_reconciliation_fails_on_symbol_side_and_signal_mismatch():
    report = reconcile_daily_execution(
        expected_records=[_expected(signal_id="signal-1", symbol="AAPL", side="buy")],
        observed_records=[_observed(signal_id="signal-2", symbol="MSFT", side="sell")],
    )

    codes = {issue.code for issue in report.issues}
    assert not report.passed
    assert "signal_id_mismatch" in codes
    assert "symbol_mismatch" in codes
    assert "side_mismatch" in codes


def test_daily_execution_reconciliation_fails_on_duplicate_keys():
    report = reconcile_daily_execution(
        expected_records=[_expected(), _expected(expected_r=0.5)],
        observed_records=[_observed(), _observed(realized_r=0.5)],
    )

    codes = {issue.code for issue in report.issues}
    assert not report.passed
    assert "duplicate_expected_execution" in codes
    assert "duplicate_observed_execution" in codes


def test_daily_execution_reconciliation_loads_json_and_writes_report(tmp_path):
    expected_path = tmp_path / "expected.json"
    observed_path = tmp_path / "observed.json"
    output_dir = tmp_path / "out"
    expected_path.write_text(json.dumps({"records": [_expected().to_dict()]}), encoding="utf-8")
    observed_path.write_text(json.dumps([_observed().to_dict()]), encoding="utf-8")

    report = reconcile_daily_execution(
        expected_records=load_expected_execution_records(expected_path),
        observed_records=load_observed_execution_records(observed_path),
    )
    write_daily_execution_reconciliation_report(
        report,
        json_path=output_dir / "daily_execution_reconciliation.json",
        markdown_path=output_dir / "daily_execution_reconciliation.md",
    )

    assert report.passed
    assert (output_dir / "daily_execution_reconciliation.json").exists()
    assert "# C5 Daily Execution Reconciliation" in (output_dir / "daily_execution_reconciliation.md").read_text(encoding="utf-8")
