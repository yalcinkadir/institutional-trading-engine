"""
Signal Generator.

Converts Decision Engine output + scanner metrics into structured signal records
with Entry, Stop, Target levels and native deterministic signal identity.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from src.signals.entry_quality import derive_entry_quality
from src.signals.exit_target_quality import derive_exit_target_quality
from src.signals.signal_identity import build_signal_id
from src.signals.stop_loss_quality import derive_stop_loss_quality
from src.signals.trade_plan_validator import validate_long_trade_plan


SIGNALS_DIR = Path("reports/signals")
BLOCKED_SCORE_SOURCES = {"demo", "fixture", "demo_arithmetic_sequence", "public_demo"}
BLOCKED_DATA_SOURCES = {"demo", "fixture", "public_demo"}
BLOCKED_THRESHOLDS_VERSIONS = {"public_demo", "demo", "fixture"}


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
    exit_model: str = "n/a"
    exit_reason: str = "n/a"
    atr14: float | None = None
    data_status: str = "UNKNOWN"
    source: str | None = None
    source_timestamp: str | None = None
    fallback_level: str | None = None
    score_source: str = "unknown"
    data_source: str = "unknown"
    thresholds_version: str = "unknown"


def _safe(v: Any, fallback: float | None = None) -> float | None:
    if v is None:
        return fallback
    try:
        f = float(v)
        return fallback if (math.isnan(f) or math.isinf(f)) else f
    except (TypeError, ValueError):
        return fallback


def _safe_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


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


def _actionable_data_quality_reasons(
    *,
    close: float | None,
    atr14: float | None,
    data_status: str,
    source: str | None,
    source_timestamp: str | None,
    fallback_level: str | None,
) -> list[str]:
    reasons: list[str] = []
    if close is None:
        reasons.append("missing_close")
    if atr14 is None:
        reasons.append("missing_atr")
    if data_status != "OK":
        reasons.append(f"data_status_{data_status.lower()}")
    if source is None:
        reasons.append("missing_source")
    if source_timestamp is None:
        reasons.append("missing_source_timestamp")
    if fallback_level is None:
        reasons.append("missing_fallback_level")
    return reasons


def _demo_provenance_reasons(
    *,
    score_source: str,
    data_source: str,
    thresholds_version: str,
) -> list[str]:
    reasons: list[str] = []
    if score_source.lower() in BLOCKED_SCORE_SOURCES:
        reasons.append("demo_score_provenance")
    if data_source.lower() in BLOCKED_DATA_SOURCES:
        reasons.append("demo_data_source")
    if thresholds_version.lower() in BLOCKED_THRESHOLDS_VERSIONS:
        reasons.append("demo_thresholds_version")
    return reasons


def build_signals(
    decision_report: dict,
    scanner_metrics_map: dict[str, Any] | None = None,
    market_regime: str = "Unknown",
) -> list[Signal]:
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
        data_status = _safe_text(scanner.get("data_status")) or "UNKNOWN"
        source = _safe_text(scanner.get("source"))
        source_timestamp = _safe_text(scanner.get("source_timestamp"))
        fallback_level = _safe_text(scanner.get("fallback_level"))
        score_source = _safe_text(item.get("score_source")) or "unknown"
        data_source = _safe_text(item.get("data_source")) or "unknown"
        thresholds_version = _safe_text(item.get("thresholds_version")) or "unknown"

        entry = stop = t1 = t2 = rr = None
        entry_type = "n/a"
        entry_reason = "n/a"
        stop_model = "n/a"
        stop_reason = "n/a"
        exit_model = "n/a"
        exit_reason = "n/a"
        entry_quality_reasons: list[str] = []
        stop_quality_reasons: list[str] = []
        exit_quality_reasons: list[str] = []
        quality_gate_failed = False
        actionable_data_reasons = _actionable_data_quality_reasons(
            close=close,
            atr14=atr14,
            data_status=data_status,
            source=source,
            source_timestamp=source_timestamp,
            fallback_level=fallback_level,
        )
        demo_provenance_reasons = _demo_provenance_reasons(
            score_source=score_source,
            data_source=data_source,
            thresholds_version=thresholds_version,
        )

        if action == "BUY_WATCH" and not actionable_data_reasons and not demo_provenance_reasons:
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
            quality_gate_failed = quality_gate_failed or not entry_quality.is_valid

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
            quality_gate_failed = quality_gate_failed or not stop_quality.is_valid

            exit_quality = derive_exit_target_quality(
                setup_type=setup_type,
                entry_trigger=entry,
                stop_loss=stop,
                atr=atr14,
                scanner_metrics=scanner,
            )
            t1 = exit_quality.target_1
            t2 = exit_quality.target_2
            exit_model = exit_quality.exit_model
            exit_reason = exit_quality.exit_reason
            exit_quality_reasons = exit_quality.reasons
            quality_gate_failed = quality_gate_failed or not exit_quality.is_valid

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
        if original_action == "BUY_WATCH" and demo_provenance_reasons:
            quality_gate_failed = True
            notes_parts.append("provenance_contract: " + ", ".join(demo_provenance_reasons))
        if original_action == "BUY_WATCH" and actionable_data_reasons:
            quality_gate_failed = True
            if data_status == "BLOCKED":
                notes_parts.append("data_quality: blocked")
            elif data_status == "DEGRADED":
                notes_parts.append("data_quality: degraded")
            else:
                notes_parts.append(f"data_quality: {data_status.lower()}")
            notes_parts.append("data_contract: " + ", ".join(actionable_data_reasons))
        if original_action == "BUY_WATCH" and entry_quality_reasons:
            notes_parts.append("entry_quality: " + ", ".join(entry_quality_reasons))
        if original_action == "BUY_WATCH" and stop_quality_reasons:
            notes_parts.append("stop_quality: " + ", ".join(stop_quality_reasons))
        if original_action == "BUY_WATCH" and exit_quality_reasons:
            notes_parts.append("exit_quality: " + ", ".join(exit_quality_reasons))
        if original_action == "BUY_WATCH" and (quality_gate_failed or not validation.is_valid):
            action = "NO_TRADE"
            rr = None
            notes_parts.append("downgraded: invalid trade plan reasons " + ", ".join(validation.reasons))
        if action == "NO_TRADE" and not notes_parts:
            notes_parts.append("regime or quality filter")

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
            notes="; ".join(notes_parts),
            exit_model=exit_model,
            exit_reason=exit_reason,
            atr14=atr14,
            data_status=data_status,
            source=source,
            source_timestamp=source_timestamp,
            fallback_level=fallback_level,
            score_source=score_source,
            data_source=data_source,
            thresholds_version=thresholds_version,
        ))

    return signals


def save_signals(
    signals: list[Signal],
    date_str: str | None = None,
    signals_dir: Path | None = None,
    data_quality: dict[str, Any] | None = None,
) -> tuple[Path, Path]:
    target_dir = signals_dir or SIGNALS_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    date = date_str or datetime.now(UTC).strftime("%Y-%m-%d")
    json_path = target_dir / f"{date}-signals.json"
    md_path = target_dir / f"{date}-signals.md"
    latest_json = target_dir / "latest-signals.json"

    buy_signals = [s for s in signals if s.action == "BUY_WATCH"]
    no_trade = [s for s in signals if s.action != "BUY_WATCH"]
    data_quality_summary = data_quality or {
        "data_quality_status": "UNKNOWN",
        "total_symbols": len(signals),
        "valid_symbols": sum(1 for signal in signals if signal.close is not None and signal.atr14 is not None),
    }

    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "date": date,
        "market_regime": signals[0].market_regime if signals else "Unknown",
        "data_quality": data_quality_summary,
        "total_signals": len(signals),
        "actionable_count": len(buy_signals),
        "no_trade_count": len(no_trade),
        "signals": [asdict(s) for s in signals],
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    latest_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    now_str = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    lines = [f"# Institutional Signals - {date}", "", f"Generated: {now_str}", ""]
    lines += ["## Data Quality", "", f"- Status: {data_quality_summary.get('data_quality_status', 'UNKNOWN')}"]
    if data_quality_summary.get("missing_required_fields"):
        lines.append(f"- Missing required fields: {data_quality_summary['missing_required_fields']}")
    if data_quality_summary.get("missing_provenance_fields"):
        lines.append(f"- Missing provenance fields: {data_quality_summary['missing_provenance_fields']}")
    if data_quality_summary.get("stale_symbols"):
        lines.append(f"- Stale symbols: {data_quality_summary['stale_symbols']}")
    lines.append("")

    if buy_signals:
        lines += ["## Actionable Setups", ""]
        for s in buy_signals:
            rr_str = f" | R:R {s.risk_reward}" if s.risk_reward else ""
            atr_parts = []
            if s.atr14 is not None:
                atr_parts.append(f"ATR14: {s.atr14:.2f}")
            if s.atr_pct is not None:
                atr_parts.append(f"ATR%: {s.atr_pct:.2f}%")
            atr_line = "- " + " | ".join(atr_parts) + f" | Valid until: {s.valid_until}" if atr_parts else f"- Valid until: {s.valid_until}"
            lines += [
                f"### {s.symbol} - {s.action} ({s.risk_tier})",
                f"- Signal ID: `{s.signal_id}`",
                f"- Setup: {s.setup_type} | Score: {s.setup_score} | Decision: {s.decision} | Size: {s.position_size:.2f}x",
                f"- Score Source: {s.score_source} | Data Source: {s.data_source} | Thresholds: {s.thresholds_version}",
                f"- Data: {s.data_status} | Source: {s.source or 'unknown'} | Fallback: {s.fallback_level or 'unknown'} | Timestamp: {s.source_timestamp or 'unknown'}",
                f"- Entry: {s.entry_trigger} ({s.entry_type}) | Entry Reason: {s.entry_reason}",
                f"- Stop: {s.stop_loss} ({s.stop_model}) | Stop Reason: {s.stop_reason}",
                f"- T1: {s.target_1}" + (f" | T2: {s.target_2}" if s.target_2 else "") + f" | Exit: {s.exit_model} | Exit Reason: {s.exit_reason}" + rr_str,
                atr_line,
            ]
            if s.notes:
                lines.append(f"- Notes: {s.notes}")
            lines.append("")
    else:
        lines += ["## No Actionable Setups", "", "- No executable BUY_WATCH signals generated.", ""]

    if no_trade:
        lines += ["## No-Trade / Blocked", ""]
        for s in no_trade:
            lines.append(f"- **{s.symbol}**: {s.decision} - `{s.signal_id}` - {s.notes or 'regime/quality filter'}")
        lines.append("")

    lines += ["---", "## Signal Validity", "- BUY_WATCH requires valid entry, stop, target and trade-plan validation."]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path
