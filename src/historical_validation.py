"""Historical setup validation using real or injected daily bars.

This module connects the existing deterministic backtesting framework to
historical daily bars. It is intentionally independent from broker execution
and safe to test with mocked bar data.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean
from typing import Protocol

from src.backtesting_framework import BacktestSignal, run_backtest
from src.data.polygon_client import PolygonClient


@dataclass(frozen=True)
class HistoricalValidationConfig:
    symbols: tuple[str, ...]
    start_date: str
    end_date: str
    horizons: tuple[int, ...] = (5, 10, 20)
    win_threshold_percent: float = 0.0
    output_path: Path = Path("reports/backtests/backtest_summary.json")


@dataclass(frozen=True)
class HorizonValidationMetrics:
    horizon_days: int
    sample_size: int
    win_rate: float
    average_return: float
    max_adverse_excursion: float
    false_positive_rate: float


@dataclass(frozen=True)
class HistoricalValidationSummary:
    symbols: tuple[str, ...]
    start_date: str
    end_date: str
    horizons: tuple[int, ...]
    metrics_by_horizon: tuple[HorizonValidationMetrics, ...]

    def to_dict(self) -> dict:
        return {
            "symbols": list(self.symbols),
            "start_date": self.start_date,
            "end_date": self.end_date,
            "horizons": list(self.horizons),
            "metrics_by_horizon": [asdict(item) for item in self.metrics_by_horizon],
        }


class HistoricalBarsClient(Protocol):
    def get_daily_bars_range(
        self,
        ticker: str,
        start_date: str,
        end_date: str,
        *,
        limit: int = 50000,
        adjusted: bool = True,
        use_ttl_cache: bool = True,
    ) -> list[dict]:
        ...


def fetch_historical_bars(
    symbols: tuple[str, ...],
    start_date: str,
    end_date: str,
    *,
    client: HistoricalBarsClient | None = None,
) -> dict[str, list[dict]]:
    """Fetch daily bars for every symbol through an injectable client."""

    data_client = client or PolygonClient()
    return {
        symbol: data_client.get_daily_bars_range(symbol, start_date, end_date)
        for symbol in symbols
    }


def run_historical_validation(
    signals: list[BacktestSignal],
    bars_by_symbol: dict[str, list[dict]],
    config: HistoricalValidationConfig,
) -> HistoricalValidationSummary:
    """Run forward-return validation for fixed holding horizons."""

    metrics: list[HorizonValidationMetrics] = []

    for horizon in config.horizons:
        horizon_signals = [
            BacktestSignal(
                timestamp_utc=signal.timestamp_utc,
                symbol=signal.symbol,
                market_state=signal.market_state,
                setup_type=signal.setup_type,
                decision=signal.decision,
                risk_tier=signal.risk_tier,
                entry_price=signal.entry_price,
                position_size_multiplier=signal.position_size_multiplier,
                holding_days=horizon,
            )
            for signal in signals
        ]
        report = run_backtest(horizon_signals, bars_by_symbol)
        returns = [trade.raw_return_percent for trade in report.trades]
        adverse = [trade.mae_percent for trade in report.trades]

        if not returns:
            metrics.append(
                HorizonValidationMetrics(
                    horizon_days=horizon,
                    sample_size=0,
                    win_rate=0.0,
                    average_return=0.0,
                    max_adverse_excursion=0.0,
                    false_positive_rate=0.0,
                )
            )
            continue

        wins = [value for value in returns if value > config.win_threshold_percent]
        false_positives = [value for value in returns if value <= config.win_threshold_percent]

        metrics.append(
            HorizonValidationMetrics(
                horizon_days=horizon,
                sample_size=len(returns),
                win_rate=round(len(wins) / len(returns), 4),
                average_return=round(mean(returns), 4),
                max_adverse_excursion=round(min(adverse), 4) if adverse else 0.0,
                false_positive_rate=round(len(false_positives) / len(returns), 4),
            )
        )

    return HistoricalValidationSummary(
        symbols=config.symbols,
        start_date=config.start_date,
        end_date=config.end_date,
        horizons=config.horizons,
        metrics_by_horizon=tuple(metrics),
    )


def save_historical_validation_summary(
    summary: HistoricalValidationSummary,
    output_path: Path,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    return output_path


def run_and_save_historical_validation(
    signals: list[BacktestSignal],
    config: HistoricalValidationConfig,
    *,
    client: HistoricalBarsClient | None = None,
) -> HistoricalValidationSummary:
    bars_by_symbol = fetch_historical_bars(
        config.symbols,
        config.start_date,
        config.end_date,
        client=client,
    )
    summary = run_historical_validation(signals, bars_by_symbol, config)
    save_historical_validation_summary(summary, config.output_path)
    return summary
