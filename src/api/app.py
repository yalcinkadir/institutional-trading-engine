from __future__ import annotations

from fastapi import FastAPI

from src.api.health_api import health_response
from src.api.metrics_api import metrics_registry

app = FastAPI(title="Institutional Trading Engine")


@app.get("/")
def root() -> dict:
    return {
        "service": "institutional-trading-engine",
        "status": "running",
    }


@app.get("/health")
def health() -> dict:
    metrics_registry.increment("healthcheck_requests_total")
    return health_response()


@app.get("/metrics")
def metrics() -> dict:
    return metrics_registry.export()
