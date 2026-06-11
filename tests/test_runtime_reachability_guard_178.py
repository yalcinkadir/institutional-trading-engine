from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REACHABILITY_REGISTRY = REPO_ROOT / "docs" / "architecture" / "decision_critical_runtime_reachability.json"
MODULE_CLASSIFICATION = REPO_ROOT / "docs" / "architecture" / "module_classification.json"
README = REPO_ROOT / "README.md"
ROADMAP = REPO_ROOT / "ROADMAP.md"

ALLOWED_STATES = {
    "runtime_connected",
    "experimental",
    "quarantine",
    "test_only",
    "deprecated",
}

NON_RUNTIME_STATES = {
    "experimental",
    "quarantine",
    "test_only",
    "deprecated",
}

REQUIRED_DECISION_CRITICAL_MODULES = {
    "src/reporting/decision_report.py",
    "src/signals/signal_generator.py",
    "src/signals/trade_plan_validator.py",
    "src/decision_confidence.py",
    "src/data_quality_engine.py",
    "src/event_risk_engine.py",
    "src/liquidity_volatility_engine.py",
}

FORBIDDEN_NON_RUNTIME_CLAIMS = {
    "decision_stack_validated",
    "runtime_active",
    "module_complete",
    "strategy_validated",
    "paper_confidence_authorized",
    "live_ready",
}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_178_decision_critical_reachability_registry_exists_and_has_required_schema() -> None:
    payload = _load_json(REACHABILITY_REGISTRY)

    assert payload["schema_version"] == 1
    assert payload["issue"] == "#178"
    assert set(payload["allowed_states"]) == ALLOWED_STATES
    assert set(payload["forbidden_claims_for_non_runtime"]) == FORBIDDEN_NON_RUNTIME_CLAIMS
    assert isinstance(payload["modules"], list)
    assert payload["modules"]

    for record in payload["modules"]:
        assert record["path"].startswith("src/"), record
        assert record["path"].endswith(".py"), record
        assert (REPO_ROOT / record["path"]).exists(), record["path"]
        assert record["state"] in ALLOWED_STATES, record
        assert "claim_boundary" in record and record["claim_boundary"].strip(), record
        assert "runtime_entrypoint" in record, record
        assert "runtime_execution_proof" in record, record


def test_178_required_decision_critical_modules_are_explicitly_registered() -> None:
    payload = _load_json(REACHABILITY_REGISTRY)
    registered = {record["path"] for record in payload["modules"]}

    assert REQUIRED_DECISION_CRITICAL_MODULES <= registered


def test_178_runtime_connected_modules_have_entrypoint_and_existing_guard_proof() -> None:
    payload = _load_json(REACHABILITY_REGISTRY)

    for record in payload["modules"]:
        if record["state"] != "runtime_connected":
            continue

        entrypoint = record["runtime_entrypoint"]
        proof = record["runtime_execution_proof"]
        proof_path = proof.split("::", 1)[0]

        assert entrypoint, record
        assert proof, record
        assert (REPO_ROOT / entrypoint).exists(), record
        assert (REPO_ROOT / proof_path).exists(), record


def test_178_non_runtime_decision_modules_have_explicit_forbidden_claim_boundary() -> None:
    payload = _load_json(REACHABILITY_REGISTRY)
    forbidden_claims = set(payload["forbidden_claims_for_non_runtime"])

    assert forbidden_claims == FORBIDDEN_NON_RUNTIME_CLAIMS

    for record in payload["modules"]:
        if record["state"] not in NON_RUNTIME_STATES:
            continue

        assert record["runtime_entrypoint"] is None, record
        assert record["runtime_execution_proof"] is None, record
        boundary = record["claim_boundary"].lower()
        assert "not counted as active runtime" in boundary or "must not imply" in boundary, record


def test_178_reachability_registry_matches_arch106_module_classification_for_connected_runtime() -> None:
    payload = _load_json(REACHABILITY_REGISTRY)
    classification = _load_json(MODULE_CLASSIFICATION)["classified_modules"]

    for record in payload["modules"]:
        if record["state"] != "runtime_connected":
            continue

        classified = classification.get(record["path"])
        assert classified is not None, record["path"]
        assert classified["classification"] == "connected_runtime", record["path"]
        assert classified["runtime_entrypoint"] == record["runtime_entrypoint"], record["path"]
        assert classified["runtime_execution_proof"] == record["runtime_execution_proof"], record["path"]


def test_178_project_status_mentions_runtime_reachability_boundary() -> None:
    readme = README.read_text(encoding="utf-8")
    roadmap = ROADMAP.read_text(encoding="utf-8")

    assert "#178" in readme
    assert "Runtime reachability" in readme
    assert "decision_critical_runtime_reachability.json" in readme

    assert "#178" in roadmap
    assert "Runtime reachability" in roadmap
    assert "decision_critical_runtime_reachability.json" in roadmap
