"""Polygon live-readiness checks for historical/live data operations.

This module does not call Polygon. It validates local configuration and returns
an executable checklist for the first real-data run after the subscription/API
key is active.
"""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Any


DEFAULT_LIVE_SYMBOLS = ("SPY", "QQQ", "NVDA", "AAPL", "MSFT")
DEFAULT_LOOKBACK_DAYS = 5000


@dataclass(frozen=True)
class ReadinessCheck:
    name: str
    passed: bool
    message: str


@dataclass(frozen=True)
class PolygonLiveReadinessResult:
    passed: bool
    start_date: str
    end_date: str
    symbols: list[str]
    checks: list[ReadinessCheck] = field(default_factory=list)
    commands: list[str] = field(default_factory=list)
    gates: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "symbols": self.symbols,
            "checks": [asdict(check) for check in self.checks],
            "commands": self.commands,
            "gates": self.gates,
        }


def _check(name: str, passed: bool, message: str) -> ReadinessCheck:
    return ReadinessCheck(name=name, passed=passed, message=message)


def calculate_start_date(*, end_date: date, lookback_days: int = DEFAULT_LOOKBACK_DAYS) -> date:
    return end_date - timedelta(days=lookback_days)


def normalize_symbols(symbols: str | list[str] | tuple[str, ...] | None) -> list[str]:
    if symbols is None:
        raw = list(DEFAULT_LIVE_SYMBOLS)
    elif isinstance(symbols, str):
        raw = symbols.split(",")
    else:
        raw = list(symbols)
    return sorted({item.strip().upper() for item in raw if item and item.strip()})


def build_live_readiness_commands(
    *,
    symbols: list[str],
    start_date: str,
    end_date: str,
) -> list[str]:
    joined = ",".join(symbols)
    return [
        (
            "python scripts/ingest_historical_polygon.py "
            f"--symbols {joined} --start-date {start_date} --end-date {end_date}"
        ),
        "python scripts/generate_report.py --type intraday --output reports/manual-e2e-report.md",
        "python scripts/run_e2e_dry_run.py --signals-file reports/signals/latest-signals.json",
        "python scripts/run_entry_exit_watcher.py --signals-file reports/signals/latest-signals.json",
    ]


def build_live_gates() -> list[str]:
    return [
        "Historical ingestion returns ok/empty metadata per symbol with no unexpected errors.",
        "latest-signals.json is generated from real Polygon data.",
        "E2E dry-run returns PASS.",
        "Manual watcher run completes successfully with current prices.",
        "Telegram/notification output is verified.",
        "5 consecutive entry-exit-watcher runs are green.",
        "Historical strategy validation is completed before any trading decision.",
    ]


def run_polygon_live_readiness(
    *,
    symbols: str | list[str] | tuple[str, ...] | None = None,
    end_date: date | None = None,
    lookback_days: int = DEFAULT_LOOKBACK_DAYS,
    api_key: str | None = None,
    signal_file: Path = Path("reports/signals/latest-signals.json"),
    portfolio_state_file: Path = Path("data/portfolio_state.json"),
) -> PolygonLiveReadinessResult:
    """Validate local readiness for first real Polygon data run."""
    resolved_end = end_date or date.today()
    resolved_start = calculate_start_date(end_date=resolved_end, lookback_days=lookback_days)
    resolved_symbols = normalize_symbols(symbols)
    resolved_api_key = api_key if api_key is not None else os.getenv("POLYGON_API_KEY")

    checks = [
        _check(
            "polygon_api_key_present",
            bool(resolved_api_key),
            "POLYGON_API_KEY is present" if resolved_api_key else "POLYGON_API_KEY is missing",
        ),
        _check(
            "lookback_days",
            lookback_days >= 365,
            f"lookback_days={lookback_days}",
        ),
        _check(
            "symbols_configured",
            bool(resolved_symbols),
            f"symbols={','.join(resolved_symbols) if resolved_symbols else 'none'}",
        ),
        _check(
            "portfolio_state_present",
            portfolio_state_file.exists(),
            f"portfolio state path: {portfolio_state_file}",
        ),
        _check(
            "signal_file_optional",
            True,
            f"signal file will be produced/validated later: {signal_file}",
        ),
    ]

    commands = build_live_readiness_commands(
        symbols=resolved_symbols,
        start_date=resolved_start.isoformat(),
        end_date=resolved_end.isoformat(),
    )

    return PolygonLiveReadinessResult(
        passed=all(check.passed for check in checks),
        start_date=resolved_start.isoformat(),
        end_date=resolved_end.isoformat(),
        symbols=resolved_symbols,
        checks=checks,
        commands=commands,
        gates=build_live_gates(),
    )
