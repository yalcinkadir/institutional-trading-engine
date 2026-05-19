from __future__ import annotations

from fastapi import Depends, FastAPI, Request
from fastapi.responses import PlainTextResponse

from src.api.auth import validate_api_key
from src.api.health_api import health_response
from src.api.metrics_api import metrics_registry
from src.api.rate_limit import rate_limiter

app = FastAPI(title="Institutional Trading Engine")


def apply_rate_limit(request: Request) -> None:
    client = request.client.host if request.client else "unknown"
    rate_limiter.check(client)


@app.get("/")
def root(request: Request) -> dict:
    apply_rate_limit(request)
    metrics_registry.increment("api_requests_total")

    return {
        "service": "institutional-trading-engine",
        "status": "running",
    }


@app.get("/health")
def health(request: Request) -> dict:
    apply_rate_limit(request)

    metrics_registry.increment("api_requests_total")
    metrics_registry.increment("healthcheck_requests_total")

    return health_response()


@app.get("/metrics", dependencies=[Depends(validate_api_key)])
def metrics(request: Request) -> dict:
    apply_rate_limit(request)
    metrics_registry.increment("api_requests_total")

    return metrics_registry.export()


@app.get(
    "/metrics/prometheus",
    response_class=PlainTextResponse,
    dependencies=[Depends(validate_api_key)],
)
def prometheus_metrics(request: Request) -> str:
    apply_rate_limit(request)
    metrics_registry.increment("api_requests_total")

    return metrics_registry.export_prometheus()
