#!/usr/bin/env python3
"""Validate the P150 true-orphan quarantine manifest.

This guard intentionally does not delete source files. It validates that the
quarantine list is scoped to paths that the static reachability report currently
classifies as true orphans. Test/dispatch-only modules are explicitly excluded.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from tools.module_reachability import analyze

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = REPO_ROOT / "docs" / "architecture" / "p150_orphan_quarantine_manifest.json"


def _load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_manifest(manifest_path: Path = DEFAULT_MANIFEST, root: Path = REPO_ROOT) -> list[str]:
    manifest = _load_manifest(manifest_path)
    result = analyze(root)
    true_orphans = set(result["true_orphans"])
    test_or_dispatch_only = set(result["test_or_dispatch_only"])
    scheduled = set(result["scheduled_production_modules"])

    errors: list[str] = []
    actions = manifest.get("actions", [])
    if not actions:
        errors.append("manifest has no actions")
        return errors

    seen: set[str] = set()
    for index, action in enumerate(actions, start=1):
        path = str(action.get("path", "")).strip()
        classification = action.get("classification")
        decision = action.get("decision")
        if not path:
            errors.append(f"action #{index}: missing path")
            continue
        if path in seen:
            errors.append(f"{path}: duplicate manifest action")
        seen.add(path)
        if classification != "quarantine_candidate":
            errors.append(f"{path}: classification must be quarantine_candidate")
        if not decision:
            errors.append(f"{path}: decision is required")
        if path not in true_orphans:
            errors.append(f"{path}: not currently classified as a true orphan")
        if path in test_or_dispatch_only:
            errors.append(f"{path}: test/dispatch-only module must not be quarantined in P150")
        if path in scheduled:
            errors.append(f"{path}: scheduled-production module must not be quarantined")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--root", default=str(REPO_ROOT))
    args = parser.parse_args(argv)

    errors = validate_manifest(Path(args.manifest), Path(args.root).resolve())
    if errors:
        print("P150 orphan quarantine validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("P150 orphan quarantine manifest is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
