from src.api.metrics_api import MetricsRegistry


def test_metrics_registry_increment():
    registry = MetricsRegistry()

    registry.increment("reports_generated_total")

    exported = registry.export()

    assert exported["metrics"]["reports_generated_total"] == 1


def test_prometheus_export_contains_metric():
    registry = MetricsRegistry()

    registry.increment("api_requests_total")

    output = registry.export_prometheus()

    assert "api_requests_total" in output
