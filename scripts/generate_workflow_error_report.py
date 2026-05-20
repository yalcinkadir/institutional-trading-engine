#!/usr/bin/env python3
"""Generate a Markdown report for recent GitHub Actions workflow failures.

The script uses the GitHub REST API with GITHUB_TOKEN and writes:
- reports/workflow-errors/YYYY-MM-DD-workflow-errors.md
- reports/workflow-errors/latest-workflow-errors.md

By default it only includes failed runs from the last 24 hours. Use
--since-date to provide an explicit ISO timestamp.
"""

from __future__ import annotations

import argparse
import os
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import requests

DEFAULT_OUTPUT_DIR = Path("reports/workflow-errors")
ERROR_PATTERNS = (
    "##[error]",
    "ERROR",
    "FAILED",
    "FAILURES",
    "Traceback",
    "AssertionError",
    "ImportError",
    "ModuleNotFoundError",
    "Process completed with exit code",
)


def _request_json(url: str, token: str) -> dict[str, Any]:
    response = requests.get(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def _request_text(url: str, token: str) -> str:
    response = requests.get(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        timeout=60,
        allow_redirects=True,
    )
    response.raise_for_status()
    return response.text


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def _list_recent_failed_runs(
    repo: str,
    token: str,
    limit: int,
    since: datetime | None,
) -> list[dict[str, Any]]:
    # Fetch more than the display limit so date filtering has enough candidates.
    per_page = min(100, max(limit * 3, 30))
    url = (
        f"https://api.github.com/repos/{repo}/actions/runs"
        f"?per_page={per_page}&status=completed"
    )
    payload = _request_json(url, token)
    runs = payload.get("workflow_runs", [])
    failed = [run for run in runs if run.get("conclusion") == "failure"]

    if since is not None:
        failed = [
            run for run in failed
            if (_parse_datetime(run.get("created_at")) or datetime.min.replace(tzinfo=UTC)) >= since
        ]

    return failed[:limit]


def _list_jobs(repo: str, token: str, run_id: int) -> list[dict[str, Any]]:
    url = f"https://api.github.com/repos/{repo}/actions/runs/{run_id}/jobs?per_page=100"
    payload = _request_json(url, token)
    return payload.get("jobs", [])


def _extract_error_context(log_text: str, max_blocks: int = 8) -> list[str]:
    lines = log_text.splitlines()
    blocks: list[str] = []
    seen: set[str] = set()

    for index, line in enumerate(lines):
        if any(pattern in line for pattern in ERROR_PATTERNS):
            start = max(0, index - 4)
            end = min(len(lines), index + 12)
            block = "\n".join(lines[start:end]).strip()
            normalized = re.sub(r"\d{4}-\d{2}-\d{2}T[^ ]+Z\s*", "", block)
            if normalized and normalized not in seen:
                seen.add(normalized)
                blocks.append(block)
        if len(blocks) >= max_blocks:
            break

    return blocks


def _failed_steps(job: dict[str, Any]) -> list[str]:
    result = []
    for step in job.get("steps", []) or []:
        if step.get("conclusion") == "failure":
            result.append(f"{step.get('number')}. {step.get('name')}")
    return result


def build_report(repo: str, token: str, limit: int, since: datetime | None) -> str:
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    runs = _list_recent_failed_runs(repo, token, limit, since)
    since_text = since.strftime("%Y-%m-%d %H:%M UTC") if since else "not set"

    lines: list[str] = [
        "# GitHub Actions Workflow Error Report",
        "",
        f"Generated: {now}",
        f"Repository: `{repo}`",
        f"Filter since: {since_text}",
        f"Failed runs included: {len(runs)}",
        "",
    ]

    if not runs:
        lines.append("✅ No failed workflow runs found for the selected time window.")
        return "\n".join(lines)

    for run in runs:
        run_id = run.get("id")
        workflow_name = run.get("name") or "unknown workflow"
        display_title = run.get("display_title") or run.get("head_commit", {}).get("message") or "unknown commit"
        branch = run.get("head_branch") or "unknown"
        sha = str(run.get("head_sha") or "")[:12]
        html_url = run.get("html_url")
        created_at = run.get("created_at")
        updated_at = run.get("updated_at")

        lines += [
            f"## {workflow_name}",
            "",
            f"- Run ID: `{run_id}`",
            f"- Branch: `{branch}`",
            f"- Commit: `{sha}`",
            f"- Title: {display_title}",
            f"- Created: {created_at}",
            f"- Updated: {updated_at}",
            f"- URL: {html_url}",
            "",
        ]

        jobs = _list_jobs(repo, token, int(run_id))
        failed_jobs = [job for job in jobs if job.get("conclusion") == "failure"]

        if not failed_jobs:
            lines.append("- No failed jobs returned by API, although run concluded as failure.")
            lines.append("")
            continue

        for job in failed_jobs:
            job_id = job.get("id")
            job_name = job.get("name") or "unknown job"
            steps = _failed_steps(job)

            lines += [
                f"### Failed job: {job_name}",
                "",
                f"- Job ID: `{job_id}`",
                f"- Started: {job.get('started_at')}",
                f"- Completed: {job.get('completed_at')}",
            ]

            if steps:
                lines.append(f"- Failed steps: {', '.join(steps)}")
            lines.append("")

            try:
                log_url = f"https://api.github.com/repos/{repo}/actions/jobs/{job_id}/logs"
                log_text = _request_text(log_url, token)
                error_blocks = _extract_error_context(log_text)
            except Exception as exc:
                error_blocks = [f"Could not fetch job logs: {type(exc).__name__}: {exc}"]

            if error_blocks:
                lines.append("#### Error context")
                lines.append("")
                for block in error_blocks:
                    lines.append("```text")
                    lines.append(block[:3000])
                    lines.append("```")
                    lines.append("")
            else:
                lines.append("No obvious error context found in logs.")
                lines.append("")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate GitHub Actions workflow error report.")
    parser.add_argument("--repo", default=os.getenv("GITHUB_REPOSITORY"), help="Repository in owner/name format")
    parser.add_argument("--token", default=os.getenv("GITHUB_TOKEN"), help="GitHub token")
    parser.add_argument("--limit", type=int, default=10, help="Number of failed runs to include")
    parser.add_argument("--since-date", default=None, help="Only include failed runs created at/after this ISO timestamp")
    parser.add_argument("--lookback-hours", type=int, default=24, help="Default lookback window when --since-date is not supplied")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Output directory")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.repo:
        raise SystemExit("GITHUB_REPOSITORY or --repo is required")
    if not args.token:
        raise SystemExit("GITHUB_TOKEN or --token is required")

    since = _parse_datetime(args.since_date)
    if since is None and args.lookback_hours > 0:
        since = datetime.now(UTC) - timedelta(hours=args.lookback_hours)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = build_report(args.repo, args.token, args.limit, since)
    date_str = datetime.now(UTC).strftime("%Y-%m-%d")

    dated = output_dir / f"{date_str}-workflow-errors.md"
    latest = output_dir / "latest-workflow-errors.md"

    dated.write_text(report, encoding="utf-8")
    latest.write_text(report, encoding="utf-8")

    print(f"Workflow error report written: {dated}")
    print(f"Latest workflow error report written: {latest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
