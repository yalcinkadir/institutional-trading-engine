from __future__ import annotations

import json
from pathlib import Path

from src.backtesting_framework import BacktestSignal
from src.historical_validation import (
    HistoricalValidationConfig,
    fetch_historical_bars,
    run_historical_validation,
    run_and_save_historical_validation,
    save_historical_validation_summary,
)


class FakeHistoricalClient:
    def __init__(self, bars_by_symbol: dict[str, list[dict]]) -> None:
        self.bars_by_symbol = bars_by_symbol
        self.calls: list[tuple[str, str, str]] = []

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
        self.calls.append((ticker, start_date, end_date))
        return self.bars_by_symbol[ticker]


def _bars(start: float = 100.0, drift: float = 1.0, count: int = 40) -> list[dict]:
    bars: list[dict] = []
    close = start
    for index in range(count):
        close += drift
        bars.append(
            {
                "t": 1704067200000 + index * 86400000,
                "c": round(close, 2),
                "h": round(close + 1.5, 2),
                "l": round(close - 2.0, 2),
            }
        )
    return bars


def _signals() -> list[BacktestSignal]:
    return [
        BacktestSignal(
            timestamp_utc="2024-01-01T00:00:00+00:00",
            symbol="AAPL",
            market_state="risk_on",
            setup_type="momentum_breakout",
            decision="approved",
            risk_tier="tier_1",
            entry_price=101.0,
            position_size_multiplier=1.0,
        ),
        BacktestSignal(
            timestamp_utc="2024-01-02T00:00:00+00:00",
            symbol="AAPL",
            market_state="risk_on",
            setup_type="pullback_continuation",
            decision="approved",
            risk_tier="tier_2",
            entry_price=102.0,
            position_size_multiplier=0.5,
        ),
    ]


def test_fetch_historical_bars_uses_injected_client() -> None:
    client = FakeHistoricalClient({"AAPL": _bars()})

    result = fetch_historical_bars(
        ("AAPL",),
        "2024-01-01",
        "2024-02-01",
        client=client,
    )

    assert "AAPL" in result
    assert client.calls == [("AAPL", "2024-01-01", "2024-02-01")]


def test_run_historical_validation_generates_horizon_metrics() -> None:
    config = HistoricalValidationConfig(
        symbols=("AAPL",),
        start_date="2024-01-01",
        end_date="2024-02-15",
        horizons=(5, 10, 20),
    )

    summary = run_historical_validation(
        _signals(),
        {"AAPL": _bars()},
        config,
    )

    assert summary.symbols == ("AAPL",)
    assert summary.horizons == (5, 10, 20)
    assert len(summary.metrics_by_horizon) == 3
    assert summary.metrics_by_horizon[0].sample_size == 2
    assert summary.metrics_by_horizon[0].win_rate == 1.0
    assert summary.metrics_by_horizon[0].false_positive_rate == 0.0


def test_run_historical_validation_handles_no_trades() -> None:
    config = HistoricalValidationConfig(
        symbols=("MSFT",),
        start_date="2024-01-01",
        end_date="2024-02-15",
        horizons=(5,),
    )

    summary = run_historical_validation(
        _signals(),
        {"MSFT": _bars()},
        config,
    )

    metric = summary.metrics_by_horizon[0]
    assert metric.sample_size == 0
    assert metric.win_rate == 0.0
    assert metric.average_return == 0.0


def test_save_historical_validation_summary(tmp_path: Path) -> None:
    config = HistoricalValidationConfig(
        symbols=("AAPL",),
        start_date="2024-01-01",
        end_date="2024-02-15",
        horizons=(5,),
    )
    summary = run_historical_validation(_signals(), {"AAPL": _bars()}, config)
    output_path = tmp_path / "reports" / "backtests" / "backtest_summary.json"

    saved = save_historical_validation_summary(summary, output_path)
    payload = json.loads(saved.read_text(encoding="utf-8"))

    assert saved == output_path
    assert payload["symbols"] == ["AAPL"]
    assert payload["metrics_by_horizon"][0]["horizon_days"] == 5


def test_run_and_save_historical_validation_uses_client_and_writes_output(tmp_path: Path) -> None:
    output_path = tmp_path / "backtest_summary.json"
    config = HistoricalValidationConfig(
        symbols=("AAPL",),
        start_date="2024-01-01",
        end_date="2024-02-15",
        horizons=(5,),
        output_path=output_path,
    )
    client = FakeHistoricalClient({"AAPL": _bars()})

    summary = run_and_save_historical_validation(_signals(), config, client=client)

    assert output_path.exists()
    assert summary.metrics_by_horizon[0].sample_size == 2
    assert client.calls == [("AAPL", "2024-01-01", "2024-02-15")]
