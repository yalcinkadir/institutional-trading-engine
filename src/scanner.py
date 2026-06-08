import os
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any

import pandas as pd
import requests

from src.config import SYMBOLS, BENCHMARK_MAP
from src.signals.structure_levels import latest_confirmed_swing_low_3bar

API_KEY = os.getenv("POLYGON_API_KEY")


class MarketDataFailureKind(str, Enum):
    MISSING_API_KEY = "MISSING_API_KEY"
    AUTH_FORBIDDEN = "AUTH_FORBIDDEN"
    RATE_LIMIT = "RATE_LIMIT"
    EMPTY_BARS = "EMPTY_BARS"
    HTTP_ERROR = "HTTP_ERROR"
    NETWORK_ERROR = "NETWORK_ERROR"
    PARSE_ERROR = "PARSE_ERROR"


@dataclass(frozen=True)
class MarketDataFailure:
    symbol: str
    kind: MarketDataFailureKind
    message: str
    provider: str = "polygon"
    status_code: int | None = None
    attempts: int = 1

    def as_metrics_fields(self) -> dict[str, Any]:
        return {
            "source": self.provider,
            "fallback_level": "primary",
            "data_status": "BLOCKED",
            "data_failure_kind": self.kind.value,
            "data_failure_message": self.message,
            "provider_status_code": self.status_code,
        }


MARKET_DATA_FAILURES: dict[str, MarketDataFailure] = {}


def _record_market_data_failure(failure: MarketDataFailure) -> None:
    MARKET_DATA_FAILURES[failure.symbol] = failure


def get_market_data_failure(symbol: str) -> MarketDataFailure | None:
    return MARKET_DATA_FAILURES.get(symbol)


def clear_market_data_failures() -> None:
    MARKET_DATA_FAILURES.clear()


