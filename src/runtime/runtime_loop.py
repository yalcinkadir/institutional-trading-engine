from __future__ import annotations

import asyncio
from dataclasses import asdict
from typing import Awaitable, Callable

from src.runtime.runtime_state import runtime_state


class RuntimeLoop:
    async def start(
        self,
        cycle_provider: Callable[[], Awaitable[dict]],
        cycle_interval_seconds: int = 60,
        max_cycles: int | None = None,
    ) -> None:
        cycles = 0

        while True:
            decision = await cycle_provider()

            runtime_state.update(decision)

            cycles += 1

            if max_cycles is not None and cycles >= max_cycles:
                break

            await asyncio.sleep(cycle_interval_seconds)

    def current_state(self) -> dict:
        return asdict(runtime_state)


runtime_loop = RuntimeLoop()
