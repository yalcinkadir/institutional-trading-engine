from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DistributedTask:
    task_id: str
    task_type: str
    payload: dict[str, Any]
    status: str = "pending"


@dataclass
class DistributedTaskManager:
    tasks: list[DistributedTask] = field(default_factory=list)

    def submit(
        self,
        task_id: str,
        task_type: str,
        payload: dict[str, Any],
    ) -> DistributedTask:
        task = DistributedTask(
            task_id=task_id,
            task_type=task_type,
            payload=payload,
        )

        self.tasks.append(task)

        return task


distributed_task_manager = DistributedTaskManager()
