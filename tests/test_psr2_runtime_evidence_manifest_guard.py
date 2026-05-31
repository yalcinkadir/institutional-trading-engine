from __future__ import annotations

import json
from pathlib import Path

from src.operations.runtime_evidence_manifest import (
    build_runtime_evidence_manifest,
    write_runtime_evidence_manifest,
)
from src.operations.runtime_evidence_manifest_guard import (
    evaluate_runtime_evidence_manifest,
    evaluate_runtime_evidence_manifest_file,
    evaluate_runtime_evidence_manifest_for_date,
    manifest_path_for_date,
    write_manifest_guard_report,
)


def test_manifest_path_for_date_uses_standard_name(tmp_path: Path) -> None:
    path = manifest_path_for_date("2026-05-31", manifest_dir=tmp_path)

    assert path == tmp_path / "2026-05-31-runtime-evidence-manifest.json"


def test_guard_fails_closed_when_manifest_is_missing(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing-manifest.json"

    result = evaluate_runtime_evidence_manifest_file(missing_path)

    assert result.status == "FAIL"
    assert result.passed is False
    assert result.errors == ["manifest_missing"]
    assert result.manifest_path == missing_path.as_posix()


def test_guard_fails_closed_when_manifest_json_is_invalid(tmp_path: Path) -> None:
    invalid_path = tmp_path / "invalid.json"
    invalid_path.write_text("{not-json", encoding="utf-8")

    result = evaluate_runtime_evidence_manifest_file(invalid_path)

    assert result.status == "FAIL"
    assert "manifest_invalid_json_or_schema" in result.errors


def test_guard_passes_for_valid_pass_manifest(tmp_path: Path) -> None:
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
    manifest_path = write_runtime_evidence_manifest(manifest, output_dir=tmp_path)

    result = evaluate_runtime_evidence_manifest_file(manifest_path)

    assert result.status == "PASS"
    assert result.passed is True
    assert result.errors == []
    assert result.trading_date == "2026-05-31"
    assert result.manifest_status == "PASS"
    assert result.live_trading_authorized is False


def test_guard_fails_when_manifest_status_is_fail(tmp_path: Path) -> None:
    required_input = tmp_path / "signals.json"
    missing_output = tmp_path / "alerts.json"

    required_input.write_text('{"signals":[]}', encoding="utf-8")

    manifest = build_runtime_evidence_manifest(
        trading_date="2026-05-31",
        required_inputs=[required_input],
        required_outputs=[missing_output],
        created_at="2026-05-31T20:00:00+00:00",
    )
    manifest_path = write_runtime_evidence_manifest(manifest, output_dir=tmp_path)

    result = evaluate_runtime_evidence_manifest_file(manifest_path)

    assert result.status == "FAIL"
    assert "manifest_status_not_pass" in result.errors
    assert "required_artifacts_missing" in result.errors
    assert result.missing_required_artifacts == [missing_output.as_posix()]


def test_guard_fails_when_loaded_manifest_was_mutated_to_authorize_live_trading(
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

    result = evaluate_runtime_evidence_manifest(
        mutated,
        manifest_path=tmp_path / "manifest.json",
    )

    assert result.status == "FAIL"
    assert "live_trading_authorized_must_be_false" in result.errors


def test_guard_for_date_uses_expected_manifest_path(tmp_path: Path) -> None:
    required_input = tmp_path / "signals.json"
    required_input.write_text('{"signals":[]}', encoding="utf-8")

    manifest = build_runtime_evidence_manifest(
        trading_date="2026-05-31",
        required_inputs=[required_input],
        created_at="2026-05-31T20:00:00+00:00",
    )
    write_runtime_evidence_manifest(manifest, output_dir=tmp_path)

    result = evaluate_runtime_evidence_manifest_for_date(
        "2026-05-31",
        manifest_dir=tmp_path,
    )

    assert result.status == "PASS"
    assert result.manifest_path == (
        tmp_path / "2026-05-31-runtime-evidence-manifest.json"
    ).as_posix()


def test_write_manifest_guard_report_round_trip(tmp_path: Path) -> None:
    missing_manifest = tmp_path / "missing.json"
    result = evaluate_runtime_evidence_manifest_file(missing_manifest)

    report_path = write_manifest_guard_report(
        result,
        output_path=tmp_path / "guard-report.json",
    )

    payload = json.loads(report_path.read_text(encoding="utf-8"))

    assert payload["status"] == "FAIL"
    assert payload["errors"] == ["manifest_missing"]
    assert payload["manifest_path"] == missing_manifest.as_posix()