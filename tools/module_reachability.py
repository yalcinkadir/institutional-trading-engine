#!/usr/bin/env python3
"""Static module-reachability analysis for the institutional trading engine.

Evidence-based answer to: which ``src/`` modules are actually reachable, and
from where? Computes three transitive import closures over the real entrypoints
instead of relying on a hand-maintained classification:

 1. SCHEDULED PRODUCTION - modules reachable from cron-scheduled workflows.
 2. ALL SCRIPTS - reachable from any ``scripts/`` entrypoint
    (includes manual / workflow_dispatch tools).
 3. TESTS - reachable from the test suite.

From these it derives:

 * TRUE ORPHANS - imported by no script AND no test. Safest
   delete / quarantine candidates.
 * TEST/DISPATCH-ONLY - exercised by tests or manual scripts but never by a
   scheduled production path (i.e. "has a test, but does
   not run in production"). These are *not* dead, but are
   outside the live decision path.

This makes the project's own principle - "reachability != execution proof" -
measurable. Static reachability here is necessary-but-not-sufficient: a module
in the SCHEDULED set is *importable* from production, not *proven executed*.
Runtime execution proof remains a separate, stronger gate.

Usage:
    python tools/module_reachability.py
    python tools/module_reachability.py --json module_reachability.baseline.json
    python tools/module_reachability.py --list-orphans

Exit code is always 0; this is a reporting tool, not a gate. Wrap it in a CI
guard separately if you want to fail on new orphans.
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from collections import Counter, deque
from pathlib import Path

# Workflows that run on a cron schedule define the "production" surface.
# Keep this in sync with `.github/workflows/*` `on.schedule` triggers.
SCHEDULED_ENTRYPOINT_SCRIPTS = (
    "bootstrap_daily_evidence_sources",
    "build_daily_evidence_inputs",
    "build_daily_paper_observation_sources",
    "generate_daily_evidence_components",
    "persist_daily_observation_sources",
    "review_daily_observation_cadence",
    "run_daily_evidence_report",
    "validate_daily_evidence_inputs",
    "run_entry_exit_watcher",
    "send_notification",
    "generate_report",
    "validate_paper_observation_health",
    "validate_report_quality",
    "update_outcomes",
    "generate_outcomes",
    "generate_paper_observation_asset_timeline",
    "send_paper_observation_notification",
    "run_scheduled_decision_support_dry_run",
    "build_weekly_expectancy_summary",
    "generate_workflow_error_report",
    "create_backup",
)


def _module_name(path: Path, root: Path) -> str:
    return ".".join(path.relative_to(root).with_suffix("").parts)


def _index_src_modules(src_dir: Path, root: Path) -> dict[str, Path]:
    """Map every dotted module name in src/ to its file (packages included)."""
    index: dict[str, Path] = {}
    for path in src_dir.rglob("*.py"):
        if path.name == "__init__.py":
            index[_module_name(path.parent, root)] = path
        index[_module_name(path, root)] = path
    return index


def _imports_in(path: Path) -> set[str]:
    """Return dotted import targets found in a file.

    For ``from a.b import c`` we emit both ``a.b`` and ``a.b.c`` so that
    leaf-module imports resolve regardless of package layout.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
    except (SyntaxError, OSError):
        return set()
    out: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                out.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.level == 0:
                out.add(node.module)
                for alias in node.names:
                    out.add(f"{node.module}.{alias.name}")
    return out


def _closure(seed_files: list[Path], index: dict[str, Path]) -> set[str]:
    """Transitive import closure (within src/) starting from seed files."""
    keys = set(index)
    reached: set[str] = set()
    frontier: deque[str] = deque()

    def add(name: str) -> None:
        if name in keys and name not in reached:
            reached.add(name)
            frontier.append(name)

    for seed in seed_files:
        for imp in _imports_in(seed):
            add(imp)
    while frontier:
        current = frontier.popleft()
        src_file = index.get(current)
        if src_file and src_file.is_file():
            for imp in _imports_in(src_file):
                add(imp)
    return reached


