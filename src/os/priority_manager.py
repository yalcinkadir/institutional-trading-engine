from __future__ import annotations


def prioritize_tasks(tasks: list[dict]) -> dict:
    ordered = sorted(
        tasks,
        key=lambda task: (
            task.get("priority", 0),
            task.get("urgency", 0),
        ),
        reverse=True,
    )

    return {
        "task_count": len(ordered),
        "prioritized_tasks": ordered,
    }


def classify_priority(priority: int) -> str:
    if priority >= 90:
        return "Critical"
    if priority >= 70:
        return "High"
    if priority >= 50:
        return "Moderate"
    return "Low"
