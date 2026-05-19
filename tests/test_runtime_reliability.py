from src.runtime.dead_letter_queue import DeadLetterQueue
from src.runtime.retry import RetryError, retry_operation


def test_retry_operation_success_after_failure():
    attempts = {"count": 0}

    def flaky_operation() -> str:
        attempts["count"] += 1

        if attempts["count"] < 2:
            raise ValueError("temporary failure")

        return "success"

    result = retry_operation(flaky_operation)

    assert result == "success"


def test_retry_operation_raises_after_exhaustion():
    def broken_operation() -> str:
        raise ValueError("permanent failure")

    failed = False

    try:
        retry_operation(broken_operation, retries=2)
    except RetryError:
        failed = True

    assert failed is True


def test_dead_letter_queue_adds_failed_task():
    queue = DeadLetterQueue()

    queue.add(
        name="report_generation",
        payload={"type": "premarket"},
        error="timeout",
    )

    assert len(queue.failed_tasks) == 1
