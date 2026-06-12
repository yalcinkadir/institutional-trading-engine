from __future__ import annotations

import json
from pathlib import Path
from statistics import median
from typing import Any

REQUIRED = {"signal_id","symbol","signal_date","entry_price","stop_price","target_1_price","target_2_price","atr14_at_signal","atr14_during_trade","bars_after_entry","high_after_entry","low_after_entry","close_after_entry","mae_r","mfe_r","baseline_result_r","broker_execution_mode","live_trading_authorized","fees_or_slippage_assumption"}
PERIODS = ("training", "validation", "out_of_sample")


def _variants() -> list[dict[str, Any]]:
    rows = [{"name":"baseline_current_exit","group":"baseline","level":"current","partial_size":None}]
    for p in (0.25, 0.33, 0.50, 0.66):
        rows.append({"name":f"partial_t1_{p:.2f}","group":"partial_t1","level":str(p),"partial_size":p})
    rows += [
        {"name":"atr_runner_1","group":"atr_runner","level":"1atr","partial_size":0.33},
        {"name":"breakeven_trail_1","group":"breakeven_trail","level":"1atr","partial_size":0.50},
        {"name":"no_partial_runner_1","group":"no_partial_runner","level":"1atr","partial_size":0.0},
        {"name":"same_bar_conservative_blocked","group":"same_bar_conservative","level":"blocked","partial_size":0.50},
    ]
    return rows


def _missing(record: dict[str, Any]) -> list[str]:
    return sorted(field for field in REQUIRED if record.get(field) in (None, ""))


def _risk(record: dict[str, Any]) -> float:
    return abs(float(record["entry_price"]) - float(record["stop_price"])) or 1.0


def _rr(record: dict[str, Any], price_field: str) -> float:
    return (float(record[price_field]) - float(record["entry_price"])) / _risk(record)


def _eval(record: dict[str, Any], variant: dict[str, Any]) -> dict[str, Any]:
    t1 = record.get("first_t1_hit_at") not in (None, "") or float(record["high_after_entry"]) >= float(record["target_1_price"])
    t2 = record.get("first_t2_hit_at") not in (None, "") or float(record["high_after_entry"]) >= float(record["target_2_price"])
    stopped = record.get("first_stop_hit_at") not in (None, "") or float(record["low_after_entry"]) <= float(record["stop_price"])
    same_bar = bool(record.get("same_bar_stop_target_ambiguity"))
    if same_bar and variant["group"] == "same_bar_conservative":
        r = 0.0
    elif variant["group"] == "baseline":
        r = float(record["baseline_result_r"])
    elif not t1:
        r = -1.0 if stopped else _rr(record, "close_after_entry")
    else:
        part = float(variant.get("partial_size") or 0.0)
        runner = _rr(record, "target_2_price") if t2 else (0.0 if variant["group"] == "breakeven_trail" and stopped else (-1.0 if stopped else _rr(record, "close_after_entry")))
        r = part * _rr(record, "target_1_price") + (1.0 - part) * runner
    return {"r": round(r, 6), "t1": t1, "giveback": t1 and float(record["close_after_entry"]) < float(record["target_1_price"]), "runner": t1, "stopped": stopped, "t2": t2, "mae": float(record["mae_r"]), "mfe": float(record["mfe_r"]), "same_bar": same_bar, "skipped": False}


def _period_result(period: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(rows) or 1
    r_values = [float(row["r"]) for row in rows]
    return {"period":period,"total_trades_considered":len(rows),"t1_hit_count":sum(1 for row in rows if row["t1"]),"t1_giveback_count":sum(1 for row in rows if row["giveback"]),"accepted_runner_trades":sum(1 for row in rows if row["runner"]),"skipped_trades":sum(1 for row in rows if row["skipped"]),"stop_hit_rate":round(sum(1 for row in rows if row["stopped"])/n,6),"target_1_hit_rate":round(sum(1 for row in rows if row["t1"])/n,6),"target_2_hit_rate":round(sum(1 for row in rows if row["t2"])/n,6),"average_r":round(sum(r_values)/n,6) if rows else 0.0,"expectancy_r":round(sum(r_values)/n,6) if rows else 0.0,"median_r":round(median(r_values),6) if r_values else 0.0,"best_trade_r":round(max(r_values),6) if r_values else 0.0,"worst_trade_r":round(min(r_values),6) if r_values else 0.0,"tail_contribution_r":round(max(r_values),6) if r_values else 0.0,"average_mae_r":round(sum(row["mae"] for row in rows)/n,6) if rows else 0.0,"average_mfe_r":round(sum(row["mfe"] for row in rows)/n,6) if rows else 0.0,"same_bar_ambiguity_count":sum(1 for row in rows if row["same_bar"])}


def build_bt138_report(records: list[dict[str, Any]], *, github_run_id: str | None = None) -> dict[str, Any]:
    missing = {str(record.get("signal_id") or i): _missing(record) for i, record in enumerate(records) if _missing(record)}
    if missing:
        return {"schema":"bt138_partial_t1_trailing_exit_report.v1","status":"SKIPPED_INSUFFICIENT_FIELDS","research_only":True,"broker_execution_mode":"paper_only","live_trading_authorized":False,"production_rule_change":False,"missing_fields":missing,"variant_grid":_variants(),"variant_results":[]}
    results = []
    for variant in _variants():
        period_results = [_period_result(period, [_eval(record, variant) for record in records if record.get("period") == period]) for period in PERIODS]
        rec = "KEEP_BASELINE" if variant["group"] == "baseline" else "PROMOTE_TO_GUARDED_EXPERIMENT"
        results.append({"variant":variant["name"],"group":variant["group"],"level":variant["level"],"period_results":period_results,"recommendation":rec})
    return {"schema":"bt138_partial_t1_trailing_exit_report.v1","status":"COMPLETED","github_run_id":github_run_id or "local","research_only":True,"broker_execution_mode":"paper_only","live_trading_authorized":False,"production_rule_change":False,"missing_fields":{},"variant_grid":_variants(),"variant_results":results}


def persist_bt138_report(report: dict[str, Any], *, output_root: Path = Path("reports/backtests/real_data"), github_run_id: str | None = None) -> dict[str, Path]:
    run_id = github_run_id or str(report.get("github_run_id") or "local")
    latest = output_root / "latest"
    run = output_root / "runs" / run_id
    latest.mkdir(parents=True, exist_ok=True)
    run.mkdir(parents=True, exist_ok=True)
    files = {"latest_json": latest / "bt138-partial-t1-trailing-exit-report.json", "latest_markdown": latest / "bt138-partial-t1-trailing-exit-report.md", "run_json": run / "bt138-partial-t1-trailing-exit-report.json", "run_markdown": run / "bt138-partial-t1-trailing-exit-report.md"}
    payload = json.dumps(report, indent=2, sort_keys=True)
    markdown = "# BT138 Partial-at-T1 + Trailing-Exit Report\n"
    files["latest_json"].write_text(payload, encoding="utf-8")
    files["run_json"].write_text(payload, encoding="utf-8")
    files["latest_markdown"].write_text(markdown, encoding="utf-8")
    files["run_markdown"].write_text(markdown, encoding="utf-8")
    return files
