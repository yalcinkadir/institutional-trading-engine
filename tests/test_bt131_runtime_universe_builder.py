from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.build_bt131_runtime_universe import build_runtime_universe


def test_build_bt131_runtime_universe_uses_only_covered_symbols(tmp_path: Path) -> None:
    manifest = {
        "requested_start_date": "2024-01-01",
        "symbols": [
            {"symbol": "MSFT", "status": "ok", "bar_count": 605},
            {"symbol": "MU", "status": "ok", "bar_count": 605},
            {"symbol": "SLV", "status": "ok", "bar_count": 605},
            {"symbol": "GOOGL", "status": "missing", "bar_count": 0},
            {"symbol": "SPY", "status": "ok", "bar_count": 0},
        ],
    }
    manifest_path = tmp_path / "coverage_manifest.json"
    output_path = tmp_path / "bt131_runtime_universe.csv"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    summary = build_runtime_universe(manifest_path, output_path)

    rows = list(csv.DictReader(output_path.read_text(encoding="utf-8").splitlines()))
    symbols = [row["symbol"] for row in rows]

    assert summary["status"] == "OK"
    assert summary["symbols"] == ["MSFT", "MU", "SLV"]
    assert symbols == ["MSFT", "MU", "SLV"]
    assert all(row["active"] == "true" for row in rows)
    assert {row["source"] for row in rows} == {"bt131_runtime_coverage_manifest"}
    assert {row["status"] for row in rows} == {"active"}
    assert {row["asset_class"] for row in rows} == {"equity", "etf"}


def test_build_bt131_runtime_universe_rejects_empty_coverage(tmp_path: Path) -> None:
    manifest_path = tmp_path / "coverage_manifest.json"
    output_path = tmp_path / "bt131_runtime_universe.csv"
    manifest_path.write_text(json.dumps({"symbols": [{"symbol": "MSFT", "status": "missing", "bar_count": 0}]}), encoding="utf-8")

    try:
        build_runtime_universe(manifest_path, output_path)
    except SystemExit as exc:
        assert "no covered symbols" in str(exc)
    else:  # pragma: no cover - defensive assertion
        raise AssertionError("expected SystemExit for empty coverage")
