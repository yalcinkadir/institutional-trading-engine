from __future__ import annotations

import os
from datetime import UTC, datetime
from statistics import mean
from typing import Any

from src.data.polygon_client import PolygonClient
from src.indicators.technical_indicators import calculate_atr, sma
from src.scoring.market_health_score import MarketHealthScore

INDEX_TICKERS = ["SPY", "QQQ"]
VIX_TICKER = "I:VIX"
DEFAULT_VOLATILITY_PROXY_SYMBOL = "VIXY"
NEUTRAL_FALLBACK_VIX = 20.0
VIX_UNAVAILABLE_ENTITLEMENT = "VIX_UNAVAILABLE_ENTITLEMENT"
VIX_UNAVAILABLE = "VIX_UNAVAILABLE"
VIX_PROXY_FALLBACK = "VIX_PROXY_FALLBACK"
REGIME_STATUS_LIVE = "LIVE"
REGIME_STATUS_DEGRADED = "DEGRADED"
REGIME_STATUS_PROXY_DEGRADED = "PROXY_DEGRADED"
REGIME_STATUS_UNVALIDATED = "UNVALIDATED"
REGIME_STATUS_BLOCKED = "BLOCKED"
UNVALIDATED_REGIME = "UNVALIDATED_REGIME"
BLOCKED_MARKET_REGIME_UNAVAILABLE = "BLOCKED_MARKET_REGIME_UNAVAILABLE"
REGIME_CONFIDENCE_FULL = "FULL"
REGIME_CONFIDENCE_DEGRADED = "DEGRADED"
REGIME_CONFIDENCE_BLOCKED = "BLOCKED"
REGIME_POLICY_ALLOW = "ALLOW"
REGIME_POLICY_DEGRADE = "DEGRADE"
REGIME_POLICY_BLOCK = "BLOCK"
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


def _volatility_proxy_symbol() -> str:
    return os.getenv("VOLATILITY_PROXY_SYMBOL", DEFAULT_VOLATILITY_PROXY_SYMBOL).strip() or DEFAULT_VOLATILITY_PROXY_SYMBOL


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


def _is_vix_entitlement_error(ticker: str, exc: Exception | str | None) -> bool:
    if ticker != VIX_TICKER or exc is None:
        return False
    text = str(exc).lower()
    return "403" in text or "forbidden" in text or "entitlement" in text


def _try_symbol_snapshot(client: PolygonClient, ticker: str) -> tuple[dict | None, str | None]:
    try:
        return _safe_symbol_snapshot(client, ticker), None
    except Exception as exc:
        if _is_vix_entitlement_error(ticker, exc):
            return None, (
                f"{ticker}: {VIX_UNAVAILABLE_ENTITLEMENT}: "
                "Polygon VIX index entitlement unavailable; volatility proxy fallback required"
            )
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


def _vix_failure_reason(vix_error: str | None) -> str:
    if vix_error and VIX_UNAVAILABLE_ENTITLEMENT in vix_error:
        return VIX_UNAVAILABLE_ENTITLEMENT
    return VIX_UNAVAILABLE


def _vix_status(vix_error: str | None) -> str:
    if vix_error and VIX_UNAVAILABLE_ENTITLEMENT in vix_error:
        return REGIME_STATUS_BLOCKED
    return REGIME_STATUS_BLOCKED


def _synthetic_vix_from_proxy(proxy: dict) -> float:
    """Map a tradable volatility proxy into a conservative VIX-like score input.

    The proxy price is not the VIX index. We only use its trend state to choose a
    conservative scoring input while preserving PROXY_DEGRADED provenance.
    """

    if proxy.get("above_sma50") and proxy.get("above_sma200"):
        return 28.0
    if proxy.get("above_sma50"):
        return 24.0
    return 18.0


