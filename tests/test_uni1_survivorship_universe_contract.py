from __future__ import annotations

from pathlib import Path

from scripts.validate_survivorship_universe import validate_survivorship_universe


def _write_universe(path: Path, rows: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "symbol,effective_from,effective_to,active,asset_class,exchange,source,status,reason\n" + rows,
        encoding="utf-8",
    )


def test_missing_universe_file_blocks_real_backtesting(tmp_path: Path) -> None:
    report = validate_survivorship_universe(
        universe_path=tmp_path / "missing.csv",
        requested_symbols=["SPY"],
        start_date="2021-01-01",
        end_date="2021-01-02",
    )

    assert not report.passed
    assert "missing_universe_file" in report.failures


def test_malformed_universe_rows_block_real_backtesting(tmp_path: Path) -> None:
    universe = tmp_path / "survivorship_universe.csv"
    _write_universe(
        universe,
        "SPY,not-a-date,,true,etf,NYSEARCA,initial_universe,active,initial\n"
        ",2020-01-01,,true,etf,NYSEARCA,initial_universe,active,missing symbol\n"
        "QQQ,2020-01-01,2019-01-01,true,etf,NASDAQ,initial_universe,active,bad range\n"
        "AAPL,2020-01-01,,maybe,equity,NASDAQ,initial_universe,active,bad active\n",
    )

    report = validate_survivorship_universe(
        universe_path=universe,
        requested_symbols=["SPY"],
        start_date="2021-01-01",
        end_date="2021-01-02",
    )

    assert not report.passed
    assert "row_2_invalid_effective_from:not-a-date" in report.failures
    assert "row_3_missing_symbol" in report.failures
    assert "row_4_effective_to_before_from:QQQ" in report.failures
    assert "row_5_invalid_active:maybe" in report.failures


def test_symbol_not_active_in_requested_range_blocks_real_backtesting(tmp_path: Path) -> None:
    universe = tmp_path / "survivorship_universe.csv"
    _write_universe(
        universe,
        "SPY,2020-01-01,2020-12-31,true,etf,NYSEARCA,initial_universe,inactive,ended before test range\n"
        "QQQ,2020-01-01,,false,etf,NASDAQ,initial_universe,inactive,not active\n",
    )

    report = validate_survivorship_universe(
        universe_path=universe,
        requested_symbols=["SPY", "QQQ"],
        start_date="2021-01-01",
        end_date="2021-01-02",
    )

    assert not report.passed
    assert "requested_symbol_not_active:SPY" in report.failures
    assert "requested_symbol_not_active:QQQ" in report.failures


def test_demo_marker_in_universe_blocks_real_backtesting(tmp_path: Path) -> None:
    universe = tmp_path / "survivorship_universe.csv"
    _write_universe(
        universe,
        "SPY,2020-01-01,,true,etf,NYSEARCA,demo_source,active,demo placeholder\n",
    )

    report = validate_survivorship_universe(
        universe_path=universe,
        requested_symbols=["SPY"],
        start_date="2021-01-01",
        end_date="2021-01-02",
    )

    assert not report.passed
    assert "row_2_demo_marker" in report.failures


def test_valid_initial_8_symbol_universe_passes() -> None:
    report = validate_survivorship_universe(
        universe_path=Path("data/universe/survivorship_universe.csv"),
        requested_symbols=["SPY", "QQQ", "AAPL", "MSFT", "NVDA", "GOOGL", "META", "GLD"],
        start_date="2021-01-01",
        end_date="2021-01-02",
    )

    assert report.passed
    assert report.row_count == 8
    assert report.active_symbols == ["AAPL", "GLD", "GOOGL", "META", "MSFT", "NVDA", "QQQ", "SPY"]
