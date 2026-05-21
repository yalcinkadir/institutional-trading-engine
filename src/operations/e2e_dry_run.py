"""End-to-end dry-run validation for go-live readiness.

The validator is intentionally broker-free and external-API-free. It validates
local artifacts and writeability of runtime output locations before live
Decision-Support operation is enabled.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


REQUIRED_SIGNAL_FIELDS = {"signal_id", "symbol", "action"}
REQUIRED_BUY_WATCH_FIELDS = {
    "entry_trigger",
    "stop_loss",
    "target_1",
    "entry_reason",
    "stop_reason",
    "exit_reason",
}


@dataclass(frozen=True)
class DryRunCheck:
    name: str
    passed: bool
    message: str


@dataclass(frozen=True)
class DryRunResult:
    passed: bool
    checks: list[DryRunCheck] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "checks": [asdict(check) for check in self.checks],
        }


def _check(name: str, passed: bool, message: str) -> DryRunCheck:
    return DryRunCheck(name=name, passed=passed, message=message)


def _load_signal_payload(signal_file: Path) -> tuple[Any | None, DryRunCheck]:
    if not signal_file.exists():
        return None, _check("signal_file_exists", False, f"missing signal file: {signal_file}")
    try:
        payload = json.loads(signal_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, _check("signal_file_json", False, f"invalid JSON: {exc}")
    return payload, _check("signal_file_json", True, "signal file is valid JSON")


def _extract_signals(payload: Any) -> tuple[list[dict[str, Any]], DryRunCheck]:
    if isinstance(payload, list):
        raw_signals = payload
    elif isinstance(payload, dict) and isinstance(payload.get("signals"), list):
        raw_signals = payload["signals"]
    else:
        return [], _check("signals_array", False, "payload must be list or object with signals[]")

    signals = [item for item in raw_signals if isinstance(item, dict)]
    if len(signals) != len(raw_signals):
        return signals, _check("signals_array", False, "signals[] contains non-object items")
    return signals, _check("signals_array", True, f"loaded {len(signals)} signal records")


def _validate_signal_identity(signals: list[dict[str, Any]]) -> DryRunCheck:
    missing: list[str] = []
    for index, signal in enumerate(signals):
        absent = sorted(field for field in REQUIRED_SIGNAL_FIELDS if not signal.get(field))
        if absent:
            missing.append(f"#{index}:{','.join(absent)}")
    if missing:
        return _check("signal_identity_fields", False, "; ".join(missing))
    return _check("signal_identity_fields", True, "all signals have signal_id, symbol and action")


def _validate_buy_watch_trade_plans(signals: list[dict[str, Any]]) -> DryRunCheck:
    incomplete: list[str] = []
    for signal in signals:
        if signal.get("action") != "BUY_WATCH":
            continue
        symbol = str(signal.get("symbol") or "unknown")
        absent = sorted(field for field in REQUIRED_BUY_WATCH_FIELDS if signal.get(field) in (None, ""))
        if absent:
            incomplete.append(f"{symbol}:{','.join(absent)}")
    if incomplete:
        return _check("buy_watch_trade_plans", False, "; ".join(incomplete))
    return _check("buy_watch_trade_plans", True, "all BUY_WATCH signals have executable trade-plan fields")


def _validate_writable_path(path: Path, *, name: str) -> DryRunCheck:
    try:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / ".dry-run-write-test"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return _check(name, True, f"writable: {path}")
    except Exception as exc:
        return _check(name, False, f"not writable: {path}: {type(exc).__name__}: {exc}")


def run_e2e_dry_run_validation(
    *,
    signal_file: Path = Path("reports/signals/latest-signals.json"),
    alerts_dir: Path = Path("reports/alerts"),
    lifecycle_dir: Path = Path("data"),
) -> DryRunResult:
    """Validate local end-to-end readiness without external side effects."""
    checks: list[DryRunCheck] = []

    payload, load_check = _load_signal_payload(signal_file)
    checks.append(load_check)
    signals: list[dict[str, Any]] = []

    if payload is not None:
        signals, signals_check = _extract_signals(payload)
        checks.append(signals_check)
        if signals_check.passed:
            checks.append(_validate_signal_identity(signals))
            checks.append(_validate_buy_watch_trade_plans(signals))

    checks.append(_validate_writable_path(alerts_dir, name="alerts_dir_writable"))
    checks.append(_validate_writable_path(lifecycle_dir, name="lifecycle_dir_writable"))

    return DryRunResult(passed=all(check.passed for check in checks), checks=checks)
