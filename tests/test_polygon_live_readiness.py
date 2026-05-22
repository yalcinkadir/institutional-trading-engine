from __future__ import annotations

from datetime import date
from pathlib import Path

from src.operations.polygon_live_readiness import (
    build_live_readiness_commands,
    calculate_start_date,
    normalize_symbols,
    run_polygon_live_readiness,
)


def test_calculate_start_date_uses_lookback_days() -> None:
    assert calculate_start_date(end_date=date(2026, 5, 22), lookback_days=5000).isoformat() == "2012-09-13"


def test_normalize_symbols_dedupes_uppercases_and_sorts() -> None:
    assert normalize_symbols("nvda,AAPL, nvda, spy") == ["AAPL", "NVDA", "SPY"]


def test_build_live_readiness_commands_include_required_sequence() -> None:
    commands = build_live_readiness_commands(
        symbols=["NVDA", "SPY"],
        start_date="2012-09-13",
        end_date="2026-05-22",
    )

    assert commands[0] == (
        "python scripts/ingest_historical_polygon.py "
        "--symbols NVDA,SPY --start-date 2012-09-13 --end-date 2026-05-22"
    )
    assert "generate_report.py" in commands[1]
    assert "run_e2e_dry_run.py" in commands[2]
    assert "run_entry_exit_watcher.py" in commands[3]


def test_polygon_live_readiness_fails_without_api_key(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.delenv("POLYGON_API_KEY", raising=False)
    portfolio_state = tmp_path / "portfolio_state.json"
    portfolio_state.write_text("{}", encoding="utf-8")

    result = run_polygon_live_readiness(
        symbols="NVDA,SPY",
        end_date=date(2026, 5, 22),
        lookback_days=5000,
        portfolio_state_file=portfolio_state,
    )

    assert not result.passed
    assert result.start_date == "2012-09-13"
    assert result.end_date == "2026-05-22"
    assert any(check.name == "polygon_api_key_present" and not check.passed for check in result.checks)


def test_polygon_live_readiness_passes_with_api_key_and_portfolio_state(tmp_path: Path) -> None:
    portfolio_state = tmp_path / "portfolio_state.json"
    portfolio_state.write_text("{}", encoding="utf-8")

    result = run_polygon_live_readiness(
        symbols="NVDA,SPY",
        end_date=date(2026, 5, 22),
        lookback_days=5000,
        api_key="test-key",
        portfolio_state_file=portfolio_state,
    )

    assert result.passed
    assert result.symbols == ["NVDA", "SPY"]
    assert result.commands[0].startswith("python scripts/ingest_historical_polygon.py")
    assert "5 consecutive entry-exit-watcher runs are green." in result.gates
    assert result.to_dict()["passed"] is True


def test_polygon_live_readiness_fails_when_portfolio_state_missing() -> None:
    result = run_polygon_live_readiness(
        symbols="NVDA",
        end_date=date(2026, 5, 22),
        api_key="test-key",
        portfolio_state_file=Path("/tmp/non-existent-portfolio-state-for-test.json"),
    )

    assert not result.passed
    assert any(check.name == "portfolio_state_present" and not check.passed for check in result.checks)


def test_polygon_live_readiness_flags_too_short_lookback(tmp_path: Path) -> None:
    portfolio_state = tmp_path / "portfolio_state.json"
    portfolio_state.write_text("{}", encoding="utf-8")

    result = run_polygon_live_readiness(
        symbols="NVDA",
        end_date=date(2026, 5, 22),
        lookback_days=30,
        api_key="test-key",
        portfolio_state_file=portfolio_state,
    )

    assert not result.passed
    assert any(check.name == "lookback_days" and not check.passed for check in result.checks)
