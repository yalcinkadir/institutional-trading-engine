from __future__ import annotations

from src.observability.alerts import alert_manager


class RuntimeMonitor:
    def check_health(
        self,
        failed_jobs: int,
        queue_backlog: int,
    ) -> None:
        if failed_jobs > 5:
            alert_manager.trigger(
                level="critical",
                message="High failed job count detected",
            )

        if queue_backlog > 100:
            alert_manager.trigger(
                level="warning",
                message="Queue backlog exceeded threshold",
            )


runtime_monitor = RuntimeMonitor()
