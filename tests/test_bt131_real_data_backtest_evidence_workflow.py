from __future__ import annotations

from pathlib import Path

WORKFLOW_PATH = Path(".github/workflows/bt131_real_data_backtest_evidence.yml")


def _workflow_text() -> str:
    return WORKFLOW_PATH.read_text(encoding="utf-8")


def test_bt131_workflow_exists_and_supports_manual_dispatch() -> None:
    text = _workflow_text()

    assert WORKFLOW_PATH.exists()
    assert "workflow_dispatch:" in text
    for input_name in ("symbols", "start_date", "end_date", "run_id", "strategy_version", "plans_file", "source_observations"):
        assert f"{input_name}:" in text


def test_bt131_workflow_uses_python_311_and_repo_write_for_report_persistence() -> None:
    text = _workflow_text()

    assert "python-version: \"3.11\"" in text
    assert "permissions:" in text
    assert "contents: write" in text
    assert "concurrency:" in text
    assert "group: repo-write-${{ github.ref }}" in text
    assert "cancel-in-progress: false" in text
    assert "persist-credentials: true" in text
    assert "PYTHONPATH: ${{ github.workspace }}" in text


def test_bt131_workflow_orchestrates_real_data_gates_in_order() -> None:
    text = _workflow_text()

    ingestion = text.index("Ingest historical Polygon bars when API key is available")
    runtime_universe = text.index("Build BT131 runtime universe from ingested coverage")
    observation_export = text.index("Export pipeline-coupled trade plans from validated observations")
    missing_observations = text.index("Block BT131 when validated observations are absent")
    bt9 = text.index("Run BT9 input-pack gate")
    runner = text.index("Run real-data historical entry/exit backtest")
    gate = text.index("Validate accepted real-data evidence when backtest passed")
    bt132 = text.index("Generate BT132 strategy improvement reports")
    bt133 = text.index("Generate BT133 entry confirmation variant reports")
    bt134 = text.index("Generate BT134 stop-loss variant reports")
    bt139 = text.index("Generate BT139 sample expansion reports")
    bt176 = text.index("Generate BT176 guarded entry confirmation experiment reports")
    persist = text.index("Persist validated backtest reports and source inputs to repository")

    assert ingestion < runtime_universe < observation_export < missing_observations < bt9 < runner < gate < bt132 < bt133 < bt134 < bt139 < bt176 < persist
    assert "scripts/ingest_historical_polygon.py" in text
    assert "scripts/build_bt131_runtime_universe.py" in text
    assert "scripts/export_historical_trade_plans.py" in text
    assert "scripts/generate_historical_trade_plans.py" not in text
    assert "scripts/validate_bt9_real_historical_input_pack.py" in text
    assert "scripts/run_historical_entry_exit_backtest.py" in text
    assert "scripts/validate_real_data_backtest_evidence_gate.py" in text
    assert "scripts/analyze_bt132_strategy_improvement.py" in text
    assert "scripts/analyze_bt133_entry_confirmation_variants.py" in text
    assert "scripts/analyze_bt134_stop_loss_variants.py" in text
    assert "scripts/analyze_bt139_bt131_sample_expansion.py" in text
    assert "scripts/analyze_bt176_guarded_entry_confirmation_experiment.py" in text


def test_bt131_workflow_builds_and_uses_runtime_universe() -> None:
    text = _workflow_text()

    assert "runtime_universe=\"data/historical/metadata/bt131_runtime_universe.csv\"" in text
    assert "coverage_manifest=\"data/historical/metadata/coverage_manifest.json\"" in text
    assert "--coverage-manifest \"${{ steps.runtime.outputs.coverage_manifest }}\"" in text
    assert "--output \"${{ steps.runtime.outputs.runtime_universe }}\"" in text
    assert "bt131-runtime-universe.json" in text
    assert "--universe \"${{ steps.runtime.outputs.runtime_universe }}\"" in text
    assert "data/historical/metadata/*.csv" in text
    assert "--universe data/universe/survivorship_universe.csv" not in text


