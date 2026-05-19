from __future__ import annotations

from fastapi import FastAPI

from src.api.health_api import health_response

app = FastAPI(title="Institutional Trading Engine")


@app.get("/")
def root() -> dict:
    return {
        "service": "institutional-trading-engine",
        "status": "running",
    }


@app.get("/health")
def health() -> dict:
    return health_response()
