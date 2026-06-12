from __future__ import annotations

import ast
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_ALLOWLIST_PATH = Path("docs/architecture/broad_exception_allowlist.json")
ACTIVE_PATHS = (
    Path("src/cache/redis_cache.py"),
    Path("src/historical/polygon_ingestion.py"),
    Path("src/macro/vix_adapter.py"),
    Path("src/persistence/atomic_write.py"),
    Path("src/reporting/market_regime.py"),
    Path("src/runtime/runtime_loop.py"),
    Path("src/outcome_tracking.py"),
)


@dataclass(frozen=True)
class BroadExceptionHandler:
    path: str
    function: str
    lineno: int

    @property
    def key(self) -> tuple[str, str]:
        return (self.path, self.function)


class _BroadExceptionVisitor(ast.NodeVisitor):
    def __init__(self, path: Path) -> None:
        self.path = path
        self.scope: list[str] = []
        self.handlers: list[BroadExceptionHandler] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.scope.append(node.name)
        self.generic_visit(node)
        self.scope.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.scope.append(node.name)
        self.generic_visit(node)
        self.scope.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
        self.scope.append(node.name)
        self.generic_visit(node)
        self.scope.pop()

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> Any:
        if _is_broad_exception_handler(node):
            self.handlers.append(
                BroadExceptionHandler(
                    path=self.path.as_posix(),
                    function=".".join(self.scope) if self.scope else "<module>",
                    lineno=node.lineno,
                )
            )
        self.generic_visit(node)


def _is_broad_exception_handler(node: ast.ExceptHandler) -> bool:
    if node.type is None:
        return True
    if isinstance(node.type, ast.Name):
        return node.type.id in {"Exception", "BaseException"}
    if isinstance(node.type, ast.Attribute):
        return node.type.attr in {"Exception", "BaseException"}
    return False


def discover_broad_exception_handlers(paths: tuple[Path, ...] = ACTIVE_PATHS) -> list[BroadExceptionHandler]:
    handlers: list[BroadExceptionHandler] = []
    for path in paths:
        if not path.exists():
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        visitor = _BroadExceptionVisitor(path)
        visitor.visit(tree)
        handlers.extend(visitor.handlers)
    return handlers


def load_allowlist(path: Path = DEFAULT_ALLOWLIST_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def allowlist_entries(path: Path = DEFAULT_ALLOWLIST_PATH) -> list[dict[str, Any]]:
    payload = load_allowlist(path)
    entries = payload.get("entries", [])
    if not isinstance(entries, list):
        raise ValueError("allowlist entries must be a list")
    return entries


def validate_allowlist_contract(path: Path = DEFAULT_ALLOWLIST_PATH) -> list[str]:
    payload = load_allowlist(path)
    required = tuple(payload.get("required_fields", ()))
    errors: list[str] = []
    seen: set[tuple[str, str]] = set()
    for index, entry in enumerate(allowlist_entries(path)):
        if not isinstance(entry, dict):
            errors.append(f"entry[{index}] is not an object")
            continue
        missing = [field for field in required if not str(entry.get(field) or "").strip()]
        if missing:
            errors.append(f"entry[{index}] missing fields: {','.join(missing)}")
        key = (str(entry.get("path")), str(entry.get("function")))
        if key in seen:
            errors.append(f"duplicate allowlist entry: {key[0]}::{key[1]}")
        seen.add(key)
    return errors


def validate_active_broad_exception_handlers(
    *,
    allowlist_path: Path = DEFAULT_ALLOWLIST_PATH,
    active_paths: tuple[Path, ...] = ACTIVE_PATHS,
) -> list[str]:
    errors = validate_allowlist_contract(allowlist_path)
    allowed = {
        (str(entry.get("path")), str(entry.get("function")))
        for entry in allowlist_entries(allowlist_path)
        if isinstance(entry, dict)
    }
    for handler in discover_broad_exception_handlers(active_paths):
        if handler.key not in allowed:
            errors.append(
                f"unallowlisted broad exception: {handler.path}:{handler.lineno}::{handler.function}"
            )
    return errors


def main() -> int:
    errors = validate_active_broad_exception_handlers()
    if errors:
        print("Broad exception policy check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Broad exception policy check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