def test_bt131_workflow_requires_validated_observations_for_trade_plan_export() -> None:
    text = _workflow_text()

    assert "Export pipeline-coupled trade plans from validated observations" in text
    assert "if: ${{ inputs.source_observations != '' }}" in text
    assert "scripts/export_historical_trade_plans.py" in text
    assert "--source \"${{ steps.runtime.outputs.source_observations }}\"" in text
    assert "--output \"${{ steps.runtime.outputs.plans_file }}\"" in text
    assert "historical_trade_plan_export_exit_code" in text


def test_bt131_workflow_blocks_real_data_evidence_when_validated_observations_are_absent() -> None:
    text = _workflow_text()

    assert "Block BT131 when validated observations are absent" in text
    assert "if: ${{ inputs.source_observations == '' }}" in text
    assert "BLOCKED_MISSING_VALIDATED_OBSERVATIONS" in text
    assert "missing_validated_observations_for_pipeline_coupled_backtest" in text
    assert "source_observations is required for pipeline-coupled BT131 real-data evidence" in text
    assert '"input_checksums": {}' in text
    assert "historical_trade_plan_generation_exit_code" not in text
    assert "bt131-generated-trade-plans.json" not in text


def test_bt131_workflow_forces_real_data_and_blocks_demo_claims() -> None:
    text = _workflow_text()

    assert "--real-data" in text
    assert "--data-source real_data" in text
    assert "data_source=real_data" in text
    assert "must not be demo" in text
    assert "historical_demo" not in text


def test_bt131_workflow_accepts_blocked_artifact_path_without_fake_success() -> None:
    text = _workflow_text()

    assert "Backtest did not pass; expecting explicit BLOCKED evidence artifact." in text
    assert "test -f reports/backtests/real-data-backtest-evidence.json" in text
    assert "run_health_status" in text
    assert "input_pack_gate_status" in text


def test_bt131_workflow_requires_input_checksums_for_accepted_input_pack() -> None:
    text = _workflow_text()

    assert "input_checksums" in text
    assert "BT131 accepted input pack must include input_checksums" in text
    assert "input_checksum_count" in text
    assert "input_checksums = evidence.get(\"input_checksums\", {})" in text
    assert "BT131 input checksums:" in text


def test_bt131_workflow_generates_bt132_strategy_improvement_report() -> None:
    text = _workflow_text()

    assert "Generate BT132 strategy improvement reports" in text
    assert "scripts/analyze_bt132_strategy_improvement.py" in text
    assert "--evidence reports/backtests/real-data-backtest-evidence.json" in text
    assert "--output-json reports/backtests/bt132-strategy-improvement-report.json" in text
    assert "--output-md reports/backtests/bt132-strategy-improvement-report.md" in text


def test_bt131_workflow_generates_bt133_entry_confirmation_variants() -> None:
    text = _workflow_text()

    assert "Generate BT133 entry confirmation variant reports" in text
    assert "scripts/analyze_bt133_entry_confirmation_variants.py" in text
    assert "--output-json reports/backtests/bt133-entry-confirmation-variant-report.json" in text
    assert "--output-md reports/backtests/bt133-entry-confirmation-variant-report.md" in text


def test_bt131_workflow_generates_bt134_stop_loss_variants() -> None:
    text = _workflow_text()

    assert "Generate BT134 stop-loss variant reports" in text
    assert "scripts/analyze_bt134_stop_loss_variants.py" in text
    assert "--output-json reports/backtests/bt134-stop-loss-variant-report.json" in text
    assert "--output-md reports/backtests/bt134-stop-loss-variant-report.md" in text


def test_bt131_workflow_generates_bt139_sample_expansion_report() -> None:
    text = _workflow_text()

    assert "Generate BT139 sample expansion reports" in text
    assert "scripts/analyze_bt139_bt131_sample_expansion.py" in text
    assert "--output-json reports/backtests/bt139-bt131-sample-expansion-report.json" in text
    assert "--output-md reports/backtests/bt139-bt131-sample-expansion-report.md" in text


def test_bt131_workflow_generates_bt176_guarded_entry_confirmation_experiment() -> None:
    text = _workflow_text()

    assert "Generate BT176 guarded entry confirmation experiment reports" in text
    assert "scripts/analyze_bt176_guarded_entry_confirmation_experiment.py" in text
    assert "--variant-report reports/backtests/bt133-entry-confirmation-variant-report.json" in text
    assert "--candidate-variant-id next_bar_close_confirmation_1bar" in text
    assert "--output-json reports/backtests/bt133-guarded-entry-confirmation-experiment.json" in text
    assert "--output-md reports/backtests/bt133-guarded-entry-confirmation-experiment.md" in text


