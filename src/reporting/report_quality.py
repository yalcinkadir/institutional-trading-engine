from __future__ import annotations

import re
from dataclasses import dataclass, field

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


@dataclass
class ReportQualityResult:
    report_type: str
    passed: bool
    score: int
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


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


def validate_report_quality(report: str, report_type: str) -> ReportQualityResult:
    errors: list[str] = []
    warnings: list[str] = []
    score = 100

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
            "Risk Tier",
            "Asymmetry Score",
            "Decision",
        ]

        for term in required_terms:
            if term not in report:
                errors.append(f"Missing analytical term: {term}")
                score -= 8

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
    )
