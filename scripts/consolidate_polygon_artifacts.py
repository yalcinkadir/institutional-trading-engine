"""Consolidate Polygon batch runtime artifacts into one dataset.

The script expects one or more extracted artifact directories. Each artifact root
may contain:

- data/universe/survivorship_universe.csv
- data/historical_bars/*.csv
- reports/edge_evidence_data/polygon-bars-manifest.md

It also supports nested download layouts such as:

- run-id/artifact-name/data/...

It copies unique bar files into a combined output directory, keeps the first
available universe CSV, and writes a combined manifest. Generated data remains a
runtime artifact and should not be committed to Git.
"""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ConsolidationResult:
    artifact_dirs: int
    universe_found: bool
    copied_bar_files: int
    duplicate_bar_files: int
    manifest_files: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Consolidate Polygon batch artifacts")
    parser.add_argument(
        "--artifacts-root",
        type=Path,
        required=True,
        help="Directory containing extracted batch artifacts or artifact directories",
    )
    parser.add_argument("--output-root", type=Path, default=Path("data/polygon_combined_runtime"))
    parser.add_argument(
        "--combined-manifest",
        type=Path,
        default=Path("reports/edge_evidence_data/combined-polygon-bars-manifest.md"),
    )
    return parser.parse_args()


def _is_artifact_root(path: Path) -> bool:
    return (
        (path / "data" / "universe" / "survivorship_universe.csv").exists()
        or (path / "data" / "historical_bars").exists()
        or (path / "reports" / "edge_evidence_data" / "polygon-bars-manifest.md").exists()
    )


def iter_artifact_dirs(root: Path) -> list[Path]:
    if not root.exists():
        raise FileNotFoundError(f"artifacts root does not exist: {root}")
    if _is_artifact_root(root):
        return [root]
    artifact_dirs = [path for path in sorted(root.rglob("*")) if path.is_dir() and _is_artifact_root(path)]
    return artifact_dirs


def _copy_first_universe(artifact_dirs: list[Path], output_root: Path) -> bool:
    output_path = output_root / "data" / "universe" / "survivorship_universe.csv"
    for directory in artifact_dirs:
        source = directory / "data" / "universe" / "survivorship_universe.csv"
        if source.exists():
            output_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, output_path)
            return True
    return False


def _copy_bar_files(artifact_dirs: list[Path], output_root: Path) -> tuple[int, int]:
    output_dir = output_root / "data" / "historical_bars"
    output_dir.mkdir(parents=True, exist_ok=True)
    copied = 0
    duplicates = 0
    seen: set[str] = set()
    for directory in artifact_dirs:
        bars_dir = directory / "data" / "historical_bars"
        if not bars_dir.exists():
            continue
        for source in sorted(bars_dir.glob("*.csv")):
            symbol = source.stem.upper()
            if symbol in seen:
                duplicates += 1
                continue
            seen.add(symbol)
            shutil.copy2(source, output_dir / source.name)
            copied += 1
    return copied, duplicates


def _collect_manifests(artifact_dirs: list[Path]) -> list[Path]:
    manifests: list[Path] = []
    for directory in artifact_dirs:
        manifest = directory / "reports" / "edge_evidence_data" / "polygon-bars-manifest.md"
        if manifest.exists():
            manifests.append(manifest)
    return manifests


def write_combined_manifest(path: Path, result: ConsolidationResult, manifest_paths: list[Path]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Combined Polygon Daily Bars Dataset",
        "",
        f"Artifact directories scanned: **{result.artifact_dirs}**",
        f"Universe file found: **{result.universe_found}**",
        f"Copied unique bar files: **{result.copied_bar_files}**",
        f"Duplicate bar files skipped: **{result.duplicate_bar_files}**",
        f"Source manifest files: **{result.manifest_files}**",
        "",
        "## Source manifests",
        "",
    ]
    if manifest_paths:
        lines.extend(f"- {manifest}" for manifest in manifest_paths)
    else:
        lines.append("- none")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def consolidate(artifacts_root: Path, output_root: Path, combined_manifest: Path) -> ConsolidationResult:
    artifact_dirs = iter_artifact_dirs(artifacts_root)
    universe_found = _copy_first_universe(artifact_dirs, output_root)
    copied, duplicates = _copy_bar_files(artifact_dirs, output_root)
    manifests = _collect_manifests(artifact_dirs)
    result = ConsolidationResult(
        artifact_dirs=len(artifact_dirs),
        universe_found=universe_found,
        copied_bar_files=copied,
        duplicate_bar_files=duplicates,
        manifest_files=len(manifests),
    )
    write_combined_manifest(combined_manifest, result, manifests)
    return result


def main() -> int:
    args = parse_args()
    result = consolidate(args.artifacts_root, args.output_root, args.combined_manifest)
    print(f"Scanned {result.artifact_dirs} artifact directories")
    print(f"Copied {result.copied_bar_files} unique bar files")
    print(f"Skipped {result.duplicate_bar_files} duplicate bar files")
    if not result.universe_found:
        raise SystemExit("No survivorship_universe.csv found in artifacts")
    if result.copied_bar_files < 500:
        raise SystemExit("Combined dataset has fewer than 500 bar files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
