import time

from src.runtime.background_worker import BackgroundWorker
from src.runtime.distributed_tasks import DistributedTaskManager


def test_background_worker_executes_task():
    state = {"count": 0}

    def task() -> None:
        state["count"] += 1

    worker = BackgroundWorker(
        name="test-worker",
        interval_seconds=1,
        task=task,
    )

    worker.start()

    time.sleep(1.2)

    worker.stop()

    assert state["count"] >= 1


def test_distributed_task_submission():
    manager = DistributedTaskManager()

    task = manager.submit(
        task_id="task-1",
        task_type="report_generation",
        payload={"report": "premarket"},
    )

    assert task.status == "pending"
    assert len(manager.tasks) == 1
