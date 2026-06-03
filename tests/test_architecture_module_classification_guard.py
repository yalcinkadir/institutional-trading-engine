from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


CLASSIFICATION_PATH = Path("docs/architecture/module_classification.json")
ALLOWED_CLASSIFICATIONS = {
    "connected_runtime",
    "runtime_entrypoint",
    "test_only",
    "experimental",
    "quarantine",
    "delete_candidate",
}
IGNORED_SRC_PATH_PARTS = {
    "__pycache__",
}


def _run_git(args: list[str]) -> str:
    completed = subprocess.run(
        ["git", *args],
        check=True,
        text=True,
        capture_output=True,
    )
    return completed.stdout.strip()


def _current_src_python_modules() -> set[str]:
    return {
        str(path).replace("\\", "/")
        for path in Path("src").rglob("*.py")
        if not any(part in IGNORED_SRC_PATH_PARTS for part in path.parts)
    }


def _base_ref() -> str | None:
    for env_name in ("GITHUB_BASE_REF", "ARCH106_BASE_REF"):
        value = os.environ.get(env_name)
        if value:
            return value
    return None


def _base_src_python_modules() -> set[str]:
    base_ref = _base_ref()
    if not base_ref:
        return _current_src_python_modules()

    try:
        merge_base = _run_git(["merge-base", "HEAD", f"origin/{base_ref}"])
    except subprocess.CalledProcessError:
        return _current_src_python_modules()

    try:
        output = _run_git(["ls-tree", "-r", "--name-only", merge_base, "src"])
    except subprocess.CalledProcessError:
        return set()

    return {
        line.strip()
        for line in output.splitlines()
        if line.strip().endswith(".py")
    }


def _new_src_python_modules() -> set[str]:
    return _current_src_python_modules() - _base_src_python_modules()


def _load_classification() -> dict:
    assert CLASSIFICATION_PATH.exists(), f"Missing architecture classification file: {CLASSIFICATION_PATH}"
    payload = json.loads(CLASSIFICATION_PATH.read_text(encoding="utf-8"))
    assert payload.get("schema_version") == 1
    return payload


def test_arch106_module_classification_file_has_valid_schema() -> None:
    payload = _load_classification()
    allowed = set(payload.get("allowed_classifications", []))
    assert allowed == ALLOWED_CLASSIFICATIONS
    classified = payload.get("classified_modules")
    assert isinstance(classified, dict)

    for module_path, record in classified.items():
        assert module_path.startswith("src/"), module_path
        assert module_path.endswith(".py"), module_path
        assert record.get("classification") in ALLOWED_CLASSIFICATIONS, module_path
        if record.get("classification") in {"connected_runtime", "runtime_entrypoint"}:
            assert record.get("runtime_entrypoint"), module_path
            assert record.get("runtime_execution_proof"), module_path


def test_arch106_new_src_modules_require_explicit_classification() -> None:
    payload = _load_classification()
    classified_modules = set(payload.get("classified_modules", {}))
    new_modules = _new_src_python_modules()
    unclassified = sorted(new_modules - classified_modules)

    assert not unclassified, (
        "ARCH106 blocks new unclassified production modules. "
        "Add each new src/**/*.py file to docs/architecture/module_classification.json "
        "with classification and runtime_execution_proof where applicable. "
        f"Unclassified: {unclassified}"
    )
