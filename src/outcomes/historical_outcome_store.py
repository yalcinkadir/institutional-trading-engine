from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from src.outcomes.real_outcome_evaluator import OutcomeEvaluation


OUTCOME_STORE_PATH = Path("reports/outcomes/historical_outcomes.jsonl")


class HistoricalOutcomeStore:
    def __init__(self) -> None:
        OUTCOME_STORE_PATH.parent.mkdir(parents=True, exist_ok=True)

    def append(
        self,
        module: str,
        regime: str,
        outcome: OutcomeEvaluation,
    ) -> None:
        payload = {
            "module": module,
            "regime": regime,
            "outcome": asdict(outcome),
        }

        with OUTCOME_STORE_PATH.open("a", encoding="utf-8") as file:
            file.write(json.dumps(payload) + "\n")

    def load_all(self) -> list[dict]:
        if not OUTCOME_STORE_PATH.exists():
            return []

        with OUTCOME_STORE_PATH.open("r", encoding="utf-8") as file:
            return [json.loads(line) for line in file if line.strip()]
