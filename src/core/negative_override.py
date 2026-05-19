from __future__ import annotations

from typing import Any


SEVERITY_BLOCKING = "BLOCKING"
SEVERITY_MAJOR = "MAJOR"
SEVERITY_MINOR = "MINOR"


OVERRIDE_RANK = {
    "STRONG BUY": 4,
    "BUY": 3,
    "WATCH": 2,
    "HOLD": 1,
    "AVOID": 0,
}

REVERSE_OVERRIDE_RANK = {value: key for key, value in OVERRIDE_RANK.items()}


def evaluate_negative_overrides(context: dict[str, Any]) -> dict:
    overrides: list[dict[str, str]] = []

    if context.get("kill_switch") is True:
        overrides.append(
            {
                "severity": SEVERITY_BLOCKING,
                "reason": "kill_switch_active",
                "message": "Emergency kill switch is active",
            }
        )

    if context.get("data_status") == "FALLBACK":
        overrides.append(
            {
                "severity": SEVERITY_BLOCKING,
                "reason": "fallback_data_status",
                "message": "Market data is unavailable or unreliable",
            }
        )

    if context.get("report_quality_score", 100) < 75:
        overrides.append(
            {
                "severity": SEVERITY_BLOCKING,
                "reason": "low_report_quality",
                "message": "Report quality score is below institutional threshold",
            }
        )

    if context.get("days_until_earnings", 999) <= 3:
        overrides.append(
            {
                "severity": SEVERITY_MAJOR,
                "reason": "earnings_imminent",
                "message": "Earnings event is too close",
            }
        )

    if context.get("vix", 0) >= 30:
        overrides.append(
            {
                "severity": SEVERITY_MAJOR,
                "reason": "extreme_vix",
                "message": "VIX indicates elevated market stress",
            }
        )

    if context.get("event_risk", "low") == "high":
        overrides.append(
            {
                "severity": SEVERITY_MAJOR,
                "reason": "high_event_risk",
                "message": "High event risk detected",
            }
        )

    if context.get("liquidity_classification") == "Illiquid":
        overrides.append(
            {
                "severity": SEVERITY_MAJOR,
                "reason": "illiquid_asset",
                "message": "Asset liquidity is insufficient",
            }
        )

    if context.get("correlation", 0) >= 0.85:
        overrides.append(
            {
                "severity": SEVERITY_MINOR,
                "reason": "high_correlation",
                "message": "Portfolio correlation is elevated",
            }
        )

    if context.get("gap_percent", 0) >= 5:
        overrides.append(
            {
                "severity": SEVERITY_MINOR,
                "reason": "large_gap",
                "message": "Opening gap is elevated",
            }
        )

    if context.get("setup_status") in {"RISKY", "AVOID"}:
        overrides.append(
            {
                "severity": SEVERITY_MAJOR,
                "reason": "weak_setup_status",
                "message": "Setup status is not institutionally acceptable",
            }
        )

    blocking_count = sum(1 for item in overrides if item["severity"] == SEVERITY_BLOCKING)
    major_count = sum(1 for item in overrides if item["severity"] == SEVERITY_MAJOR)
    minor_count = sum(1 for item in overrides if item["severity"] == SEVERITY_MINOR)

    if blocking_count > 0:
        max_recommendation = "AVOID"
    elif major_count >= 2:
        max_recommendation = "AVOID"
    elif major_count == 1:
        max_recommendation = "WATCH"
    elif minor_count >= 2:
        max_recommendation = "HOLD"
    elif minor_count == 1:
        max_recommendation = "BUY"
    else:
        max_recommendation = "STRONG BUY"

    return {
        "has_overrides": bool(overrides),
        "overrides": overrides,
        "blocking_count": blocking_count,
        "major_count": major_count,
        "minor_count": minor_count,
        "max_recommendation": max_recommendation,
    }


def apply_negative_override(
    recommendation: str,
    override_result: dict[str, Any],
) -> dict:
    max_recommendation = override_result.get("max_recommendation", "STRONG BUY")

    original_rank = OVERRIDE_RANK.get(recommendation, 0)
    max_rank = OVERRIDE_RANK.get(max_recommendation, 0)
    final_rank = min(original_rank, max_rank)
    final_recommendation = REVERSE_OVERRIDE_RANK[final_rank]

    return {
        "original_recommendation": recommendation,
        "final_recommendation": final_recommendation,
        "max_allowed_recommendation": max_recommendation,
        "overrides_applied": recommendation != final_recommendation,
        "override_reasons": [
            item["reason"] for item in override_result.get("overrides", [])
        ],
    }
