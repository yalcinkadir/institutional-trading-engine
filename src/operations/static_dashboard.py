"""Static HTML dashboard generation.

P35 builds a lightweight static dashboard from existing local reports.
It is reporting-only and intentionally tolerates missing inputs.
"""

from __future__ import annotations

import html
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_INPUTS = {
    "latest_signals": "reports/signals/latest-signals.json",
    "portfolio_state": "data/portfolio_state.json",
    "paper_live_observation": "reports/paper-live/paper-live-observation.json",
    "operational_readiness": "reports/operations/operational-readiness-review.json",
    "scheduled_dry_run": "reports/operations/scheduled-decision-support-dry-run.json",
    "manual_portfolio_sync": "reports/portfolio/manual-portfolio-sync.json",
    "archive_manifest": "reports/archive/latest/manifest.json",
}


@dataclass(frozen=True)
class DashboardInput:
    name: str
    path: Path
    status: str
    summary: dict[str, Any]
    error: str | None = None


@dataclass(frozen=True)
class DashboardResult:
    generated_at: str
    status: str
    output_html: str
    output_json: str
    inputs: tuple[DashboardInput, ...]
    warnings: tuple[str, ...]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _read_json(path: Path) -> tuple[str, dict[str, Any], str | None]:
    if not path.exists():
        return "missing", {}, "file_missing"
    try:
        content = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return "invalid", {}, f"invalid_json:{exc.msg}"
    if not isinstance(content, dict):
        return "invalid", {}, "json_root_not_object"
    return "available", content, None


def _summarize_latest_signals(payload: dict[str, Any]) -> dict[str, Any]:
    signals = payload.get("signals", payload if isinstance(payload, list) else [])
    if not isinstance(signals, list):
        signals = []
    actions: dict[str, int] = {}
    for signal in signals:
        if isinstance(signal, dict):
            action = str(signal.get("action", "unknown"))
            actions[action] = actions.get(action, 0) + 1
    return {"signal_count": len(signals), "actions": actions}


def _summarize_portfolio_state(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "equity_current": payload.get("equity_current"),
        "drawdown_percent": payload.get("drawdown_percent"),
        "daily_loss_percent": payload.get("daily_loss_percent"),
        "open_position_count": len(payload.get("open_positions", []) or []),
        "source": payload.get("source"),
    }


