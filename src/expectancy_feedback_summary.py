"""Weekly expectancy feedback summary helpers.

This module turns the full adaptive expectancy summary into a compact text block
that is safe for GitHub Actions logs and optional Telegram delivery.
"""

from __future__ import annotations

from typing import Any


def build_weekly_expectancy_summary(summary: dict[str, Any], *, max_edges: int = 5) -> str:
    """Build a compact weekly expectancy feedback summary.

    The function is intentionally pure so CI can test it without Polygon,
    Telegram or filesystem side effects.
    """

    setup_profiles = summary.get("setup_profiles", []) or []
    regime_profiles = summary.get("regime_profiles", []) or []
    entry_profiles = summary.get("entry_type_profiles", []) or []
    strongest_edges = list(summary.get("strongest_edges", []) or [])
    weakest_edges = list(summary.get("weakest_edges", []) or [])

    evaluated_samples = _count_evaluated_samples(
        setup_profiles,
        regime_profiles,
        entry_profiles,
    )

    lines = [
        "Weekly Expectancy Feedback",
        f"Evaluated profile samples: {evaluated_samples}",
        "",
        "Strongest edges:",
    ]

    if strongest_edges:
        lines.extend(f"- {edge}" for edge in strongest_edges[:max_edges])
    else:
        lines.append("- Insufficient evaluated data.")

    lines.extend(["", "Weakest edges:"])
    if weakest_edges:
        lines.extend(f"- {edge}" for edge in weakest_edges[:max_edges])
    else:
        lines.append("- Insufficient evaluated data.")

    lines.extend(["", "Data quality:"])
    if evaluated_samples == 0:
        lines.append("- No evaluated samples yet. Treat expectancy as unavailable.")
    elif evaluated_samples < 10:
        lines.append("- Low sample size. Treat expectancy as directional only.")
    else:
        lines.append("- Sample size available for weekly review.")

    return "\n".join(lines)


def _count_evaluated_samples(*profile_groups: list[dict[str, Any]]) -> int:
    """Return the max available trade count across expectancy profile groups."""

    counts: list[int] = []
    for profiles in profile_groups:
        for profile in profiles:
            try:
                counts.append(int(profile.get("trades", 0)))
            except (TypeError, ValueError):
                counts.append(0)

    return max(counts) if counts else 0