def test_bt131_workflow_persists_validated_reports_and_inputs_to_repo_without_telegram() -> None:
    text = _workflow_text()

    assert "Persist validated backtest reports and source inputs to repository" in text
    assert "reports/backtests/real_data/runs/${GITHUB_RUN_ID_VALUE}" in text
    assert "reports/backtests/real_data/latest" in text
    assert "reports/backtests/real_data/index.json" in text
    assert "bt132-strategy-improvement-report.json" in text
    assert "bt132-strategy-improvement-report.md" in text
    assert "bt133-entry-confirmation-variant-report.json" in text
    assert "bt133-entry-confirmation-variant-report.md" in text
    assert "bt134-stop-loss-variant-report.json" in text
    assert "bt134-stop-loss-variant-report.md" in text
    assert "bt139-bt131-sample-expansion-report.json" in text
    assert "bt139-bt131-sample-expansion-report.md" in text
    assert "bt133-guarded-entry-confirmation-experiment.json" in text
    assert "bt133-guarded-entry-confirmation-experiment.md" in text
    assert "historical_trade_plans_manifest.json" in text
    assert "bt132_review_status" in text
    assert "bt132_recommendation_count" in text
    assert "bt133_final_recommendation" in text
    assert "bt134_final_recommendation" in text
    assert "bt134_variant_count" in text
    assert "bt134_production_rule_change_allowed" in text
    assert "bt139_evidence_quality" in text
    assert "bt139_promotion_allowed" in text
    assert "bt139_trade_count" in text
    assert "bt139_symbol_count" in text
    assert "bt139_signal_day_count" in text
    assert "bt139_production_rule_change_allowed" in text
    assert "bt176_guard_status" in text
    assert "bt176_candidate_variant_id" in text
    assert "bt176_experiment_scope" in text
    assert "bt176_production_rule_change_allowed" in text
    assert "git pull --rebase" in text
    assert "git add reports/backtests/real_data/" in text
    assert "git add data/historical/bars/1day/*.csv data/historical/metadata/*.json data/historical/metadata/*.csv data/trade_plans/*.json data/trade_plans/*manifest*.json" in text
    assert "git commit -m \"Persist BT131 real-data backtest reports and source inputs" in text
    assert "git push" in text
    assert text.index("git pull --rebase") < text.index('report_dir="reports/backtests/real_data/runs/${GITHUB_RUN_ID_VALUE}"')
    assert "TELEGRAM_BOT_TOKEN" not in text
    assert "sendMessage" not in text
    assert "telegram" not in text.lower()


def test_bt131_workflow_uploads_reviewable_evidence_artifacts() -> None:
    text = _workflow_text()

    assert "actions/upload-artifact@v4" in text
    assert "bt131-real-data-backtest-evidence" in text
    assert "reports/backtests/*.json" in text
    assert "reports/backtests/*.md" in text
    assert "reports/backtests/real_data/**/*.json" in text
    assert "reports/backtests/real_data/**/*.md" in text
    assert "reports/backtests/real_data/**/*.csv" in text
    assert "data/historical/bars/1day/*.csv" in text
    assert "data/historical/metadata/*.json" in text
    assert "data/historical/metadata/*.csv" in text
    assert "data/trade_plans/*.json" in text
    assert "data/trade_plans/*manifest*.json" in text
    assert "retention-days: 90" in text


def test_bt131_workflow_preserves_research_only_safety_boundary() -> None:
    text = _workflow_text()

    assert "live_trading_authorized" in text
    assert "broker_execution_mode" in text
    assert "paper_only" in text
    assert "production_rule_change_allowed" in text
    forbidden_tokens = (
        "alpaca_api_key",
        "alpaca_secret",
        "broker_secret",
        "broker_execution_mode=live",
        "live_trading_authorized=true",
        "production_rule_change_allowed=true",
    )
    lower = text.lower()
    for token in forbidden_tokens:
        assert token not in lower
