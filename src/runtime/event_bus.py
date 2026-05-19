from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Any


EventHandler = Callable[[dict[str, Any]], None]


class EventBus:
    def __init__(self) -> None:
        self.handlers: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        self.handlers[event_type].append(handler)

    def publish(self, event_type: str, payload: dict[str, Any]) -> None:
        for handler in self.handlers[event_type]:
            handler(payload)


event_bus = EventBus()
