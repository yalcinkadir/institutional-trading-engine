from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class RuntimeState:
    latest_decision: dict[str, Any] | None = None
    cycle_count: int = 0
    updated_at: str | None = None
    history: list[dict[str, Any]] = field(default_factory=list)

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
        }


runtime_state = RuntimeState()
