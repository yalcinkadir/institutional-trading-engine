from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = REPO_ROOT / "reports"
GITIGNORE = REPO_ROOT / ".gitignore"

PUBLIC_REPORTS = [
    REPORTS_DIR / "premarket-report.md",
    REPORTS_DIR / "postmarket-report.md",
    REPORTS_DIR / "weekly-report.md",
]

REQUIRED_GITIGNORE_PATTERNS = [
    ".env.*",
    "private_edge/",
    "external_edge/",
    "edge_config.local.*",
    "strategy_config.local.*",
    "thresholds.local.*",
    "scoring_weights.local.*",
    "exit_profiles.local.*",
    "setup_mappings.local.*",
    ".cache/",
    "data/raw/",
    "data/live/",
    "data/private/",
    "evidence/",
    "lockbox/",
    "artifacts/",
    "outputs/",
    "generated/",
    "reports/generated/",
    "reports/private/",
    "reports/live/",
    "reports/raw/",
    "reports/*-live.md",
    "reports/*-private.md",
    "reports/*-raw.md",
    "reports/*-generated.md",
    "*.db",
    "*.sqlite",
    "*.duckdb",
    "logs/",
]

PROHIBITED_PUBLIC_REPORT_TERMS = [
    "Generated: 2026-",
    "Live data source: Polygon",
    "Polygon.io",
    "Data Status: LIVE",
    "Data Status: PARTIAL",
    "### Recommended Assets",
    "Ranked Opportunities\n\n####",
    "thresholds_version=public-demo-",
]

PROHIBITED_RANKED_SYMBOL_HEADINGS = [
    "#### MSFT",
    "#### NVDA",
    "#### META",
    "#### AAPL",
    "#### MU",
    "#### QQQ",
    "#### GLD",
    "#### SLV",
]


def test_gitignore_blocks_private_edge_and_generated_artifacts() -> None:
    content = GITIGNORE.read_text(encoding="utf-8")

    missing = [pattern for pattern in REQUIRED_GITIGNORE_PATTERNS if pattern not in content]

    assert missing == []


def test_public_reports_are_synthetic_examples_only() -> None:
    for report_path in PUBLIC_REPORTS:
        content = report_path.read_text(encoding="utf-8")

        assert "Synthetic example: yes" in content
        assert "Public-safe artifact: yes" in content
        assert "Live data source: none" in content
        assert "must not contain real ranked opportunities" in content

        leaked_terms = [term for term in PROHIBITED_PUBLIC_REPORT_TERMS if term in content]
        leaked_symbol_headings = [term for term in PROHIBITED_RANKED_SYMBOL_HEADINGS if term in content]

        assert leaked_terms == []
        assert leaked_symbol_headings == []
