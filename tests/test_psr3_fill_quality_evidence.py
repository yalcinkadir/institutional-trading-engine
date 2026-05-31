from __future__ import annotations

from pathlib import Path

from src.operations.fill_quality_evidence import (
    SCHEMA_VERSION,
    build_fill_quality_evidence,
    build_fill_quality_record,
    load_fill_quality_evidence,
    validate_fill_quality_evidence,
    write_fill_quality_evidence,
)


def _clean_fill() -> dict:
    return {
        "order_id": "paper-1",
        "signal_id": "sig-1",
        "symbol": "NVDA",
        "side": "BUY",
        "quantity": 10,
        "expected_price": 100.0,
        "actual_price": 100.1,
        "fill_status": "FILLED",
        "reconciliation_status": "RECONCILED",
        "timestamp": "2026-05-31T14:30:00+00:00",
    }


def test_build_fill_quality_record_calculates_buy_slippage_bps() -> None:
    record = build_fill_quality_record(_clean_fill())

    assert record.status == "PASS"
    assert record.slippage_absolute == 0.09999999999999432
    assert round(record.slippage_bps or 0.0, 2) == 10.0
    assert record.warnings == []


def test_sell_slippage_is_worse_when_actual_price_is_lower() -> None:
    raw = _clean_fill()
    raw["side"] = "SELL"
    raw["expected_price"] = 100.0
    raw["actual_price"] = 99.5

    record = build_fill_quality_record(raw)

    assert record.status == "WARN"
    assert round(record.slippage_bps or 0.0, 2) == 50.0
    assert "slippage_warn_threshold_exceeded" in record.warnings


def test_failed_fill_status_fails_record() -> None:
    raw = _clean_fill()
    raw["fill_status"] = "REJECTED"

    record = build_fill_quality_record(raw)

    assert record.status == "FAIL"
    assert "fill_status_failed" in record.warnings


def test_unreconciled_fill_fails_record() -> None:
    raw = _clean_fill()
    raw["reconciliation_status"] = "UNRECONCILED"

    record = build_fill_quality_record(raw)

    assert record.status == "FAIL"
    assert "reconciliation_not_clean" in record.warnings


def test_missing_required_record_fields_fail_record() -> None:
    record = build_fill_quality_record({})

    assert record.status == "FAIL"
    assert "order_id_missing" in record.warnings
    assert "symbol_missing" in record.warnings
    assert "quantity_non_positive" in record.warnings
    assert "expected_price_non_positive" in record.warnings


def test_fill_quality_evidence_passes_for_clean_records() -> None:
    evidence = build_fill_quality_evidence(
        trading_date="2026-05-31",
        raw_records=[_clean_fill()],
        created_at="2026-05-31T20:00:00+00:00",
    )

    assert evidence.schema_version == SCHEMA_VERSION
    assert evidence.status == "PASS"
    assert evidence.total_records == 1
    assert evidence.filled_count == 1
    assert evidence.partial_fill_count == 0
    assert evidence.failed_count == 0
    assert evidence.unreconciled_count == 0
    assert round(evidence.average_slippage_bps or 0.0, 2) == 10.0
    assert round(evidence.max_abs_slippage_bps or 0.0, 2) == 10.0
    assert evidence.live_trading_authorized is False
    assert validate_fill_quality_evidence(evidence) == {
        "status": "PASS",
        "errors": [],
    }


def test_fill_quality_evidence_warns_for_no_records() -> None:
    evidence = build_fill_quality_evidence(
        trading_date="2026-05-31",
        raw_records=[],
        created_at="2026-05-31T20:00:00+00:00",
    )

    assert evidence.status == "WARN"
    assert evidence.total_records == 0
    assert evidence.average_slippage_bps is None


def test_fill_quality_evidence_fails_for_failed_records() -> None:
    raw = _clean_fill()
    raw["fill_status"] = "FAILED"

    evidence = build_fill_quality_evidence(
        trading_date="2026-05-31",
        raw_records=[raw],
        created_at="2026-05-31T20:00:00+00:00",
    )

    assert evidence.status == "FAIL"
    assert evidence.failed_count == 1


def test_write_and_load_fill_quality_evidence_round_trip(tmp_path: Path) -> None:
    evidence = build_fill_quality_evidence(
        trading_date="2026-05-31",
        raw_records=[_clean_fill()],
        created_at="2026-05-31T20:00:00+00:00",
        notes=["paper observation only"],
    )

    output_path = write_fill_quality_evidence(evidence, output_dir=tmp_path)
    latest_path = tmp_path / "latest-fill-quality-evidence.json"

    assert output_path.exists()
    assert latest_path.exists()

    loaded = load_fill_quality_evidence(output_path)

    assert loaded == evidence


def test_validation_rejects_live_trading_authorization_mutation() -> None:
    evidence = build_fill_quality_evidence(
        trading_date="2026-05-31",
        raw_records=[_clean_fill()],
        created_at="2026-05-31T20:00:00+00:00",
    )

    mutated = evidence.__class__(
        schema_version=evidence.schema_version,
        trading_date=evidence.trading_date,
        created_at=evidence.created_at,
        status=evidence.status,
        total_records=evidence.total_records,
        filled_count=evidence.filled_count,
        partial_fill_count=evidence.partial_fill_count,
        failed_count=evidence.failed_count,
        unreconciled_count=evidence.unreconciled_count,
        average_slippage_bps=evidence.average_slippage_bps,
        max_abs_slippage_bps=evidence.max_abs_slippage_bps,
        records=evidence.records,
        notes=evidence.notes,
        live_trading_authorized=True,
    )

    validation = validate_fill_quality_evidence(mutated)

    assert validation["status"] == "FAIL"
    assert "live_trading_authorized_must_be_false" in validation["errors"]