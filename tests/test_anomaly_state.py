from __future__ import annotations

import json
from pathlib import Path

from src.runtime.anomaly_state import AnomalyStateStore


def test_missing_anomaly_state_returns_auditable_zero_count(tmp_path: Path) -> None:
    state = AnomalyStateStore(tmp_path / "missing.json").load()

    assert state.severe_anomaly_count == 0
    assert state.anomaly_count == 0
    assert state.source == "anomaly_state_missing"
    assert state.warnings


def test_loads_persistent_severe_anomaly_count(tmp_path: Path) -> None:
    path = tmp_path / "anomaly_state.json"
    path.write_text(
        json.dumps(
            {
                "severe_anomaly_count": 5,
                "anomaly_count": 7,
                "classification": "Extreme Instability",
                "updated_at": "2026-05-31T18:00:00+00:00",
            }
        ),
        encoding="utf-8",
    )

    state = AnomalyStateStore(path).load()

    assert state.severe_anomaly_count == 5
    assert state.anomaly_count == 7
    assert state.classification == "Extreme Instability"
    assert state.updated_at == "2026-05-31T18:00:00+00:00"
    assert state.source == "anomaly_state_json"
    assert state.warnings == []


def test_supports_legacy_severe_count_alias(tmp_path: Path) -> None:
    path = tmp_path / "anomaly_state.json"
    path.write_text(json.dumps({"severe_count": 3}), encoding="utf-8")

    state = AnomalyStateStore(path).load()

    assert state.severe_anomaly_count == 3
    assert state.classification == "Elevated Instability"


def test_invalid_anomaly_state_is_auditable_and_safe(tmp_path: Path) -> None:
    path = tmp_path / "anomaly_state.json"
    path.write_text("not-json", encoding="utf-8")

    state = AnomalyStateStore(path).load()

    assert state.severe_anomaly_count == 0
    assert state.source == "anomaly_state_invalid"
    assert state.warnings


def test_negative_and_non_numeric_counts_are_sanitized(tmp_path: Path) -> None:
    path = tmp_path / "anomaly_state.json"
    path.write_text(
        json.dumps({"severe_anomaly_count": -2, "anomaly_count": "bad"}),
        encoding="utf-8",
    )

    state = AnomalyStateStore(path).load()

    assert state.severe_anomaly_count == 0
    assert state.anomaly_count == 0
    assert len(state.warnings) == 2