def _failure_stub_metrics(symbol: str) -> dict:
    failure = get_market_data_failure(symbol)
    if failure is None:
        failure = MarketDataFailure(
            symbol=symbol,
            kind=MarketDataFailureKind.EMPTY_BARS,
            message="scanner returned no bars without a provider-level failure detail",
        )
    return {
        "symbol": symbol,
        "close": None,
        "high": None,
        "low": None,
        "volume": 0,
        "sma20": None,
        "sma50": None,
        "sma200": None,
        "rsi14": None,
        "atr14": None,
        "atr_pct": None,
        "vol20": None,
        "rvol": None,
        "swing_low_3bar": None,
        "ret_20d": None,
        "benchmark": benchmark_for_symbol(symbol),
        "benchmark_ret_20d": None,
        "rs_spread": None,
        "trend": "N/A",
        "momentum": "N/A",
        "volatility": "N/A",
        "rvol_label": "N/A",
        "rs_label": "N/A",
        "setup_readiness": "Data Blocked",
        "entry": None,
        "stop_loss": None,
        "exit_1": None,
        "exit_2": None,
        "warnings": [failure.message],
        **failure.as_metrics_fields(),
        "source_timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _is_blocked_metrics(metrics: dict | None) -> bool:
    return not metrics or str(metrics.get("data_status", "")).upper() == "BLOCKED"


def get_daily_bars(symbol, days=500, retries=3):
    end_date = datetime.now(timezone.utc).date()
    start_date = end_date - timedelta(days=days)

    if not API_KEY:
        failure = MarketDataFailure(
            symbol=symbol,
            kind=MarketDataFailureKind.MISSING_API_KEY,
            message="POLYGON_API_KEY is not configured",
            attempts=0,
        )
        _record_market_data_failure(failure)
        print(f"Market data failure for {symbol}: {failure.kind.value}: {failure.message}")
        return None

    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "limit": 5000,
        "apiKey": API_KEY,
    }

    last_failure: MarketDataFailure | None = None
    for attempt in range(retries):
        attempt_no = attempt + 1
        try:
            response = requests.get(url, params=params, timeout=30)

            if response.status_code == 429:
                last_failure = MarketDataFailure(
                    symbol=symbol,
                    kind=MarketDataFailureKind.RATE_LIMIT,
                    message="Polygon rate limit while loading daily bars",
                    status_code=429,
                    attempts=attempt_no,
                )
                _record_market_data_failure(last_failure)
                wait_time = 15
                print(f"Rate limit hit for {symbol}. Waiting {wait_time}s...")
                if attempt < retries - 1:
                    time.sleep(wait_time)
                    continue
                return None

            if response.status_code == 403:
                failure = MarketDataFailure(
                    symbol=symbol,
                    kind=MarketDataFailureKind.AUTH_FORBIDDEN,
                    message="Polygon returned 403 Forbidden for daily bars",
                    status_code=403,
                    attempts=attempt_no,
                )
                _record_market_data_failure(failure)
                print(f"Market data failure for {symbol}: {failure.kind.value}: {failure.message}")
                return None

            try:
                response.raise_for_status()
            except requests.HTTPError as exc:
                failure = MarketDataFailure(
                    symbol=symbol,
                    kind=MarketDataFailureKind.HTTP_ERROR,
                    message=f"Polygon HTTP error while loading daily bars: {exc}",
                    status_code=response.status_code,
                    attempts=attempt_no,
                )
                _record_market_data_failure(failure)
                print(f"Market data failure for {symbol}: {failure.kind.value}: {failure.message}")
                return None

            try:
                data = response.json()
            except ValueError as exc:
                failure = MarketDataFailure(
                    symbol=symbol,
                    kind=MarketDataFailureKind.PARSE_ERROR,
                    message=f"Polygon response JSON parse failed: {exc}",
                    status_code=response.status_code,
                    attempts=attempt_no,
                )
                _record_market_data_failure(failure)
                print(f"Market data failure for {symbol}: {failure.kind.value}: {failure.message}")
                return None

            if "results" not in data or not data["results"]:
                failure = MarketDataFailure(
                    symbol=symbol,
                    kind=MarketDataFailureKind.EMPTY_BARS,
                    message="Polygon returned no daily bars",
                    status_code=response.status_code,
                    attempts=attempt_no,
                )
                _record_market_data_failure(failure)
                print(f"Market data failure for {symbol}: {failure.kind.value}: {failure.message}")
                return None

            MARKET_DATA_FAILURES.pop(symbol, None)
            df = pd.DataFrame(data["results"])
            df["date"] = pd.to_datetime(df["t"], unit="ms").dt.date
            df = df.rename(
                columns={
                    "o": "open",
                    "h": "high",
                    "l": "low",
                    "c": "close",
                    "v": "volume",
                }
            )

            return df[["date", "open", "high", "low", "close", "volume"]].copy()

        except requests.RequestException as exc:
            last_failure = MarketDataFailure(
                symbol=symbol,
                kind=MarketDataFailureKind.NETWORK_ERROR,
                message=f"Polygon request failed while loading daily bars: {exc}",
                attempts=attempt_no,
            )
            _record_market_data_failure(last_failure)
            print(f"Market data failure for {symbol}: {last_failure.kind.value}: {last_failure.message}")
            if attempt < retries - 1:
                time.sleep(10)
            else:
                return None

    if last_failure is not None:
        _record_market_data_failure(last_failure)
    return None


def get_vix_value(retries=3):
    # Polygon index ticker format can depend on plan/feed.
    # We try I:VIX. If unavailable, return None gracefully.
    symbol = "I:VIX"
    end_date = datetime.now(timezone.utc).date()
    start_date = end_date - timedelta(days=30)

    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "limit": 100,
        "apiKey": API_KEY,
    }

    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=30)

            if response.status_code == 429:
                time.sleep(15)
                continue

            response.raise_for_status()
            data = response.json()

            if "results" not in data or not data["results"]:
                return None

            df = pd.DataFrame(data["results"])
            df = df.rename(columns={"c": "close"})
            latest_close = df.iloc[-1]["close"]
            prev_close = df.iloc[-2]["close"] if len(df) >= 2 else pd.NA

            direction = "Flat"
            if pd.notna(prev_close):
                if latest_close > prev_close:
                    direction = "Rising"
                elif latest_close < prev_close:
                    direction = "Falling"

            return {
                "close": latest_close,
                "direction": direction,
            }

        except Exception:
            if attempt < retries - 1:
                time.sleep(10)
            else:
                return None


