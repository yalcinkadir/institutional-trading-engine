from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = REPO_ROOT / "requirements.txt"
LOCKFILE = REPO_ROOT / "requirements.lock"
WORKFLOW_REQUIREMENTS = REPO_ROOT / ".github" / "workflows" / "requirements.txt"


def _meaningful_lines(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def test_requirements_txt_delegates_to_lockfile() -> None:
    assert REQUIREMENTS.exists()
    assert _meaningful_lines(REQUIREMENTS) == ["-r requirements.lock"]


def test_requirements_lock_exists_and_has_exact_pins() -> None:
    assert LOCKFILE.exists()

    lines = _meaningful_lines(LOCKFILE)
    assert lines

    for line in lines:
        assert "==" in line, f"Dependency must be exactly pinned: {line}"
        assert ">=" not in line, f"Lower-bound dependency is not reproducible: {line}"
        assert "<=" not in line, f"Upper-bound dependency is not a lock contract: {line}"
        assert "~=" not in line, f"Compatible-release dependency is not a lock contract: {line}"
        assert ">" not in line.replace("==", ""), f"Floating dependency comparator found: {line}"
        assert "<" not in line.replace("==", ""), f"Floating dependency comparator found: {line}"


def test_required_runtime_and_test_dependencies_are_locked() -> None:
    locked = set(_meaningful_lines(LOCKFILE))

    expected = {
        "requests==2.32.3",
        "pandas==2.2.3",
        "pytest==8.3.4",
        "PyYAML==6.0.2",
        "fastapi==0.115.6",
        "uvicorn==0.32.1",
        "httpx==0.28.1",
        "PyJWT==2.10.1",
        "redis==5.2.1",
        "psycopg[binary]==3.2.3",
    }

    assert expected.issubset(locked)


def test_workflow_local_requirements_file_does_not_override_root_lock() -> None:
    if not WORKFLOW_REQUIREMENTS.exists():
        return

    lines = _meaningful_lines(WORKFLOW_REQUIREMENTS)

    # Historically this file was empty. It must remain empty or delegate to the
    # root lockfile; it must not become a second dependency source of truth.
    assert lines in ([], ["-r ../../requirements.lock"])