#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path

from src.outcomes.outcome_summary import summarize_outcomes

REPORTS_DIR = Path("reports")
OUTCOMES_DIR = REPORTS_DIR / "outcomes"

SIGNAL_PATTERN = re.compile(r"\b(AAPL|MSFT|NVDA|QQQ|SPY|TSLA|AMD|MU|META|AMZN)\b")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate outcome tracking reports.")
    parser.add_argument("--days", type=int, default=7)
    return parser.parse_args()


def discover_reports() -> list[Path]:
    report_files: list[Path] = []

    for folder in ["premarket", "postmarket", "weekly"]:
        path = REPORTS_DIR / folder
        if path.exists():
            report_files.extend(sorted(path.glob("*.md")))

    return sorted(report_files)


def extract_signals(report_text: str) -> list[str]:
    return sorted(set(SIGNAL_PATTERN.findall(report_text)))


def build_mock_outcomes(signals: list[str]) -> list[dict]:
    outcomes: list[dict] = []

    for index, signal in enumerate(signals):
        performance = round(((index % 5) - 2) * 2.5, 2)

        if performance > 1:
            classification = "WIN"
        elif performance < -1:
            classification = "LOSS"
        else:
            classification = "NEUTRAL"

        outcomes.append(
            {
                "symbol": signal,
                "classification": classification,
                "performance_percent": performance,
            }
        )

    return outcomes


def write_outcome_reports(outcomes: list[dict]) -> None:
    OUTCOMES_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(UTC).strftime("%Y-%m-%d")

    summary = summarize_outcomes(outcomes)

    markdown_lines = [
        "# Institutional Outcome Report",
        "",
        f"Generated: {datetime.now(UTC).isoformat()}",
        "",
        "## Summary",
        "",
        f"- Total Outcomes: {summary['total_outcomes']}",
        f"- Win Rate: {summary['win_rate']}%",
        f"- Average Performance: {summary['average_performance']}%",
        "",
        "## Signals",
        "",
    ]

    for outcome in outcomes:
        markdown_lines.append(
            f"- {outcome['symbol']}: {outcome['classification']} ({outcome['performance_percent']}%)"
        )

    dated_file = OUTCOMES_DIR / f"{timestamp}-outcomes.md"
    latest_file = OUTCOMES_DIR / "latest-outcomes.md"
    history_file = OUTCOMES_DIR / "outcome-history.json"
    performance_file = OUTCOMES_DIR / "signal-performance.json"

    markdown_content = "\n".join(markdown_lines)

    dated_file.write_text(markdown_content, encoding="utf-8")
    latest_file.write_text(markdown_content, encoding="utf-8")

    history_file.write_text(json.dumps(outcomes, indent=2), encoding="utf-8")

    signal_summary = {
        outcome["symbol"]: {
            "classification": outcome["classification"],
            "performance_percent": outcome["performance_percent"],
        }
        for outcome in outcomes
    }

    performance_file.write_text(
        json.dumps(signal_summary, indent=2),
        encoding="utf-8",
    )


def main() -> int:
    reports = discover_reports()

    all_signals: list[str] = []

    for report in reports:
        try:
            text = report.read_text(encoding="utf-8")
            all_signals.extend(extract_signals(text))
        except Exception:
            continue

    signals = sorted(set(all_signals))
    outcomes = build_mock_outcomes(signals)

    write_outcome_reports(outcomes)

    print(f"Generated outcomes for {len(outcomes)} signals")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
