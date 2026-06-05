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


def _repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def discover_src_modules(repo_root: Path = REPO_ROOT) -> list[str]:
    src_dir = repo_root / "src"
    if not src_dir.exists():
        return []
    modules: list[str] = []
    for path in src_dir.rglob("*.py"):
        if any(part in IGNORED_PARTS for part in path.parts):
            continue
        modules.append(path.relative_to(repo_root).as_posix())
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
        "classification_source": _repo_relative(classification_path),
        "grandfather_existing_modules": bool(classification.get("grandfather_existing_modules")),
        "counters": counters,
        "modules": modules,
    }


def render_inventory(inventory: dict[str, Any]) -> str:
    return json.dumps(inventory, indent=2, sort_keys=True) + "\n"


def _records_by_path(inventory: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {record["path"]: record for record in inventory.get("modules", [])}


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


def write_inventory(output_path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    inventory = build_inventory()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_inventory(inventory), encoding="utf-8")
    return output_path


def check_inventory(output_path: Path = DEFAULT_OUTPUT_PATH) -> tuple[bool, str]:
    expected = build_inventory()
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

    if actual == expected:
        return True, "ARCH106 module inventory artifact is current.\n"

    return False, format_inventory_diff(inventory_diff(expected, actual))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate or validate ARCH106 module inventory JSON.")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help="Output JSON path. Defaults to docs/architecture/module_inventory.generated.json",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate that the committed inventory matches the generator output without writing files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = REPO_ROOT / output_path

    if args.check:
        is_current, message = check_inventory(output_path)
        print(message, end="")
        return 0 if is_current else 1

    written = write_inventory(output_path)
    print(f"Module inventory written: {_repo_relative(written)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