def calculate_rsi(series, period=14):
    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / avg_loss.replace(0, pd.NA)
    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_atr(df, period=14):
    prev_close = df["close"].shift(1)

    tr1 = df["high"] - df["low"]
    tr2 = (df["high"] - prev_close).abs()
    tr3 = (df["low"] - prev_close).abs()

    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = true_range.rolling(window=period, min_periods=period).mean()

    return atr


def trend_label(close, sma20, sma50, sma200):
    if pd.isna(sma20) or pd.isna(sma50) or pd.isna(sma200):
        return "N/A"

    if close > sma20 > sma50 > sma200:
        return "Strong Uptrend"
    if close > sma50 and close > sma200:
        return "Uptrend"
    if close < sma50 and close < sma200:
        return "Downtrend"
    return "Mixed"


def rsi_label(rsi):
    if pd.isna(rsi):
        return "N/A"
    if rsi >= 70:
        return "Overbought"
    if rsi <= 30:
        return "Oversold"
    if rsi >= 55:
        return "Strong"
    if rsi <= 45:
        return "Weak"
    return "Neutral"


def volatility_label(atr_percent):
    if pd.isna(atr_percent):
        return "N/A"
    if atr_percent >= 4:
        return "Very High"
    if atr_percent >= 2.5:
        return "High"
    if atr_percent >= 1.2:
        return "Normal"
    return "Low"


def rvol_label(rvol):
    if pd.isna(rvol):
        return "N/A"
    if rvol >= 1.5:
        return "Strong"
    if rvol >= 1.0:
        return "Normal"
    return "Weak"


def rs_spread_label(rs_spread):
    if pd.isna(rs_spread):
        return "N/A"
    if rs_spread > 5:
        return "Leader"
    if rs_spread < -5:
        return "Weak"
    return "Neutral"


def fmt_number(value, digits=2):
    if pd.isna(value):
        return "N/A"
    return f"{float(value):.{digits}f}"


def fmt_signed_percent(value, digits=2):
    if pd.isna(value):
        return "N/A"
    value = float(value)
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.{digits}f}%"


def benchmark_for_symbol(symbol):
    return BENCHMARK_MAP.get(symbol, "SPY")


def calculate_20d_return(close_series):
    if len(close_series) < 21:
        return pd.NA
    current_close = close_series.iloc[-1]
    past_close = close_series.iloc[-21]
    if past_close == 0:
        return pd.NA
    return ((current_close / past_close) - 1) * 100


def setup_readiness_label(metrics):
    if not metrics:
        return "N/A"

    trend = metrics["trend"]
    rsi = metrics["rsi14"]
    atr_pct = metrics["atr_pct"]
    rs_spread = metrics["rs_spread"]
    rvol = metrics["rvol"]
    close = metrics["close"]
    sma20 = metrics["sma20"]
    sma50 = metrics["sma50"]

    if trend in ["Mixed", "Downtrend"] or metrics["rs_label"] == "Weak":
        return "Weak - Avoid"

    if pd.notna(atr_pct) and atr_pct > 5:
        return "High Volatility Caution"

    near_sma20 = pd.notna(sma20) and abs((close - sma20) / sma20) <= 0.03
    near_sma50 = pd.notna(sma50) and abs((close - sma50) / sma50) <= 0.03

    if (
        trend in ["Strong Uptrend", "Uptrend"]
        and pd.notna(rsi) and 45 <= rsi <= 65
        and pd.notna(rs_spread) and rs_spread >= -2
        and (near_sma20 or near_sma50)
    ):
        return "Pullback Candidate"

    if (
        trend in ["Strong Uptrend", "Uptrend"]
        and pd.notna(rsi) and 52 <= rsi <= 68
        and pd.notna(rs_spread) and rs_spread >= 0
        and pd.notna(rvol) and rvol >= 1.0
    ):
        return "Breakout Watch"

    if (
        trend == "Strong Uptrend"
        and pd.notna(rsi) and 65 < rsi < 70
        and pd.notna(rs_spread) and rs_spread >= 0
        and pd.notna(rvol) and rvol >= 0.9
    ):
        return "Trend Strong, Entry Unclear"

    if trend in ["Strong Uptrend", "Uptrend"] and pd.notna(rsi) and rsi >= 70:
        return "Extended - Avoid Chase"

    return "Not Ready"


