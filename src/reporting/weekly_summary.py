from __future__ import annotations

from datetime import UTC, datetime


def build_weekly_summary() -> dict:
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "sections": {
            "recommended_assets": [
                "MSFT — monitor only when market regime and cross-asset risk remain supportive.",
                "NVDA — high-quality leader candidate, but position size should depend on volatility and sector heat.",
                "META — watch relative strength versus QQQ and confirm follow-through before new exposure.",
                "QQQ — use as the primary growth benchmark for leadership and risk-on confirmation.",
            ],
            "focus_for_next_week": [
                "Validate whether AI and semiconductor leaders continue to outperform the benchmark.",
                "Track whether cross-asset conditions confirm risk-on behavior or shift toward defensive rotation.",
                "Use the Decision Engine to separate strong trend from efficient asymmetric entry quality.",
                "Prioritize no-trade discipline if breadth weakens or failed breakout pressure expands.",
            ],
            "risk_notes": [
                "Monitor macroeconomic calendar events before increasing exposure.",
                "Track volatility expansion and reduce position size during high-volatility transitions.",
                "Avoid concentrated exposure when multiple candidates share the same sector or factor risk.",
                "Treat all outputs as research and decision support, not financial advice.",
            ],
        },
    }
