"""
Signal Generator.

Converts Decision Engine output + scanner metrics into structured,
maschinenlesbare signal records with concrete Entry, Stop, Target levels and
native deterministic signal identity.

These signals are:
  1. Written to reports/signals/YYYY-MM-DD-signals.json  (maschinenlesbar)
  2. Written to reports/signals/YYYY-MM-DD-signals.md    (menschenlesbar)
  3. Committed to the repo by GitHub Actions
  4. Read by the Entry/Exit Watcher and Outcome Tracker

Signal schema per symbol:
  signal_id        deterministic signal identity
  symbol           ticker
  action           BUY_WATCH | SELL_WATCH | NO_TRADE | AVOID
  setup_type       momentum_breakout | pullback_continuation | ...
  setup_score      0–100
  decision         approved | reduced_size | watch | blocked | no_trade
  risk_tier        tier_1 | tier_2 | tier_3 | no_trade
  position_size    0.0–1.0 multiplier
  close            closing price at signal time
  entry_trigger    price level that activates the trade
  entry_type       break_above | pullback_to | gap_fill
  stop_loss        invalidation price
  target_1         first target
  target_2         second target (or None)
  risk_reward      R:R ratio
  atr_pct          ATR% at signal time
  valid_until      ISO date — signal expires if not triggered
  market_regime    regime at signal generation
  generated_at     ISO UTC timestamp
  notes            human-readable context
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
    """
    now_iso = datetime.now(UTC).isoformat()
    signals: list[Signal] = []

    for item in decision_report.get("decisions", []):
        symbol = item["symbol"]
        decision = item["decision"]
        setup_type = item["setup_type"]
        action = _action_for_decision(decision)

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
            position_size=item["position_size_multiplier"],
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
        lines += ["## No Actionable Setups", "", "- No BUY_WATCH signals generated.", ""]

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
        "- Check next-day open price vs entry_trigger.",
        "- Stop and targets are ATR-derived; adjust to structure as appropriate.",
    ]

    md_path.write_text("\n".join(lines), encoding="utf-8")

    return json_path, md_path
