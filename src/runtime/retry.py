from __future__ import annotations

import time
from collections.abc import Callable
from typing import TypeVar


T = TypeVar("T")


class RetryError(Exception):
    pass


def retry_operation(
    operation: Callable[[], T],
    retries: int = 3,
    delay_seconds: float = 1.0,
) -> T:
    last_error: Exception | None = None

    for attempt in range(retries):
        try:
            return operation()
        except Exception as exc:
            last_error = exc

            if attempt < retries - 1:
                time.sleep(delay_seconds)

    raise RetryError(str(last_error)) from last_error
