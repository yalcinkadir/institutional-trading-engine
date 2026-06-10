from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SYSTEM_INVARIANTS = REPO_ROOT / "docs" / "architecture" / "system-invariants.md"
LOGIC_SAFETY = REPO_ROOT / "docs" / "operations" / "logic-safety-governance.md"
README = REPO_ROOT / "README.md"
ROADMAP = REPO_ROOT / "ROADMAP.md"
CHANGELOG = REPO_ROOT / "CHANGELOG.md"
PR_TEMPLATE = REPO_ROOT / ".github" / "pull_request_template.md"

REQUIRED_INVARIANTS = [
    "SI-001",
    "SI-002",
    "SI-003",
    "SI-004",
    "SI-005",
    "SI-006",
    "SI-007",
]

REQUIRED_SCHEMA_FIELDS = [
    "id:",
    "name:",
    "rationale:",
    "severity:",
    "affected_layers:",
    "enforced_by:",
    "valid_states:",
    "forbidden_claims:",
    "required_evidence:",
    "exception_policy:",
]

REQUIRED_SEVERITIES = [
    "P0_BLOCKER",
    "P1_DEGRADED",
    "P2_WARNING",
]

REQUIRED_STATES = [
    "PASS",
    "DEGRADED",
    "BLOCKED",
    "FAILED",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_system_invariants_document_exists_and_declares_core_invariants() -> None:
    content = _read(SYSTEM_INVARIANTS)

    missing = [invariant for invariant in REQUIRED_INVARIANTS if invariant not in content]

    assert missing == []
    assert "DEGRADED must never behave like `PASS`" in content
    assert "Logic-safety state matrix" in content


def test_each_invariant_uses_required_machine_checkable_schema_fields() -> None:
    content = _read(SYSTEM_INVARIANTS)

    for invariant in REQUIRED_INVARIANTS:
        match = re.search(
            rf"## {invariant}.*?(?=\n## SI-|\n## Logic-safety state matrix|\Z)",
            content,
            flags=re.DOTALL,
        )
        assert match is not None, f"Missing section for {invariant}"
        section = match.group(0)
        missing_fields = [field for field in REQUIRED_SCHEMA_FIELDS if field not in section]
        assert missing_fields == [], f"{invariant} missing schema fields: {missing_fields}"


def test_severity_and_state_vocabulary_are_documented() -> None:
    content = _read(SYSTEM_INVARIANTS)

    missing_severities = [severity for severity in REQUIRED_SEVERITIES if severity not in content]
    missing_states = [state for state in REQUIRED_STATES if state not in content]

    assert missing_severities == []
    assert missing_states == []


def test_logic_safety_governance_connects_policy_to_automated_evidence() -> None:
    content = _read(LOGIC_SAFETY)

    required_phrases = [
        "Manual checkboxes are not enough",
        "guard test",
        "contract test",
        "validation script",
        "CI workflow result",
        "evidence artifact",
        "Forbidden conversions",
        "Promotion rule",
    ]

    missing = [phrase for phrase in required_phrases if phrase not in content]

    assert missing == []


def test_project_status_files_reference_issue_189_logic_safety_governance() -> None:
    readme = _read(README)
    roadmap = _read(ROADMAP)
    changelog = _read(CHANGELOG)

    assert "#189" in readme and "System Invariants" in readme
    assert "#189" in roadmap and "Logic Safety Governance" in roadmap
    assert "#189" in changelog and "Logic Safety Governance" in changelog


def test_pr_template_requires_logic_safety_mapping_and_evidence_command() -> None:
    content = _read(PR_TEMPLATE)

    required_phrases = [
        "Logic Safety Governance",
        "Affected invariants",
        "SI-___",
        "Evidence / test command",
        "DEGRADED states have explicit forbidden claims",
        "CI evidence gate result",
    ]

    missing = [phrase for phrase in required_phrases if phrase not in content]

    assert missing == []
