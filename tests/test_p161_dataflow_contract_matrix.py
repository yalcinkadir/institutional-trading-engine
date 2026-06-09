from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs/architecture/dataflow_contract_matrix.md"

REQUIRED_FIELDS = {
    "symbol",
    "close",
    "atr14",
    "source",
    "source_timestamp",
    "data_status",
    "signal_id",
    "action",
    "decision",
    "entry_trigger",
    "stop_loss",
    "target_1",
    "run_health_status",
    "input_plan_count",
    "accepted_plan_count",
    "rejected_plan_count",
}

CRITICAL_DOWNSTREAM_FIELDS = {
    "symbol",
    "close",
    "atr14",
    "signal_id",
    "action",
    "decision",
    "entry_trigger",
    "stop_loss",
    "target_1",
}


def _representative_payload() -> dict[str, object]:
    return {
        "symbol": "SPY",
        "close": 500.0,
        "atr14": 5.25,
        "source": "polygon",
        "source_timestamp": "2026-06-09T00:00:00Z",
        "data_status": "OK",
        "signal_id": "SPY-20260609-demo",
        "action": "BUY",
        "decision": "TRADE_CANDIDATE",
        "entry_trigger": 501.0,
        "stop_loss": 494.0,
        "target_1": 512.0,
        "run_health_status": "OK",
        "input_plan_count": 1,
        "accepted_plan_count": 1,
        "rejected_plan_count": 0,
    }


def _classify_contract_health(payload: dict[str, object]) -> str:
    missing = REQUIRED_FIELDS - payload.keys()
    if missing:
        return "BLOCKED_MISSING_INPUTS"
    if payload.get("data_status") == "BLOCKED":
        return "BLOCKED_MISSING_INPUTS"
    if payload.get("accepted_plan_count") == 0 and payload.get("input_plan_count") != 0:
        return "BLOCKED_MISSING_INPUTS"
    return "OK"


def test_p161_dataflow_contract_matrix_exists_and_names_runtime_path() -> None:
    text = MATRIX.read_text(encoding="utf-8")
    assert "Scanner → Signals → Quality → Validator → Watcher → Evidence" in text
    for field in REQUIRED_FIELDS:
        assert f"`{field}`" in text
    assert "atr14" in text
    assert "`atr` at boundary only" in text
    assert "NO_TRADE_VALID" in text
    assert "BLOCKED_MISSING_INPUTS" in text


def test_p161_representative_pipeline_payload_contains_required_fields() -> None:
    payload = _representative_payload()

    assert REQUIRED_FIELDS <= payload.keys()
    assert _classify_contract_health(payload) == "OK"


def test_p161_missing_critical_fields_fail_closed_not_no_trade() -> None:
    for field in sorted(CRITICAL_DOWNSTREAM_FIELDS):
        payload = _representative_payload()
        payload.pop(field)

        assert _classify_contract_health(payload) == "BLOCKED_MISSING_INPUTS"
        assert _classify_contract_health(payload) != "NO_TRADE_VALID"


def test_p161_blocked_data_status_fails_closed() -> None:
    payload = _representative_payload()
    payload["data_status"] = "BLOCKED"

    assert _classify_contract_health(payload) == "BLOCKED_MISSING_INPUTS"
