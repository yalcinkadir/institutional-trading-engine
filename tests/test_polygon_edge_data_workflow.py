from __future__ import annotations

from pathlib import Path


def test_polygon_edge_data_workflow_exists() -> None:
    workflow = Path(".github/workflows/polygon-edge-data-pipeline.yml")

    assert workflow.exists()


def test_polygon_edge_data_workflow_uses_all_assets_by_default() -> None:
    content = Path(".github/workflows/polygon-edge-data-pipeline.yml").read_text(encoding="utf-8")

    assert "name: Polygon Edge Data Pipeline" in content
    assert "workflow_dispatch" in content
    assert "max_symbols" in content
    assert 'default: "0"' in content
    assert "0 means all available symbols" in content
    assert "Build all-assets Polygon universe" in content


def test_polygon_edge_data_workflow_uploads_runtime_artifact() -> None:
    content = Path(".github/workflows/polygon-edge-data-pipeline.yml").read_text(encoding="utf-8")

    assert "actions/upload-artifact@v4" in content
    assert "polygon-edge-runtime-dataset" in content
    assert "data/universe/survivorship_universe.csv" in content
    assert "data/historical_bars/" in content
    assert "reports/edge_evidence_data/" in content


def test_polygon_edge_data_workflow_validates_secret_and_minimum_coverage() -> None:
    content = Path(".github/workflows/polygon-edge-data-pipeline.yml").read_text(encoding="utf-8")

    assert "POLYGON_API_KEY" in content
    assert "Validate Polygon credential" in content
    assert "validate_universe_coverage.py" in content
    assert "--minimum 500" in content
