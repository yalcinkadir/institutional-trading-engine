from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ALLOWED_CI_WIRED_MARKERS = (
    "Phase B1.1",
    "Phase EV1-EV2",
    "IP5/IP6",
    "IP9/IP10",
    "CL1",
    "CL2",
    "CL3",
    "CL4",
    "CL5",
    "TG2/TG3",
    "TG2 |",
    "TG3 |",
)

CHECKED_DOCUMENTS = (
    "README.md",
    "ROADMAP.md",
)


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _ci_wired_lines(path: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    for line_number, line in enumerate(_read(path).splitlines(), start=1):
        if "CI-wired" in line:
            lines.append((line_number, line))
    return lines


def test_ci_wired_statuses_are_explicitly_allowlisted_after_rgp_closure() -> None:
    unexpected: list[str] = []

    for path in CHECKED_DOCUMENTS:
        for line_number, line in _ci_wired_lines(path):
            if not any(marker in line for marker in ALLOWED_CI_WIRED_MARKERS):
                unexpected.append(f"{path}:{line_number}: {line}")

    assert unexpected == []


def test_no_rgp_status_is_left_ci_wired_after_rgp_closure() -> None:
    for path in CHECKED_DOCUMENTS:
        for line_number, line in _ci_wired_lines(path):
            assert "RGP" not in line, f"{path}:{line_number}: {line}"
