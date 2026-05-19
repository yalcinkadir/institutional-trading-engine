from __future__ import annotations

from datetime import UTC, datetime


class MetricsRegistry:
    def __init__(self) -> None:
        self.metrics = {
            "reports_generated_total": 0,
            "outcomes_generated_total": 0,
            "healthcheck_requests_total": 0,
            "api_requests_total": 0,
        }

    def increment(self, key: str) -> None:
        if key not in self.metrics:
            self.metrics[key] = 0

        self.metrics[key] += 1

    def export(self) -> dict:
        return {
            "timestamp_utc": datetime.now(UTC).isoformat(),
            "metrics": self.metrics,
        }

    def export_prometheus(self) -> str:
        lines: list[str] = []

        for key, value in sorted(self.metrics.items()):
            metric_name = key.replace("-", "_").replace(".", "_")
            lines.append(f"{metric_name} {value}")

        return "\n".join(lines) + "\n"


metrics_registry = MetricsRegistry()