def _vix_regime_input(
    *,
    vix: dict | None,
    vix_error: str | None,
    vix_proxy: dict | None,
    vix_proxy_error: str | None,
    timestamp_utc: str,
) -> dict[str, Any]:
    if vix and vix.get("close") is not None:
        return {
            "symbol": VIX_TICKER,
            "source": "polygon",
            "timestamp": timestamp_utc,
            "status": REGIME_STATUS_LIVE,
            "validation_status": REGIME_STATUS_LIVE,
            "value": float(vix["close"]),
            "fallback_used": False,
            "fallback_value": None,
            "reason": None,
            "error": None,
        }

    if vix_proxy and vix_proxy.get("close") is not None:
        proxy_value = _synthetic_vix_from_proxy(vix_proxy)
        return {
            "symbol": VIX_TICKER,
            "source": "polygon_proxy",
            "proxy_symbol": vix_proxy["ticker"],
            "timestamp": timestamp_utc,
            "status": REGIME_STATUS_PROXY_DEGRADED,
            "validation_status": REGIME_STATUS_DEGRADED,
            "value": proxy_value,
            "fallback_used": True,
            "fallback_value": proxy_value,
            "reason": VIX_PROXY_FALLBACK,
            "error": vix_error,
            "proxy_error": vix_proxy_error,
            "proxy_close": float(vix_proxy["close"]),
            "proxy_above_sma50": bool(vix_proxy.get("above_sma50")),
            "proxy_above_sma200": bool(vix_proxy.get("above_sma200")),
            "live_or_paper_confidence_authorized": False,
        }

    reason = _vix_failure_reason(vix_error)
    return {
        "symbol": VIX_TICKER,
        "source": "polygon",
        "timestamp": timestamp_utc,
        "status": _vix_status(vix_error),
        "validation_status": REGIME_STATUS_BLOCKED,
        "value": None,
        "fallback_used": True,
        "fallback_value": None,
        "reason": reason,
        "error": vix_error or "VIX input unavailable",
        "proxy_error": vix_proxy_error,
        "live_or_paper_confidence_authorized": False,
    }


def _index_trend_regime_input(
    *,
    spy: dict | None,
    qqq: dict | None,
    timestamp_utc: str,
) -> dict[str, Any]:
    symbols = []
    if spy is not None:
        symbols.append("SPY")
    if qqq is not None:
        symbols.append("QQQ")

    if not symbols:
        status = REGIME_STATUS_BLOCKED
    elif len(symbols) < 2:
        status = REGIME_STATUS_DEGRADED
    else:
        status = REGIME_STATUS_LIVE

    return {
        "symbols": symbols,
        "source": "polygon",
        "timestamp": timestamp_utc,
        "status": status,
        "required_symbols": INDEX_TICKERS,
    }


def _calculate_partial_market_score(
    spy: dict | None,
    qqq: dict | None,
    vix_input: dict[str, Any],
    breadth: dict,
) -> dict:
    if spy is None and qqq is None:
        return {
            "score": "DATA_UNAVAILABLE",
            "regime": BLOCKED_MARKET_REGIME_UNAVAILABLE,
        }

    vix_value = float(vix_input.get("value") or NEUTRAL_FALLBACK_VIX)

    score = MarketHealthScore(
        spy_above_sma50=bool(spy and spy["above_sma50"]),
        spy_above_sma200=bool(spy and spy["above_sma200"]),
        qqq_above_sma50=bool(qqq and qqq["above_sma50"]),
        qqq_above_sma200=bool(qqq and qqq["above_sma200"]),
        vix=vix_value,
        breadth_percent=float(breadth.get("breadth_percent", 0)),
    ).calculate()

    if vix_input.get("validation_status") == REGIME_STATUS_BLOCKED:
        score["regime"] = BLOCKED_MARKET_REGIME_UNAVAILABLE
    elif vix_input.get("status") == REGIME_STATUS_PROXY_DEGRADED:
        score["regime"] = f"{score['regime']} (VIX proxy degraded)"
    elif vix_input.get("fallback_used"):
        score["regime"] = f"{score['regime']} (VIX degraded)"

    return score


