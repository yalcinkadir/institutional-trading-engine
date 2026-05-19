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
    if not bars:
        raise ValueError("No bars returned")

    return round(float(bars[-1]["c"]), 2)


def _safe_symbol_snapshot(client: PolygonClient, ticker: str) -> dict:
    bars = client.get_daily_bars(ticker, days=260)

    if not bars:
        raise ValueError(f"No daily bars returned for {ticker}")

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


def _try_symbol_snapshot(client: PolygonClient, ticker: str) -> tuple[dict | None, str | None]:
    try:
        return _safe_symbol_snapshot(client, ticker), None
    except Exception as exc:
        return None, f"{ticker}: {type(exc).__name__}: {exc}"


def _calculate_breadth(client: PolygonClient) -> dict:
    valid = 0
    above_sma50 = 0
    failed: list[str] = []

    for ticker in BREADTH_UNIVERSE:
        snapshot, error = _try_symbol_snapshot(client, ticker)
        if snapshot is None:
            failed.append(error or ticker)
            continue

        valid += 1
        if snapshot["above_sma50"]:
            above_sma50 += 1

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


def _fallback_snapshot(ticker: str) -> dict:
    return {
        "ticker": ticker,
        "close": None,
        "sma50": None,
        "sma200": None,
        "above_sma50": False,
        "above_sma200": False,
        "atr14": None,
        "avg_volume_20": 0,
    }


def _calculate_partial_market_score(
    spy: dict | None,
    qqq: dict | None,
    vix: dict | None,
    breadth: dict,
) -> dict:
    if spy is None and qqq is None:
        return {
            "score": "DATA_UNAVAILABLE",
            "regime": "Unknown",
        }

    vix_value = float(vix["close"]) if vix and vix.get("close") is not None else 20.0

    score = MarketHealthScore(
        spy_above_sma50=bool(spy and spy["above_sma50"]),
        spy_above_sma200=bool(spy and spy["above_sma200"]),
        qqq_above_sma50=bool(qqq and qqq["above_sma50"]),
        qqq_above_sma200=bool(qqq and qqq["above_sma200"]),
        vix=vix_value,
        breadth_percent=float(breadth.get("breadth_percent", 0)),
    ).calculate()

    if vix is None:
        score["regime"] = f"{score['regime']} (VIX missing)"

    return score


def build_market_regime_summary(report_type: str) -> dict:
    now = datetime.now(UTC)
    errors: list[str] = []

    try:
        client = PolygonClient()
    except Exception as exc:
        return {
            "timestamp_utc": now.isoformat(),
            "market_health_score": "DATA_UNAVAILABLE",
            "regime": "Unknown",
            "focus_areas": _focus_areas(report_type),
            "symbols": {},
            "breadth": {},
            "notes": [
                "Polygon client could not be initialized.",
                f"Error: {type(exc).__name__}: {exc}",
            ],
            "data_status": "FALLBACK",
            "errors": [f"PolygonClient: {type(exc).__name__}: {exc}"],
        }

    spy, spy_error = _try_symbol_snapshot(client, "SPY")
    qqq, qqq_error = _try_symbol_snapshot(client, "QQQ")
    vix, vix_error = _try_symbol_snapshot(client, VIX_TICKER)

    for error in [spy_error, qqq_error, vix_error]:
        if error:
            errors.append(error)

    try:
        breadth = _calculate_breadth(client)
    except Exception as exc:
        breadth = {
            "universe_size": 0,
            "above_sma50": 0,
            "breadth_percent": 0.0,
            "failed_symbols": [f"Breadth: {type(exc).__name__}: {exc}"],
        }
        errors.append(f"Breadth: {type(exc).__name__}: {exc}")

    errors.extend(breadth.get("failed_symbols", []))

    score = _calculate_partial_market_score(spy, qqq, vix, breadth)

    symbols: dict[str, dict] = {}
    if spy is not None:
        symbols["SPY"] = spy
    if qqq is not None:
        symbols["QQQ"] = qqq
    if vix is not None:
        symbols["VIX"] = vix

    if spy is None and qqq is None and vix is None and breadth.get("universe_size", 0) == 0:
        data_status = "FALLBACK"
    elif errors:
        data_status = "PARTIAL"
    else:
        data_status = "LIVE"

    notes = [
        "Live data source: Polygon.io daily aggregates.",
        "Breadth currently uses the configured leader universe, not the full S&P 500 universe.",
    ]

    if vix is None:
        notes.append("VIX data unavailable; scoring used a neutral fallback VIX value of 20.0.")

    if errors:
        notes.append("Some market data feeds failed; report is running in degraded mode.")

    return {
        "timestamp_utc": now.isoformat(),
        "market_health_score": score["score"],
        "regime": score["regime"],
        "focus_areas": _focus_areas(report_type),
        "symbols": symbols,
        "breadth": breadth,
        "notes": notes,
        "data_status": data_status,
        "errors": errors[:20],
    }
