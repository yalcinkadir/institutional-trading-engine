"""Persistent anomaly state for runtime governance.

The live runtime must not depend only on process-local cache for the severe
anomaly count. GitHub Actions and other batch runtimes start a fresh Python
process for every run, so in-memory state is not a reliable governance source.

This module provides a small JSON-backed store for the current anomaly state.
Missing or malformed files do not crash the runtime; they produce a conservative
zero-count state with explicit warnings so the audit payload remains honest.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


DEFAULT_ANOMALY_STATE_PATH = Path("data/anomaly_state.json")


@dataclass(frozen=True)
class AnomalyState:
    """Governance-ready anomaly state loaded from a persistent source."""

    severe_anomaly_count: int
    anomaly_count: int = 0
    classification: str = "Stable"
    updated_at: str | None = None
    source: str = "anomaly_state_json"
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "severe_anomaly_count": self.severe_anomaly_count,
            "anomaly_count": self.anomaly_count,
            "classification": self.classification,
            "updated_at": self.updated_at,
            "source": self.source,
            "warnings": list(self.warnings),
        }


class AnomalyStateStore:
    """JSON-backed anomaly state reader for live governance."""

    def __init__(self, path: Path | str = DEFAULT_ANOMALY_STATE_PATH) -> None:
        self.path = Path(path)

    def load(self) -> AnomalyState:
        """Load persistent anomaly state.

        Supported input fields:
        - severe_anomaly_count: canonical governance count
        - severe_count: compatibility alias from anomaly_memory
        - anomaly_count: total anomaly count for audit context
        - classification: human-readable environment classification
        - updated_at: optional ISO timestamp
        """

        if not self.path.exists():
            return AnomalyState(
                severe_anomaly_count=0,
                anomaly_count=0,
                classification="Unknown",
                source="anomaly_state_missing",
                warnings=[
                    f"Persistent anomaly state file not found: {self.path}",
                    "Using severe_anomaly_count=0; governance anomaly kill switch requires a persistent state file for live evidence.",
                ],
            )

        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return AnomalyState(
                severe_anomaly_count=0,
                anomaly_count=0,
                classification="Invalid",
                source="anomaly_state_invalid",
                warnings=[
                    f"Persistent anomaly state file could not be read: {self.path}",
                    f"{type(exc).__name__}: {exc}",
                    "Using severe_anomaly_count=0 because anomaly state is invalid.",
                ],
            )

        if not isinstance(raw, dict):
            return AnomalyState(
                severe_anomaly_count=0,
                anomaly_count=0,
                classification="Invalid",
                source="anomaly_state_invalid",
                warnings=[
                    f"Persistent anomaly state file must contain a JSON object: {self.path}",
                    "Using severe_anomaly_count=0 because anomaly state is invalid.",
                ],
            )

        warnings: list[str] = []
        severe_value = raw.get("severe_anomaly_count", raw.get("severe_count", 0))
        anomaly_value = raw.get("anomaly_count", raw.get("total_anomaly_count", 0))

        severe_count = _coerce_non_negative_int(
            severe_value,
            field_name="severe_anomaly_count",
            warnings=warnings,
        )
        anomaly_count = _coerce_non_negative_int(
            anomaly_value,
            field_name="anomaly_count",
            warnings=warnings,
        )
        classification = raw.get("classification")
        if not isinstance(classification, str) or not classification.strip():
            classification = _classify_anomaly_environment(severe_count)

        updated_at = raw.get("updated_at")
        if updated_at is not None and not isinstance(updated_at, str):
            warnings.append("updated_at must be a string when supplied; ignoring invalid value.")
            updated_at = None

        return AnomalyState(
            severe_anomaly_count=severe_count,
            anomaly_count=anomaly_count,
            classification=classification,
            updated_at=updated_at,
            source="anomaly_state_json",
            warnings=warnings,
        )


def _coerce_non_negative_int(value: Any, *, field_name: str, warnings: list[str]) -> int:
    try:
        parsed = int(float(value))
    except (TypeError, ValueError):
        warnings.append(f"{field_name} could not be parsed as a number; using 0.")
        return 0
    if parsed < 0:
        warnings.append(f"{field_name} was negative; clamped to 0.")
        return 0
    return parsed


def _classify_anomaly_environment(severe_count: int) -> str:
    if severe_count >= 5:
        return "Extreme Instability"
    if severe_count >= 3:
        return "Elevated Instability"
    if severe_count >= 1:
        return "Watchlist Environment"
    return "Stable"