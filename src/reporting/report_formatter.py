from __future__ import annotations

from datetime import UTC, datetime


def _bool_icon(value: bool) -> str:
    return "✅" if value else "❌"


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
    lines.append(f"- Data Status: {market['data_status']}")
    lines.append(f"- Regime: {market['regime']}")
    lines.append(f"- Market Health Score: {market['market_health_score']}")
    lines.append("")

    symbols = market.get("symbols", {})

    if symbols:
        lines.append("### Core Market Metrics")
        lines.append("")

        for ticker, snapshot in symbols.items():
            lines.append(f"#### {ticker}")
            lines.append(f"- Close: {snapshot['close']}")
            lines.append(f"- SMA50: {snapshot['sma50']} {_bool_icon(snapshot['above_sma50'])}")
            lines.append(f"- SMA200: {snapshot['sma200']} {_bool_icon(snapshot['above_sma200'])}")
            lines.append(f"- ATR14: {snapshot['atr14']}")
            lines.append("")

    breadth = market.get("breadth", {})

    if breadth:
        lines.append("### Market Breadth")
        lines.append(f"- Universe Size: {breadth['universe_size']}")
        lines.append(f"- Above SMA50: {breadth['above_sma50']}")
        lines.append(f"- Breadth %: {breadth['breadth_percent']}%")
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
    lines.append("")

    lines.append("### Notes")
    for note in market["notes"]:
        lines.append(f"- {note}")

    return "\n".join(lines)
