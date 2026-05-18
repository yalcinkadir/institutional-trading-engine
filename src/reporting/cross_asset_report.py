from __future__ import annotations

from src.cross_asset_regime import CrossAssetInput, evaluate_cross_asset_regime
from src.data.polygon_client import PolygonClient
from src.indicators.technical_indicators import sma

CROSS_ASSET_TICKERS = {
    "dollar": "UUP",
    "long_bonds": "TLT",
    "high_yield": "HYG",
    "investment_grade": "LQD",
    "small_caps": "IWM",
    "growth": "QQQ",
    "gold": "GLD",
    "equities": "SPY",
}


def _return_20d(closes: list[float]) -> float:
    if len(closes) < 21 or closes[-21] == 0:
        return 0.0
    return round((closes[-1] / closes[-21]) - 1, 4)


def _cross_asset_input(client: PolygonClient, symbol: str) -> CrossAssetInput:
    bars = client.get_daily_bars(symbol, days=260)
    closes = [float(bar["c"]) for bar in bars]
    close = closes[-1]
    sma50 = sma(closes, 50)
    sma200 = sma(closes, 200)

    return CrossAssetInput(
        symbol=symbol,
        return_20d=_return_20d(closes),
        above_sma50=close > sma50,
        above_sma200=close > sma200,
    )


def build_cross_asset_report() -> dict:
    try:
        client = PolygonClient()
        inputs = {
            key: _cross_asset_input(client, ticker)
            for key, ticker in CROSS_ASSET_TICKERS.items()
        }

        regime = evaluate_cross_asset_regime(**inputs)

        return {
            "data_status": "LIVE",
            "regime": regime.regime,
            "risk_score": regime.risk_score,
            "risk_on_score": regime.risk_on_score,
            "risk_off_score": regime.risk_off_score,
            "warnings": list(regime.warnings),
            "confirmations": list(regime.confirmations),
            "inputs": {
                key: {
                    "symbol": value.symbol,
                    "return_20d": value.return_20d,
                    "above_sma50": value.above_sma50,
                    "above_sma200": value.above_sma200,
                }
                for key, value in inputs.items()
            },
        }
    except Exception as exc:
        return {
            "data_status": "FALLBACK",
            "regime": "cross_asset_unknown",
            "risk_score": 50,
            "risk_on_score": 0,
            "risk_off_score": 0,
            "warnings": [f"cross_asset_data_unavailable: {type(exc).__name__}: {exc}"],
            "confirmations": [],
            "inputs": {},
        }
