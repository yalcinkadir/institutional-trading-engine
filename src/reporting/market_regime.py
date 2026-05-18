from __future__ import annotations

from datetime import datetime, UTC


def build_market_regime_summary(report_type: str) -> dict:
    now = datetime.now(UTC)

    if report_type == "premarket":
        focus = [
            "US index futures",
            "overnight volatility",
            "macro event risk",
            "leader continuation potential",
        ]
    else:
        focus = [
            "closing breadth",
            "sector rotation",
            "institutional accumulation",
            "risk-off signals",
        ]

    return {
        "timestamp_utc": now.isoformat(),
        "market_health_score": "PENDING_LIVE_DATA",
        "regime": "Bullish / Neutral / Defensive",
        "focus_areas": focus,
        "notes": [
            "Polygon.io integration should populate live metrics.",
            "Future implementation: VIX term structure and breadth engine.",
        ],
    }