def analyze(root: Path) -> dict:
    src_dir = root / "src"
    scripts_dir = root / "scripts"
    tests_dir = root / "tests"
    if not src_dir.is_dir():
        raise SystemExit(f"src/ not found under {root}")

    index = _index_src_modules(src_dir, root)
    leaf = {m: p for m, p in index.items() if p.name != "__init__.py"}
    leaf_keys = set(leaf)

    sched_files = [
        scripts_dir / f"{name}.py"
        for name in SCHEDULED_ENTRYPOINT_SCRIPTS
        if (scripts_dir / f"{name}.py").is_file()
    ]
    all_scripts = list(scripts_dir.rglob("*.py")) if scripts_dir.is_dir() else []
    all_tests = list(tests_dir.rglob("*.py")) if tests_dir.is_dir() else []

    scheduled = _closure(sched_files, index) & leaf_keys
    all_script_reach = _closure(all_scripts, index) & leaf_keys
    test_reach = _closure(all_tests, index) & leaf_keys
    any_reach = scheduled | all_script_reach | test_reach

    true_orphans = sorted(leaf_keys - any_reach)
    test_or_dispatch_only = sorted((all_script_reach | test_reach) - scheduled)

    def _pkg(mod: str) -> str:
        parts = mod.split(".")
        return parts[1] if len(parts) > 2 else "src(root)"

    return {
        "totals": {
            "leaf_src_modules": len(leaf),
            "reachable_scheduled_production": len(scheduled),
            "reachable_all_scripts": len(all_script_reach),
            "reachable_tests": len(test_reach),
            "reachable_any": len(any_reach),
            "true_orphans": len(true_orphans),
            "test_or_dispatch_only": len(test_or_dispatch_only),
        },
        "true_orphans": [leaf[m].relative_to(root).as_posix() for m in true_orphans],
        "true_orphans_by_package": dict(
            Counter(_pkg(m) for m in true_orphans).most_common()
        ),
        "test_or_dispatch_only": [
            leaf[m].relative_to(root).as_posix() for m in test_or_dispatch_only
        ],
        "scheduled_production_modules": sorted(
            leaf[m].relative_to(root).as_posix() for m in scheduled
        ),
    }


def _print_summary(result: dict) -> None:
    t = result["totals"]
    print("Module reachability (static import closure)\n")
    print(f" Leaf src modules ............................. {t['leaf_src_modules']}")
    print(
        " Reachable from scheduled production .......... "
        f"{t['reachable_scheduled_production']}"
    )
    print(f" Reachable from all scripts/ ................. {t['reachable_all_scripts']}")
    print(f" Reachable from tests ........................ {t['reachable_tests']}")
    print(f" Reachable from anything ..................... {t['reachable_any']}")
    print(f" TRUE ORPHANS (no script, no test) ........... {t['true_orphans']}")
    print(f" Test/dispatch-only (not in production) ...... {t['test_or_dispatch_only']}")
    if result["true_orphans"]:
        print("\n True orphans (safest delete/quarantine candidates):")
        for path in result["true_orphans"]:
            print(f" - {path}")
    if result["true_orphans_by_package"]:
        print("\n Orphans by package:")
        for pkg, count in result["true_orphans_by_package"].items():
            print(f" {pkg}: {count}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parent.parent),
        help="Repository root (defaults to the parent of tools/).",
    )
    parser.add_argument("--json", metavar="PATH", help="Write full result as JSON to PATH.")
    parser.add_argument(
        "--list-orphans",
        action="store_true",
        help="Print only true-orphan paths, one per line (script-friendly).",
    )
    args = parser.parse_args(argv)

    result = analyze(Path(args.root).resolve())

    if args.list_orphans:
        for path in result["true_orphans"]:
            print(path)
        return 0

    if args.json:
        Path(args.json).write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(f"Wrote {args.json}")
    _print_summary(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
