from __future__ import annotations


def coordinate_agents(agents: list[dict], task: str) -> dict:
    assigned: list[dict] = []

    for agent in agents:
        capabilities = agent.get("capabilities", [])
        if task in capabilities or "general" in capabilities:
            assigned.append(
                {
                    "agent": agent.get("name", "unknown"),
                    "role": agent.get("role", "analyst"),
                    "task": task,
                }
            )

    return {
        "task": task,
        "assigned_count": len(assigned),
        "assigned_agents": assigned,
    }
