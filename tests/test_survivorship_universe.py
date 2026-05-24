from __future__ import annotations

from datetime import date

from src.data.survivorship_universe import (
    DelistingReason,
    SurvivorshipUniverse,
    TickerLifecycle,
    load_survivorship_universe,
    validate_universe_coverage,
)


def _universe() -> SurvivorshipUniverse:
    return SurvivorshipUniverse(
        [
            TickerLifecycle(symbol="AAPL", active_from=date(1980, 12, 12)),
            TickerLifecycle(
                symbol="LEH",
                active_from=date(1994, 1, 1),
                active_to=date(2008, 9, 15),
                delisting_reason=DelistingReason.BANKRUPTCY,
            ),
            TickerLifecycle(symbol="META", active_from=date(2012, 5, 18)),
        ]
    )


def test_point_in_time_snapshot_excludes_delisted_and_not_yet_listed() -> None:
    snapshot = _universe().tradeable_universe(date(2010, 1, 1))

    assert "AAPL" in snapshot.tradeable
    assert "LEH" in snapshot.delisted_before
    assert "LEH" not in snapshot.tradeable
    assert "META" in snapshot.not_yet_listed


def test_audit_backtest_records_catches_survivorship_leak() -> None:
    report = _universe().audit_backtest_records(
        [
            {"symbol": "AAPL", "signal_date": "2010-01-01"},
            {"symbol": "LEH", "signal_date": "2010-01-01"},
            {"symbol": "UNKNOWN", "signal_date": "2010-01-01"},
        ]
    )

    assert report.passed is False
    assert report.valid_records == 1
    assert report.out_of_window_records == 1
    assert report.unknown_ticker_records == 1


def test_load_csv_requires_delisting_reason_when_active_to_exists(tmp_path) -> None:
    path = tmp_path / "universe.csv"
    path.write_text(
        "symbol,active_from,active_to,delisting_reason\n"
        "BAD,2000-01-01,2010-01-01,\n",
        encoding="utf-8",
    )

    try:
        load_survivorship_universe(path)
    except ValueError as exc:
        assert "no delisting_reason" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_coverage_gate_fails_below_500_assets() -> None:
    report = validate_universe_coverage(_universe(), date(2024, 1, 2), minimum_tradeable_count=500)

    assert report.passed is False
    assert report.tradeable_count == 2
    assert report.missing_count == 498
