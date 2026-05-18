from __future__ import annotations

WATCHLIST = [
    "MSFT",
    "NVDA",
    "META",
    "AAPL",
    "MU",
    "QQQ",
    "GLD",
    "SLV",
]


def build_screener_snapshot(report_type: str) -> dict:
    if report_type == "premarket":
        title = "Pre-Market Watchlist"
        objectives = [
            "Gap analysis",
            "Opening range preparation",
            "High relative strength leaders",
        ]
    else:
        title = "Post-Market Review"
        objectives = [
            "Closing strength validation",
            "Failed breakout detection",
            "Swing continuation candidates",
        ]

    return {
        "title": title,
        "watchlist": WATCHLIST,
        "objectives": objectives,
        "warnings": [
            "Avoid oversized exposure before macro events.",
            "Confirm liquidity before entering trades.",
        ],
    }
