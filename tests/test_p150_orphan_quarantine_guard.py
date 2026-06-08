from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.validate_p150_orphan_quarantine import validate_manifest
from tools.module_reachability import analyze

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "docs" / "architecture" / "p150_orphan_quarantine_manifest.json"


def test_p150_manifest_contains_only_current_true_orphans() -> None:
    errors = validate_manifest(MANIFEST, REPO_ROOT)
    assert errors == []


def test_p150_manifest_has_no_test_or_dispatch_only_modules() -> None:
    reachability = analyze(REPO_ROOT)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    quarantined = {entry["path"] for entry in manifest["actions"]}

    assert quarantined
    assert quarantined <= set(reachability["true_orphans"])
    assert quarantined.isdisjoint(set(reachability["test_or_dispatch_only"]))
    assert quarantined.isdisjoint(set(reachability["scheduled_production_modules"]))


def test_p150_guard_rejects_test_or_dispatch_only_module(tmp_path: Path) -> None:
    reachability = analyze(REPO_ROOT)
    candidates = reachability["test_or_dispatch_only"]
    if not candidates:
        pytest.skip("no test/dispatch-only module available in current baseline")

    manifest = {
        "actions": [
            {
                "path": candidates[0],
                "classification": "quarantine_candidate",
                "decision": "invalid_test_only_candidate",
            }
        ]
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    errors = validate_manifest(manifest_path, REPO_ROOT)
    assert any("test/dispatch-only" in error for error in errors)


def test_p150_guard_rejects_scheduled_production_module(tmp_path: Path) -> None:
    reachability = analyze(REPO_ROOT)
    candidates = reachability["scheduled_production_modules"]
    assert candidates, "scheduled production baseline must not be empty"

    manifest = {
        "actions": [
            {
                "path": candidates[0],
                "classification": "quarantine_candidate",
                "decision": "invalid_scheduled_candidate",
            }
        ]
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    errors = validate_manifest(manifest_path, REPO_ROOT)
    assert any("scheduled-production" in error for error in errors)