def build_symbol_metrics(symbol, benchmark_returns):
    df = get_daily_bars(symbol)

    if df is None or df.empty:
        return _failure_stub_metrics(symbol)

    df["SMA20"] = df["close"].rolling(20).mean()
    df["SMA50"] = df["close"].rolling(50).mean()
    df["SMA200"] = df["close"].rolling(200).mean()
    df["RSI14"] = calculate_rsi(df["close"], 14)
    df["ATR14"] = calculate_atr(df, 14)
    df["ATR_PCT"] = (df["ATR14"] / df["close"]) * 100
    df["VOL20"] = df["volume"].rolling(20).mean()
    df["RVOL"] = df["volume"] / df["VOL20"]
    swing_low_3bar = latest_confirmed_swing_low_3bar(list(df["low"]))

    last = df.iloc[-1]
    ret_20d = calculate_20d_return(df["close"])

    benchmark_symbol = benchmark_for_symbol(symbol)
    benchmark_ret_20d = benchmark_returns.get(benchmark_symbol, pd.NA)

    if pd.isna(ret_20d) or pd.isna(benchmark_ret_20d):
        rs_spread = pd.NA
    else:
        rs_spread = ret_20d - benchmark_ret_20d

    warnings = []
    if pd.notna(ret_20d) and abs(ret_20d) > 40:
        warnings.append("Extreme 20D move")
    if pd.notna(last["ATR_PCT"]) and last["ATR_PCT"] > 6:
        warnings.append("Extreme volatility")

    entry = pd.NA
    stop_loss = pd.NA
    exit_1 = pd.NA
    exit_2 = pd.NA
    
    metrics = {
        "symbol": symbol,
        "close": last["close"],
        "high": last["high"],
        "low": last["low"],
        "volume": int(last["volume"]),
        "sma20": last["SMA20"],
        "sma50": last["SMA50"],
        "sma200": last["SMA200"],
        "rsi14": last["RSI14"],
        "atr14": last["ATR14"],
        "atr_pct": last["ATR_PCT"],
        "vol20": last["VOL20"],
        "rvol": last["RVOL"],
        "swing_low_3bar": swing_low_3bar,
        "ret_20d": ret_20d,
        "benchmark": benchmark_symbol,
        "benchmark_ret_20d": benchmark_ret_20d,
        "rs_spread": rs_spread,
        "warnings": warnings,
    }

    metrics["trend"] = trend_label(
        metrics["close"], metrics["sma20"], metrics["sma50"], metrics["sma200"]
    )
    metrics["momentum"] = rsi_label(metrics["rsi14"])
    metrics["volatility"] = volatility_label(metrics["atr_pct"])
    metrics["rvol_label"] = rvol_label(metrics["rvol"])
    metrics["rs_label"] = rs_spread_label(metrics["rs_spread"])
    metrics["setup_readiness"] = setup_readiness_label(metrics)
    
    if metrics["setup_readiness"] == "Breakout Watch":
        entry = metrics["high"] * 1.002
        stop_loss = entry - metrics["atr14"]
        exit_1 = entry + (1.5 * metrics["atr14"])
        exit_2 = entry + (2.5 * metrics["atr14"])

    elif metrics["setup_readiness"] == "Pullback Candidate":
        if pd.notna(metrics["sma20"]) and abs((metrics["close"] - metrics["sma20"]) / metrics["sma20"]) <= 0.03:
            entry = metrics["sma20"]
        elif pd.notna(metrics["sma50"]):
            entry = metrics["sma50"]

        if pd.notna(entry):
            stop_loss = entry - metrics["atr14"]
            exit_1 = entry + (1.5 * metrics["atr14"])
            exit_2 = entry + (2.5 * metrics["atr14"])

    metrics["entry"] = entry
    metrics["stop_loss"] = stop_loss
    metrics["exit_1"] = exit_1
    metrics["exit_2"] = exit_2
    return metrics