def _regime_policy(
    *,
    vix_input: dict[str, Any],
    index_trend_input: dict[str, Any],
) -> dict[str, Any]:
    if vix_input.get("validation_status") == REGIME_STATUS_BLOCKED:
        status = REGIME_STATUS_BLOCKED
        confidence = REGIME_CONFIDENCE_BLOCKED
        action = REGIME_POLICY_BLOCK
    elif index_trend_input.get("status") == REGIME_STATUS_BLOCKED:
        status = REGIME_STATUS_BLOCKED
        confidence = REGIME_CONFIDENCE_BLOCKED
        action = REGIME_POLICY_BLOCK
    elif vix_input.get("status") == REGIME_STATUS_PROXY_DEGRADED:
        status = REGIME_STATUS_DEGRADED
        confidence = REGIME_CONFIDENCE_DEGRADED
        action = REGIME_POLICY_DEGRADE
    elif index_trend_input.get("status") == REGIME_STATUS_DEGRADED:
        status = REGIME_STATUS_DEGRADED
        confidence = REGIME_CONFIDENCE_DEGRADED
        action = REGIME_POLICY_DEGRADE
    else:
        status = REGIME_STATUS_LIVE
        confidence = REGIME_CONFIDENCE_FULL
        action = REGIME_POLICY_ALLOW

    return {
        "status": status,
        "source": str(vix_input.get("source") or "unknown"),
        "fallback_used": bool(vix_input.get("fallback_used")),
        "confidence": confidence,
        "action": action,
        "reason": vix_input.get("reason"),
        "vix_status": vix_input.get("status"),
        "vix_validation_status": vix_input.get("validation_status"),
        "index_trend_status": index_trend_input.get("status"),
        "proxy_symbol": vix_input.get("proxy_symbol"),
    }


def _blocked_client_regime_input(timestamp_utc: str, error: str) -> dict[str, Any]:
    return {
        "vix": {
            "symbol": VIX_TICKER,
            "source": "polygon",
            "timestamp": timestamp_utc,
            "status": REGIME_STATUS_BLOCKED,
            "validation_status": REGIME_STATUS_BLOCKED,
            "value": None,
            "fallback_used": False,
            "fallback_value": None,
            "reason": "POLYGON_CLIENT_UNAVAILABLE",
            "error": error,
        },
        "index_trend": {
            "symbols": [],
            "source": "polygon",
            "timestamp": timestamp_utc,
            "status": REGIME_STATUS_BLOCKED,
            "required_symbols": INDEX_TICKERS,
        },
    }


