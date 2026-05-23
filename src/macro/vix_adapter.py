"""
VIX and Volatility Term-Structure Adapter.

The Decision Engine's hard-override logic relies on
`vix_term_structure_inverted` being a reliable boolean. Today, the
scanner has VIX as "Unavailable" because Polygon's I:VIX symbol
behavior depends on subscription plan and intermittently returns nothing.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Any, Callable, Iterable


VIX_SYMBOL_CANDIDATES = ("I:VIX", "VIX", "$VIX.X")
VIX9D_SYMBOL_CANDIDATES = ("I:VIX9D", "VIX9D", "$VIX9D.X")
VIX3M_SYMBOL_CANDIDATES = ("I:VIX3M", "VIX3M", "$VIX3M.X")

INVERSION_THRESHOLD = 1.0
PROXY_SHORT_WINDOW = 5
PROXY_LONG_WINDOW = 21
PROXY_INVERSION_THRESHOLD = 1.10


class VixDataQuality(str, Enum):
    DIRECT = "direct"
    PARTIAL = "partial"
    REALIZED_PROXY = "realized_proxy"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class VixSnapshot:
    as_of: date | None
    spot_vix: float | None
    vix_9d: float | None
    vix_3m: float | None
    term_structure_ratio: float | None
    inverted: bool
    quality: VixDataQuality
    source_notes: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of.isoformat() if self.as_of else None,
            "spot_vix": self.spot_vix,
            "vix_9d": self.vix_9d,
            "vix_3m": self.vix_3m,
            "term_structure_ratio": self.term_structure_ratio,
            "inverted": self.inverted,
            "quality": self.quality.value,
            "source_notes": list(self.source_notes),
        }


BarFetcher = Callable[[str], list[dict[str, Any]]]


def build_vix_snapshot(
    *,
    bar_fetcher: BarFetcher,
    spy_bar_fetcher: BarFetcher | None = None,
    inversion_threshold: float = INVERSION_THRESHOLD,
) -> VixSnapshot:
    notes: list[str] = []

    spot_vix, spot_source = _try_fetch_latest_close(bar_fetcher, VIX_SYMBOL_CANDIDATES)
    if spot_source:
        notes.append(f"spot_vix_from:{spot_source}")

    vix_9d, vix9d_source = _try_fetch_latest_close(bar_fetcher, VIX9D_SYMBOL_CANDIDATES)
    if vix9d_source:
        notes.append(f"vix_9d_from:{vix9d_source}")

    vix_3m, vix3m_source = _try_fetch_latest_close(bar_fetcher, VIX3M_SYMBOL_CANDIDATES)
    if vix3m_source:
        notes.append(f"vix_3m_from:{vix3m_source}")

    as_of = _latest_date_from_any(bar_fetcher, VIX_SYMBOL_CANDIDATES)

    if spot_vix is not None and vix_9d is not None:
        ratio = vix_9d / spot_vix
        return VixSnapshot(
            as_of=as_of,
            spot_vix=spot_vix,
            vix_9d=vix_9d,
            vix_3m=vix_3m,
            term_structure_ratio=round(ratio, 4),
            inverted=ratio > inversion_threshold,
            quality=VixDataQuality.DIRECT,
            source_notes=tuple(notes),
        )

    if spot_vix is not None and vix_3m is not None:
        ratio = spot_vix / vix_3m
        notes.append("term_structure_from_vix_vs_vix3m")
        return VixSnapshot(
            as_of=as_of,
            spot_vix=spot_vix,
            vix_9d=None,
            vix_3m=vix_3m,
            term_structure_ratio=round(ratio, 4),
            inverted=ratio > inversion_threshold,
            quality=VixDataQuality.PARTIAL,
            source_notes=tuple(notes),
        )

    if spot_vix is not None:
        notes.append("term_structure_unavailable")
        return VixSnapshot(
            as_of=as_of,
            spot_vix=spot_vix,
            vix_9d=None,
            vix_3m=None,
            term_structure_ratio=None,
            inverted=False,
            quality=VixDataQuality.PARTIAL,
            source_notes=tuple(notes),
        )

    if spy_bar_fetcher is not None:
        spy_bars = spy_bar_fetcher("SPY")
        proxy = _realized_volatility_term_proxy(spy_bars)
        if proxy is not None:
            short_vol, long_vol, proxy_as_of = proxy
            ratio = short_vol / long_vol if long_vol > 0 else None
            notes.append("realized_vol_proxy_on_spy")
            return VixSnapshot(
                as_of=proxy_as_of,
                spot_vix=None,
                vix_9d=None,
                vix_3m=None,
                term_structure_ratio=round(ratio, 4) if ratio else None,
                inverted=bool(ratio and ratio > PROXY_INVERSION_THRESHOLD),
                quality=VixDataQuality.REALIZED_PROXY,
                source_notes=tuple(notes),
            )

    return VixSnapshot(
        as_of=None,
        spot_vix=None,
        vix_9d=None,
        vix_3m=None,
        term_structure_ratio=None,
        inverted=False,
        quality=VixDataQuality.UNAVAILABLE,
        source_notes=tuple(notes) if notes else ("no_vix_source_returned_data",),
    )


def _try_fetch_latest_close(bar_fetcher: BarFetcher, candidates: Iterable[str]) -> tuple[float | None, str | None]:
    for symbol in candidates:
        try:
            bars = bar_fetcher(symbol)
        except Exception:
            continue
        if not bars:
            continue
        for bar in reversed(bars):
            close = bar.get("c") if isinstance(bar, dict) else None
            if close is None:
                continue
            try:
                value = float(close)
            except (TypeError, ValueError):
                continue
            if value > 0:
                return value, symbol
    return None, None


def _latest_date_from_any(bar_fetcher: BarFetcher, candidates: Iterable[str]) -> date | None:
    for symbol in candidates:
        try:
            bars = bar_fetcher(symbol)
        except Exception:
            continue
        if not bars:
            continue
        last = bars[-1]
        raw = last.get("date") if isinstance(last, dict) else None
        if raw is None:
            continue
        if isinstance(raw, date):
            return raw
        if isinstance(raw, str):
            try:
                return date.fromisoformat(raw[:10])
            except ValueError:
                continue
    return None


def _realized_volatility_term_proxy(spy_bars: list[dict[str, Any]]) -> tuple[float, float, date | None] | None:
    closes: list[tuple[date | None, float]] = []
    for bar in spy_bars:
        if not isinstance(bar, dict):
            continue
        try:
            close = float(bar["c"])
        except (KeyError, TypeError, ValueError):
            continue
        raw_date = bar.get("date")
        parsed_date: date | None = None
        if isinstance(raw_date, date):
            parsed_date = raw_date
        elif isinstance(raw_date, str):
            try:
                parsed_date = date.fromisoformat(raw_date[:10])
            except ValueError:
                parsed_date = None
        closes.append((parsed_date, close))

    if len(closes) < PROXY_LONG_WINDOW + 1:
        return None

    returns: list[float] = []
    for index in range(1, len(closes)):
        prev = closes[index - 1][1]
        curr = closes[index][1]
        if prev > 0:
            returns.append(math.log(curr / prev))

    if len(returns) < PROXY_LONG_WINDOW:
        return None

    short_window = returns[-PROXY_SHORT_WINDOW:]
    long_window = returns[-PROXY_LONG_WINDOW:]

    short_vol = _annualized_stdev_pct(short_window)
    long_vol = _annualized_stdev_pct(long_window)
    as_of = closes[-1][0]
    return short_vol, long_vol, as_of


def _annualized_stdev_pct(returns: list[float]) -> float:
    if len(returns) < 2:
        return 0.0
    mean = sum(returns) / len(returns)
    variance = sum((r - mean) ** 2 for r in returns) / (len(returns) - 1)
    daily_stdev = math.sqrt(variance)
    annualized = daily_stdev * math.sqrt(252)
    return annualized * 100.0