def format_symbol_report(metrics):
    if not metrics:
        return "- ERROR - No data"

    warning_text = ""
    if metrics["warnings"]:
        warning_text = f" | Warnings: {', '.join(metrics['warnings'])}"

    return (
        f"- {metrics['symbol']}: "
        f"Setup {metrics['setup_readiness']} | "
        f"Close {fmt_number(metrics['close'])} | "
        f"High {fmt_number(metrics['high'])} | "
        f"Low {fmt_number(metrics['low'])} | "
        f"Volume {metrics['volume']} | "
        f"RVOL {fmt_number(metrics['rvol'])} ({metrics['rvol_label']}) | "
        f"20D Return {fmt_signed_percent(metrics['ret_20d'])} | "
        f"RS Spread {fmt_signed_percent(metrics['rs_spread'])} vs {metrics['benchmark']} ({metrics['rs_label']}) | "
        f"RSI14 {fmt_number(metrics['rsi14'])} ({metrics['momentum']}) | "
        f"ATR14 {fmt_number(metrics['atr14'])} | "
        f"ATR% {fmt_number(metrics['atr_pct'])} ({metrics['volatility']}) | "
        f"SMA20 {fmt_number(metrics['sma20'])} | "
        f"SMA50 {fmt_number(metrics['sma50'])} | "
        f"SMA200 {fmt_number(metrics['sma200'])} | "
        f"Trend {metrics['trend']}"
        f"{warning_text}"
    )


def build_market_regime_summary(metrics_map, vix_data):
    spy = metrics_map.get("SPY")
    qqq = metrics_map.get("QQQ")

    if _is_blocked_metrics(spy) or _is_blocked_metrics(qqq):
        return [
            "## Market Regime Summary",
            "- Market Regime: N/A",
            "- Extension Status: N/A",
            "- Risk State: N/A",
            "- Fresh Longs: N/A",
            "- VIX: N/A",
            "- Comment: Missing or blocked SPY/QQQ data",
        ]

    score = 0

    if spy["trend"] in ["Strong Uptrend", "Uptrend"]:
        score += 2
    elif spy["trend"] == "Mixed":
        score += 1

    if qqq["trend"] in ["Strong Uptrend", "Uptrend"]:
        score += 2
    elif qqq["trend"] == "Mixed":
        score += 1

    if spy["rsi14"] >= 55:
        score += 1
    if qqq["rsi14"] >= 55:
        score += 1

    if score >= 5:
        market_regime = "Bullish"
    elif score >= 3:
        market_regime = "Neutral"
    else:
        market_regime = "Bearish"

    overbought_count = sum([spy["rsi14"] >= 70, qqq["rsi14"] >= 70])
    if overbought_count == 2:
        extension_status = "Extended"
    elif overbought_count == 1:
        extension_status = "Moderately Extended"
    else:
        extension_status = "Healthy"

    risk_state = "Cautious"
    if market_regime == "Bullish" and spy["atr_pct"] < 1.5 and qqq["atr_pct"] < 2.0:
        risk_state = "Risk-On"
    elif market_regime == "Bearish":
        risk_state = "Risk-Off"

    vix_text = "Unavailable"
    if vix_data:
        vix_close = fmt_number(vix_data["close"])
        vix_dir = vix_data["direction"]
        vix_text = f"{vix_close} ({vix_dir})"

        if pd.notna(vix_data["close"]):
            if vix_data["close"] > 25:
                risk_state = "Risk-Off"
            elif vix_data["close"] > 18 and risk_state == "Risk-On":
                risk_state = "Cautious"

            if vix_data["direction"] == "Rising" and risk_state == "Risk-On":
                risk_state = "Cautious"

    if market_regime == "Bullish" and extension_status == "Healthy" and risk_state == "Risk-On":
        fresh_longs = "Allowed"
    elif market_regime == "Bullish":
        fresh_longs = "Selective"
    else:
        fresh_longs = "Avoid"

    comment_parts = []

    if market_regime == "Bullish":
        comment_parts.append("Trend backdrop is supportive")
    elif market_regime == "Neutral":
        comment_parts.append("Trend backdrop is mixed")
    else:
        comment_parts.append("Trend backdrop is weak")

    if extension_status == "Extended":
        comment_parts.append("indices are short-term stretched")
    elif extension_status == "Moderately Extended":
        comment_parts.append("one index is getting stretched")
    else:
        comment_parts.append("extension is not excessive")

    if risk_state == "Risk-On":
        comment_parts.append("volatility remains controlled")
    elif risk_state == "Cautious":
        comment_parts.append("risk should stay selective")
    else:
        comment_parts.append("capital protection should dominate")

    comment = ". ".join(comment_parts) + "."

    return [
        "## Market Regime Summary",
        f"- Market Regime: {market_regime}",
        f"- Extension Status: {extension_status}",
        f"- Risk State: {risk_state}",
        f"- Fresh Longs: {fresh_longs}",
        f"- VIX: {vix_text}",
        f"- Comment: {comment}",
    ]


