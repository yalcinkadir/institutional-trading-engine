from __future__ import annotations

from datetime import UTC, datetime
from statistics import mean

from src.data.polygon_client import PolygonClient
from src.indicators.technical_indicators import calculate_atr, sma
from src.scoring.market_health_score import MarketHealthScore

INDEX_TICKERS = ["SPY", "QQQ"]
VIX_TICKER = "I:VIX"
BREADTH_UNIVERSE = [
    "MSFT",
    "NVDA",
    "META",
    "AAPL",
    "AMZN",
    "AVGO",
    "AMD",
    "MU",
    "ADBE",
    "CSCO",
    "TSLA",
    "NFLX",
    "CRWD",
    "PANW",
    "SHOP",
    "PLTR",
]


def _latest_close(bars: list[dict]) -> float:
    return round(float(bars[-1]["c"]), 2)


def _safe_symbol_snapshot(client: PolygonClient, ticker: str) -> dict:
    bars = client.get_daily_bars(ticker, days=260)
    closes = [float(bar["c"]) for bar in bars]
    volumes = [float(bar.get("v", 0)) for bar in bars]

    close = _latest_close(bars)
    sma50 = sma(closes, 50)
    sma200 = sma(closes, 200)
    atr14 = calculate_atr(bars, 14)
    avg_volume_20 = round(mean(volumes[-20:]), 0) if len(volumes) >= 20 else 0

    return {
        "ticker": ticker,
        "close": close,
        "sma50": sma50,
        "sma200": sma200,
        "above_sma50": close > sma50,
        "above_sma200": close > sma200,
        "atr14": atr14,
        "avg_volume_20": avg_volume_20,
    }


def _calculate_breadth(client: PolygonClient) -> dict:
    valid = 0
    above_sma50 = 0
    failed: list[str] = []

    for ticker in BREADTH_UNIVERSE:
        try:
            snapshot = _safe_symbol_snapshot(client, ticker)
            valid += 1
            if snapshot["above_sma50"]:
                above_sma50 += 1
        except Exception:
            failed.append(ticker)

    breadth_percent = round((above_sma50 / valid) * 100, 2) if valid else 0.0

    return {
        "universe_size": valid,
        "above_sma50": above_sma50,
        "breadth_percent": breadth_percent,
        "failed_symbols": failed,
    }


def _focus_areas(report_type: str) -> list[str]:
    if report_type == "premarket":
        return [
            "US index trend confirmation before open",
            "VIX risk regime before new exposure",
            "Leader continuation potential",
            "Opening gap and volatility risk",
        ]

    return [
        "Closing trend confirmation",
        "Sector and leader rotation",
        "Institutional accumulation / distribution clues",
        "Risk-off signals after cash close",
    ]


def build_market_regime_summary(report_type: str) -> dict:
    now = datetime.now(UTC)

    try:
        client = PolygonClient()
        spy = _safe_symbol_snapshot(client, "SPY")
        qqq = _safe_symbol_snapshot(client, "QQQ")
        vix = _safe_symbol_snapshot(client, VIX_TICKER)
        breadth = _calculate_breadth(client)

        score = MarketHealthScore(
            spy_above_sma50=spy["above_sma50"],
            spy_above_sma200=spy["above_sma200"],
            qqq_above_sma50=qqq["above_sma50"],
            qqq_above_sma200=qqq["above_sma200"],
            vix=vix["close"],
            breadth_percent=breadth["breadth_percent"],
        ).calculate()

        return {
            "timestamp_utc": now.isoformat(),
            "market_health_score": score["score"],
            "regime": score["regime"],
            "focus_areas": _focus_areas(report_type),
            "symbols": {
                "SPY": spy,
                "QQQ": qqq,
                "VIX": vix,
            },
            "breadth": breadth,
            "notes": [
                "Live data source: Polygon.io daily aggregates.",
                "Breadth currently uses the configured leader universe, not the full S&P 500 universe.",
            ],
            "data_status": "LIVE",
        }
    except Exception as exc:
        return {
            "timestamp_utc": now.isoformat(),
            "market_health_score": "DATA_UNAVAILABLE",
            "regime": "Unknown",
            "focus_areas": _focus_areas(report_type),
            "symbols": {},
            "breadth": {},
            "notes": [
                "Live market data could not be loaded.",
                f"Error: {type(exc).__name__}: {exc}",
            ],
            "data_status": "FALLBACK",
        }
