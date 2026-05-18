from __future__ import annotations


def route_task(task_type: str) -> dict:
    routes = {
        "market_analysis": "market_intelligence",
        "ranking": "ranking_engine",
        "risk": "risk_engine",
        "portfolio": "portfolio_intelligence",
        "execution": "execution_intelligence",
        "research": "research_intelligence",
        "decision": "decision_core",
        "memory": "memory_layer",
        "meta": "meta_intelligence",
    }

    destination = routes.get(task_type, "orchestrator")

    return {
        "task_type": task_type,
        "destination": destination,
    }
