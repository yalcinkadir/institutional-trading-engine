from __future__ import annotations

import json
from pathlib import Path

from src.operations.runtime_evidence_manifest import (
    SCHEMA_VERSION,
    build_artifact,
    build_runtime_evidence_manifest,
    load_runtime_evidence_manifest,
    sha256_file,
    validate_runtime_evidence_manifest,
    write_runtime_evidence_manifest,
)


def test_sha256_file_is_deterministic(tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.json"
    artifact.write_text('{"status":"ok"}', encoding="utf-8")

    first = sha256_file(artifact)
    second = sha256_file(artifact)

    assert first == second
    assert len(first) == 64


def test_build_artifact_records_existing_file_metadata(tmp_path: Path) -> None:
    artifact_path = tmp_path / "daily-report.json"
    artifact_path.write_text('{"result":"PASS"}', encoding="utf-8")

    artifact = build_artifact(
        artifact_path,
        category="required_output",
        required=True,
    )

    assert artifact.exists is True
    assert artifact.required is True
    assert artifact.category == "required_output"
    assert artifact.sha256 == sha256_file(artifact_path)
    assert artifact.size_bytes == artifact_path.stat().st_size


def test_build_artifact_records_missing_file_metadata(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.json"

    artifact = build_artifact(
        missing_path,
        category="required_input",
        required=True,
    )

    assert artifact.exists is False
    assert artifact.sha256 is None
    assert artifact.size_bytes is None


def test_manifest_passes_when_all_required_artifacts_exist(tmp_path: Path) -> None:
    required_input = tmp_path / "signals.json"
    required_output = tmp_path / "alerts.json"
    governance_state = tmp_path / "portfolio_state.json"

    required_input.write_text('{"signals":[]}', encoding="utf-8")
    required_output.write_text('{"alerts":[]}', encoding="utf-8")
    governance_state.write_text('{"governance_valid":true}', encoding="utf-8")

    manifest = build_runtime_evidence_manifest(
        trading_date="2026-05-31",
        required_inputs=[required_input],
        required_outputs=[required_output],
        required_governance_state=[governance_state],
        created_at="2026-05-31T20:00:00+00:00",
    )

    assert manifest.schema_version == SCHEMA_VERSION
    assert manifest.trading_date == "2026-05-31"
    assert manifest.status == "PASS"
    assert manifest.live_trading_authorized is False
    assert manifest.missing_required_artifacts == []
    assert validate_runtime_evidence_manifest(manifest) == {
        "status": "PASS",
        "errors": [],
    }


def test_manifest_fails_when_required_artifact_is_missing(tmp_path: Path) -> None:
    existing_input = tmp_path / "signals.json"
    missing_output = tmp_path / "alerts.json"

    existing_input.write_text('{"signals":[]}', encoding="utf-8")

    manifest = build_runtime_evidence_manifest(
        trading_date="2026-05-31",
        required_inputs=[existing_input],
        required_outputs=[missing_output],
        created_at="2026-05-31T20:00:00+00:00",
    )

    assert manifest.status == "FAIL"
    assert manifest.missing_required_artifacts == [missing_output.as_posix()]
    assert validate_runtime_evidence_manifest(manifest) == {
        "status": "PASS",
        "errors": [],
    }


def test_optional_missing_artifact_does_not_fail_manifest(tmp_path: Path) -> None:
    required_input = tmp_path / "signals.json"
    optional_missing = tmp_path / "debug.json"

    required_input.write_text('{"signals":[]}', encoding="utf-8")

    manifest = build_runtime_evidence_manifest(
        trading_date="2026-05-31",
        required_inputs=[required_input],
        optional_artifacts=[optional_missing],
        created_at="2026-05-31T20:00:00+00:00",
    )

    assert manifest.status == "PASS"
    assert manifest.missing_required_artifacts == []

    optional_artifact = [
        artifact
        for artifact in manifest.artifacts
        if artifact.path == optional_missing.as_posix()
    ][0]
    assert optional_artifact.required is False
    assert optional_artifact.exists is False


def test_write_and_load_manifest_round_trip(tmp_path: Path) -> None:
    required_input = tmp_path / "signals.json"
    required_input.write_text('{"signals":[]}', encoding="utf-8")

    manifest = build_runtime_evidence_manifest(
        trading_date="2026-05-31",
        required_inputs=[required_input],
        created_at="2026-05-31T20:00:00+00:00",
        notes=["paper observation only"],
    )

    output_path = write_runtime_evidence_manifest(manifest, output_dir=tmp_path)
    latest_path = tmp_path / "latest-runtime-evidence-manifest.json"

    assert output_path.exists()
    assert latest_path.exists()

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == SCHEMA_VERSION
    assert payload["live_trading_authorized"] is False

    loaded = load_runtime_evidence_manifest(output_path)

    assert loaded == manifest


def test_manifest_validation_rejects_live_trading_authorization_mutation(
    tmp_path: Path,
) -> None:
    required_input = tmp_path / "signals.json"
    required_input.write_text('{"signals":[]}', encoding="utf-8")

    manifest = build_runtime_evidence_manifest(
        trading_date="2026-05-31",
        required_inputs=[required_input],
        created_at="2026-05-31T20:00:00+00:00",
    )

    mutated = manifest.__class__(
        schema_version=manifest.schema_version,
        trading_date=manifest.trading_date,
        created_at=manifest.created_at,
        observation_mode=manifest.observation_mode,
        live_trading_authorized=True,
        status=manifest.status,
        missing_required_artifacts=manifest.missing_required_artifacts,
        artifacts=manifest.artifacts,
        notes=manifest.notes,
    )

    validation = validate_runtime_evidence_manifest(mutated)

    assert validation["status"] == "FAIL"
    assert "live_trading_authorized_must_be_false" in validation["errors"]