def _summarize_generic(payload: dict[str, Any]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for key in (
        "status",
        "ready",
        "result",
        "generated_at",
        "run_mode",
        "overall_status",
        "paper_live_ready_for_review",
    ):
        if key in payload:
            summary[key] = payload[key]
    if "checks" in payload and isinstance(payload["checks"], list):
        summary["check_count"] = len(payload["checks"])
    if "warnings" in payload and isinstance(payload["warnings"], list):
        summary["warning_count"] = len(payload["warnings"])
    if not summary:
        summary["top_level_keys"] = sorted(payload.keys())[:10]
    return summary


def _summarize_input(name: str, payload: dict[str, Any]) -> dict[str, Any]:
    if name == "latest_signals":
        return _summarize_latest_signals(payload)
    if name == "portfolio_state":
        return _summarize_portfolio_state(payload)
    return _summarize_generic(payload)


def collect_dashboard_inputs(
    *,
    root: Path,
    input_paths: dict[str, str] | None = None,
) -> tuple[DashboardInput, ...]:
    paths = input_paths or DEFAULT_INPUTS
    collected: list[DashboardInput] = []
    for name, relative_path in paths.items():
        path = root / relative_path
        status, payload, error = _read_json(path)
        summary = _summarize_input(name, payload) if status == "available" else {}
        collected.append(
            DashboardInput(
                name=name,
                path=Path(relative_path),
                status=status,
                summary=summary,
                error=error,
            )
        )
    return tuple(collected)


def _dashboard_status(inputs: tuple[DashboardInput, ...]) -> str:
    if all(item.status == "missing" for item in inputs):
        return "EMPTY"
    if any(item.status == "invalid" for item in inputs):
        return "WARN"
    if any(item.status == "missing" for item in inputs):
        return "PARTIAL"
    return "PASS"


def _warnings(inputs: tuple[DashboardInput, ...]) -> tuple[str, ...]:
    warnings: list[str] = []
    for item in inputs:
        if item.status != "available":
            warnings.append(f"{item.name}:{item.error or item.status}")
    return tuple(warnings)


def _render_summary_list(summary: dict[str, Any]) -> str:
    if not summary:
        return "<p>No summary available.</p>"
    rows = []
    for key, value in summary.items():
        rows.append(
            "<tr>"
            f"<th>{html.escape(str(key))}</th>"
            f"<td>{html.escape(json.dumps(value, sort_keys=True))}</td>"
            "</tr>"
        )
    return "<table>" + "".join(rows) + "</table>"


def render_dashboard_html(result: DashboardResult) -> str:
    cards = []
    for item in result.inputs:
        status_class = html.escape(item.status)
        cards.append(
            f"<section class='card {status_class}'>"
            f"<h2>{html.escape(item.name)}</h2>"
            f"<p><strong>Status:</strong> {html.escape(item.status)}</p>"
            f"<p><strong>Path:</strong> {html.escape(str(item.path))}</p>"
            + (f"<p><strong>Error:</strong> {html.escape(item.error)}</p>" if item.error else "")
            + _render_summary_list(item.summary)
            + "</section>"
        )

    warning_items = "".join(f"<li>{html.escape(warning)}</li>" for warning in result.warnings)
    warnings_html = f"<ul>{warning_items}</ul>" if warning_items else "<p>No warnings.</p>"

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Institutional Trading Engine Dashboard</title>
  <style>
    body {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 2rem; background: #f7f7f8; color: #1f2937; }}
    header {{ margin-bottom: 1.5rem; }}
    .status {{ display: inline-block; padding: 0.35rem 0.65rem; border-radius: 999px; background: #e5e7eb; font-weight: 700; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; }}
    .card {{ background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 1rem; box-shadow: 0 1px 2px rgba(0,0,0,0.04); }}
    .available {{ border-left: 6px solid #16a34a; }}
    .missing {{ border-left: 6px solid #f59e0b; }}
    .invalid {{ border-left: 6px solid #dc2626; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 0.75rem; }}
    th, td {{ text-align: left; border-top: 1px solid #e5e7eb; padding: 0.45rem; vertical-align: top; }}
    th {{ width: 42%; color: #374151; }}
    code {{ background: #f3f4f6; padding: 0.1rem 0.25rem; border-radius: 4px; }}
  </style>
</head>
<body>
  <header>
    <h1>Institutional Trading Engine Dashboard</h1>
    <p><span class="status">{html.escape(result.status)}</span></p>
    <p>Generated at: <code>{html.escape(result.generated_at)}</code></p>
    <p>Static reporting only. No broker connection, no order execution.</p>
  </header>
  <section class="card">
    <h2>Warnings</h2>
    {warnings_html}
  </section>
  <main class="grid">
    {''.join(cards)}
  </main>
</body>
</html>
"""


def build_dashboard_payload(result: DashboardResult) -> dict[str, Any]:
    return {
        "generated_at": result.generated_at,
        "status": result.status,
        "output_html": result.output_html,
        "output_json": result.output_json,
        "warnings": list(result.warnings),
        "inputs": [
            {
                "name": item.name,
                "path": str(item.path),
                "status": item.status,
                "summary": item.summary,
                "error": item.error,
            }
            for item in result.inputs
        ],
    }


def build_static_dashboard(
    *,
    root: Path | str = Path("."),
    output_html: Path | str = Path("reports/dashboard/index.html"),
    output_json: Path | str = Path("reports/dashboard/dashboard.json"),
    input_paths: dict[str, str] | None = None,
) -> DashboardResult:
    root_path = Path(root)
    html_path = Path(output_html)
    json_path = Path(output_json)
    inputs = collect_dashboard_inputs(root=root_path, input_paths=input_paths)
    generated_at = utc_now_iso()
    status = _dashboard_status(inputs)
    warnings = _warnings(inputs)

    result = DashboardResult(
        generated_at=generated_at,
        status=status,
        output_html=str(html_path),
        output_json=str(json_path),
        inputs=inputs,
        warnings=warnings,
    )

    html_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(render_dashboard_html(result), encoding="utf-8")
    json_path.write_text(json.dumps(build_dashboard_payload(result), indent=2, sort_keys=True), encoding="utf-8")
    return result
