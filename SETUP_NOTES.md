# SETUP NOTES

## Repository Secret

Der Polygon API-Key liegt in GitHub unter:

**Settings → Secrets and variables → Actions**

Name des Secrets:

```text
POLYGON_API_KEY
```

Wichtig:

- API-Key niemals im Code speichern
- API-Key niemals in README oder Reports schreiben
- Bei Verdacht auf Leak sofort rotieren
- Vor großen Datenläufen prüfen, ob das Secret aktiv ist
- Secrets mindestens quartalsweise prüfen und rotieren

---

## Aktueller Projektstatus

Das Projekt ist inzwischen kein einfacher Cloud-Scanner mehr. Es ist ein institutionell ausgerichtetes Research- und Decision-Support-System.

Aktueller Stand:

```text
P36-P47 validation stack: implemented
Phase A evidence-hygiene work A3-A10: implemented
Broker execution: not implemented
Live trading authorization: not granted by code
Phase B: not started
```

Das System dient weiterhin der Analyse, Validierung, Marktbeobachtung und Entscheidungsunterstützung. Es führt keine Live-Trades aus.

---

## Phase A Evidence-Hygiene Features

Implementiert:

```text
A3 Versioned decision thresholds
A4 Threshold-aware evidence / lockbox invalidation
A5 Square-root regime-aware slippage model
A6 Deflated Sharpe probability + bootstrap confidence intervals
A7 Polygon structured logging
A8 Polygon cache locking
A9 CHANGELOG.md and SETUP_NOTES.md update
A10 Quarterly secrets rotation policy
```

Noch offen vor Phase B:

```text
Phase A CI stabilization pass
CI workflow update for Phase A tests
Phase A test execution
Fixes if needed
README final update
```

---

## Relevante neue Dokumentation

```text
docs/operations/threshold_evidence_contract.md
docs/operations/slippage_model.md
docs/operations/statistical_robustness.md
docs/operations/polygon_structured_logging.md
docs/operations/polygon_cache_locking.md
docs/operations/secrets_rotation_policy.md
docs/operations/phase_a_ci_stabilization.md
ROADMAP.md
```

---

## Was aktuell funktioniert

### Scanner / Reporting

- Polygon-Datenabruf über GitHub Actions
- automatische Markdown-Reports im Ordner `reports/`
- Berechnung von:
  - RSI(14)
  - ATR(14)
  - ATR%
  - SMA20
  - SMA50
  - SMA200
  - RVOL
  - 20D Return
  - RS Spread vs Benchmark
- Marktregime-Ausgabe:
  - Market Regime
  - Extension Status
  - Risk State
  - Fresh Longs
- Strukturierte Report-Sektionen:
  - Market Regime Summary
  - Watchlist Candidates
  - Leaders
  - Weak Names
  - Setup Readiness
  - Data / Risk Warnings
  - Full Asset Report

### Evidence / Validation

- Historical edge validation
- Regime-phase backtest matrix
- Walk-forward validation
- Execution realism adjustment
- Out-of-sample validation lockbox
- Threshold evidence contract
- Deflated Sharpe probability
- Bootstrap confidence intervals for expectancy and win rate
- Paper trading journal / live observation v2
- Final live readiness gate

### Polygon Data Operations

- Polygon active universe builder
- Polygon daily bars downloader
- Polygon artifact consolidation workflow
- Polygon structured logging
- Polygon cache locking infrastructure
- Edge-evidence diagnostics artifacts
- Edge-evidence workflow log snapshot

### Security / Operations

- Quarterly secrets rotation policy
- Phase A CI stabilization plan

---

## Phase A Test Commands

Vor Phase B müssen mindestens diese Tests in CI laufen und grün sein:

```bash
pytest tests/test_decision_engine.py -q
pytest tests/test_out_of_sample_lockbox.py -q
pytest tests/test_slippage_model.py -q
pytest tests/test_execution_realism.py -q
pytest tests/test_statistical_robustness.py -q
pytest tests/test_historical_edge_validation.py -q
pytest tests/test_polygon_structured_logging.py -q
pytest tests/test_polygon_data_pipeline.py -q
pytest tests/test_polygon_cache.py -q
```

Danach vollständige Regression:

```bash
pytest -q
```

---

## CI-Stabilization-Regel vor Phase B

Phase B darf erst starten, wenn:

1. alle Phase-A Feature-Tests im CI-Workflow enthalten sind
2. der CI-Run ausgeführt wurde
3. alle Fehler analysiert und gefixt wurden
4. `pytest -q` grün ist
5. README, CHANGELOG und SETUP_NOTES aktuell sind

---

## Secret Rotation Smoke Test

Nach Rotation von `POLYGON_API_KEY`:

```bash
POLYGON_API_KEY=... python scripts/build_polygon_universe.py --max-symbols 25
```

Danach:

```bash
pytest tests/test_polygon_data_pipeline.py -q
pytest tests/test_polygon_structured_logging.py -q
pytest -q
```

---

## Polygon Datenläufe

Aktiver Polygon Runtime Universe Build:

```bash
POLYGON_API_KEY=... python scripts/build_polygon_universe.py \
  --output data/universe/survivorship_universe.csv \
  --active-from 2026-05-24
```

Daily Bars Download:

```bash
POLYGON_API_KEY=... python scripts/download_polygon_daily_bars.py \
  --universe data/universe/survivorship_universe.csv \
  --output-dir data/historical_bars \
  --from-date 2016-01-01 \
  --to-date 2026-05-24 \
  --min-bars 120
```

Für große Läufe bevorzugt batching nutzen:

```bash
POLYGON_API_KEY=... python scripts/download_polygon_daily_bars.py \
  --universe data/universe/survivorship_universe.csv \
  --output-dir data/historical_bars \
  --from-date 2016-01-01 \
  --to-date 2026-05-24 \
  --min-bars 120 \
  --batch-size 500 \
  --batch-index 0
```

---

## Bewusst noch nicht umgesetzt

Diese Punkte sind absichtlich noch nicht aktiv:

- keine Live-Trading-Freigabe
- keine Broker-Orderausführung
- keine automatische Kapitalallokation
- keine Crypto-/Forex-Erweiterung
- kein ML-Layer vor statistisch signifikanter regelbasierter Edge
- keine Phase-B Forward Evidence ohne vorherige CI-Stabilisierung

---

## Nächste Schritte

```text
Phase A CI workflow update
Phase A test execution
Fixes if needed
README final update
Phase B start only after green CI
```
