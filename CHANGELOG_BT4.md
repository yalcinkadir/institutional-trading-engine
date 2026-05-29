# BT4 Changelog Addendum

## BT4 Backtest Result Quality Gate — 2026-05-29

### Added
- BT4 result quality model in `src/validation/backtest_result_quality_gate.py`.
- Public-safe demo quality cases in `data/demo_backtest_result_quality.json`.
- CLI report generator in `scripts/generate_bt4_quality_report.py`.
- Operational documentation in `docs/operations/bt4_backtest_result_quality_gate.md`.
- README addendum in `README_BT4.md`.
- Dedicated BT4 pull-request workflow in `.github/workflows/bt4-quality.yml`.

### Tests Added
- `tests/test_bt4_backtest_result_quality_gate.py`.

### Improved
- Reported historical results can now be screened for sample size, drawdown, expectancy, profit factor, Sharpe, loss rate and regime concentration.
- BT4 complements BT3 by checking quality after reproducibility.
- Generated BT4 reports remain research/paper-observation only.

### Boundary
- BT4 is a quality screen for continued research observation.
- It does not prove long-term edge or replace forward observation.
