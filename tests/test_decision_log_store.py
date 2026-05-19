from pathlib import Path

from src.storage.decision_log_store import DecisionLogStore


def test_decision_log_persistence(tmp_path: Path):
    store = DecisionLogStore(
        path=tmp_path / "decision_log.jsonl",
    )

    store.append(
        decision_id="decision-1",
        payload={
            "classification": "bullish",
            "confidence": 80,
        },
    )

    results = store.load_all()

    assert len(results) == 1
    assert results[0].decision_id == "decision-1"
