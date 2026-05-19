from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable


class AsyncTaskQueue:
    """
    Lightweight async task queue foundation.

    Current:
    - async task scheduling
    - worker execution
    - queue abstraction

    Future:
    - distributed workers
    - retry policies
    - dead-letter queues
    - task prioritization
    - persistence
    """

    def __init__(self) -> None:
        self.queue: asyncio.Queue = asyncio.Queue()

    async def enqueue(
        self,
        task: Callable[[], Awaitable[None]],
    ) -> None:
        await self.queue.put(task)

    async def worker(self) -> None:
        while True:
            task = await self.queue.get()

            try:
                await task()
            finally:
                self.queue.task_done()
