from __future__ import annotations

import json
from pathlib import Path
from typing import Any

OUTCOME_STATUS_NOT_LINKED = "NOT_LINKED"
OUTCOME_STATUS_MISSING = "BLOCKED_MISSING_OUTCOME_MANIFEST"


def build_outcome_run_status_link(manifest_path: str | Path) -> dict[str, Any]:
    """Build a compact Paper Observation reference to the outcome run manifest."""

    path = Path(manifest_path)
    if not path.exists():
        return {
            "outcome_run_status": OUTCOME_STATUS_MISSING,
            "outcome_run_manifest_path": str(path),
            "outcome_manifest_available": False,
        }

    payload = json.loads(path.read_text(encoding="utf-8"))
    return {
        "outcome_run_status": str(payload.get("run_status") or OUTCOME_STATUS_NOT_LINKED),
        "outcome_run_manifest_path": str(path),
        "outcome_manifest_available": True,
        "evaluable_signal_count": int(payload.get("evaluable_signal_count") or 0),
        "evaluated_outcome_count": int(payload.get("evaluated_outcome_count") or 0),
        "skipped_count": int(payload.get("skipped_count") or 0),
        "skip_reasons": list(payload.get("skip_reasons") or []),
    }
