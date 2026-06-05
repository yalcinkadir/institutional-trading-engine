from __future__ import annotations

from pathlib import Path

from src.data_path_policy import (
    DATA_PATH_POLICY_VERSION,
    REQUIRED_IGNORED_DATA_PATTERNS,
    missing_required_ignored_data_patterns,
    prohibited_global_data_ignore_patterns,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = REPO_ROOT / "reports"
GITIGNORE = REPO_ROOT / ".gitignore"

PUBLIC_REPORTS = [
    REPORTS_DIR / "premarket-report.md",
    REPORTS_DIR / "postmarket-report.md",
]

REQUIRED_NON_DATA_GITIGNORE_PATTERNS = [
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
    "reports/weekly-report.md",
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

    missing = [pattern for pattern in REQUIRED_NON_DATA_GITIGNORE_PATTERNS if pattern not in content]
    missing.extend(missing_required_ignored_data_patterns(content))

    assert missing == []


def test_gitignore_uses_canonical_data_path_policy() -> None:
    content = GITIGNORE.read_text(encoding="utf-8")

    assert DATA_PATH_POLICY_VERSION == "data-path-policy-v1"
    assert missing_required_ignored_data_patterns(content) == []
    assert prohibited_global_data_ignore_patterns(content) == []
    for pattern in REQUIRED_IGNORED_DATA_PATTERNS:
        assert pattern in content


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
