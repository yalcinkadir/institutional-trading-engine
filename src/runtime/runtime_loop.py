from __future__ import annotations

import asyncio
from dataclasses import asdict
from typing import Awaitable, Callable

from src.runtime.runtime_state import runtime_state
from src.structured_logging import emit_structured_log


class RuntimeLoopError(RuntimeError):
    """Raised when the runtime loop exceeds its tolerated consecutive errors."""


class RuntimeLoop:
    async def start(
        self,
        cycle_provider: Callable[[], Awaitable[dict]],
        cycle_interval_seconds: int = 60,
        max_cycles: int | None = None,
        max_consecutive_errors: int = 3,
    ) -> None:
        cycles = 0
        consecutive_errors = 0

        while True:
            try:
                decision = await cycle_provider()
            except Exception as exc:  # noqa: BLE001 - runtime loop must catch provider failures
                consecutive_errors += 1
                emit_structured_log(
                    level="ERROR",
                    event_type="runtime_loop_cycle_provider_error",
                    component="runtime_loop",
                    message="Runtime cycle provider raised an exception.",
                    context={
                        "consecutive_errors": consecutive_errors,
                        "max_consecutive_errors": max_consecutive_errors,
                        "error_type": type(exc).__name__,
                        "error_message": str(exc),
                    },
                )
                if consecutive_errors >= max_consecutive_errors:
                    raise RuntimeLoopError(
                        f"Runtime loop stopped after {consecutive_errors} consecutive cycle provider errors"
                    ) from exc

                await asyncio.sleep(cycle_interval_seconds)
                continue

            consecutive_errors = 0
            runtime_state.update(decision)
            cycles += 1

            if max_cycles is not None and cycles >= max_cycles:
                break

            await asyncio.sleep(cycle_interval_seconds)

    def current_state(self) -> dict:
        return asdict(runtime_state)


runtime_loop = RuntimeLoop()
