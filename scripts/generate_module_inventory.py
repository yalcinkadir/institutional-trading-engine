#!/usr/bin/env python3
"""Generate and validate an ARCH106 module inventory from the current checkout.

This script intentionally scans the repository at runtime instead of relying on a
manually maintained list. It is a tooling entry point, not a production trading
module.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CLASSIFICATION_PATH = REPO_ROOT / "docs" / "architecture" / "module_classification.json"
DEFAULT_OUTPUT_PATH = REPO_ROOT / "docs" / "architecture" / "module_inventory.generated.json"
IGNORED_PARTS = {"__pycache__"}
IGNORED_MODULES = {
    # #188 evidence-governance helper. It is intentionally not a trading runtime
    # module and is guarded separately by tests/test_evidence_quality_gate_188.py.
    "src/evidence_quality_gate.py",
    # #191 compatibility shim only. The implementation lives in the ARCH106-
    # classified report/signal runtime module src/signals/scanner_metrics_pipeline.py.
    "src/validation/datafeed_liveness.py",
    # #198 compatibility shim only. The implementation lives in the already
    # existing structured logging helper src/structured_logging.py.
    "src/exception_audit.py",
}


def _repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def _classification_source_label(classification_path: Path) -> str:
    try:
        return _repo_relative(classification_path)
    except ValueError:
        return classification_path.as_posix()


def discover_src_modules(repo_root: Path = REPO_ROOT) -> list[str]:
    src_dir = repo_root / "src"
    if not src_dir.exists():
        return []
    modules: list[str] = []
    for path in src_dir.rglob("*.py"):
        if any(part in IGNORED_PARTS for part in path.parts):
            continue
        relative = path.relative_to(repo_root).as_posix()
        if relative in IGNORED_MODULES:
            continue
        modules.append(relative)
    return sorted(modules)


def load_classification(path: Path = DEFAULT_CLASSIFICATION_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_inventory(
    *,
    repo_root: Path = REPO_ROOT,
    classification_path: Path = DEFAULT_CLASSIFICATION_PATH,
) -> dict[str, Any]:
    classification = load_classification(classification_path)
    classified_modules = classification.get("classified_modules", {})
    allowed_classifications = set(classification.get("allowed_classifications", []))

    modules = []
    counters: dict[str, int] = {
        "total_src_modules": 0,
        "classified_modules": 0,
        "unclassified_legacy_modules": 0,
    }

    for module_path in discover_src_modules(repo_root):
        record = classified_modules.get(module_path)
        if record:
            module_classification = record.get("classification")
            if module_classification not in allowed_classifications:
                raise ValueError(f"Invalid classification for {module_path}: {module_classification}")
            status = "classified"
            counters["classified_modules"] += 1
            counters[module_classification] = counters.get(module_classification, 0) + 1
        else:
            module_classification = "unclassified_legacy"
            status = "unclassified_legacy"
            counters["unclassified_legacy_modules"] += 1
            counters[module_classification] = counters.get(module_classification, 0) + 1

        modules.append(
            {
                "path": module_path,
                "status": status,
                "classification": module_classification,
                "runtime_entrypoint": record.get("runtime_entrypoint") if record else None,
                "runtime_execution_proof": record.get("runtime_execution_proof") if record else None,
                "notes": record.get("notes") if record else "Legacy module not yet classified in ARCH106 Step 3.",
            }
        )
        counters["total_src_modules"] += 1

    return {
        "schema_version": 1,
        "source": "scripts/generate_module_inventory.py",
        "classification_source": _classification_source_label(classification_path),
        "grandfather_existing_modules": bool(classification.get("grandfather_existing_modules")),
        "counters": counters,
        "modules": modules,
    }


def render_inventory(inventory: dict[str, Any]) -> str:
    return json.dumps(inventory, indent=2, sort_keys=True) + "\n"


def _records_by_path(inventory: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {record["path"]: record for record in inventory.get("modules", [])}


def _recompute_counters(modules: list[dict[str, Any]]) -> dict[str, int]:
    counters: dict[str, int] = {
        "total_src_modules": 0,
        "classified_modules": 0,
        "unclassified_legacy_modules": 0,
    }
    for record in modules:
        classification = str(record.get("classification"))
        counters["total_src_modules"] += 1
        if record.get("status") == "classified":
            counters["classified_modules"] += 1
        if classification == "unclassified_legacy":
            counters["unclassified_legacy_modules"] += 1
        counters[classification] = counters.get(classification, 0) + 1
    return counters


def _normalize_inventory_for_ignored_modules(inventory: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(inventory)
    modules = [
        record
        for record in inventory.get("modules", [])
        if str(record.get("path")) not in IGNORED_MODULES
    ]
    normalized["modules"] = modules
    normalized["counters"] = _recompute_counters(modules)
    return normalized


def inventory_diff(expected: dict[str, Any], actual: dict[str, Any]) -> dict[str, Any]:
    expected_records = _records_by_path(expected)
    actual_records = _records_by_path(actual)
    expected_paths = set(expected_records)
    actual_paths = set(actual_records)

    added = sorted(expected_paths - actual_paths)
    removed = sorted(actual_paths - expected_paths)
    changed: list[dict[str, Any]] = []

    for path in sorted(expected_paths & actual_paths):
        expected_record = expected_records[path]
        actual_record = actual_records[path]
        changes: dict[str, Any] = {}
        for key in ["classification", "status", "runtime_entrypoint", "runtime_execution_proof"]:
            if expected_record.get(key) != actual_record.get(key):
                changes[key] = {
                    "expected": expected_record.get(key),
                    "actual": actual_record.get(key),
                }
        if changes:
            changed.append({"path": path, "changes": changes})

    counter_changes = {
        key: {"expected": expected["counters"].get(key), "actual": actual["counters"].get(key)}
        for key in sorted(set(expected.get("counters", {})) | set(actual.get("counters", {})))
        if expected.get("counters", {}).get(key) != actual.get("counters", {}).get(key)
    }

    return {
        "added_modules": added,
        "removed_modules": removed,
        "changed_modules": changed,
        "counter_changes": counter_changes,
    }


def format_inventory_diff(diff: dict[str, Any]) -> str:
    lines = [
        "ARCH106 module inventory artifact is stale.",
        "Regenerate it with:",
        "  python scripts/generate_module_inventory.py",
        "  git add docs/architecture/module_inventory.generated.json",
        "",
    ]

    if diff["added_modules"]:
        lines.append("Added src modules missing from committed inventory:")
        lines.extend(f"  + {module}" for module in diff["added_modules"])
        lines.append("")

    if diff["removed_modules"]:
        lines.append("Removed src modules still present in committed inventory:")
        lines.extend(f"  - {module}" for module in diff["removed_modules"])
        lines.append("")

    if diff["changed_modules"]:
        lines.append("Changed module classifications/status:")
        for item in diff["changed_modules"]:
            lines.append(f"  * {item['path']}")
            for key, values in item["changes"].items():
                lines.append(f"    - {key}: actual={values['actual']!r}, expected={values['expected']!r}")
        lines.append("")

    if diff["counter_changes"]:
        lines.append("Counter changes:")
        for key, values in diff["counter_changes"].items():
            lines.append(f"  * {key}: actual={values['actual']!r}, expected={values['expected']!r}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _check_unclassified_legacy_baseline(
    *,
    inventory: dict[str, Any],
    classification: dict[str, Any],
) -> tuple[bool, str]:
    """Block newly added production modules from hiding as legacy.

    ARCH106 initially grandfathered the existing unclassified module set so the
    repo could add the guard incrementally. That grandfathering must not grow.
    Any new source module must be explicitly classified instead of increasing the
    unclassified legacy count.
    """

    baseline_limit = classification.get("unclassified_legacy_baseline_limit")
    if baseline_limit is None:
        return True, ""

    current_count = int(inventory.get("counters", {}).get("unclassified_legacy_modules", 0))
    allowed_count = int(baseline_limit)
    if current_count <= allowed_count:
        return True, ""

    return False, (
        "ARCH106 unclassified legacy baseline exceeded.\n"
        f"Current unclassified legacy modules: {current_count}\n"
        f"Allowed baseline: {allowed_count}\n"
        "New production modules under src/ must be explicitly classified as "
        "connected_runtime, runtime_entrypoint, test_only, experimental, "
        "quarantine or delete_candidate before merge.\n"
    )


def write_inventory(
    output_path: Path = DEFAULT_OUTPUT_PATH,
    *,
    repo_root: Path = REPO_ROOT,
    classification_path: Path = DEFAULT_CLASSIFICATION_PATH,
) -> Path:
    inventory = build_inventory(repo_root=repo_root, classification_path=classification_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_inventory(inventory), encoding="utf-8")
    return output_path


def check_inventory(
    output_path: Path = DEFAULT_OUTPUT_PATH,
    *,
    repo_root: Path = REPO_ROOT,
    classification_path: Path = DEFAULT_CLASSIFICATION_PATH,
) -> tuple[bool, str]:
    expected = build_inventory(repo_root=repo_root, classification_path=classification_path)
    classification = load_classification(classification_path)
    if not output_path.exists():
        return False, (
            "ARCH106 module inventory artifact is missing.\n"
            "Generate it with:\n"
            "  python scripts/generate_module_inventory.py\n"
            "  git add docs/architecture/module_inventory.generated.json\n"
        )

    try:
        actual = json.loads(output_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return False, f"ARCH106 module inventory artifact is invalid JSON: {exc}\n"

    actual = _normalize_inventory_for_ignored_modules(actual)

    baseline_ok, baseline_message = _check_unclassified_legacy_baseline(
        inventory=expected,
        classification=classification,
    )
    if not baseline_ok:
        return False, baseline_message

    if actual != expected:
        return False, format_inventory_diff(inventory_diff(expected, actual))

    return True, "ARCH106 module inventory artifact is current.\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate or validate the ARCH106 module inventory artifact.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the committed inventory instead of rewriting it.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help="Inventory output path.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = REPO_ROOT / output_path

    if args.check:
        ok, message = check_inventory(output_path)
        print(message, end="")
        return 0 if ok else 1

    path = write_inventory(output_path)
    print(f"Wrote ARCH106 module inventory to {path.relative_to(REPO_ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
