"""
Entry / Exit Watcher.

Pure, testable signal lifecycle evaluation.

This module intentionally does NOT fetch market data itself. It evaluates
signal records against injected price bars/snapshots and returns deterministic
alerts + lifecycle updates.

Responsibilities:
- assign deterministic signal identity as fallback for legacy signals
- detect ENTRY_TRIGGERED
- detect INVALIDATED_BEFORE_ENTRY
- detect STOP_HIT
- detect TARGET_1_HIT
- detect TARGET_2_HIT
- detect EXPIRED
- manage partial exit + runner stop after TARGET_1_HIT
- detect REGIME_INVALIDATION_EXIT
- write alert JSON files
- append lifecycle JSONL records with duplicate protection

Data fetching belongs to scripts/run_entry_exit_watcher.py or another adapter.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable

from src.signals.signal_identity import (
    build_signal_id,
    ensure_signal_identity,
    signal_date_from_payload,
)
from src.signals.signal_status import (
    ACTIONABLE_SIGNAL_ACTIONS,
    TERMINAL_SIGNAL_STATUSES,
    SignalEventType,
    SignalStatus,
    is_terminal_signal_status,
    normalize_signal_status,
)
from src.watchers.regime_invalidation import apply_regime_invalidation
from src.watchers.trailing_stop_manager import apply_target_1_runner_management

ALERTS_DIR = Path("reports/alerts")
LIFECYCLE_LOG = Path("data/signal_lifecycle.jsonl")

ACTIONABLE_ACTIONS = ACTIONABLE_SIGNAL_ACTIONS
TERMINAL_STATUSES = TERMINAL_SIGNAL_STATUSES


@dataclass(frozen=True)
class PriceBar:
    symbol: str
    timestamp: str
    open: float | None = None
    high: float | None = None
    low: float | None = None
    close: float | None = None
    is_complete: bool = True
    completed_at: str | None = None
    completion_source: str = "assumed_complete"


@dataclass(frozen=True)
class WatcherAlert:
    alert_type: str
    symbol: str
    timestamp: str
    signal_date: str
    price: float | None
    trigger_price: float | None
    stop_loss: float | None
    target_1: float | None
    target_2: float | None
    previous_status: str
    new_status: str
    signal_id: str
    notes: str = ""


@dataclass(frozen=True)
class SignalLifecycleUpdate:
    signal_id: str
    symbol: str
    signal_date: str
    timestamp: str
    previous_status: str
    new_status: str
    event_type: str
    price: float | None
    signal: dict[str, Any]


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _today_utc() -> date:
    return datetime.now(UTC).date()


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def _signal_date(signal: dict[str, Any]) -> str:
    return signal_date_from_payload(signal)


def _current_status(signal: dict[str, Any]) -> str:
    return normalize_signal_status(signal.get("status"))


def load_signal_file(path: str | Path) -> list[dict[str, Any]]:
    """Load signal records from reports/signals/*.json and ensure ids."""
    signal_path = Path(path)
    if not signal_path.exists():
        return []

    payload = json.loads(signal_path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        signals = payload
    else:
        signals = payload.get("signals", []) if isinstance(payload, dict) else []

    if not isinstance(signals, list):
        return []
    return [ensure_signal_identity(item) for item in signals if isinstance(item, dict)]


def _bar_high(bar: PriceBar) -> float | None:
    return bar.high if bar.high is not None else bar.close


def _bar_low(bar: PriceBar) -> float | None:
    return bar.low if bar.low is not None else bar.close


def _bar_price_for_alert(bar: PriceBar, level: float | None) -> float | None:
    if level is not None:
        return level
    return bar.close or bar.high or bar.low or bar.open


def _parse_bar_timestamp_date(timestamp: str) -> date | None:
    if not timestamp:
        return None
    try:
        normalized = str(timestamp).replace("Z", "+00:00")
        return datetime.fromisoformat(normalized).date()
    except ValueError:
        try:
            return date.fromisoformat(str(timestamp)[:10])
        except ValueError:
            return None


def _bar_sort_key(bar: dict[str, Any]) -> tuple[int, float, str]:
    """Return a deterministic sort key for Polygon-style bars.

    RGP10 rule: provider order is not trusted. Numeric millisecond timestamps are
    preferred, ISO-like timestamps are second, and unknown timestamps sort last so
    they cannot replace a known newest bar.
    """
    timestamp = bar.get("t")
    if timestamp is not None:
        try:
            return (2, float(timestamp), str(timestamp))
        except (TypeError, ValueError):
            pass

    for key in ("timestamp", "datetime", "date"):
        value = bar.get(key)
        if not value:
            continue
        text = str(value)
        normalized = text.replace("Z", "+00:00")
        try:
            return (1, datetime.fromisoformat(normalized).timestamp(), text)
        except ValueError:
            try:
                return (1, datetime.fromisoformat(text[:10]).timestamp(), text)
            except ValueError:
                return (0, float("-inf"), text)

    return (0, float("-inf"), "")


def _latest_bar(bars: Iterable[dict[str, Any]]) -> dict[str, Any] | None:
    bars_list = list(bars)
    if not bars_list:
        return None
    return max(bars_list, key=_bar_sort_key)


def _is_daily_bar_complete(bar_timestamp: str, *, today: date | None = None) -> bool:
    bar_date = _parse_bar_timestamp_date(bar_timestamp)
    if bar_date is None:
        return False
    return bar_date < (today or _today_utc())


def _completion_timestamp_for_daily_bar(bar_timestamp: str) -> str | None:
    bar_date = _parse_bar_timestamp_date(bar_timestamp)
    if bar_date is None:
        return None
    return datetime.combine(
        bar_date + timedelta(days=1),
        datetime.min.time(),
        tzinfo=UTC,
    ).isoformat()


def _is_expired(signal: dict[str, Any], today: date | None = None) -> bool:
    valid_until = _parse_date(signal.get("valid_until"))
    if valid_until is None:
        return False
    return (today or _today_utc()) > valid_until


def evaluate_signal_against_bar(
    signal: dict[str, Any],
    bar: PriceBar,
    *,
    today: date | None = None,
) -> tuple[WatcherAlert | None, SignalLifecycleUpdate | None]:
    """
    Evaluate one signal against one price bar.

    For BUY_WATCH signals:
    - PENDING becomes INVALIDATED_BEFORE_ENTRY when low <= stop_loss.
    - PENDING becomes TRIGGERED when high >= entry_trigger.
    - TRIGGERED becomes STOP_HIT when low <= stop_loss.
    - TRIGGERED becomes TARGET_1_HIT when high >= target_1.
    - TARGET_1_HIT becomes TARGET_2_HIT when high >= target_2.
    - PENDING becomes EXPIRED after valid_until.

    Conservative ordering when a single bar touches invalidation/stop and entry/target:
    invalidation/stop is evaluated before entry/targets. This avoids optimistic
    backtest bias and prevents stale PENDING plans from activating after their
    original risk boundary was already breached.

    SR7 completed-bar rule:
    price lifecycle transitions are evaluated only on complete bars. If the bar
    is explicitly incomplete, the signal is preserved and no lifecycle event is
    emitted. This prevents intrabar high/low noise from being treated as final.
    """
    signal = ensure_signal_identity(signal)

    if not bar.is_complete:
        return None, None

    signal_id = str(signal["signal_id"])
    symbol = str(signal.get("symbol") or "")
    if not symbol or symbol != bar.symbol:
        return None, None

    action = str(signal.get("action") or "")
    if action not in ACTIONABLE_ACTIONS:
        return None, None

    previous_status = _current_status(signal)
    if is_terminal_signal_status(previous_status):
        return None, None

    signal_date = _signal_date(signal)
    entry = _safe_float(signal.get("entry_trigger"))
    stop = _safe_float(signal.get("stop_loss"))
    target_1 = _safe_float(signal.get("target_1"))
    target_2 = _safe_float(signal.get("target_2"))
    atr = _safe_float(signal.get("atr14") or signal.get("atr"))
    high = _bar_high(bar)
    low = _bar_low(bar)

    event_type: str | None = None
    new_status: str | None = None
    trigger_price: float | None = None

    if previous_status == SignalStatus.PENDING.value and stop is not None and low is not None and low <= stop:
        event_type = SignalEventType.INVALIDATED_BEFORE_ENTRY.value
        new_status = SignalStatus.INVALIDATED_BEFORE_ENTRY.value
        trigger_price = stop

    elif previous_status == SignalStatus.PENDING.value and _is_expired(signal, today=today):
        event_type = SignalEventType.EXPIRED.value
        new_status = SignalStatus.EXPIRED.value
        trigger_price = None

    elif previous_status == SignalStatus.PENDING.value and entry is not None and high is not None and high >= entry:
        event_type = SignalEventType.ENTRY_TRIGGERED.value
        new_status = SignalStatus.TRIGGERED.value
        trigger_price = entry

    elif previous_status in {SignalStatus.TRIGGERED.value, SignalStatus.TARGET_1_HIT.value}:
        if stop is not None and low is not None and low <= stop:
            event_type = SignalEventType.STOP_HIT.value
            new_status = SignalStatus.STOP_HIT.value
            trigger_price = stop
        elif previous_status == SignalStatus.TRIGGERED.value and target_1 is not None and high is not None and high >= target_1:
            event_type = SignalEventType.TARGET_1_HIT.value
            new_status = SignalStatus.TARGET_1_HIT.value
            trigger_price = target_1
        elif previous_status == SignalStatus.TARGET_1_HIT.value and target_2 is not None and high is not None and high >= target_2:
            event_type = SignalEventType.TARGET_2_HIT.value
            new_status = SignalStatus.TARGET_2_HIT.value
            trigger_price = target_2

    if not event_type or not new_status:
        return None, None

    updated_signal = dict(signal)
    updated_signal["signal_id"] = signal_id
    updated_signal["status"] = new_status

    if event_type == SignalEventType.ENTRY_TRIGGERED.value:
        updated_signal["entry_triggered_at"] = bar.timestamp
        updated_signal["entry_price"] = trigger_price
    elif event_type in {
        SignalEventType.INVALIDATED_BEFORE_ENTRY.value,
        SignalEventType.STOP_HIT.value,
        SignalEventType.TARGET_1_HIT.value,
        SignalEventType.TARGET_2_HIT.value,
        SignalEventType.EXPIRED.value,
    }:
        updated_signal["last_event_at"] = bar.timestamp
        updated_signal["last_event_price"] = trigger_price

    if event_type == SignalEventType.TARGET_1_HIT.value:
        runner_result = apply_target_1_runner_management(
            updated_signal,
            latest_high=high,
            atr=atr,
        )
        updated_signal = runner_result.signal
        stop = _safe_float(updated_signal.get("stop_loss"))

    alert = WatcherAlert(
        alert_type=event_type,
        symbol=symbol,
        timestamp=bar.timestamp,
        signal_date=signal_date,
        price=_bar_price_for_alert(bar, trigger_price),
        trigger_price=trigger_price,
        stop_loss=stop,
        target_1=target_1,
        target_2=target_2,
        previous_status=previous_status,
        new_status=new_status,
        signal_id=signal_id,
        notes=f"{previous_status} → {new_status}",
    )

    lifecycle = SignalLifecycleUpdate(
        signal_id=signal_id,
        symbol=symbol,
        signal_date=signal_date,
        timestamp=bar.timestamp,
        previous_status=previous_status,
        new_status=new_status,
        event_type=event_type,
        price=alert.price,
        signal=updated_signal,
    )

    return alert, lifecycle


def evaluate_regime_invalidation(
    signal: dict[str, Any],
    *,
    regime: Any,
    timestamp: str,
) -> tuple[WatcherAlert | None, SignalLifecycleUpdate | None]:
    """Evaluate whether one active signal should be invalidated by regime."""
    signal = ensure_signal_identity(signal)
    result = apply_regime_invalidation(signal, regime=regime, timestamp=timestamp)
    if not result.invalidated or not result.event_type or not result.new_status:
        return None, None

    signal_id = str(signal["signal_id"])
    symbol = str(signal.get("symbol") or "")
    trigger_price = _safe_float(
        signal.get("last_event_price") or signal.get("close") or signal.get("entry_price")
    )

    alert = WatcherAlert(
        alert_type=result.event_type,
        symbol=symbol,
        timestamp=timestamp,
        signal_date=_signal_date(signal),
        price=trigger_price,
        trigger_price=trigger_price,
        stop_loss=_safe_float(result.signal.get("stop_loss")),
        target_1=_safe_float(result.signal.get("target_1")),
        target_2=_safe_float(result.signal.get("target_2")),
        previous_status=str(result.previous_status),
        new_status=result.new_status,
        signal_id=signal_id,
        notes=f"{result.previous_status} → {result.new_status}: regime invalidation",
    )

    lifecycle = SignalLifecycleUpdate(
        signal_id=signal_id,
        symbol=symbol,
        signal_date=_signal_date(signal),
        timestamp=timestamp,
        previous_status=str(result.previous_status),
        new_status=result.new_status,
        event_type=result.event_type,
        price=trigger_price,
        signal=result.signal,
    )

    return alert, lifecycle


def evaluate_regime_invalidations(
    signals: list[dict[str, Any]],
    *,
    regime: Any,
    timestamp: str | None = None,
) -> tuple[list[WatcherAlert], list[SignalLifecycleUpdate], list[dict[str, Any]]]:
    """Evaluate regime invalidation across all signals."""
    event_timestamp = timestamp or utc_now_iso()
    alerts: list[WatcherAlert] = []
    updates: list[SignalLifecycleUpdate] = []
    updated_signals: list[dict[str, Any]] = []

    for raw_signal in signals:
        signal = ensure_signal_identity(raw_signal)
        alert, lifecycle = evaluate_regime_invalidation(
            signal,
            regime=regime,
            timestamp=event_timestamp,
        )
        if alert and lifecycle:
            alerts.append(alert)
            updates.append(lifecycle)
            updated_signals.append(lifecycle.signal)
        else:
            updated_signals.append(signal)

    return alerts, updates, updated_signals


def evaluate_signals(
    signals: list[dict[str, Any]],
    bars_by_symbol: dict[str, PriceBar],
    *,
    today: date | None = None,
) -> tuple[list[WatcherAlert], list[SignalLifecycleUpdate], list[dict[str, Any]]]:
    """Evaluate all signals and return alerts, lifecycle updates, updated signals."""
    alerts: list[WatcherAlert] = []
    updates: list[SignalLifecycleUpdate] = []
    updated_signals: list[dict[str, Any]] = []

    for raw_signal in signals:
        signal = ensure_signal_identity(raw_signal)
        symbol = str(signal.get("symbol") or "")
        bar = bars_by_symbol.get(symbol)

        if not bar:
            updated_signals.append(signal)
            continue

        alert, lifecycle = evaluate_signal_against_bar(signal, bar, today=today)
        if alert and lifecycle:
            alerts.append(alert)
            updates.append(lifecycle)
            updated_signals.append(lifecycle.signal)
        else:
            updated_signals.append(signal)

    return alerts, updates, updated_signals


def save_alerts(
    alerts: list[WatcherAlert],
    *,
    alerts_dir: Path | None = None,
    date_str: str | None = None,
) -> tuple[Path, Path]:
    """Persist alerts as dated JSON and latest-alerts.json."""
    target_dir = alerts_dir or ALERTS_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    current_date = date_str or datetime.now(UTC).strftime("%Y-%m-%d")
    dated_path = target_dir / f"{current_date}-alerts.json"
    latest_path = target_dir / "latest-alerts.json"

    existing: list[dict[str, Any]] = []
    if dated_path.exists():
        try:
            existing = json.loads(dated_path.read_text(encoding="utf-8"))
            if not isinstance(existing, list):
                existing = []
        except json.JSONDecodeError:
            existing = []

    payload = existing + [asdict(alert) for alert in alerts]
    dated_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    latest_path.write_text(
        json.dumps([asdict(alert) for alert in alerts], indent=2),
        encoding="utf-8",
    )

    return dated_path, latest_path


def _lifecycle_key(payload: dict[str, Any]) -> tuple[str, str]:
    signal_id = str(payload.get("signal_id") or payload.get("signal", {}).get("signal_id") or "")
    event_type = str(payload.get("event_type") or "")
    return signal_id, event_type


def _read_existing_lifecycle_keys(path: Path) -> set[tuple[str, str]]:
    if not path.exists():
        return set()

    keys: set[tuple[str, str]] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        key = _lifecycle_key(payload)
        if all(key):
            keys.add(key)
    return keys


def append_lifecycle_updates(
    updates: list[SignalLifecycleUpdate],
    *,
    log_path: Path | None = None,
) -> Path:
    """Append lifecycle updates to data/signal_lifecycle.jsonl with deduplication."""
    target = log_path or LIFECYCLE_LOG
    target.parent.mkdir(parents=True, exist_ok=True)
    existing_keys = _read_existing_lifecycle_keys(target)

    with target.open("a", encoding="utf-8") as handle:
        for update in updates:
            payload = asdict(update)
            key = _lifecycle_key(payload)
            if all(key) and key in existing_keys:
                continue
            handle.write(json.dumps(payload) + "\n")
            if all(key):
                existing_keys.add(key)

    return target


def save_updated_signal_file(
    original_signal_file: str | Path,
    updated_signals: list[dict[str, Any]],
) -> Path:
    """Update the signal JSON file with identity and lifecycle status fields."""
    signal_path = Path(original_signal_file)
    payload: dict[str, Any] = {}

    if signal_path.exists():
        try:
            existing_payload = json.loads(signal_path.read_text(encoding="utf-8"))
            payload = existing_payload if isinstance(existing_payload, dict) else {}
        except json.JSONDecodeError:
            payload = {}

    signals_with_identity = [ensure_signal_identity(signal) for signal in updated_signals]
    payload["signals"] = signals_with_identity
    payload["last_watcher_update"] = utc_now_iso()
    payload["actionable_count"] = sum(
        1 for signal in signals_with_identity if signal.get("action") in ACTIONABLE_ACTIONS
    )
    payload["open_count"] = sum(
        1
        for signal in signals_with_identity
        if not is_terminal_signal_status(signal.get("status", SignalStatus.PENDING.value))
    )

    signal_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    latest_path = signal_path.parent / "latest-signals.json"
    latest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    return signal_path


def build_price_bar_from_polygon(symbol: str, bar: dict[str, Any]) -> PriceBar:
    """Convert Polygon aggregate bar to PriceBar."""
    timestamp = bar.get("t")
    if timestamp is not None:
        ts = datetime.fromtimestamp(float(timestamp) / 1000, tz=UTC).isoformat()
    else:
        ts = utc_now_iso()

    explicit_complete = bar.get("is_complete")
    if explicit_complete is None:
        explicit_complete = bar.get("complete")

    if explicit_complete is None:
        is_complete = _is_daily_bar_complete(ts)
        completion_source = "daily_bar_timestamp"
    else:
        is_complete = bool(explicit_complete)
        completion_source = "provider_flag"

    return PriceBar(
        symbol=symbol,
        timestamp=ts,
        open=_safe_float(bar.get("o")),
        high=_safe_float(bar.get("h")),
        low=_safe_float(bar.get("l")),
        close=_safe_float(bar.get("c")),
        is_complete=is_complete,
        completed_at=_completion_timestamp_for_daily_bar(ts),
        completion_source=completion_source,
    )


def latest_bars_to_price_map(
    bars_by_symbol: dict[str, Iterable[dict[str, Any]]],
) -> dict[str, PriceBar]:
    """Build a symbol → latest PriceBar map from Polygon-style bar lists."""
    result: dict[str, PriceBar] = {}

    for symbol, bars in bars_by_symbol.items():
        latest = _latest_bar(bars)
        if latest is None:
            continue
        result[symbol] = build_price_bar_from_polygon(symbol, latest)

    return result
