"""
Liquidity Filter.

Filters universe candidates by tradeable-liquidity criteria before they
ever reach the scanner or backtest. This is what separates a backtest
that simulates execution honestly from one that pretends every signal
was filled at the close on tiny-cap names.

Defaults are deliberately conservative and target the assumptions the
existing execution_realism layer makes (50 bps + 10-30 bps slippage).
For names below these thresholds, those slippage assumptions are fiction.

Why the values are what they are:
- $50M average daily dollar volume: at 0.5% participation rate, you can
  trade $250k without meaningfully moving price. Smaller than this and
  the slippage model in execution_realism understates real cost by 3-10x.
- $5 minimum price: avoids penny-stock and post-reverse-split artifacts
  where bid-ask spread can be 1-5% of price.
- 60-day lookback: long enough to smooth IPO volatility and short-term
  liquidity shocks, short enough to react to structural deterioration.

These are starting defaults. A volatility-arbitrage strategy on liquid
ETFs might tolerate looser thresholds. A small-cap mean reversion
strategy needs much stricter ones. The dataclass exists so callers
can override per-strategy.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from statistics import median
from typing import Any


DEFAULT_MIN_AVG_DAILY_DOLLAR_VOLUME = 50_000_000.0
DEFAULT_MIN_CLOSE_PRICE = 5.0
DEFAULT_MIN_BAR_COUNT = 60
DEFAULT_MAX_ZERO_VOLUME_DAYS = 2
DEFAULT_LOOKBACK_BARS = 60


@dataclass(frozen=True)
class LiquidityFilterConfig:
    min_avg_daily_dollar_volume: float = DEFAULT_MIN_AVG_DAILY_DOLLAR_VOLUME
    min_close_price: float = DEFAULT_MIN_CLOSE_PRICE
    min_bar_count: int = DEFAULT_MIN_BAR_COUNT
    max_zero_volume_days: int = DEFAULT_MAX_ZERO_VOLUME_DAYS
    lookback_bars: int = DEFAULT_LOOKBACK_BARS


@dataclass(frozen=True)
class LiquidityMetrics:
    """
    Per-symbol liquidity snapshot.

    avg_dollar_volume uses the arithmetic mean which is sensitive to
    spikes. median_dollar_volume is included as a robustness check;
    if mean >> median, the liquidity is event-driven and unreliable.
    """

    symbol: str
    bar_count: int
    last_close: float
    avg_dollar_volume: float
    median_dollar_volume: float
    zero_volume_days: int
    spread_proxy_pct: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LiquidityVerdict:
    """
    Yes/no result with structured reasons. Reasons are codes, not
    sentences, so downstream code can branch on them.
    """

    symbol: str
    tradeable: bool
    metrics: LiquidityMetrics | None
    reasons: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "symbol": self.symbol,
            "tradeable": self.tradeable,
            "metrics": self.metrics.to_dict() if self.metrics else None,
            "reasons": list(self.reasons),
        }


@dataclass(frozen=True)
class LiquidityFilterReport:
    total_symbols: int
    tradeable_count: int
    rejected_count: int
    verdicts: list[LiquidityVerdict] = field(default_factory=list)

    @property
    def tradeable_symbols(self) -> list[str]:
        return [v.symbol for v in self.verdicts if v.tradeable]

    @property
    def rejected_symbols(self) -> list[str]:
        return [v.symbol for v in self.verdicts if not v.tradeable]

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_symbols": self.total_symbols,
            "tradeable_count": self.tradeable_count,
            "rejected_count": self.rejected_count,
            "tradeable_symbols": self.tradeable_symbols,
            "rejected_symbols": self.rejected_symbols,
            "verdicts": [v.to_dict() for v in self.verdicts],
        }


def evaluate_liquidity(
    symbol: str,
    bars: list[dict[str, Any]],
    *,
    config: LiquidityFilterConfig = LiquidityFilterConfig(),
) -> LiquidityVerdict:
    """
    Evaluate liquidity for a single symbol using its recent daily bars.

    Expects bars in the same shape the existing data_validator uses:
        [{"o": float, "h": float, "l": float, "c": float, "v": float}, ...]

    Bars should be in chronological order. The function will use the last
    `lookback_bars` bars only.
    """
    if not bars:
        return LiquidityVerdict(symbol=symbol, tradeable=False, metrics=None, reasons=("no_bars",))

    window = bars[-config.lookback_bars :] if len(bars) > config.lookback_bars else bars

    reasons: list[str] = []
    if len(window) < config.min_bar_count:
        reasons.append("insufficient_bar_history")

    dollar_volumes: list[float] = []
    zero_volume_days = 0
    spread_proxies: list[float] = []
    last_close: float = 0.0

    for bar in window:
        try:
            close = float(bar["c"])
            volume = float(bar["v"])
            high = float(bar["h"])
            low = float(bar["l"])
        except (KeyError, TypeError, ValueError):
            continue

        if close <= 0:
            continue

        last_close = close
        dollar_volume = close * volume
        dollar_volumes.append(dollar_volume)

        if volume <= 0:
            zero_volume_days += 1

        if high > 0:
            spread_proxies.append((high - low) / close)

    if not dollar_volumes:
        return LiquidityVerdict(symbol=symbol, tradeable=False, metrics=None, reasons=("no_valid_bars",))

    avg_dollar_volume = sum(dollar_volumes) / len(dollar_volumes)
    median_dollar_volume = median(dollar_volumes)
    spread_proxy = median(spread_proxies) if spread_proxies else 0.0

    metrics = LiquidityMetrics(
        symbol=symbol,
        bar_count=len(dollar_volumes),
        last_close=round(last_close, 4),
        avg_dollar_volume=round(avg_dollar_volume, 2),
        median_dollar_volume=round(median_dollar_volume, 2),
        zero_volume_days=zero_volume_days,
        spread_proxy_pct=round(spread_proxy, 6),
    )

    if last_close < config.min_close_price:
        reasons.append("price_below_minimum")

    if avg_dollar_volume < config.min_avg_daily_dollar_volume:
        reasons.append("dollar_volume_below_minimum")

    if median_dollar_volume > 0 and avg_dollar_volume > 3 * median_dollar_volume:
        reasons.append("dollar_volume_spike_dominated")

    if zero_volume_days > config.max_zero_volume_days:
        reasons.append("excessive_zero_volume_days")

    return LiquidityVerdict(
        symbol=symbol,
        tradeable=not reasons,
        metrics=metrics,
        reasons=tuple(reasons),
    )


def filter_universe(
    symbol_bars: dict[str, list[dict[str, Any]]],
    *,
    config: LiquidityFilterConfig = LiquidityFilterConfig(),
) -> LiquidityFilterReport:
    """Apply liquidity filter to an entire universe."""
    verdicts: list[LiquidityVerdict] = []
    for symbol, bars in sorted(symbol_bars.items()):
        verdicts.append(evaluate_liquidity(symbol, bars, config=config))

    tradeable = sum(1 for v in verdicts if v.tradeable)
    return LiquidityFilterReport(
        total_symbols=len(verdicts),
        tradeable_count=tradeable,
        rejected_count=len(verdicts) - tradeable,
        verdicts=verdicts,
    )


def render_liquidity_markdown(report: LiquidityFilterReport) -> str:
    lines = [
        "# Liquidity Filter Report",
        "",
        f"Total symbols evaluated: **{report.total_symbols}**",
        f"Tradeable: **{report.tradeable_count}**",
        f"Rejected: **{report.rejected_count}**",
        "",
        "| Symbol | Tradeable | Last Close | Avg $ Volume | Median $ Volume | Spread % | Reasons |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for verdict in report.verdicts:
        if verdict.metrics is None:
            lines.append(
                f"| {verdict.symbol} | {'yes' if verdict.tradeable else 'no'} | - | - | - | - | {', '.join(verdict.reasons) or '-'} |"
            )
            continue
        m = verdict.metrics
        lines.append(
            f"| {verdict.symbol} | "
            f"{'yes' if verdict.tradeable else 'no'} | "
            f"{m.last_close:.2f} | "
            f"{m.avg_dollar_volume:,.0f} | "
            f"{m.median_dollar_volume:,.0f} | "
            f"{m.spread_proxy_pct * 100:.2f} | "
            f"{', '.join(verdict.reasons) or '-'} |"
        )
    return "\n".join(lines).rstrip() + "\n"
