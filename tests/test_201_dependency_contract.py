from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS_TXT = REPO_ROOT / "requirements.txt"
REQUIREMENTS_LOCK = REPO_ROOT / "requirements.lock"
README = REPO_ROOT / "README.md"
CI_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "ci.yml"
CONTRACT_DOC = REPO_ROOT / "docs" / "operations" / "dependency_contract_201.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_201_requirements_txt_is_authoritative_install_entrypoint() -> None:
    assert REQUIREMENTS_TXT.exists()
    assert REQUIREMENTS_TXT.read_text(encoding="utf-8").strip() == "-r requirements.lock"


def test_201_requirements_lock_is_exactly_pinned() -> None:
    lines = [
        line.strip()
        for line in _text(REQUIREMENTS_LOCK).splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    assert lines
    for line in lines:
        assert "==" in line
        assert not any(marker in line.replace("==", "") for marker in (">=", "<=", "~=", ">", "<"))


def test_201_ci_uses_authoritative_install_entrypoint() -> None:
    workflow = _text(CI_WORKFLOW)
    assert "pip install -r requirements.txt" in workflow
    assert "pip install -r requirements.lock" not in workflow


def test_201_dependency_contract_is_documented() -> None:
    doc = _text(CONTRACT_DOC).replace("`", "")
    assert "requirements.txt is the authoritative install entry point" in doc
    assert "-r requirements.lock" in doc
    assert "pip install -r requirements.txt" in doc
    assert "Security/dependency scan target" in doc


def test_201_readme_mentions_dependency_install_contract() -> None:
    readme = _text(README)
    assert "pip install -r requirements.txt" in readme
    assert "requirements.lock" in readme
