from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

REQUIRED_SECTIONS = {
    "premarket": [
        "# Institutional Trading Engine — PREMARKET REPORT",
        "## Market Regime",
        "### Core Market Metrics",
        "### Market Breadth",
        "### Focus Areas",
        "## Decision Engine",
        "### Active Strategy Types",
        "### Decision Summary",
        "### Ranked Opportunities",
        "## Pre-Market Watchlist",
        "### Watchlist",
        "### Objectives",
        "### Warnings",
        "### Notes",
    ],
    "postmarket": [
        "# Institutional Trading Engine — POSTMARKET REPORT",
        "## Market Regime",
        "### Core Market Metrics",
        "### Market Breadth",
        "### Focus Areas",
        "## Decision Engine",
        "### Active Strategy Types",
        "### Decision Summary",
        "### Ranked Opportunities",
        "## Post-Market Review",
        "### Watchlist",
        "### Objectives",
        "### Warnings",
        "### Notes",
    ],
    "weekly": [
        "# Institutional Trading Engine — WEEKLY REPORT",
        "## Weekly Summary",
        "### Recommended Assets",
        "### Focus For Next Week",
        "### Risk Notes",
    ],
}

FORBIDDEN_WEAK_PHRASES = [
    "PENDING_LIVE_DATA",
    "Bullish / Neutral / Defensive",
    "TODO",
    "tbd",
    "lorem ipsum",
]

ENGLISH_MARKERS = [
    "market",
    "regime",
    "watchlist",
    "risk",
    "breadth",
    "score",
    "generated",
    "leaders",
    "weak names",
]

GERMAN_MARKERS = [
    "börse",
    "marktbreite",
    "risiko",
    "empfehlung",
    "analyse",
    "woche",
]

ALLOWED_RISK_TIERS = {"tier_1", "tier_2", "tier_3", "no_trade"}
ACTIONABLE_DECISIONS = {"approved", "reduced_size", "watch"}
NON_ACTIONABLE_DECISIONS = {"blocked", "no_trade"}
VALID_DECISIONS = ACTIONABLE_DECISIONS | NON_ACTIONABLE_DECISIONS
RISK_TIER_DECISION_LINE_RE = re.compile(
    r"^-\s*Decision:\s*\*\*(?P<decision>[a-z_]+)\*\*\s*\|\s*Risk Tier:\s*(?P<tier>[a-zA-Z0-9_ -]+)\s*$",
    re.MULTILINE,
)
EXPLICIT_NO_ACTIVE_RISK_MARKERS = (
    "No ranked opportunities qualified for active risk",
    "No-Trade / watch mode",
)


@dataclass
class ReportQualityResult:
    report_type: str
    passed: bool
    score: int
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    risk_tier_evidence: dict[str, Any] = field(default_factory=dict)


def _word_count(report: str) -> int:
    return len(re.findall(r"\b\w+\b", report))


def _detect_language(report: str) -> str:
    lower = report.lower()
    english_hits = sum(1 for marker in ENGLISH_MARKERS if marker in lower)
    german_hits = sum(1 for marker in GERMAN_MARKERS if marker in lower)

    if english_hits > german_hits:
        return "en"
    if german_hits > english_hits:
        return "de"
    return "unknown"


def _normalize_risk_tier(value: str) -> str:
    return str(value).strip().lower().replace(" ", "_").replace("-", "_")


