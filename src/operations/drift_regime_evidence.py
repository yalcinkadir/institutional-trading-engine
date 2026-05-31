"""
Drift and Regime-Change Evidence.

PSR4 adds a public-safe daily evidence artifact for observation drift and
market-regime changes.

The goal is not to predict markets or prove edge. The goal is to document:
- signal / score / decision drift
- cumulative drift
- regime transitions
- whether the observation day is PASS / WARN / FAIL

This module is deterministic and side-effect free except for explicit JSON
write helpers.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "PSR4_DRIFT_REGIME_EVIDENCE_V1"
DEFAULT_DRIFT_REGIME_DIR = Path("reports/evidence/drift_regime")

STABLE_REGIME_TRANSITIONS = {
    ("BULL", "BULL"),
    ("BEAR", "BEAR"),
    ("NEUTRAL", "NEUTRAL"),
    ("RISK_ON", "RISK_ON"),
    ("RISK_OFF", "RISK_OFF"),
}

WARN_REGIME_TRANSITIONS = {
    ("BULL", "NEUTRAL"),
    ("NEUTRAL", "BULL"),
    ("BEAR", "NEUTRAL"),
    ("NEUTRAL", "BEAR"),
    ("RISK_ON", "NEUTRAL"),
    ("NEUTRAL", "RISK_ON"),
    ("RISK_OFF", "NEUTRAL"),
    ("NEUTRAL", "RISK_OFF"),
}

FAIL_REGIME_TRANSITIONS = {
    ("BULL", "BEAR"),
    ("BEAR", "BULL"),
    ("RISK_ON", "RISK_OFF"),
    ("RISK_OFF", "RISK_ON"),
}


@dataclass(frozen=True)
class DriftMetric:
    """One drift metric."""

    name: str
    observed_value: float
    expected_value: float
    drift_value: float
    abs_drift_value: float
    warn_threshold: float
    fail_threshold: float
    status: str


@dataclass(frozen=True)
class RegimeChangeEvidence:
    """One regime transition evidence record."""

    previous_regime: str
    current_regime: str
    transition: str
    status: str
    warnings: list[str]


@dataclass(frozen=True)
class DriftRegimeEvidence:
    """Daily drift and regime-change evidence summary."""

    schema_version: str
    trading_date: str
    created_at: str
    status: str
    drift_metrics: list[DriftMetric]
    regime_change: RegimeChangeEvidence
    cumulative_drift_value: float
    cumulative_drift_warn_threshold: float
    cumulative_drift_fail_threshold: float
    cumulative_drift_status: str
    notes: list[str]
    live_trading_authorized: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["drift_metrics"] = [asdict(metric) for metric in self.drift_metrics]
        payload["regime_change"] = asdict(self.regime_change)
        return payload


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _normalize_regime(value: Any) -> str:
    if value is None:
        return "UNKNOWN"
    normalized = str(value).strip().upper()
    return normalized or "UNKNOWN"


def _status_from_value(
    value: float,
    *,
    warn_threshold: float,
    fail_threshold: float,
) -> str:
    absolute = abs(value)

    if absolute > fail_threshold:
        return "FAIL"
    if absolute > warn_threshold:
        return "WARN"
    return "PASS"


def build_drift_metric(
    *,
    name: str,
    observed_value: float,
    expected_value: float,
    warn_threshold: float = 0.05,
    fail_threshold: float = 0.15,
) -> DriftMetric:
    """Build one drift metric from observed and expected values."""
    drift_value = float(observed_value) - float(expected_value)
    abs_drift_value = abs(drift_value)

    return DriftMetric(
        name=str(name),
        observed_value=float(observed_value),
        expected_value=float(expected_value),
        drift_value=drift_value,
        abs_drift_value=abs_drift_value,
        warn_threshold=float(warn_threshold),
        fail_threshold=float(fail_threshold),
        status=_status_from_value(
            drift_value,
            warn_threshold=float(warn_threshold),
            fail_threshold=float(fail_threshold),
        ),
    )


def build_regime_change_evidence(
    *,
    previous_regime: str | None,
    current_regime: str | None,
) -> RegimeChangeEvidence:
    """Build one regime-change evidence record."""
    previous = _normalize_regime(previous_regime)
    current = _normalize_regime(current_regime)
    transition_tuple = (previous, current)
    transition = f"{previous}->{current}"
    warnings: list[str] = []

    if "UNKNOWN" in transition_tuple:
        warnings.append("regime_unknown")
        status = "WARN"
    elif transition_tuple in FAIL_REGIME_TRANSITIONS:
        warnings.append("major_regime_transition")
        status = "FAIL"
    elif transition_tuple in WARN_REGIME_TRANSITIONS:
        warnings.append("minor_regime_transition")
        status = "WARN"
    elif transition_tuple in STABLE_REGIME_TRANSITIONS:
        status = "PASS"
    elif previous != current:
        warnings.append("unclassified_regime_transition")
        status = "WARN"
    else:
        status = "PASS"

    return RegimeChangeEvidence(
        previous_regime=previous,
        current_regime=current,
        transition=transition,
        status=status,
        warnings=warnings,
    )


def build_drift_regime_evidence(
    *,
    trading_date: str | date,
    drift_metrics: Iterable[DriftMetric],
    previous_regime: str | None,
    current_regime: str | None,
    cumulative_drift_value: float = 0.0,
    cumulative_drift_warn_threshold: float = 0.10,
    cumulative_drift_fail_threshold: float = 0.30,
    created_at: str | None = None,
    notes: Iterable[str] = (),
) -> DriftRegimeEvidence:
    """Build daily drift/regime evidence."""
    trading_date_str = (
        trading_date.isoformat() if isinstance(trading_date, date) else str(trading_date)
    )

    metrics = list(drift_metrics)
    regime_change = build_regime_change_evidence(
        previous_regime=previous_regime,
        current_regime=current_regime,
    )

    cumulative_status = _status_from_value(
        float(cumulative_drift_value),
        warn_threshold=float(cumulative_drift_warn_threshold),
        fail_threshold=float(cumulative_drift_fail_threshold),
    )

    statuses = [metric.status for metric in metrics]
    statuses.append(regime_change.status)
    statuses.append(cumulative_status)

    if "FAIL" in statuses:
        status = "FAIL"
    elif "WARN" in statuses:
        status = "WARN"
    else:
        status = "PASS"

    return DriftRegimeEvidence(
        schema_version=SCHEMA_VERSION,
        trading_date=trading_date_str,
        created_at=created_at or utc_now_iso(),
        status=status,
        drift_metrics=metrics,
        regime_change=regime_change,
        cumulative_drift_value=float(cumulative_drift_value),
        cumulative_drift_warn_threshold=float(cumulative_drift_warn_threshold),
        cumulative_drift_fail_threshold=float(cumulative_drift_fail_threshold),
        cumulative_drift_status=cumulative_status,
        notes=list(notes),
        live_trading_authorized=False,
    )


def write_drift_regime_evidence(
    evidence: DriftRegimeEvidence,
    *,
    output_dir: str | Path = DEFAULT_DRIFT_REGIME_DIR,
) -> Path:
    """Write daily drift/regime evidence JSON."""
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    output_path = target_dir / f"{evidence.trading_date}-drift-regime-evidence.json"
    latest_path = target_dir / "latest-drift-regime-evidence.json"

    payload = json.dumps(evidence.to_dict(), indent=2, sort_keys=True)
    output_path.write_text(payload, encoding="utf-8")
    latest_path.write_text(payload, encoding="utf-8")

    return output_path


def load_drift_regime_evidence(path: str | Path) -> DriftRegimeEvidence:
    """Load daily drift/regime evidence JSON."""
    payload = json.loads(Path(path).read_text(encoding="utf-8"))

    metrics = [
        DriftMetric(
            name=str(item["name"]),
            observed_value=float(item["observed_value"]),
            expected_value=float(item["expected_value"]),
            drift_value=float(item["drift_value"]),
            abs_drift_value=float(item["abs_drift_value"]),
            warn_threshold=float(item["warn_threshold"]),
            fail_threshold=float(item["fail_threshold"]),
            status=str(item["status"]),
        )
        for item in payload.get("drift_metrics", [])
    ]

    regime_payload = payload["regime_change"]
    regime_change = RegimeChangeEvidence(
        previous_regime=str(regime_payload["previous_regime"]),
        current_regime=str(regime_payload["current_regime"]),
        transition=str(regime_payload["transition"]),
        status=str(regime_payload["status"]),
        warnings=[str(value) for value in regime_payload.get("warnings", [])],
    )

    return DriftRegimeEvidence(
        schema_version=str(payload["schema_version"]),
        trading_date=str(payload["trading_date"]),
        created_at=str(payload["created_at"]),
        status=str(payload["status"]),
        drift_metrics=metrics,
        regime_change=regime_change,
        cumulative_drift_value=float(payload["cumulative_drift_value"]),
        cumulative_drift_warn_threshold=float(payload["cumulative_drift_warn_threshold"]),
        cumulative_drift_fail_threshold=float(payload["cumulative_drift_fail_threshold"]),
        cumulative_drift_status=str(payload["cumulative_drift_status"]),
        notes=[str(value) for value in payload.get("notes", [])],
        live_trading_authorized=bool(payload.get("live_trading_authorized", False)),
    )


def validate_drift_regime_evidence(evidence: DriftRegimeEvidence) -> dict[str, Any]:
    """Validate daily drift/regime evidence consistency."""
    errors: list[str] = []

    if evidence.schema_version != SCHEMA_VERSION:
        errors.append("invalid_schema_version")

    if evidence.live_trading_authorized:
        errors.append("live_trading_authorized_must_be_false")

    for metric in evidence.drift_metrics:
        expected_drift = metric.observed_value - metric.expected_value
        if round(metric.drift_value, 12) != round(expected_drift, 12):
            errors.append(f"metric_drift_mismatch:{metric.name}")

        expected_status = _status_from_value(
            metric.drift_value,
            warn_threshold=metric.warn_threshold,
            fail_threshold=metric.fail_threshold,
        )
        if metric.status != expected_status:
            errors.append(f"metric_status_mismatch:{metric.name}")

    expected_regime = build_regime_change_evidence(
        previous_regime=evidence.regime_change.previous_regime,
        current_regime=evidence.regime_change.current_regime,
    )
    if evidence.regime_change.status != expected_regime.status:
        errors.append("regime_status_mismatch")

    expected_cumulative_status = _status_from_value(
        evidence.cumulative_drift_value,
        warn_threshold=evidence.cumulative_drift_warn_threshold,
        fail_threshold=evidence.cumulative_drift_fail_threshold,
    )
    if evidence.cumulative_drift_status != expected_cumulative_status:
        errors.append("cumulative_drift_status_mismatch")

    statuses = [metric.status for metric in evidence.drift_metrics]
    statuses.append(evidence.regime_change.status)
    statuses.append(evidence.cumulative_drift_status)

    expected_status = "FAIL" if "FAIL" in statuses else "WARN" if "WARN" in statuses else "PASS"
    if evidence.status != expected_status:
        errors.append("status_mismatch")

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
    }