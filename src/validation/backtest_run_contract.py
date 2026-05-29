"""BT3 backtest run contract validation.

Validates whether a historical validation result can be reproduced from pinned
inputs, versions, symbols, dates, seed and artifact fingerprints.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

RESEARCH_ONLY_FOOTER = "Research / Paper Observation Only. Execution is not authorized by this report."

_COMMIT_SHA_PATTERN = re.compile(r"^[0-9a-f]{7,40}$")
_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_REQUIRED_METRICS = ("total_return_pct", "max_drawdown_pct", "sharpe", "win_rate_pct", "trade_count")
_REQUIRED_ARTIFACTS = ("input_manifest", "result_summary")
_PUBLIC_SAFE_TAG = "public_safe"
_DEMO_TAG = "demo"


@dataclass(frozen=True)
class BacktestRunContractConfig:
    required_metrics: tuple[str, ...] = _REQUIRED_METRICS
    required_artifacts: tuple[str, ...] = _REQUIRED_ARTIFACTS
    allowed_data_modes: tuple[str, ...] = ("synthetic", "paper_observation", "historical_demo")
    allowed_execution_models: tuple[str, ...] = ("close_only", "next_bar_open", "paper_fill_model")
    min_symbols: int = 1
    require_seed: bool = True
    require_determinism: bool = True
    require_public_safe_tags: bool = True
    require_research_footer: bool = True


@dataclass(frozen=True)
class BacktestArtifactReference:
    name: str
    path: str
    sha256: str

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "BacktestArtifactReference":
        return cls(
            name=str(payload.get("name", "")).strip(),
            path=str(payload.get("path", "")).strip(),
            sha256=str(payload.get("sha256", "")).strip(),
        )

    def to_dict(self) -> dict[str, str]:
        return {"name": self.name, "path": self.path, "sha256": self.sha256}


@dataclass(frozen=True)
class BacktestRunContract:
    run_id: str
    strategy_id: str
    strategy_version: str
    code_commit_sha: str
    parameter_version: str
    dataset_id: str
    dataset_fingerprint: str
    symbols: tuple[str, ...]
    start_date: str
    end_date: str
    data_mode: str
    execution_model: str
    seed: int | None
    deterministic: bool
    metrics: Mapping[str, float | int]
    artifacts: tuple[BacktestArtifactReference, ...]
    tags: tuple[str, ...] = (_DEMO_TAG, _PUBLIC_SAFE_TAG)
    notes: str = ""
    footer: str = RESEARCH_ONLY_FOOTER

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "BacktestRunContract":
        seed_value = payload.get("seed")
        return cls(
            run_id=str(payload.get("run_id", "")).strip(),
            strategy_id=str(payload.get("strategy_id", "")).strip(),
            strategy_version=str(payload.get("strategy_version", "")).strip(),
            code_commit_sha=str(payload.get("code_commit_sha", "")).strip().lower(),
            parameter_version=str(payload.get("parameter_version", "")).strip(),
            dataset_id=str(payload.get("dataset_id", "")).strip(),
            dataset_fingerprint=str(payload.get("dataset_fingerprint", "")).strip(),
            symbols=tuple(str(symbol).strip().upper() for symbol in payload.get("symbols", [])),
            start_date=str(payload.get("start_date", "")).strip(),
            end_date=str(payload.get("end_date", "")).strip(),
            data_mode=str(payload.get("data_mode", "")).strip(),
            execution_model=str(payload.get("execution_model", "")).strip(),
            seed=None if seed_value is None else int(seed_value),
            deterministic=bool(payload.get("deterministic", False)),
            metrics=dict(payload.get("metrics", {})),
            artifacts=tuple(BacktestArtifactReference.from_mapping(item) for item in payload.get("artifacts", [])),
            tags=tuple(str(tag).strip() for tag in payload.get("tags", (_DEMO_TAG, _PUBLIC_SAFE_TAG))),
            notes=str(payload.get("notes", "")).strip(),
            footer=str(payload.get("footer", RESEARCH_ONLY_FOOTER)).strip(),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "strategy_id": self.strategy_id,
            "strategy_version": self.strategy_version,
            "code_commit_sha": self.code_commit_sha,
            "parameter_version": self.parameter_version,
            "dataset_id": self.dataset_id,
            "dataset_fingerprint": self.dataset_fingerprint,
            "symbols": list(self.symbols),
            "start_date": self.start_date,
            "end_date": self.end_date,
            "data_mode": self.data_mode,
            "execution_model": self.execution_model,
            "seed": self.seed,
            "deterministic": self.deterministic,
            "metrics": dict(self.metrics),
            "artifacts": [artifact.to_dict() for artifact in self.artifacts],
            "tags": list(self.tags),
            "notes": self.notes,
            "footer": self.footer,
        }


@dataclass(frozen=True)
class BacktestRunContractMetrics:
    run_count: int
    strategy_count: int
    dataset_count: int
    symbol_count: int
    deterministic_runs: int
    seeded_runs: int
    metric_coverage_pct: float
    artifact_coverage_pct: float
    unique_contract_fingerprints: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_count": self.run_count,
            "strategy_count": self.strategy_count,
            "dataset_count": self.dataset_count,
            "symbol_count": self.symbol_count,
            "deterministic_runs": self.deterministic_runs,
            "seeded_runs": self.seeded_runs,
            "metric_coverage_pct": round(self.metric_coverage_pct, 2),
            "artifact_coverage_pct": round(self.artifact_coverage_pct, 2),
            "unique_contract_fingerprints": self.unique_contract_fingerprints,
        }


@dataclass(frozen=True)
class BacktestRunContractGate:
    name: str
    passed: bool
    message: str
    failures: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "passed": self.passed, "message": self.message, "failures": list(self.failures)}


@dataclass(frozen=True)
class BacktestRunContractReport:
    version: str
    generated_at: str
    contracts: tuple[BacktestRunContract, ...]
    metrics: BacktestRunContractMetrics
    gates: tuple[BacktestRunContractGate, ...]
    passed: bool
    footer: str = RESEARCH_ONLY_FOOTER

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "generated_at": self.generated_at,
            "passed": self.passed,
            "metrics": self.metrics.to_dict(),
            "gates": [gate.to_dict() for gate in self.gates],
            "contracts": [contract.to_dict() for contract in self.contracts],
            "footer": self.footer,
        }


def build_backtest_run_contract_report(
    contracts: Sequence[BacktestRunContract | Mapping[str, Any]],
    *,
    config: BacktestRunContractConfig | None = None,
    version: str = "BT3-v1",
    generated_at: str | None = None,
) -> BacktestRunContractReport:
    policy = config or BacktestRunContractConfig()
    normalized = tuple(contract if isinstance(contract, BacktestRunContract) else BacktestRunContract.from_mapping(contract) for contract in contracts)
    metrics = _build_metrics(normalized, policy)
    gates = _build_gates(normalized, policy)
    return BacktestRunContractReport(
        version=version,
        generated_at=generated_at or datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        contracts=normalized,
        metrics=metrics,
        gates=gates,
        passed=all(gate.passed for gate in gates),
    )


def load_backtest_run_contracts_json(path: str | Path) -> tuple[BacktestRunContract, ...]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    raw_contracts = payload.get("contracts", payload.get("runs", [])) if isinstance(payload, Mapping) else payload
    if not isinstance(raw_contracts, list):
        raise ValueError("Backtest run contract JSON must contain a list, 'contracts' or 'runs'.")
    return tuple(BacktestRunContract.from_mapping(item) for item in raw_contracts)


def demo_backtest_run_contracts() -> tuple[BacktestRunContract, ...]:
    return tuple(BacktestRunContract.from_mapping(payload) for payload in _demo_payloads())


def render_backtest_run_contract_markdown(report: BacktestRunContractReport) -> str:
    lines = [
        "# BT3 Backtest Run Contract Report",
        "",
        f"Generated at: `{report.generated_at}`",
        f"Overall status: `{'PASS' if report.passed else 'FAIL'}`",
        "",
        "## Metrics",
        "",
        "| Metric | Value |",
        "|---|---:|",
    ]
    for key, value in report.metrics.to_dict().items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(["", "## Gates", "", "| Gate | Status | Message |", "|---|---|---|"])
    for gate in report.gates:
        status = "PASS" if gate.passed else "FAIL"
        message = gate.message if not gate.failures else f"{gate.message} Failures: {'; '.join(gate.failures)}"
        lines.append(f"| `{gate.name}` | `{status}` | {message} |")
    lines.extend(["", "## Contracts", "", "| Run | Strategy | Dataset | Dates | Seed | Deterministic | Data Mode | Execution Model |", "|---|---|---|---|---:|---|---|---|"])
    for contract in report.contracts:
        lines.append(f"| `{contract.run_id}` | `{contract.strategy_id}` | `{contract.dataset_id}` | {contract.start_date} to {contract.end_date} | {contract.seed} | {contract.deterministic} | `{contract.data_mode}` | `{contract.execution_model}` |")
    lines.extend(["", "---", "", report.footer, ""])
    return "\n".join(lines)


def write_backtest_run_contract_report(report: BacktestRunContractReport, *, output_json: str | Path, output_md: str | Path) -> None:
    json_path = Path(output_json)
    md_path = Path(output_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_backtest_run_contract_markdown(report), encoding="utf-8")


def _build_metrics(contracts: Sequence[BacktestRunContract], policy: BacktestRunContractConfig) -> BacktestRunContractMetrics:
    metric_slots = max(1, len(contracts) * len(policy.required_metrics))
    artifact_slots = max(1, len(contracts) * len(policy.required_artifacts))
    present_metrics = sum(1 for contract in contracts for metric in policy.required_metrics if metric in contract.metrics)
    present_artifacts = sum(1 for contract in contracts for name in policy.required_artifacts if name in {artifact.name for artifact in contract.artifacts})
    symbols = {symbol for contract in contracts for symbol in contract.symbols}
    fingerprints = {_contract_fingerprint(contract) for contract in contracts}
    return BacktestRunContractMetrics(
        run_count=len(contracts),
        strategy_count=len({contract.strategy_id for contract in contracts if contract.strategy_id}),
        dataset_count=len({contract.dataset_id for contract in contracts if contract.dataset_id}),
        symbol_count=len(symbols),
        deterministic_runs=sum(1 for contract in contracts if contract.deterministic),
        seeded_runs=sum(1 for contract in contracts if contract.seed is not None),
        metric_coverage_pct=present_metrics / metric_slots * 100.0,
        artifact_coverage_pct=present_artifacts / artifact_slots * 100.0,
        unique_contract_fingerprints=len(fingerprints),
    )


def _build_gates(contracts: Sequence[BacktestRunContract], policy: BacktestRunContractConfig) -> tuple[BacktestRunContractGate, ...]:
    return (
        _gate("non_empty_contract_set", [] if contracts else ["no contracts supplied"], "At least one contract is present."),
        _required_fields_gate(contracts),
        _date_window_gate(contracts),
        _commit_sha_gate(contracts),
        _symbols_gate(contracts, policy),
        _seed_gate(contracts, policy),
        _determinism_gate(contracts, policy),
        _allowed_modes_gate(contracts, policy),
        _metrics_gate(contracts, policy),
        _artifacts_gate(contracts, policy),
        _unique_fingerprint_gate(contracts),
        _public_safe_gate(contracts, policy),
        _research_footer_gate(contracts, policy),
    )


def _required_fields_gate(contracts: Sequence[BacktestRunContract]) -> BacktestRunContractGate:
    required = ("run_id", "strategy_id", "strategy_version", "code_commit_sha", "parameter_version", "dataset_id", "dataset_fingerprint", "start_date", "end_date", "data_mode", "execution_model")
    failures: list[str] = []
    for contract in contracts:
        payload = contract.to_dict()
        missing = [field_name for field_name in required if not payload.get(field_name)]
        if missing:
            failures.append(f"{contract.run_id or '<missing-run-id>'}: missing {', '.join(missing)}")
    return _gate("required_fields_complete", failures, "All reproducibility identity fields are present.")


def _date_window_gate(contracts: Sequence[BacktestRunContract]) -> BacktestRunContractGate:
    failures: list[str] = []
    for contract in contracts:
        start = _parse_contract_date(contract.start_date)
        end = _parse_contract_date(contract.end_date)
        if start is None:
            failures.append(f"{contract.run_id}: invalid start_date")
        if end is None:
            failures.append(f"{contract.run_id}: invalid end_date")
        if start is not None and end is not None and start > end:
            failures.append(f"{contract.run_id}: start_date after end_date")
    return _gate("valid_backtest_date_windows", failures, "Backtest windows are valid ISO date ranges.")


def _commit_sha_gate(contracts: Sequence[BacktestRunContract]) -> BacktestRunContractGate:
    failures = [f"{contract.run_id}: invalid code_commit_sha" for contract in contracts if not _COMMIT_SHA_PATTERN.match(contract.code_commit_sha)]
    return _gate("commit_sha_present", failures, "Each contract pins the code version by commit SHA.")


def _symbols_gate(contracts: Sequence[BacktestRunContract], policy: BacktestRunContractConfig) -> BacktestRunContractGate:
    failures = [f"{contract.run_id}: too few symbols" for contract in contracts if len([symbol for symbol in contract.symbols if symbol]) < policy.min_symbols]
    return _gate("symbol_set_present", failures, "Each contract records a replayable symbol set.")


def _seed_gate(contracts: Sequence[BacktestRunContract], policy: BacktestRunContractConfig) -> BacktestRunContractGate:
    if not policy.require_seed:
        return BacktestRunContractGate("seed_recorded", True, "Seed is optional by policy.")
    return _gate("seed_recorded", [f"{contract.run_id}: missing seed" for contract in contracts if contract.seed is None], "Each contract records a deterministic seed.")


def _determinism_gate(contracts: Sequence[BacktestRunContract], policy: BacktestRunContractConfig) -> BacktestRunContractGate:
    if not policy.require_determinism:
        return BacktestRunContractGate("determinism_required", True, "Determinism is optional by policy.")
    return _gate("determinism_required", [f"{contract.run_id}: deterministic=false" for contract in contracts if not contract.deterministic], "Each contract declares deterministic replay behavior.")


def _allowed_modes_gate(contracts: Sequence[BacktestRunContract], policy: BacktestRunContractConfig) -> BacktestRunContractGate:
    failures: list[str] = []
    for contract in contracts:
        if contract.data_mode not in policy.allowed_data_modes:
            failures.append(f"{contract.run_id}: unsupported data_mode")
        if contract.execution_model not in policy.allowed_execution_models:
            failures.append(f"{contract.run_id}: unsupported execution_model")
    return _gate("allowed_data_and_execution_modes", failures, "Data and execution modes are explicitly allowed.")


def _metrics_gate(contracts: Sequence[BacktestRunContract], policy: BacktestRunContractConfig) -> BacktestRunContractGate:
    failures: list[str] = []
    for contract in contracts:
        missing = [metric for metric in policy.required_metrics if metric not in contract.metrics]
        if missing:
            failures.append(f"{contract.run_id}: missing metrics {', '.join(missing)}")
        non_numeric = [metric for metric, value in contract.metrics.items() if not isinstance(value, (int, float)) or isinstance(value, bool)]
        if non_numeric:
            failures.append(f"{contract.run_id}: non-numeric metrics {', '.join(non_numeric)}")
    return _gate("required_metrics_present", failures, "Required result metrics are present and numeric.")


def _artifacts_gate(contracts: Sequence[BacktestRunContract], policy: BacktestRunContractConfig) -> BacktestRunContractGate:
    failures: list[str] = []
    for contract in contracts:
        by_name = {artifact.name: artifact for artifact in contract.artifacts}
        missing = [name for name in policy.required_artifacts if name not in by_name]
        if missing:
            failures.append(f"{contract.run_id}: missing artifacts {', '.join(missing)}")
        bad = [artifact.name or "<missing-name>" for artifact in contract.artifacts if not _looks_like_sha256(artifact.sha256)]
        if bad:
            failures.append(f"{contract.run_id}: invalid artifact sha256 for {', '.join(bad)}")
    return _gate("artifact_manifest_complete", failures, "Required artifacts and SHA-256 fingerprints are present.")


def _unique_fingerprint_gate(contracts: Sequence[BacktestRunContract]) -> BacktestRunContractGate:
    fingerprints = [_contract_fingerprint(contract) for contract in contracts]
    failures = [] if len(fingerprints) == len(set(fingerprints)) else ["duplicate contract fingerprint detected"]
    return _gate("unique_contract_fingerprints", failures, "Contract fingerprints are unique.")


def _public_safe_gate(contracts: Sequence[BacktestRunContract], policy: BacktestRunContractConfig) -> BacktestRunContractGate:
    if not policy.require_public_safe_tags:
        return BacktestRunContractGate("public_safe_demo_tags", True, "Public-safe tags are optional by policy.")
    failures = []
    for contract in contracts:
        tag_set = set(contract.tags)
        if _PUBLIC_SAFE_TAG not in tag_set or _DEMO_TAG not in tag_set:
            failures.append(f"{contract.run_id}: requires demo and public_safe tags")
    return _gate("public_safe_demo_tags", failures, "Contracts are explicitly demo/public-safe.")


def _research_footer_gate(contracts: Sequence[BacktestRunContract], policy: BacktestRunContractConfig) -> BacktestRunContractGate:
    if not policy.require_research_footer:
        return BacktestRunContractGate("research_footer_present", True, "Research footer is optional by policy.")
    failures = [f"{contract.run_id}: missing research-only footer" for contract in contracts if contract.footer != RESEARCH_ONLY_FOOTER]
    return _gate("research_footer_present", failures, "Each contract preserves the research-only footer.")


def _gate(name: str, failures: Sequence[str], success_message: str) -> BacktestRunContractGate:
    return BacktestRunContractGate(name=name, passed=not failures, message=success_message if not failures else "Gate failed.", failures=tuple(failures))


def _parse_contract_date(value: str) -> date | None:
    if not _DATE_PATTERN.match(value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _looks_like_sha256(value: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{64}", value.lower()))


def _stable_fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _contract_fingerprint(contract: BacktestRunContract) -> str:
    identity = {
        "run_id": contract.run_id,
        "strategy_id": contract.strategy_id,
        "strategy_version": contract.strategy_version,
        "code_commit_sha": contract.code_commit_sha,
        "parameter_version": contract.parameter_version,
        "dataset_id": contract.dataset_id,
        "dataset_fingerprint": contract.dataset_fingerprint,
        "symbols": list(contract.symbols),
        "start_date": contract.start_date,
        "end_date": contract.end_date,
        "data_mode": contract.data_mode,
        "execution_model": contract.execution_model,
        "seed": contract.seed,
    }
    return _stable_fingerprint(json.dumps(identity, sort_keys=True))


def _demo_artifacts(run_id: str) -> list[dict[str, str]]:
    return [
        {"name": "input_manifest", "path": f"reports/backtest_run_contract/{run_id}/input_manifest.json", "sha256": _stable_fingerprint(f"{run_id}:input_manifest")},
        {"name": "result_summary", "path": f"reports/backtest_run_contract/{run_id}/result_summary.json", "sha256": _stable_fingerprint(f"{run_id}:result_summary")},
    ]


def _demo_payloads() -> tuple[dict[str, Any], ...]:
    return (
        {
            "run_id": "bt3-demo-trend-001",
            "strategy_id": "trend_demo",
            "strategy_version": "strategy-demo-v1",
            "code_commit_sha": "30dede33b0fe1ec7fd845520c9199483c1fbd8fe",
            "parameter_version": "params-demo-v1",
            "dataset_id": "synthetic-us-largecap-demo-2024",
            "dataset_fingerprint": _stable_fingerprint("synthetic-us-largecap-demo-2024"),
            "symbols": ["AAPL", "MSFT", "QQQ"],
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "data_mode": "synthetic",
            "execution_model": "next_bar_open",
            "seed": 42,
            "deterministic": True,
            "metrics": {"total_return_pct": 12.4, "max_drawdown_pct": -7.1, "sharpe": 1.18, "win_rate_pct": 54.2, "trade_count": 48},
            "artifacts": _demo_artifacts("bt3-demo-trend-001"),
            "tags": ["demo", "public_safe", "research_only"],
            "notes": "Synthetic demonstration contract for reproducibility validation.",
        },
        {
            "run_id": "bt3-demo-reversion-001",
            "strategy_id": "mean_reversion_demo",
            "strategy_version": "strategy-demo-v1",
            "code_commit_sha": "30dede33b0fe1ec7fd845520c9199483c1fbd8fe",
            "parameter_version": "params-demo-v1",
            "dataset_id": "paper-observation-demo-2024",
            "dataset_fingerprint": _stable_fingerprint("paper-observation-demo-2024"),
            "symbols": ["SPY", "IWM"],
            "start_date": "2024-03-01",
            "end_date": "2024-09-30",
            "data_mode": "paper_observation",
            "execution_model": "paper_fill_model",
            "seed": 7,
            "deterministic": True,
            "metrics": {"total_return_pct": 5.8, "max_drawdown_pct": -3.6, "sharpe": 0.91, "win_rate_pct": 51.0, "trade_count": 31},
            "artifacts": _demo_artifacts("bt3-demo-reversion-001"),
            "tags": ["demo", "public_safe", "research_only"],
            "notes": "Paper-observation demonstration contract for reproducibility validation.",
        },
    )
