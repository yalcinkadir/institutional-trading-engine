from __future__ import annotations


def orchestrate_modules(context: dict) -> dict:
    market_regime = context.get("market_regime", "Unknown")
    report_type = context.get("report_type", "premarket")

    modules: list[str] = [
        "market_intelligence",
        "relative_strength",
        "ranking_engine",
        "risk_engine",
    ]

    if report_type in {"premarket", "postmarket"}:
        modules.extend([
            "execution_intelligence",
            "decision_core",
            "research_intelligence",
        ])

    if market_regime in {"Defensive", "Risk-Off"}:
        modules.extend([
            "portfolio_intelligence",
            "global_risk_monitor",
            "risk_adaptation",
        ])

    if report_type == "weekly":
        modules.extend([
            "historical_analytics",
            "performance_tracker",
            "memory_layer",
            "meta_intelligence",
        ])

    return {
        "module_count": len(modules),
        "modules": modules,
    }
