from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROADMAP = ROOT / "ROADMAP.md"


EXPECTED_EV_ROWS = [
    "| EV1 |",
    "| EV2 |",
    "| EV3 |",
    "| EV4 |",
    "| EV5 |",
    "| EV6 |",
    "| EV7 |",
    "| EV8 |",
    "| EV9 |",
    "| EV10 |",
    "| EV11 |",
    "| EV12 |",
]


def test_roadmap_marks_all_ev_items_done_and_ci_green() -> None:
    roadmap = ROADMAP.read_text(encoding="utf-8")

    for row_prefix in EXPECTED_EV_ROWS:
        matching_rows = [line for line in roadmap.splitlines() if line.startswith(row_prefix)]
        assert matching_rows, f"Missing roadmap row for {row_prefix}"
        assert "Done / CI-green" in matching_rows[0]


def test_roadmap_current_focus_no_longer_points_to_old_ev_next_block() -> None:
    roadmap = ROADMAP.read_text(encoding="utf-8")

    stale_phrases = [
        "EV3-EV6 are the next critical backtest-fidelity block",
        "get EV1-EV2 CI-green",
        "After EV1-EV2 are green",
        "Planned / Next",
    ]

    for phrase in stale_phrases:
        assert phrase not in roadmap

    assert "EV1-EV12 evidence-integrity remediation" in roadmap
    assert "CI runtime simplification" in roadmap