def build_market_regime_summary(report_type: str) -> dict:
    now = datetime.now(UTC)
    timestamp_utc = now.isoformat()
    errors: list[str] = []

    try:
        client = PolygonClient()
    except Exception as exc:
        error = f"PolygonClient: {type(exc).__name__}: {exc}"
        regime_input = _blocked_client_regime_input(timestamp_utc, error)
        policy = _regime_policy(
            vix_input=regime_input["vix"],
            index_trend_input=regime_input["index_trend"],
        )
        return {
            "timestamp_utc": timestamp_utc,
            "market_health_score": "DATA_UNAVAILABLE",
            "regime": BLOCKED_MARKET_REGIME_UNAVAILABLE,
            "regime_policy": policy,
            "focus_areas": _focus_areas(report_type),
            "symbols": {},
            "breadth": {},
            "notes": [
                "Polygon client could not be initialized.",
                f"Error: {type(exc).__name__}: {exc}",
                "Market regime is explicitly blocked because required regime inputs are unavailable.",
            ],
            "data_status": "FALLBACK",
            "regime_validation_status": REGIME_STATUS_BLOCKED,
            "errors": [error],
            "regime_input": regime_input,
        }

    spy, spy_error = _try_symbol_snapshot(client, "SPY")
    qqq, qqq_error = _try_symbol_snapshot(client, "QQQ")
    vix, vix_error = _try_symbol_snapshot(client, VIX_TICKER)
    vix_proxy = None
    vix_proxy_error = None
    if vix is None and vix_error and VIX_UNAVAILABLE_ENTITLEMENT in vix_error:
        vix_proxy, vix_proxy_error = _try_symbol_snapshot(client, _volatility_proxy_symbol())

    for error in [spy_error, qqq_error, vix_error, vix_proxy_error]:
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

    regime_input = {
        "vix": _vix_regime_input(
            vix=vix,
            vix_error=vix_error,
            vix_proxy=vix_proxy,
            vix_proxy_error=vix_proxy_error,
            timestamp_utc=timestamp_utc,
        ),
        "index_trend": _index_trend_regime_input(spy=spy, qqq=qqq, timestamp_utc=timestamp_utc),
    }
    policy = _regime_policy(
        vix_input=regime_input["vix"],
        index_trend_input=regime_input["index_trend"],
    )
    score = _calculate_partial_market_score(spy, qqq, regime_input["vix"], breadth)
    if policy["action"] == REGIME_POLICY_BLOCK:
        score["regime"] = BLOCKED_MARKET_REGIME_UNAVAILABLE

    symbols: dict[str, dict] = {}
    if spy is not None:
        symbols["SPY"] = spy
    if qqq is not None:
        symbols["QQQ"] = qqq
    if vix is not None:
        symbols["VIX"] = vix
    if vix_proxy is not None:
        symbols["VIX_PROXY"] = vix_proxy

    regime_validation_status = str(regime_input["vix"].get("validation_status") or REGIME_STATUS_BLOCKED)
    if policy["action"] == REGIME_POLICY_BLOCK:
        regime_validation_status = REGIME_STATUS_BLOCKED

    if regime_input["index_trend"]["status"] == REGIME_STATUS_BLOCKED:
        data_status = "FALLBACK"
    elif (
        errors
        or regime_input["vix"]["status"] != REGIME_STATUS_LIVE
        or regime_input["index_trend"]["status"] != REGIME_STATUS_LIVE
    ):
        data_status = "PARTIAL"
    else:
        data_status = "LIVE"

    notes = [
        "Live data source: Polygon.io daily aggregates.",
        "Breadth currently uses the configured leader universe, not the full S&P 500 universe.",
    ]

    if policy["action"] == REGIME_POLICY_BLOCK:
        notes.append(
            "Market regime is explicitly blocked because required VIX/proxy or index trend inputs are unavailable."
        )
    elif regime_input["vix"].get("status") == REGIME_STATUS_PROXY_DEGRADED:
        notes.append(
            "Polygon VIX index unavailable; using configured volatility proxy for degraded regime evidence."
        )
    elif regime_input["vix"].get("fallback_used"):
        notes.append(
            f"VIX data unavailable; scoring used a neutral fallback VIX value of {NEUTRAL_FALLBACK_VIX}."
        )
    if regime_validation_status == REGIME_STATUS_UNVALIDATED:
        notes.append(
            "VIX/regime validation is UNVALIDATED; unavailable VIX evidence does not authorize live or paper confidence claims."
        )
    if regime_validation_status == REGIME_STATUS_DEGRADED:
        notes.append(
            "VIX/regime validation is DEGRADED; proxy evidence must not be treated as full VIX validation."
        )

    if errors:
        notes.append("Some market data feeds failed; report is running in degraded mode.")

    return {
        "timestamp_utc": timestamp_utc,
        "market_health_score": score["score"],
        "regime": score["regime"],
        "regime_policy": policy,
        "regime_validation_status": regime_validation_status,
        "focus_areas": _focus_areas(report_type),
        "symbols": symbols,
        "breadth": breadth,
        "notes": notes,
        "data_status": data_status,
        "errors": errors[:20],
        "regime_input": regime_input,
    }
