from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


DECISION_LOG_PATH = Path("data/decision_log.jsonl")


@dataclass(frozen=True)
class DecisionLogEntry:
    decision_id: str
    created_at: str
    payload: dict[str, Any]


class DecisionLogStore:
    def __init__(self, path: Path = DECISION_LOG_PATH) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, decision_id: str, payload: dict[str, Any]) -> DecisionLogEntry:
        entry = DecisionLogEntry(
            decision_id=decision_id,
            created_at=datetime.now(UTC).isoformat(),
            payload=payload,
        )

        with self.path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(asdict(entry)) + "\n")

        return entry

    def load_all(self) -> list[DecisionLogEntry]:
        if not self.path.exists():
            return []

        entries: list[DecisionLogEntry] = []

        with self.path.open("r", encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue
                payload = json.loads(line)
                entries.append(
                    DecisionLogEntry(
                        decision_id=payload["decision_id"],
                        created_at=payload["created_at"],
                        payload=payload["payload"],
                    )
                )

        return entries


decision_log_store = DecisionLogStore()
