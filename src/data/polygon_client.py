from __future__ import annotations

import os
from datetime import datetime, timedelta

import requests

BASE_URL = "https://api.polygon.io"


class PolygonClient:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("POLYGON_API_KEY")

        if not self.api_key:
            raise ValueError("POLYGON_API_KEY is missing")

    def get_daily_bars(self, ticker: str, days: int = 250) -> list[dict]:
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days * 2)

        url = (
            f"{BASE_URL}/v2/aggs/ticker/{ticker}/range/1/day/"
            f"{start_date}/{end_date}"
        )

        response = requests.get(
            url,
            params={
                "adjusted": "true",
                "sort": "asc",
                "limit": days,
                "apiKey": self.api_key,
            },
            timeout=30,
        )

        response.raise_for_status()

        payload = response.json()

        return payload.get("results", [])
