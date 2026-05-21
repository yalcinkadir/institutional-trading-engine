"""Deterministic signal identity helpers.

Signal ids are generated from stable signal fields so reports, watcher alerts
and lifecycle events can be joined across time.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

_SIGNAL_ID_FIELDS = (
    "symbol",
    "action",
    "signal_date",
    "generated_at",
    "entry_trigger",
    "stop_loss",
    "target_1",
    "target_2",
    "valid_until",
)


def signal_date_from_payload(signal: dict[str, Any]) -> str:
    generated_at = str(signal.get("generated_at") or "")
    if generated_at:
        return generated_at[:10]
    return str(signal.get("signal_date") or signal.get("date") or "unknown")


def build_signal_id(signal: dict[str, Any]) -> str:
    """Build a deterministic signal id from stable signal fields."""

    normalized = dict(signal)
    normalized.setdefault("signal_date", signal_date_from_payload(signal))

    identity_payload = {
        field: normalized.get(field)
        for field in _SIGNAL_ID_FIELDS
    }
    raw = json.dumps(identity_payload, sort_keys=True, separators=(",", ":"), default=str)
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
    symbol = str(signal.get("symbol") or "UNKNOWN").upper().replace("/", "_")
    return f"sig_{symbol}_{digest}"


def ensure_signal_identity(signal: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of a signal with a stable `signal_id` field."""

    result = dict(signal)
    existing = result.get("signal_id")
    if existing:
        result["signal_id"] = str(existing)
        return result

    result["signal_id"] = build_signal_id(result)
    return result
