from __future__ import annotations

import json
from pathlib import Path


ALLOWLIST_PATH = Path("docs/operations/broad_exception_allowlist.json")
REQUIRED_ACTIVE_STAGES = {
    ("src/outcome_tracking.py", "outcome_tracking.read_decision_records"),
    ("src/reporting/market_regime.py", "reporting.market_regime.PolygonClient"),
    ("src/reporting/market_regime.py", "reporting.market_regime.breadth"),
    ("src/runtime/runtime_loop.py", "runtime_loop.cycle_provider"),
}


def _allowlist() -> dict:
    return json.loads(ALLOWLIST_PATH.read_text(encoding="utf-8"))


def test_198_broad_exception_allowlist_has_required_schema() -> None:
    payload = _allowlist()

    assert payload["schema"] == "broad_exception_allowlist.v1"
    assert payload["issue"] == 198
    assert set(payload["required_fields"]) == {"path", "stage", "behavior", "component", "rationale"}
    assert "fail_closed_raise" in payload["allowed_behaviors"]
    assert "degraded_continue" in payload["allowed_behaviors"]


def test_198_active_broad_exception_stages_are_allowlisted() -> None:
    payload = _allowlist()
    entries = payload["entries"]
    observed = {(entry["path"], entry["stage"]) for entry in entries}

    assert REQUIRED_ACTIVE_STAGES <= observed


def test_198_allowlist_entries_have_rationale_and_allowed_behavior() -> None:
    payload = _allowlist()
    allowed_behaviors = set(payload["allowed_behaviors"])

    for entry in payload["entries"]:
        assert entry["path"].endswith(".py")
        assert entry["stage"]
        assert entry["component"]
        assert entry["rationale"]
        assert entry["behavior"] in allowed_behaviors
