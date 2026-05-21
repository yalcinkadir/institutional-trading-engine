# End-to-End Dry Run

P22 adds a local, deterministic dry-run validator for go-live readiness.

The dry run is broker-free and external-API-free. It validates local generated artifacts and runtime output paths before live Decision-Support operation is enabled.

---

## Command

```bash
python scripts/run_e2e_dry_run.py \
  --signals-file reports/signals/latest-signals.json
```

Machine-readable output:

```bash
python scripts/run_e2e_dry_run.py --json
```

---

## What It Validates

The validator checks:

```text
reports/signals/latest-signals.json exists
signal file is valid JSON
payload is a list or object with signals[]
every signal has signal_id, symbol and action
every BUY_WATCH has executable trade-plan fields
reports/alerts is writable
data is writable for lifecycle JSONL output
```

Required signal identity fields:

```text
signal_id
symbol
action
```

Required actionable `BUY_WATCH` trade-plan fields:

```text
entry_trigger
stop_loss
target_1
entry_reason
stop_reason
exit_reason
```

---

## Passing Result

A passing run exits with code `0` and prints:

```text
E2E dry-run validation: PASS
```

A failing run exits with code `1` and prints the failed check names and messages.

---

## Non-Goals

The dry-run validator does **not**:

```text
fetch Polygon data
send Telegram messages
execute broker orders
place trades
replace pytest or CI
```

It is a final local artifact sanity check before enabling scheduled live Decision-Support runs.

---

## Recommended Go-Live Sequence

```text
1. CI green
2. Generate report/signals
3. Run E2E dry run
4. Run watcher once manually
5. Verify latest-alerts.json / signal_lifecycle.jsonl
6. Verify Telegram/notification workflow separately
7. Enable scheduled live Decision-Support workflow
```

---

## Design Rules

- Deterministic.
- No broker execution.
- No external API dependency.
- No destructive side effects except temporary write probes.
- Clear pass/fail result.
- Machine-readable JSON output available.
