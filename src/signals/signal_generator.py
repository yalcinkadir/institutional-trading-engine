"""
Signal Generator.

Converts Decision Engine output + scanner metrics into structured,
maschinenlesbare signal records with concrete Entry, Stop, Target levels and
native deterministic signal identity.

Signals are only actionable when executable trade levels are complete and the
central Trade Plan Validator approves ordering, stop distance and risk/reward.
Entry triggers are derived by the Entry Quality Engine and must include an
entry reason. Stops are derived by the Stop-Loss Quality Engine and must include
a stop reason.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from src.signals.entry_quality import derive_entry_quality
from src.signals.signal_identity import build_signal_id
from src.signals.stop_loss_quality import derive_stop_loss_quality
from src.signals.trade_plan_validator import validate_long_trade_plan


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
    entry_reason: str
    stop_loss: float | None
    stop_model: str
    stop_reason: str
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


def _derive_targets(
    entry: float,
    stop: float,
    atr: float,
    setup_type: str,
    scanner_metrics: dict | None,
) -> tuple[float, float | None]:
    """Derive target levels after entry and stop quality have produced levels."""
    if scanner_metrics:
        sc_t1 = _safe(scanner_metrics.get("exit_1"))
        sc_t2 = _safe(scanner_metrics.get("exit_2"))
        if sc_t1 is not None:
            return sc_t1, sc_t2

    risk = abs(entry - stop)
    if setup_type == "momentum_breakout":
        return round(entry + 1.5 * risk, 2), round(entry + 2.5 * risk, 2)
    if setup_type == "pullback_continuation":
        return round(entry + 1.35 * risk, 2), round(entry + 2.25 * risk, 2)
    if setup_type == "retest_continuation":
        return round(entry + 1.4 * risk, 2), round(entry + 2.3 * risk, 2)
    if setup_type == "gap_fill":
        return round(entry + 1.35 * risk, 2), round(entry + 2.0 * risk, 2)
    if setup_type in ("defensive_rotation", "mean_reversion"):
        return round(entry + 1.5 * risk, 2), None
    return round(entry + max(1.5 * risk, 2.0 * atr), 2), None


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

    Quality gate:
    A BUY_WATCH signal is only emitted when Entry Quality, Stop-Loss Quality
    and Trade Plan validation pass. Otherwise it is downgraded to NO_TRADE.
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
        entry_type = "n/a"
        entry_reason = "n/a"
        stop_model = "n/a"
        stop_reason = "n/a"
        entry_quality_reasons: list[str] = []
        stop_quality_reasons: list[str] = []

        if action == "BUY_WATCH":
            entry_quality = derive_entry_quality(
                setup_type=setup_type,
                close=close,
                atr=atr14,
                scanner_metrics=scanner,
                allow_at_market=False,
            )
            entry = entry_quality.entry_trigger
            entry_type = entry_quality.entry_type
            entry_reason = entry_quality.entry_reason
            entry_quality_reasons = entry_quality.reasons

            stop_quality = derive_stop_loss_quality(
                setup_type=setup_type,
                entry_trigger=entry,
                close=close,
                atr=atr14,
                entry_type=entry_type,
                scanner_metrics=scanner,
            )
            stop = stop_quality.stop_loss
            stop_model = stop_quality.stop_model
            stop_reason = stop_quality.stop_reason
            stop_quality_reasons = stop_quality.reasons

            if entry_quality.is_valid and stop_quality.is_valid and entry is not None and stop is not None and atr14 is not None:
                t1, t2 = _derive_targets(entry, stop, atr14, setup_type, scanner)

        validation = validate_long_trade_plan(
            entry_trigger=entry,
            stop_loss=stop,
            target_1=t1,
            target_2=t2,
            atr=atr14,
        )
        if validation.risk_reward is not None:
            rr = round(validation.risk_reward, 2)

        notes_parts = []
        if item.get("blocked_reasons"):
            notes_parts.append(f"blocked: {', '.join(item['blocked_reasons'])}")
        if item.get("notes"):
            notes_parts.append(f"notes: {', '.join(item['notes'])}")

        if original_action == "BUY_WATCH" and entry_quality_reasons:
            notes_parts.append("entry_quality: " + ", ".join(entry_quality_reasons))
        if original_action == "BUY_WATCH" and stop_quality_reasons:
            notes_parts.append("stop_quality: " + ", ".join(stop_quality_reasons))

        if original_action == "BUY_WATCH" and not validation.is_valid:
            action = "NO_TRADE"
            rr = None
            notes_parts.append(
                "downgraded: invalid trade plan "
                f"reasons {', '.join(validation.reasons)}"
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
            entry_reason=entry_reason,
            stop_loss=stop,
            stop_model=stop_model,
            stop_reason=stop_reason,
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
                    f"Reason: {s.entry_reason} | "
                    f"**Stop**: {s.stop_loss} ({s.stop_model}) | "
                    f"Stop Reason: {s.stop_reason} | **T1**: {s.target_1}"
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
        "- BUY_WATCH requires valid entry quality, stop-loss quality and trade-plan validation.",
        "- Invalid entries, stops or trade plans are downgraded to NO_TRADE with validation reasons.",
        "- Stops and targets are ATR-derived unless supplied by scanner metrics.",
    ]

    md_path.write_text("\n".join(lines), encoding="utf-8")

    return json_path, md_path
