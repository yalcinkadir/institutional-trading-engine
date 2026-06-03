#!/usr/bin/env python3
"""Generate an ARCH106 module inventory from the current checkout.

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


def write_inventory(output_path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    inventory = build_inventory()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate ARCH106 module inventory JSON.")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help="Output JSON path. Defaults to docs/architecture/module_inventory.generated.json",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = REPO_ROOT / output_path
    written = write_inventory(output_path)
    print(f"Module inventory written: {_repo_relative(written)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
