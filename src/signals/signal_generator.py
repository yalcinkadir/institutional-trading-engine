"""
Signal Generator.

Converts Decision Engine output + scanner metrics into structured,
maschinenlesbare signal records with concrete Entry, Stop, Target levels and
native deterministic signal identity.

Signals are only actionable when executable trade levels are complete.
A signal may be analytically interesting, but it is not a BUY_WATCH unless
entry_trigger, stop_loss and target_1 are all present.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from src.signals.signal_identity import build_signal_id


SIGNALS_DIR = Path("reports/signals")
_REQUIRED_EXECUTABLE_LEVELS = ("entry_trigger", "stop_loss", "target_1")


@dataclass
class Signal:
    signal_id: str
    symbol: str
    action: str
    setup_type: str
    decision: str
    risk_tier: str
    position_size: float
    close: float | None
    entry_trigger: float | None
    entry_type: str
    stop_loss: float | None
    target_1: float | None
    target_2: float | None
    risk_reward: float | None
    atr_pct: float | None
    setup_score: float
    regime_alignment: float
    valid_until: str
    market_regime: str
    generated_at: str
    notes: str


def _safe(v: Any, fallback: float | None = None) -> float | None:
    if v is None:
        return fallback
    try:
        f = float(v)
        return fallback if (math.isnan(f) or math.isinf(f)) else f
    except (TypeError, ValueError):
        return fallback


def _derive_levels(
    close: float,
    atr: float,
    setup_type: str,
    scanner_metrics: dict | None,
) -> tuple[float, str, float, float, float | None]:
    """
    Derive Entry, Stop, Target levels from close + ATR.

    Returns: (entry_trigger, entry_type, stop_loss, target_1, target_2)
    """
    if scanner_metrics:
        sc_entry = _safe(scanner_metrics.get("entry"))
        sc_stop = _safe(scanner_metrics.get("stop_loss"))
        sc_t1 = _safe(scanner_metrics.get("exit_1"))
        sc_t2 = _safe(scanner_metrics.get("exit_2"))
        if sc_entry and sc_stop:
            return sc_entry, "break_above", sc_stop, sc_t1 or (close + 2 * atr), sc_t2

    if setup_type == "momentum_breakout":
        return (
            round(close + 0.5 * atr, 2), "break_above",
            round(close - 1.5 * atr, 2),
            round(close + 2.0 * atr, 2),
            round(close + 4.0 * atr, 2),
        )
    if setup_type == "pullback_continuation":
        return (
            round(close - 1.0 * atr, 2), "pullback_to",
            round(close - 2.5 * atr, 2),
            round(close + 1.5 * atr, 2),
            round(close + 3.0 * atr, 2),
        )
    if setup_type in ("defensive_rotation", "mean_reversion"):
        return (
            round(close, 2), "at_market",
            round(close - 2.0 * atr, 2),
            round(close + 1.5 * atr, 2),
            None,
        )
    return (
        round(close + 0.3 * atr, 2), "break_above",
        round(close - 3.0 * atr, 2),
        round(close + 3.0 * atr, 2),
        None,
    )


def _risk_reward(entry: float, stop: float, target: float) -> float | None:
    risk = abs(entry - stop)
    reward = abs(target - entry)
    if risk < 0.01:
        return None
    return round(reward / risk, 2)


def _valid_until(days: int = 3) -> str:
    return (datetime.now(UTC).date() + timedelta(days=days)).isoformat()


def _action_for_decision(decision: str) -> str:
    return {
        "approved": "BUY_WATCH",
        "reduced_size": "BUY_WATCH",
        "watch": "BUY_WATCH",
        "blocked": "NO_TRADE",
        "no_trade": "NO_TRADE",
    }.get(decision, "NO_TRADE")


def _missing_executable_levels(
    entry_trigger: float | None,
    stop_loss: float | None,
    target_1: float | None,
) -> list[str]:
    level_values = {
        "entry_trigger": entry_trigger,
        "stop_loss": stop_loss,
        "target_1": target_1,
    }
    return [name for name in _REQUIRED_EXECUTABLE_LEVELS if level_values[name] is None]


def _build_signal_payload_for_identity(
    *,
    symbol: str,
    action: str,
    entry_trigger: float | None,
    stop_loss: float | None,
    target_1: float | None,
    target_2: float | None,
    valid_until: str,
    generated_at: str,
) -> dict[str, Any]:
    return {
        "symbol": symbol,
        "action": action,
        "signal_date": generated_at[:10],
        "generated_at": generated_at,
        "entry_trigger": entry_trigger,
        "stop_loss": stop_loss,
        "target_1": target_1,
        "target_2": target_2,
        "valid_until": valid_until,
    }


def build_signals(
    decision_report: dict,
    scanner_metrics_map: dict[str, Any] | None = None,
    market_regime: str = "Unknown",
) -> list[Signal]:
    """
    Build Signal list from Decision Engine output.

    Quality gate:
    A BUY_WATCH signal is only emitted when entry_trigger, stop_loss and
    target_1 are all present. Otherwise the signal is downgraded to NO_TRADE.
    """
    now_iso = datetime.now(UTC).isoformat()
    signals: list[Signal] = []

    for item in decision_report.get("decisions", []):
        symbol = item["symbol"]
        decision = item["decision"]
        setup_type = item["setup_type"]
        action = _action_for_decision(decision)
        original_action = action

        scanner = (scanner_metrics_map or {}).get(symbol) or {}
        close = _safe(scanner.get("close"))
        atr14 = _safe(scanner.get("atr14"))
        atr_pct = _safe(scanner.get("atr_pct"))

        entry = stop = t1 = t2 = rr = None

        if close and atr14 and action == "BUY_WATCH":
            entry, entry_type, stop, t1, t2 = _derive_levels(
                close, atr14, setup_type, scanner
            )
            if entry and stop and t1:
                rr = _risk_reward(entry, stop, t1)
        else:
            entry_type = "n/a"

        notes_parts = []
        if item.get("blocked_reasons"):
            notes_parts.append(f"blocked: {', '.join(item['blocked_reasons'])}")
        if item.get("notes"):
            notes_parts.append(f"notes: {', '.join(item['notes'])}")

        missing_levels = _missing_executable_levels(entry, stop, t1)
        if original_action == "BUY_WATCH" and missing_levels:
            action = "NO_TRADE"
            entry_type = "n/a"
            rr = None
            notes_parts.append(
                "downgraded: incomplete executable levels "
                f"missing {', '.join(missing_levels)}"
            )

        if action == "NO_TRADE" and not notes_parts:
            notes_parts.append("regime or quality filter")
        notes = "; ".join(notes_parts) if notes_parts else ""
        valid_until = _valid_until(days=3)
        signal_id = build_signal_id(
            _build_signal_payload_for_identity(
                symbol=symbol,
                action=action,
                entry_trigger=entry,
                stop_loss=stop,
                target_1=t1,
                target_2=t2,
                valid_until=valid_until,
                generated_at=now_iso,
            )
        )

        signals.append(Signal(
            signal_id=signal_id,
            symbol=symbol,
            action=action,
            setup_type=setup_type,
            decision=decision,
            risk_tier=item["risk_tier"],
            position_size=item["position_size_multiplier"] if action == "BUY_WATCH" else 0.0,
            close=close,
            entry_trigger=entry,
            entry_type=entry_type,
            stop_loss=stop,
            target_1=t1,
            target_2=t2,
            risk_reward=rr,
            atr_pct=atr_pct,
            setup_score=item["setup_score"],
            regime_alignment=item["regime_alignment"],
            valid_until=valid_until,
            market_regime=market_regime,
            generated_at=now_iso,
            notes=notes,
        ))

    return signals


def save_signals(
    signals: list[Signal],
    date_str: str | None = None,
    signals_dir: Path | None = None,
) -> tuple[Path, Path]:
    """
    Save signals to JSON and Markdown files.

    Returns: (json_path, md_path)
    """
    target_dir = signals_dir or SIGNALS_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    date = date_str or datetime.now(UTC).strftime("%Y-%m-%d")

    json_path = target_dir / f"{date}-signals.json"
    md_path = target_dir / f"{date}-signals.md"
    latest_json = target_dir / "latest-signals.json"

    buy_signals = [s for s in signals if s.action == "BUY_WATCH"]
    no_trade = [s for s in signals if s.action != "BUY_WATCH"]

    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "date": date,
        "market_regime": signals[0].market_regime if signals else "Unknown",
        "total_signals": len(signals),
        "actionable_count": len(buy_signals),
        "no_trade_count": len(no_trade),
        "signals": [asdict(s) for s in signals],
    }

    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    latest_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    now_str = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# Institutional Signals — {date}",
        "",
        f"Generated: {now_str}",
        f"Market Regime: **{signals[0].market_regime if signals else 'Unknown'}**",
        "",
    ]

    if buy_signals:
        lines += ["## Actionable Setups", ""]
        for s in buy_signals:
            rr_str = f" | R:R {s.risk_reward}" if s.risk_reward else ""
            lines += [
                f"### {s.symbol} — {s.action} ({s.risk_tier})",
                f"- Signal ID: `{s.signal_id}`",
                f"- Setup: {s.setup_type} | Score: {s.setup_score} | "
                f"Decision: {s.decision} | Size: {s.position_size:.2f}x",
                f"- Close: {s.close}",
            ]
            if s.entry_trigger:
                lines.append(
                    f"- **Entry**: {s.entry_trigger} ({s.entry_type}) | "
                    f"**Stop**: {s.stop_loss} | **T1**: {s.target_1}"
                    + (f" | **T2**: {s.target_2}" if s.target_2 else "")
                    + rr_str
                )
            if s.atr_pct:
                lines.append(f"- ATR%: {s.atr_pct:.2f}% | Valid until: {s.valid_until}")
            if s.notes:
                lines.append(f"- Notes: {s.notes}")
            lines.append("")
    else:
        lines += ["## No Actionable Setups", "", "- No executable BUY_WATCH signals generated.", ""]

    if no_trade:
        lines += ["## No-Trade / Blocked", ""]
        for s in no_trade:
            reason = s.notes or "regime/quality filter"
            lines.append(f"- **{s.symbol}**: {s.decision} — `{s.signal_id}` — {reason}")
        lines.append("")

    lines += [
        "---",
        "## Signal Validity",
        f"- Signals valid until: {signals[0].valid_until if signals else 'N/A'}",
        "- BUY_WATCH requires entry_trigger, stop_loss and target_1.",
        "- Signals with incomplete executable levels are downgraded to NO_TRADE.",
        "- Stop and targets are ATR-derived unless supplied by scanner metrics.",
    ]

    md_path.write_text("\n".join(lines), encoding="utf-8")

    return json_path, md_path
