from __future__ import annotations

import threading
import time
from collections.abc import Callable


class BackgroundWorker:
    def __init__(
        self,
        name: str,
        interval_seconds: int,
        task: Callable[[], None],
    ) -> None:
        self.name = name
        self.interval_seconds = interval_seconds
        self.task = task
        self._running = False
        self._thread: threading.Thread | None = None

    def _run(self) -> None:
        while self._running:
            self.task()
            time.sleep(self.interval_seconds)

    def start(self) -> None:
        if self._running:
            return

        self._running = True

        self._thread = threading.Thread(
            target=self._run,
            daemon=True,
        )

        self._thread.start()

    def stop(self) -> None:
        self._running = False

        if self._thread:
            self._thread.join(timeout=1)
