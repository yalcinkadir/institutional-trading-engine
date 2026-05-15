import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import requests

API_KEY = os.getenv("POLYGON_API_KEY")

SYMBOLS = ["AAPL", "MSFT", "NVDA", "MU", "QQQ", "SPY"]


def get_daily_bars(symbol, days=500, retries=3):
    end_date = datetime.now(timezone.utc).date()
    start_date = end_date - timedelta(days=days)

    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "limit": 5000,
        "apiKey": API_KEY,
    }

    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=30)

            if response.status_code == 429:
                wait_time = 15
                print(f"Rate limit hit for {symbol}. Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            data = response.json()

            if "results" not in data or not data["results"]:
                print(f"No data returned for {symbol}")
                return None

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

        except Exception as e:
            print(f"Error for {symbol}: {e}")
            if attempt < retries - 1:
                time.sleep(10)
            else:
                print(f"Final error for {symbol}")
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


def fmt_number(value, digits=2):
    if pd.isna(value):
        return "N/A"
    return f"{float(value):.{digits}f}"


def build_symbol_report(symbol):
    df = get_daily_bars(symbol)

    if df is None or df.empty:
        return f"- {symbol}: ERROR - No data"

    df["SMA20"] = df["close"].rolling(20).mean()
    df["SMA50"] = df["close"].rolling(50).mean()
    df["SMA200"] = df["close"].rolling(200).mean()
    df["RSI14"] = calculate_rsi(df["close"], 14)

    last = df.iloc[-1]

    close = last["close"]
    high = last["high"]
    low = last["low"]
    volume = int(last["volume"])

    sma20 = last["SMA20"]
    sma50 = last["SMA50"]
    sma200 = last["SMA200"]
    rsi14 = last["RSI14"]

    trend = trend_label(close, sma20, sma50, sma200)
    momentum = rsi_label(rsi14)

    return (
        f"- {symbol}: Close {fmt_number(close)} | "
        f"High {fmt_number(high)} | "
        f"Low {fmt_number(low)} | "
        f"Volume {volume} | "
        f"RSI14 {fmt_number(rsi14)} ({momentum}) | "
        f"SMA20 {fmt_number(sma20)} | "
        f"SMA50 {fmt_number(sma50)} | "
        f"SMA200 {fmt_number(sma200)} | "
        f"Trend {trend}"
    )


def main():
    if not API_KEY:
        raise RuntimeError("POLYGON_API_KEY fehlt.")

    now_utc = datetime.now(timezone.utc)
    report_date = now_utc.strftime("%Y-%m-%d")
    report_timestamp = now_utc.strftime("%Y-%m-%d_%H-%M-%S")

    Path("reports").mkdir(exist_ok=True)

    lines = [f"# Market Report {report_timestamp} UTC\n"]

    for symbol in SYMBOLS:
        try:
            lines.append(build_symbol_report(symbol))
        except Exception as e:
            lines.append(f"- {symbol}: ERROR - {e}")

        time.sleep(12)

    report_path = f"reports/{report_timestamp}-market-report.md"
    Path(report_path).write_text("\n".join(lines), encoding="utf-8")

    print(f"Report created: {report_path}")


if __name__ == "__main__":
    main()
