from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .paper_observation_models import PaperObservationRecord


class PaperObservationStore:
    """
    Append-only JSONL store for paper observation records.

    This keeps observation data auditable and easy to inspect.
    No database dependency is required for Phase B.
    """

    def __init__(self, file_path: str | Path = "data/paper_observation.jsonl") -> None:
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, record: PaperObservationRecord) -> None:
        with self.file_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record.to_dict(), sort_keys=True))
            file.write("\n")

    def read_all(self) -> list[PaperObservationRecord]:
        if not self.file_path.exists():
            return []

        records: list[PaperObservationRecord] = []

        with self.file_path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                records.append(PaperObservationRecord.from_dict(json.loads(line)))

        return records

    def find_by_signal_id(self, signal_id: str) -> list[PaperObservationRecord]:
        return [
            record
            for record in self.read_all()
            if record.signal_id == signal_id
        ]

    def iter_records(self) -> Iterable[PaperObservationRecord]:
        yield from self.read_all()