def _validate_risk_tier_evidence(report: str) -> tuple[dict[str, Any], list[str]]:
    """Validate #185 market-report risk-tier evidence.

    The old gate only checked whether the literal text `Risk Tier` appeared in the
    rendered report. That was both too weak and too brittle: a prose mention could
    pass, while a valid no-trade report with no active ranked opportunity could
    fail. This validator accepts either machine-readable decision/risk-tier rows
    or an explicit no-active-risk/no-trade state, and blocks malformed tier rows.
    """

    errors: list[str] = []
    decision_rows: list[dict[str, str]] = []
    invalid_decisions: list[str] = []
    invalid_tiers: list[str] = []

    for match in RISK_TIER_DECISION_LINE_RE.finditer(report):
        decision = match.group("decision").strip().lower()
        tier = _normalize_risk_tier(match.group("tier"))
        row = {"decision": decision, "risk_tier": tier}
        decision_rows.append(row)
        if decision not in VALID_DECISIONS:
            invalid_decisions.append(decision)
        if tier not in ALLOWED_RISK_TIERS:
            invalid_tiers.append(tier)
        if decision in ACTIONABLE_DECISIONS and tier == "no_trade":
            errors.append(f"Actionable decision `{decision}` cannot carry `no_trade` risk tier.")
        if decision in NON_ACTIONABLE_DECISIONS and tier != "no_trade":
            errors.append(f"Non-actionable decision `{decision}` must carry `no_trade` risk tier.")

    explicit_no_active_risk = all(marker in report for marker in EXPLICIT_NO_ACTIVE_RISK_MARKERS)

    if invalid_decisions:
        errors.append(f"Invalid decision values in risk-tier rows: {sorted(set(invalid_decisions))}")
    if invalid_tiers:
        errors.append(f"Invalid risk tier values: {sorted(set(invalid_tiers))}")

    if not decision_rows and not explicit_no_active_risk:
        if "Risk Tier" in report:
            errors.append("Risk Tier evidence is present only as prose; expected machine-readable decision/risk-tier rows.")
        else:
            errors.append("Missing report risk-tier evidence: no decision/risk-tier rows and no explicit no-active-risk state.")

    status = "PASS" if not errors else "BLOCKED"
    if not decision_rows and explicit_no_active_risk:
        status = "PASS_NO_ACTIVE_RISK"

    evidence = {
        "schema_version": "report_validation_risk_tier.v1",
        "issue": "#185",
        "status": status,
        "decision_risk_tier_rows": decision_rows,
        "decision_risk_tier_row_count": len(decision_rows),
        "explicit_no_active_risk": explicit_no_active_risk,
        "allowed_risk_tiers": sorted(ALLOWED_RISK_TIERS),
    }
    return evidence, errors


def validate_report_quality(report: str, report_type: str) -> ReportQualityResult:
    errors: list[str] = []
    warnings: list[str] = []
    score = 100
    risk_tier_evidence: dict[str, Any] = {}

    normalized_type = report_type.lower().strip()

    if normalized_type not in REQUIRED_SECTIONS:
        errors.append(f"Unsupported report type: {report_type}")
        return ReportQualityResult(report_type, False, 0, errors, warnings)

    for section in REQUIRED_SECTIONS[normalized_type]:
        if section not in report:
            errors.append(f"Missing required section: {section}")
            score -= 10

    for phrase in FORBIDDEN_WEAK_PHRASES:
        if phrase.lower() in report.lower():
            errors.append(f"Forbidden weak placeholder found: {phrase}")
            score -= 15

    words = _word_count(report)
    if normalized_type in {"premarket", "postmarket"}:
        if words < 150:
            errors.append(f"Report is too short: {words} words")
            score -= 20
        if words > 1200:
            warnings.append(f"Report may be too long for Telegram: {words} words")
            score -= 5
    else:
        if words < 40:
            errors.append(f"Weekly report is too short: {words} words")
            score -= 20
        if words > 1200:
            warnings.append(f"Weekly report may be too long: {words} words")
            score -= 5

    detected_language = _detect_language(report)
    if detected_language == "unknown":
        warnings.append("Report language could not be detected confidently")
        score -= 5

    if "DATA_UNAVAILABLE" in report or "Data Status: FALLBACK" in report:
        warnings.append("Report used fallback data; content is structurally valid but not analytically strong")
        score -= 15

    if normalized_type in {"premarket", "postmarket"}:
        required_terms = [
            "SPY",
            "QQQ",
            "VIX",
            "SMA50",
            "SMA200",
            "ATR14",
            "Market Health Score",
            "Market State",
            "Asymmetry Score",
            "Decision",
        ]

        for term in required_terms:
            if term not in report:
                errors.append(f"Missing analytical term: {term}")
                score -= 8

        risk_tier_evidence, risk_tier_errors = _validate_risk_tier_evidence(report)
        for error in risk_tier_errors:
            errors.append(error)
            score -= 12

        optional_quality_terms = [
            "Relative Strength",
            "Trade Summary",
            "Portfolio Heat Limit",
            "No-Trade",
            "Hard Overrides",
            "Regime Alignment",
        ]

        quality_hits = sum(1 for term in optional_quality_terms if term in report)
        if quality_hits >= 3:
            score += 8
        elif quality_hits <= 1:
            warnings.append("Decision-engine quality markers are weak")
            score -= 8

    score = max(score, 0)
    passed = not errors and score >= 75

    return ReportQualityResult(
        report_type=normalized_type,
        passed=passed,
        score=score,
        errors=errors,
        warnings=warnings,
        risk_tier_evidence=risk_tier_evidence,
    )
