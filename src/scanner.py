import os
import requests
import time
from datetime import datetime
from pathlib import Path

API_KEY = os.getenv("POLYGON_API_KEY")

SYMBOLS = ["AAPL", "MSFT", "NVDA", "MU", "QQQ", "SPY"]


def get_last_close(symbol, retries=3):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/prev"
    params = {"adjusted": "true", "apiKey": API_KEY}

    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=20)

            # Rate limit handling
            if response.status_code == 429:
                wait_time = 15
                print(f"Rate limit hit for {symbol}. Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            data = response.json()

            if "results" not in data or len(data["results"]) == 0:
                raise ValueError("No data returned")

            result = data["results"][0]

            return {
                "symbol": symbol,
                "close": result["c"],
                "high": result["h"],
                "low": result["l"],
                "volume": result["v"],
            }

        except Exception as e:
            if attempt < retries - 1:
                print(f"Retry {attempt+1} for {symbol} due to error: {e}")
                time.sleep(10)
            else:
                raise e


def main():
    if not API_KEY:
        raise RuntimeError("POLYGON_API_KEY fehlt.")

    today = datetime.utcnow().strftime("%Y-%m-%d")
    Path("reports").mkdir(exist_ok=True)

    lines = [f"# Market Report {today}\n"]

    for symbol in SYMBOLS:
        try:
            data = get_last_close(symbol)

            lines.append(
                f"- {data['symbol']}: Close {data['close']} | High {data['high']} | Low {data['low']} | Volume {data['volume']}"
            )

        except Exception as e:
            lines.append(f"- {symbol}: ERROR - {e}")

        # Wichtig: Abstand zwischen Requests
        time.sleep(12)

    report_path = f"reports/{today}-market-report.md"
    Path(report_path).write_text("\n".join(lines), encoding="utf-8")

    print(f"Report created: {report_path}")


if __name__ == "__main__":
    main()
