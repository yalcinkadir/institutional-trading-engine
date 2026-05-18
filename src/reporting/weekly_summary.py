from __future__ import annotations

from datetime import datetime, UTC


def build_weekly_summary() -> dict:
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "sections": {
            "recommended_assets": [
                "MSFT",
                "NVDA",
                "META",
                "QQQ",
            ],
            "focus_for_next_week": [
                "AI leaders",
                "Semiconductor momentum",
                "Precious metals strength",
            ],
            "risk_notes": [
                "Monitor macroeconomic calendar.",
                "Track volatility expansion.",
            ],
        },
    }