def build_leaders_section(metrics_map):
    clean_rows = []
    aggressive_rows = []

    for symbol, metrics in metrics_map.items():
        if _is_blocked_metrics(metrics) or symbol in ["QQQ", "SPY"]:
            continue

        if metrics["setup_readiness"] == "Pullback Candidate":
            clean_rows.append(metrics)
        elif metrics["setup_readiness"] in ["Breakout Watch", "Trend Strong, Entry Unclear"]:
            aggressive_rows.append(metrics)

    lines = ["## Leaders & Setups"]

    if clean_rows:
        lines.append("### Clean Pullback Candidates")
        for m in clean_rows[:8]:
            lines.append(f"- {m['symbol']}: Pullback near SMA | Close {fmt_number(m['close'])} | RSI {fmt_number(m['rsi14'])} | RS {fmt_signed_percent(m['rs_spread'])}")
    else:
        lines.append("### Clean Pullback Candidates")
        lines.append("- None")

    if aggressive_rows:
        lines.append("### Aggressive / Extended Watch")
        for m in aggressive_rows[:8]:
            lines.append(f"- {m['symbol']}: {m['setup_readiness']} | Close {fmt_number(m['close'])} | RSI {fmt_number(m['rsi14'])} | RS {fmt_signed_percent(m['rs_spread'])}")
    else:
        lines.append("### Aggressive / Extended Watch")
        lines.append("- None")

    return lines


def build_report():
    benchmark_returns = {}
    for bench in ["SPY", "QQQ", "GLD"]:
        df = get_daily_bars(bench)
        benchmark_returns[bench] = calculate_20d_return(df["close"]) if df is not None else pd.NA
        time.sleep(2)

    vix_data = get_vix_value()

    metrics_map = {}
    for symbol in SYMBOLS:
        print(f"Fetching {symbol}...")
        metrics_map[symbol] = build_symbol_metrics(symbol, benchmark_returns)
        time.sleep(2)

    lines = []
    lines.extend(build_market_regime_summary(metrics_map, vix_data))
    lines.append("")
    lines.extend(build_leaders_section(metrics_map))
    lines.append("")
    lines.append("## Full Scanner Snapshot")
    for symbol in SYMBOLS:
        lines.append(format_symbol_report(metrics_map.get(symbol)))

    return "\n".join(lines)


if __name__ == "__main__":
    print(build_report())
