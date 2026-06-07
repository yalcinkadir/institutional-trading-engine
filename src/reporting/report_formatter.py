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

    base_score = item.get("base_setup_score")
    setup_score = item.get("setup_score")
    score_text = f"{setup_score}"
    if base_score is not None and base_score != setup_score:
        score_text = f"{setup_score} (base {base_score})"

    lines.append(
        f"- Setup Score: {score_text} | "
        f"Regime Alignment: {item['regime_alignment']} | "
        f"Asymmetry Score: {item.get('asymmetry_score', 'n/a')} | "
        f"Data Confidence: {item['data_confidence']}"
    )

    expectancy = item.get("expectancy") or {}
    if expectancy and expectancy.get("score_delta") not in {None, 0, 0.0}:
        lines.append(
            "- Expectancy Adjustment: "
            f"score {expectancy.get('score_delta'):+.1f} | "
            f"size×{expectancy.get('size_multiplier')}, "
            f"samples {expectancy.get('sample_size')}, "
            f"win rate {expectancy.get('win_rate')}, "
            f"expectancy {expectancy.get('expectancy')}, "
            f"source {expectancy.get('source')}"
        )
        lines.append(f"- Expectancy Profile: `{expectancy.get('profile_key')}`")

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


def _format_market_snapshot(ticker: str, snapshot: dict) -> list[str]:
    return [
        f"#### {ticker}",
        f"- Close: {snapshot.get('close', 'DATA_UNAVAILABLE')}",
        f"- SMA50: {snapshot.get('sma50', 'DATA_UNAVAILABLE')} {_bool_icon(bool(snapshot.get('above_sma50')))}",
        f"- SMA200: {snapshot.get('sma200', 'DATA_UNAVAILABLE')} {_bool_icon(bool(snapshot.get('above_sma200')))}",
        f"- ATR14: {snapshot.get('atr14', 'DATA_UNAVAILABLE')}",
        "",
    ]


def _format_unavailable_market_snapshot(ticker: str) -> list[str]:
    return [
        f"#### {ticker}",
        "- Close: DATA_UNAVAILABLE",
        "- SMA50: DATA_UNAVAILABLE",
        "- SMA200: DATA_UNAVAILABLE",
        "- ATR14: DATA_UNAVAILABLE",
        "",
    ]


def _format_run_health(decision_report: dict) -> list[str]:
    run_health = decision_report.get("run_health") or {}
    scanner_quality = decision_report.get("scanner_data_quality") or {}
    lines = ["## Run Health / Silent-Failure Gate", ""]
    lines.append(f"- Run Health: {run_health.get('run_health_status', 'UNKNOWN')}")
    lines.append(f"- Success Status: {run_health.get('success_status', 'UNKNOWN')}")
    lines.append(f"- Signal Generation: {decision_report.get('signal_generation_status', 'UNKNOWN')}")
    lines.append(f"- Scanner Data Quality: {scanner_quality.get('data_quality_status', 'UNKNOWN')}")
    if "valid_symbols" in scanner_quality or "total_symbols" in scanner_quality:
        lines.append(f"- Scanner Valid Symbols: {scanner_quality.get('valid_symbols', 'n/a')} / {scanner_quality.get('total_symbols', 'n/a')}")
    reasons = run_health.get("reasons") or []
    if reasons:
        lines.append(f"- Reasons: {', '.join(str(reason) for reason in reasons)}")
    else:
        lines.append("- Reasons: none")
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

    lines.append("## Market Regime")
    lines.append("")
    lines.append(f"- Data Status: {market.get('data_status', 'unknown')}")
    lines.append(f"- Regime: {market.get('regime', 'unknown')}")
    lines.append(f"- Market Health Score: {market.get('market_health_score', 'n/a')}")
    lines.append("")

    symbols = market.get("symbols") or {}

    lines.append("### Core Market Metrics")
    lines.append("")

    rendered = set()
    for core_ticker in ("SPY", "QQQ", "VIX"):
        if core_ticker in symbols:
            lines.extend(_format_market_snapshot(core_ticker, symbols[core_ticker]))
        else:
            lines.extend(_format_unavailable_market_snapshot(core_ticker))
        rendered.add(core_ticker)

    for ticker, snapshot in symbols.items():
        if ticker in rendered:
            continue
        lines.extend(_format_market_snapshot(ticker, snapshot))

    breadth = market.get("breadth") or {}
    lines.append("### Market Breadth")
    if breadth:
        lines.append(f"- Universe Size: {breadth['universe_size']}")
        lines.append(f"- Above SMA50: {breadth['above_sma50']}")
        lines.append(f"- Breadth %: {breadth['breadth_percent']}%")
    else:
        lines.append("- Breadth data unavailable during fallback mode.")
    lines.append("")

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
    for item in market.get("focus_areas", ["Monitor institutional risk conditions and trend quality."]):
        lines.append(f"- {item}")
    lines.append("")

    lines.extend(_format_run_health(decision_report))

    lines.append("## Decision Engine")
    lines.append("")
    lines.append(f"- Market State: {decision_report.get('market_state', 'unknown')}")
    lines.append(f"- Portfolio Heat Limit: {decision_report.get('portfolio_heat_limit', 'n/a')}")
    lines.append(f"- Approved / Reduced Size: {decision_report.get('approved_count', 0)}")
    lines.append(f"- Blocked / No Trade: {decision_report.get('blocked_count', 0)}")
    lines.append("")

    hard_overrides = decision_report.get("hard_overrides", [])
    if hard_overrides:
        lines.append("### ⚠️ Hard Overrides Active")
        for override in hard_overrides:
            lines.append(f"- {override}")
        lines.append("")

    expectancy_adjustments = decision_report.get("expectancy_adjustments_used", [])
    if expectancy_adjustments:
        lines.append("### Adaptive Expectancy Adjustments")
        lines.append("")
        for adjustment in expectancy_adjustments[:10]:
            lines.append(
                f"- `{adjustment.get('profile_key')}`: "
                f"score {adjustment.get('score_delta'):+.1f}, "
                f"size×{adjustment.get('size_multiplier')}, "
                f"samples {adjustment.get('sample_size')}, "
                f"expectancy {adjustment.get('expectancy')}, "
                f"recommendation {adjustment.get('recommendation')}"
            )
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
    approved = [d for d in decisions if d["decision"] in {"approved", "reduced_size", "watch"}]
    blocked = [d for d in decisions if d["decision"] in {"blocked", "no_trade"}]

    lines.append("### Ranked Opportunities")
    lines.append("")
    if approved:
        for item in approved:
            lines.extend(_format_decision_item(item))
    else:
        lines.append("- No ranked opportunities qualified for active risk. Decision remains No-Trade / watch mode until setup quality improves.")
        lines.append("- Asymmetry Score: n/a — no approved asymmetric setup available.")
        lines.append("")

    if blocked:
        lines.append("### 🚫 Blocked / No Trade")
        lines.append("")
        for item in blocked[:5]:
            reason = ", ".join(item.get("blocked_reasons", [])) or "regime/quality filter"
            asymmetry = item.get("asymmetry_score", "n/a")
            lines.append(f"- **{item['symbol']}**: {item['decision']} — {reason} | Asymmetry Score: {asymmetry}")
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
    for note in market.get("notes", ["Fallback mode active when live market data is unavailable."]):
        lines.append(f"- {note}")

    return "\n".join(lines)
