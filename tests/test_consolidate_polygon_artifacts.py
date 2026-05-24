from __future__ import annotations

from pathlib import Path

import pytest

from scripts.consolidate_polygon_artifacts import consolidate, iter_artifact_dirs


def _write_artifact(root: Path, name: str, symbols: list[str]) -> Path:
    artifact = root / name
    universe = artifact / "data" / "universe"
    bars = artifact / "data" / "historical_bars"
    reports = artifact / "reports" / "edge_evidence_data"
    universe.mkdir(parents=True)
    bars.mkdir(parents=True)
    reports.mkdir(parents=True)
    universe.joinpath("survivorship_universe.csv").write_text("symbol,active_from\nAAA,2026-05-24\n", encoding="utf-8")
    for symbol in symbols:
        bars.joinpath(f"{symbol}.csv").write_text("date,open,high,low,close,volume\n2024-01-01,1,2,0.5,1.5,100\n", encoding="utf-8")
    reports.joinpath("polygon-bars-manifest.md").write_text("# Polygon Daily Bars Download\n", encoding="utf-8")
    return artifact


def test_iter_artifact_dirs_accepts_single_extracted_artifact(tmp_path: Path) -> None:
    tmp_path.joinpath("data", "historical_bars").mkdir(parents=True)

    assert iter_artifact_dirs(tmp_path) == [tmp_path]


def test_iter_artifact_dirs_discovers_nested_download_layout(tmp_path: Path) -> None:
    _write_artifact(tmp_path / "run-1", "polygon-edge-runtime-dataset", ["AAA"])
    _write_artifact(tmp_path / "run-2", "polygon-edge-runtime-dataset", ["BBB"])

    discovered = iter_artifact_dirs(tmp_path)

    assert [path.name for path in discovered] == ["polygon-edge-runtime-dataset", "polygon-edge-runtime-dataset"]
    assert len(discovered) == 2


def test_iter_artifact_dirs_requires_existing_root(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        iter_artifact_dirs(tmp_path / "missing")


def test_consolidate_copies_unique_bars_and_skips_duplicates(tmp_path: Path) -> None:
    artifacts = tmp_path / "artifacts"
    artifacts.mkdir()
    _write_artifact(artifacts, "batch-0", ["AAA", "BBB"])
    _write_artifact(artifacts, "batch-1", ["BBB", "CCC"])

    output = tmp_path / "combined"
    manifest = tmp_path / "combined-manifest.md"
    result = consolidate(artifacts, output, manifest)

    assert result.artifact_dirs == 2
    assert result.universe_found is True
    assert result.copied_bar_files == 3
    assert result.duplicate_bar_files == 1
    assert result.manifest_files == 2
    assert output.joinpath("data", "universe", "survivorship_universe.csv").exists()
    assert sorted(path.name for path in output.joinpath("data", "historical_bars").glob("*.csv")) == ["AAA.csv", "BBB.csv", "CCC.csv"]


def test_consolidate_writes_combined_manifest(tmp_path: Path) -> None:
    artifacts = tmp_path / "artifacts"
    artifacts.mkdir()
    _write_artifact(artifacts, "batch-0", ["AAA"])

    output = tmp_path / "combined"
    manifest = tmp_path / "reports" / "combined.md"
    result = consolidate(artifacts, output, manifest)

    text = manifest.read_text(encoding="utf-8")
    assert result.copied_bar_files == 1
    assert "Artifact directories scanned: **1**" in text
    assert "Copied unique bar files: **1**" in text
    assert "Source manifest files: **1**" in text
