from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/generate_report.py")


def test_generate_report_cli_refuses_public_premarket_output() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--type",
            "premarket",
            "--output",
            "reports/premarket-report.md",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "protected public artifact" in result.stderr
    assert "reports/premarket-report.md" in result.stderr


def test_generate_report_cli_refuses_public_postmarket_output() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--type",
            "postmarket",
            "--output",
            "reports/postmarket-report.md",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "protected public artifact" in result.stderr
    assert "reports/postmarket-report.md" in result.stderr


def test_generate_report_cli_refuses_public_weekly_output() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--type",
            "weekly",
            "--output",
            "reports/weekly-report.md",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "protected public artifact" in result.stderr
    assert "reports/weekly-report.md" in result.stderr
