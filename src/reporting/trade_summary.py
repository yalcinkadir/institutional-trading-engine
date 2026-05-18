from __future__ import annotations


def build_trade_summary(
    market_regime: str,
    market_health_score: int | str,
    leaders: list[dict],
    weak_names: list[dict],
) -> str:
    lines: list[str] = []

    lines.append("TRADE SUMMARY")
    lines.append("")
    lines.append(f"Market Regime: {market_regime}")
    lines.append(f"Market Health Score: {market_health_score}")
    lines.append("")

    if leaders:
        lines.append("Top Leaders:")
        for index, asset in enumerate(leaders[:5], start=1):
            lines.append(
                f"{index}. {asset['ticker']} — Score {asset['score']} — {asset['status']}"
            )
        lines.append("")

    if weak_names:
        lines.append("Weak Names:")
        for asset in weak_names[:5]:
            lines.append(f"- {asset['ticker']} — Score {asset['score']}")
        lines.append("")

    return "\n".join(lines)
