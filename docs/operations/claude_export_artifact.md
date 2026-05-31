# Claude Export Artifact Workflow

This document describes how to generate a token-efficient Claude project import package from the repository.

The export is designed for project analysis only. It does not change runtime trading behavior, does not authorize broker execution and must not be treated as evidence of trading edge.

## Generated outputs

Running the exporter creates:

```text
exports/claude/
exports/claude_project_import.zip
```

`exports/` is intentionally ignored by Git because these files are generated artifacts.

## Local usage

```bash
python tools/export_for_claude.py --mode all --area all
```

Useful alternatives:

```bash
python tools/export_for_claude.py --mode lite
python tools/export_for_claude.py --mode focus --area entry_exit_watcher
python tools/export_for_claude.py --mode focus --area risk_governance
python tools/export_for_claude.py --mode focus --area decision_engine
python tools/export_for_claude.py --mode focus --area tests_ci
python tools/export_for_claude.py --mode full
```

## GitHub Actions usage

1. Open the repository in GitHub.
2. Go to **Actions**.
3. Select **Claude Project Export**.
4. Click **Run workflow**.
5. Open the completed workflow run.
6. Download one of the artifacts:
   - `claude-project-import-zip`
   - `claude-project-import-md`

Use the ZIP for a broad Claude project import. Use the Markdown artifact when you want to upload only specific focused files.

## Export modes

| Mode | Purpose |
|---|---|
| `lite` | README, roadmap, dependency and governance context for quick review |
| `focus` | Targeted review areas such as watcher, governance, decision engine, tests/CI or runtime evidence |
| `full` | Full safe source/documentation context |
| `all` | Generates lite, focus and full exports |

## Focus areas

| Area | Purpose |
|---|---|
| `entry_exit_watcher` | Entry/exit lifecycle, watcher and related tests |
| `risk_governance` | Governance, risk, validation and related tests |
| `decision_engine` | Decision/scoring/orchestration and related tests |
| `tests_ci` | Test suite and CI configuration |
| `runtime_evidence` | Runtime evidence manifests and operations documentation |

## Security and hygiene boundaries

The exporter excludes common unsafe or high-noise paths, including:

```text
.env*
secrets/
private/
private_config/
local_config/
private_edge/
external_edge/
data/
evidence/
lockbox/
artifacts/
outputs/
generated/
exports/
logs/
node_modules/
.venv/
```

It also skips common binary/database/archive formats and large files by default.

## Suggested Claude prompt

```text
You are reviewing an institutional trading engine codebase.

Analyze the uploaded project context with focus on:

1. architecture quality
2. deterministic decision logic
3. risk and governance controls
4. entry/exit and watcher edge cases
5. test coverage and missing tests
6. CI/CD reliability
7. auditability
8. production readiness
9. roadmap gaps

Important:
Do not evaluate profitability.
Do not assume that trading signals are profitable.
Do not claim live-trading readiness.
Focus only on software quality, institutional robustness, safety, correctness and maintainability.

Return:
- critical findings
- high-priority fixes
- medium-priority improvements
- roadmap updates
- suggested implementation order
- test cases to add
```
