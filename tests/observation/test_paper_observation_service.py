from pathlib import Path

from src.observation.paper_observation_models import PaperObservationDecision
from src.observation.paper_observation_service import PaperObservationService
from src.observation.paper_observation_store import PaperObservationStore


def test_record_decision_creates_jsonl_record(tmp_path: Path) -> None:
    store_path = tmp_path / "paper_observation.jsonl"
    store = PaperObservationStore(store_path)
    service = PaperObservationService(store)

    record = service.record_decision(
        signal_id="sig-001",
        symbol="aapl",
        decision="BUY",
        market_regime="RISK_ON",
        setup_classification="LEADER_PULLBACK",
        entry_level=190.50,
        stop_level=185.00,
        target_1=198.00,
        target_2=205.00,
        runner_state="NOT_STARTED",
        alert_payload={"message": "BUY AAPL"},
    )

    assert record.signal_id == "sig-001"
    assert record.symbol == "AAPL"
    assert record.decision == PaperObservationDecision.BUY
    assert store_path.exists()

    loaded_records = store.read_all()

    assert len(loaded_records) == 1
    assert loaded_records[0].symbol == "AAPL"
    assert loaded_records[0].decision == PaperObservationDecision.BUY


def test_unknown_decision_is_stored_as_unknown(tmp_path: Path) -> None:
    store = PaperObservationStore(tmp_path / "paper_observation.jsonl")
    service = PaperObservationService(store)

    record = service.record_decision(
        signal_id="sig-002",
        symbol="MSFT",
        decision="MAYBE",
    )

    assert record.decision == PaperObservationDecision.UNKNOWN


def test_find_by_signal_id_returns_matching_records(tmp_path: Path) -> None:
    store = PaperObservationStore(tmp_path / "paper_observation.jsonl")
    service = PaperObservationService(store)

    service.record_decision(signal_id="sig-001", symbol="AAPL", decision="BUY")
    service.record_decision(signal_id="sig-002", symbol="MSFT", decision="WAIT")

    matches = store.find_by_signal_id("sig-001")

    assert len(matches) == 1
    assert matches[0].symbol == "AAPL"