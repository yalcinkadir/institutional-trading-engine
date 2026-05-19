from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class InMemoryStateCache:
    state: dict[str, Any] = field(default_factory=dict)

    def set(self, key: str, value: Any) -> None:
        self.state[key] = value

    def get(self, key: str) -> Any:
        return self.state.get(key)

    def snapshot(self) -> dict[str, Any]:
        return dict(self.state)


in_memory_state_cache = InMemoryStateCache()
