from __future__ import annotations

from datetime import datetime, UTC


def format_report(payload: dict) -> str:
    report_type = payload["report_type"].upper()
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

    lines: list[str] = []
    lines.append(f"# Institutional Trading Engine — {report_type} REPORT")
    lines.append("")
    lines.append(f"Generated: {now}")
    lines.append("")

    if report_type == "WEEKLY":
        weekly = payload["weekly_summary"]

        lines.append("## Weekly Summary")
        lines.append("")

        for key, values in weekly["sections"].items():
            title = key.replace("_", " ").title()
            lines.append(f"### {title}")
            for value in values:
                lines.append(f"- {value}")
            lines.append("")

        return "\n".join(lines)

    market = payload["market_regime"]
    screener = payload["screener"]

    lines.append("## Market Regime")
    lines.append("")
    lines.append(f"- Regime: {market['regime']}")
    lines.append(f"- Market Health Score: {market['market_health_score']}")
    lines.append("")

    lines.append("### Focus Areas")
    for item in market["focus_areas"]:
        lines.append(f"- {item}")
    lines.append("")

    lines.append(f"## {screener['title']}")
    lines.append("")

    lines.append("### Watchlist")
    for asset in screener["watchlist"]:
        lines.append(f"- {asset}")
    lines.append("")

    lines.append("### Objectives")
    for objective in screener["objectives"]:
        lines.append(f"- {objective}")
    lines.append("")

    lines.append("### Warnings")
    for warning in screener["warnings"]:
        lines.append(f"- {warning}")

    return "\n".join(lines)
