"""Report formatter — renders the full institutional pre/postmarket report."""

from __future__ import annotations

from datetime import UTC, datetime


def _bool_icon(value: bool) -> str:
    return "✅" if value else "❌"


def _format_decision_item(item: dict) -> list[str]:
    """Render one decision with Entry/Stop/Target levels when available."""
    lines = [f"#### {item['symbol']}"]
    lines.append(f"- Decision: **{item['decision']}** | Risk Tier: {item['risk_tier']}")
    lines.append(f"- Setup Type: {item['setup_type']} | Size: {item['position_size_multiplier']}x")
    lines.append(
        f"- Setup Score: {item['setup_score']} | "
        f"Regime Alignment: {item['regime_alignment']} | "
        f"Data Confidence: {item['data_confidence']}"
    )

    # Entry / Stop / Target levels (only present when signals module ran)
    entry = item.get("entry_trigger")
    stop = item.get("stop_loss")
    t1 = item.get("target_1")
    t2 = item.get("target_2")
    rr = item.get("risk_reward")

    if entry and stop and t1:
        rr_str = f" | R:R **{rr}**" if rr else ""
        lines.append(
            f"- **Entry**: {entry} | **Stop**: {stop} | "
            f"**T1**: {t1}"
            + (f" | **T2**: {t2}" if t2 else "")
            + rr_str
        )

    if item.get("blocked_reasons"):
        lines.append(f"- Blocked: {', '.join(item['blocked_reasons'])}")

    if item.get("notes"):
        lines.append(f"- Notes: {', '.join(item['notes'])}")

    lines.append("")
    return lines


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
        lines.append(
            "This report summarizes market structure, leadership quality, "
            "risk conditions and focus areas for the upcoming trading week."
        )
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
    decision_report = payload.get("decision_report", {})
    cross_asset = payload.get("cross_asset", {})

    # ── Market Regime ──────────────────────────────────────────────────────
    lines.append("## Market Regime")
    lines.append("")
    lines.append(f"- Data Status: {market.get('data_status', 'unknown')}")
    lines.append(f"- Regime: {market.get('regime', 'unknown')}")
    lines.append(f"- Market Health Score: {market.get('market_health_score', 'n/a')}")
    lines.append("")

    symbols = market.get("symbols") or {}

    lines.append("### Core Market Metrics")
    lines.append("")

    if symbols:
        for ticker, snapshot in symbols.items():
            lines.append(f"#### {ticker}")
            lines.append(f"- Close: {snapshot['close']}")
            lines.append(
                f"- SMA50: {snapshot['sma50']} {_bool_icon(snapshot['above_sma50'])}"
            )
            lines.append(
                f"- SMA200: {snapshot['sma200']} {_bool_icon(snapshot['above_sma200'])}"
            )
            lines.append(f"- ATR14: {snapshot['atr14']}")
            lines.append("")
    else:
        lines += [
            "- SPY: DATA_UNAVAILABLE",
            "- VIX: DATA_UNAVAILABLE",
            "- SMA50: DATA_UNAVAILABLE",
            "- SMA200: DATA_UNAVAILABLE",
            "- ATR14: DATA_UNAVAILABLE",
            "",
        ]

    breadth = market.get("breadth") or {}
    lines.append("### Market Breadth")
    if breadth:
        lines.append(f"- Universe Size: {breadth['universe_size']}")
        lines.append(f"- Above SMA50: {breadth['above_sma50']}")
        lines.append(f"- Breadth %: {breadth['breadth_percent']}%")
    else:
        lines.append("- Breadth data unavailable during fallback mode.")
    lines.append("")

    # ── Cross-Asset ────────────────────────────────────────────────────────
    lines.append("## Cross-Asset Regime")
    lines.append("")
    lines.append(f"- Data Status: {cross_asset.get('data_status', 'unknown')}")
    lines.append(f"- Cross-Asset Regime: {cross_asset.get('regime', 'unknown')}")
    lines.append(f"- Risk Score: {cross_asset.get('risk_score', 'n/a')}")
    lines.append(f"- Risk-On Score: {cross_asset.get('risk_on_score', 'n/a')}")
    lines.append(f"- Risk-Off Score: {cross_asset.get('risk_off_score', 'n/a')}")
    lines.append("")

    warnings = cross_asset.get("warnings", [])
    confirmations = cross_asset.get("confirmations", [])

    if warnings:
        lines.append("### Cross-Asset Warnings")
        for w in warnings:
            lines.append(f"- {w}")
        lines.append("")

    if confirmations:
        lines.append("### Cross-Asset Confirmations")
        for c in confirmations:
            lines.append(f"- {c}")
        lines.append("")

    lines.append("### Focus Areas")
    for item in market.get(
        "focus_areas", ["Monitor institutional risk conditions and trend quality."]
    ):
        lines.append(f"- {item}")
    lines.append("")

    # ── Decision Engine ────────────────────────────────────────────────────
    lines.append("## Decision Engine")
    lines.append("")
    lines.append(f"- Market State: {decision_report.get('market_state', 'unknown')}")
    lines.append(
        f"- Portfolio Heat Limit: {decision_report.get('portfolio_heat_limit', 'n/a')}"
    )
    lines.append(
        f"- Approved / Reduced Size: {decision_report.get('approved_count', 0)}"
    )
    lines.append(
        f"- Blocked / No Trade: {decision_report.get('blocked_count', 0)}"
    )
    lines.append("")

    hard_overrides = decision_report.get("hard_overrides", [])
    if hard_overrides:
        lines.append("### ⚠️ Hard Overrides Active")
        for override in hard_overrides:
            lines.append(f"- {override}")
        lines.append("")

    data_note = decision_report.get("data_quality_note", "")
    if data_note:
        lines.append(f"> ℹ️ {data_note}")
        lines.append("")

    lines.append("### Active Strategy Types")
    for setup in decision_report.get("allowed_setups", []):
        lines.append(f"- {setup}")
    lines.append("")

    lines.append("### Decision Summary")
    lines.append(f"- {decision_report.get('summary', 'No summary available.')}")
    lines.append("")

    decisions = decision_report.get("decisions", [])
    if decisions:
        # Approved / Watch first
        approved = [
            d for d in decisions
            if d["decision"] in {"approved", "reduced_size", "watch"}
        ]
        blocked = [
            d for d in decisions
            if d["decision"] in {"blocked", "no_trade"}
        ]

        if approved:
            lines.append("### ✅ Actionable Setups")
            lines.append("")
            for item in approved:
                lines.extend(_format_decision_item(item))

        if blocked:
            lines.append("### 🚫 Blocked / No Trade")
            lines.append("")
            for item in blocked[:5]:
                reason = (
                    ", ".join(item.get("blocked_reasons", []))
                    or "regime/quality filter"
                )
                lines.append(f"- **{item['symbol']}**: {item['decision']} — {reason}")
            lines.append("")

    # ── Screener Watchlist ─────────────────────────────────────────────────
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
    for note in market.get(
        "notes", ["Fallback mode active when live market data is unavailable."]
    ):
        lines.append(f"- {note}")

    return "\n".join(lines)
