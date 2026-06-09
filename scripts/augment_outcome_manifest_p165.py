#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

EVALUATED_CLASSIFICATIONS = {"WIN", "LOSS", "NEUTRAL"}
EVALUABLE_STATUSES = {"TRIGGERED", "TARGET_1_HIT", "TARGET_2_HIT", "STOP_HIT"}
BLOCKED_STATUSES = {"BLOCKED_MISSING_INPUTS"}
EMPTY_STATUSES = {"NO_ELIGIBLE_SIGNALS"}


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _outcome_files(outcomes_dir: Path) -> list[Path]:
    return sorted(
        path for path in outcomes_dir.glob("*-outcomes.json")
        if path.name != "latest-outcomes.json"
    )


def _count_outcomes(outcomes_dir: Path) -> dict[str, Any]:
    input_count = 0
    evaluable_count = 0
    evaluated_count = 0
    skipped_count = 0
    skip_reasons: set[str] = set()

    for path in _outcome_files(outcomes_dir):
        payload = _load_json(path)
        if not isinstance(payload, list):
            skipped_count += 1
            skip_reasons.add("invalid_outcome_payload")
            continue

        for outcome in payload:
            input_count += 1
            status = str(outcome.get("lifecycle_status") or outcome.get("classification") or "UNKNOWN").upper()
            classification = str(outcome.get("classification") or "UNKNOWN").upper()

            if status in EVALUABLE_STATUSES:
                evaluable_count += 1
            if classification in EVALUATED_CLASSIFICATIONS:
                evaluated_count += 1
            else:
                skipped_count += 1
                if status in {"PENDING", "UNTRIGGERED", "EXPIRED"}:
                    skip_reasons.add(status.lower())
                else:
                    skip_reasons.add("not_evaluated")

    return {
        "total_input_signals": input_count,
        "evaluable_signal_count": evaluable_count,
        "evaluated_outcome_count": evaluated_count,
        "skipped_count": skipped_count,
        "skip_reasons": sorted(skip_reasons),
    }


def augment_manifest(outcomes_dir: Path) -> dict[str, Any]:
    manifest_path = outcomes_dir / "outcome-run-manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"missing outcome manifest: {manifest_path}")

    manifest = _load_json(manifest_path)
    if not isinstance(manifest, dict):
        raise ValueError("outcome manifest must be a JSON object")

    status = str(manifest.get("run_status") or "UNKNOWN")
    metrics = _count_outcomes(outcomes_dir)

    if status in BLOCKED_STATUSES | EMPTY_STATUSES:
        manifest.setdefault("total_input_signals", 0)
        manifest["evaluable_signal_count"] = 0
        manifest["evaluated_outcome_count"] = 0
        manifest["skipped_count"] = 0
    else:
        manifest["total_input_signals"] = max(int(manifest.get("total_input_signals") or 0), metrics["total_input_signals"])
        manifest["evaluable_signal_count"] = metrics["evaluable_signal_count"]
        manifest["evaluated_outcome_count"] = metrics["evaluated_outcome_count"]
        manifest["skipped_count"] = metrics["skipped_count"]

    existing_reasons = set(manifest.get("skip_reasons") or [])
    manifest["skip_reasons"] = sorted(existing_reasons | set(metrics["skip_reasons"]))
    manifest["manifest_contract_version"] = "p165.v1"
    manifest["augmented_at_utc"] = datetime.now(UTC).isoformat()
    manifest["live_trading_authorized"] = False
    manifest["broker_execution_mode"] = "paper_only"

    artifact_date = str(manifest.get("artifact_date") or datetime.now(UTC).date().isoformat())
    manifest["artifact_date"] = artifact_date

    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    dated_path = outcomes_dir / f"{artifact_date}-outcome-run.json"
    dated_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Augment P165 outcome run manifest with evidence counters.")
    parser.add_argument("--outcomes-dir", type=Path, default=Path("reports/outcomes"))
    args = parser.parse_args()

    manifest = augment_manifest(args.outcomes_dir)
    print(f"P165 manifest status={manifest.get('run_status')} evaluated={manifest.get('evaluated_outcome_count')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
