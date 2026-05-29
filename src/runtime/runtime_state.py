from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Deque


DEFAULT_RUNTIME_HISTORY_MAXLEN = 1000


@dataclass
class RuntimeState:
    latest_decision: dict[str, Any] | None = None
    cycle_count: int = 0
    updated_at: str | None = None
    history_maxlen: int = DEFAULT_RUNTIME_HISTORY_MAXLEN
    history: Deque[dict[str, Any]] = field(init=False)

    def __post_init__(self) -> None:
        self.history = deque(maxlen=max(1, int(self.history_maxlen)))

    def update(self, decision: dict[str, Any]) -> None:
        self.latest_decision = decision
        self.cycle_count += 1
        self.updated_at = datetime.now(UTC).isoformat()
        self.history.append(
            {
                "cycle": self.cycle_count,
                "updated_at": self.updated_at,
                "decision": decision,
            }
        )

    def snapshot(self) -> dict[str, Any]:
        return {
            "cycle_count": self.cycle_count,
            "updated_at": self.updated_at,
            "latest_decision": self.latest_decision,
            "history_size": len(self.history),
            "history_maxlen": self.history.maxlen,
        }


runtime_state = RuntimeState()
