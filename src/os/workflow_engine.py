from __future__ import annotations


def build_workflow(report_type: str) -> dict:
    base_steps = [
        "load_market_data",
        "validate_data",
        "calculate_market_regime",
        "run_ranking_engine",
    ]

    if report_type == "premarket":
        base_steps.extend([
            "run_execution_analysis",
            "generate_watchlist",
            "send_telegram_report",
        ])

    elif report_type == "postmarket":
        base_steps.extend([
            "run_performance_review",
            "update_memory_layer",
            "send_telegram_report",
        ])

    elif report_type == "weekly":
        base_steps.extend([
            "run_backtesting",
            "run_meta_evaluation",
            "generate_weekly_summary",
            "send_telegram_report",
        ])

    return {
        "workflow_type": report_type,
        "step_count": len(base_steps),
        "steps": base_steps,
    }
