"""
Scoring Adjustment History.

Persists every expectancy-based score/size adjustment that affected a market
report. This makes adaptive scoring auditable and prevents the learning loop
from becoming a black box.

Integration:
- decision_report.py produces per-symbol expectancy metadata.
- generate_report.py calls append_scoring_adjustments() after report creation.
- GitHub Actions commits data/ so the history survives future runs.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

DEFAULT_ADJUSTMENT_HISTORY = Path("data/scoring_adjustment_history.json")


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _load_history(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            return [item for item in payload if isinstance(item, dict)]
    except json.JSONDecodeError:
        return []
    return []


def _dedupe_key(record: dict[str, Any]) -> tuple[Any, ...]:
    return (
        record.get("run_id"),
        record.get("report_type"),
        record.get("symbol"),
        record.get("profile_key"),
        record.get("base_score"),
        record.get("final_score"),
        record.get("score_delta"),
    )


def build_scoring_adjustment_records(
    *,
    decision_report: dict,
    report_type: str,
    run_id: str | None = None,
    timestamp_utc: str | None = None,
) -> list[dict[str, Any]]:
    """
    Extract auditable scoring adjustment records from decision_report.

    Only adjustments with a non-zero score_delta or non-1.0 size_multiplier are
    persisted. No-op profiles are intentionally skipped to keep the file useful.
    """
    timestamp = timestamp_utc or utc_now_iso()
    resolved_run_id = run_id or f"{report_type}-{timestamp}"
    records: list[dict[str, Any]] = []

    for decision in decision_report.get("decisions", []):
        expectancy = decision.get("expectancy") or {}
        score_delta = expectancy.get("score_delta")
        size_multiplier = expectancy.get("size_multiplier")

        if score_delta in {None, 0, 0.0} and size_multiplier in {None, 1, 1.0}:
            continue

        base_score = decision.get("base_setup_score", decision.get("setup_score"))
        final_score = decision.get("setup_score")
        base_size = decision.get(
            "base_position_size_multiplier",
            decision.get("position_size_multiplier"),
        )
        final_size = decision.get("position_size_multiplier")

        records.append({
            "timestamp_utc": timestamp,
            "run_id": resolved_run_id,
            "report_type": report_type,
            "symbol": decision.get("symbol"),
            "setup_type": decision.get("setup_type"),
            "market_state": decision_report.get("market_state"),
            "entry_type": decision.get("entry_type") or expectancy.get("entry_type_assumption"),
            "profile_key": expectancy.get("profile_key"),
            "source": expectancy.get("source"),
            "sample_size": expectancy.get("sample_size"),
            "win_rate": expectancy.get("win_rate"),
            "expectancy": expectancy.get("expectancy"),
            "base_score": base_score,
            "score_delta": score_delta,
            "final_score": final_score,
            "base_size": base_size,
            "size_multiplier": size_multiplier,
            "final_size": final_size,
            "recommendation": expectancy.get("recommendation"),
            "reason": expectancy.get("reason"),
            "decision": decision.get("decision"),
            "risk_tier": decision.get("risk_tier"),
        })

    return records


def append_scoring_adjustments(
    *,
    decision_report: dict,
    report_type: str,
    output_path: str | Path = DEFAULT_ADJUSTMENT_HISTORY,
    run_id: str | None = None,
    timestamp_utc: str | None = None,
    max_records: int = 5000,
) -> Path:
    """
    Append scoring adjustments to data/scoring_adjustment_history.json.

    The function is deterministic and idempotent for the same run_id/symbol/profile.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    existing = _load_history(path)
    new_records = build_scoring_adjustment_records(
        decision_report=decision_report,
        report_type=report_type,
        run_id=run_id,
        timestamp_utc=timestamp_utc,
    )

    seen = {_dedupe_key(record) for record in existing}
    appended: list[dict[str, Any]] = []
    for record in new_records:
        key = _dedupe_key(record)
        if key in seen:
            continue
        seen.add(key)
        appended.append(record)

    merged = existing + appended
    if max_records > 0:
        merged = merged[-max_records:]

    path.write_text(json.dumps(merged, indent=2), encoding="utf-8")
    return path
