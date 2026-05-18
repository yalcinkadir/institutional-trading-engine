from src.os.orchestrator import orchestrate_modules
from src.os.priority_manager import classify_priority, prioritize_tasks
from src.os.task_router import route_task
from src.os.workflow_engine import build_workflow


def test_orchestrator():
    result = orchestrate_modules(
        {
            "market_regime": "Risk-Off",
            "report_type": "weekly",
        }
    )

    assert result["module_count"] >= 8
    assert "meta_intelligence" in result["modules"]


def test_workflow_engine():
    result = build_workflow("premarket")

    assert result["workflow_type"] == "premarket"
    assert "generate_watchlist" in result["steps"]


def test_task_router():
    result = route_task("research")

    assert result["destination"] == "research_intelligence"


def test_priority_manager():
    result = prioritize_tasks(
        [
            {"task": "risk", "priority": 95, "urgency": 90},
            {"task": "ranking", "priority": 60, "urgency": 50},
        ]
    )

    assert result["prioritized_tasks"][0]["task"] == "risk"
    assert classify_priority(95) == "Critical"
