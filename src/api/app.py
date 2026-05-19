from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from src.api.health_api import health_response
from src.api.metrics_api import metrics_registry

app = FastAPI(title="Institutional Trading Engine")


@app.get("/")
def root() -> dict:
    metrics_registry.increment("api_requests_total")

    return {
        "service": "institutional-trading-engine",
        "status": "running",
    }


@app.get("/health")
def health() -> dict:
    metrics_registry.increment("api_requests_total")
    metrics_registry.increment("healthcheck_requests_total")

    return health_response()


@app.get("/metrics")
def metrics() -> dict:
    metrics_registry.increment("api_requests_total")

    return metrics_registry.export()


@app.get("/metrics/prometheus", response_class=PlainTextResponse)
def prometheus_metrics() -> str:
    metrics_registry.increment("api_requests_total")

    return metrics_registry.export_prometheus()
