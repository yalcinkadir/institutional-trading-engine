from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class FailedTask:
    name: str
    payload: dict[str, Any]
    error: str


@dataclass
class DeadLetterQueue:
    failed_tasks: list[FailedTask] = field(default_factory=list)

    def add(
        self,
        name: str,
        payload: dict[str, Any],
        error: str,
    ) -> None:
        self.failed_tasks.append(
            FailedTask(
                name=name,
                payload=payload,
                error=error,
            )
        )


dead_letter_queue = DeadLetterQueue()
