from __future__ import annotations

import hashlib
import json
from pathlib import Path


BACKTEST_REPORT_ROOT = Path("reports/backtests/real_data")
ROOT_SOURCE_EVIDENCE = Path("reports/backtests/real-data-backtest-evidence.json")


def _json_files() -> list[Path]:
    return sorted(BACKTEST_REPORT_ROOT.glob("**/*.json"))


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_206_all_backtest_source_evidence_references_resolve() -> None:
    referenced: list[tuple[Path, Path]] = []

    for report_path in _json_files():
        payload = _load(report_path)
        source_evidence = payload.get("source_evidence")
        if source_evidence:
            referenced.append((report_path, Path(source_evidence)))

    assert referenced, "expected at least one backtest report with source_evidence"
    for report_path, evidence_path in referenced:
        assert evidence_path.exists(), f"{report_path} references missing source_evidence: {evidence_path}"
        assert evidence_path == ROOT_SOURCE_EVIDENCE


def test_206_root_real_data_backtest_evidence_is_reviewable_and_safe() -> None:
    assert ROOT_SOURCE_EVIDENCE.exists()
    payload = _load(ROOT_SOURCE_EVIDENCE)

    assert payload["data_source"] == "real_data"
    assert payload["is_demo"] is False
    assert payload["live_trading_authorized"] is False
    assert payload["broker_execution_mode"] == "paper_only"
    assert payload["input_pack_gate_status"] in {"PASSED", "FAILED"}
    assert payload["run_health_status"] in {"OK", "BLOCKED", "NO_TRADE_VALID", "DEGRADED_DATA"}
    assert isinstance(payload.get("input_checksums"), dict)
    assert payload.get("results") is not None
    assert payload.get("metrics", {}).get("total") == len(payload.get("results", []))


def test_206_root_real_data_backtest_evidence_has_manifest_and_results_hash() -> None:
    payload = _load(ROOT_SOURCE_EVIDENCE)
    manifest = payload.get("evidence_manifest")

    assert isinstance(manifest, dict)
    assert manifest["schema_version"] == "bt131.source_evidence.v1"
    assert manifest["source_evidence_path"] == str(ROOT_SOURCE_EVIDENCE)
    assert manifest["results_count"] == len(payload["results"])
    assert len(manifest["results_sha256"]) == 64
    assert payload["input_checksums"]["results_sha256"] == manifest["results_sha256"]

    canonical_results = json.dumps(payload["results"], sort_keys=True, separators=(",", ":"))
    assert hashlib.sha256(canonical_results.encode("utf-8")).hexdigest() == manifest["results_sha256"]


def test_206_bt131_workflow_persists_root_source_evidence_path() -> None:
    workflow = Path(".github/workflows/bt131_real_data_backtest_evidence.yml").read_text(encoding="utf-8")

    assert "reports/backtests/real-data-backtest-evidence.json" in workflow
    assert "git add reports/backtests/real-data-backtest-evidence.json" in workflow
    assert "root_source_evidence" in workflow
    assert "latest_source_evidence" in workflow
