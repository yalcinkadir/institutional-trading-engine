# Outcome Tracking

## Ziel

Outcome Tracking ist der wichtigste Schritt, um subjektive Analyse in messbare Qualität zu verwandeln.

Ohne Outcome Tracking entsteht nur mehr Komplexität. Mit Outcome Tracking entsteht eine Expectancy Engine.

---

## Implementierungsstatus

Bereits implementiert:

- `src/outcome_tracking.py`
- persistente CSV-basierte Decision Logs
- `DecisionRecord` Datenmodell
- Expectancy-Berechnung
- Outcome-Tracking-Tests

---

## Was getrackt werden muss

Nicht nur echte Trades, sondern jede Entscheidung:

- approved
- reduced_size
- watch
- blocked
- no_trade

---

## Decision Record Schema

```json
{
  "timestamp_utc": "2026-05-18T16:00:00+00:00",
  "symbol": "QQQ",
  "market_state": "low_vol_bull",
  "setup_type": "momentum_breakout",
  "decision": "approved",
  "risk_tier": "tier_1",
  "position_size_multiplier": 1.0,
  "setup_score": 86,
  "regime_alignment": 0.88,
  "asymmetry_score": 0.78,
  "data_confidence": 0.91,
  "blocked_reasons": "",
  "notes": "full_alignment",
  "price_at_decision": 0.0,
  "result_1d": null,
  "result_5d": null,
  "result_20d": null,
  "mfe": null,
  "mae": null
}
```

---

## Beispiel

```python
from src.outcome_tracking import (
    build_decision_record,
    append_decision_record,
)

record = build_decision_record(
    symbol="QQQ",
    market_state="low_vol_bull",
    setup_type="momentum_breakout",
    decision="approved",
    risk_tier="tier_1",
    position_size_multiplier=1.0,
    setup_score=86,
    regime_alignment=0.82,
    asymmetry_score=0.77,
    data_confidence=0.91,
)

append_decision_record("data/decision_log.csv", record)
```

---

## Wichtige Metriken

| Metrik | Bedeutung |
|---|---|
| Winrate pro Setup | Trefferquote je Setup-Typ |
| Expectancy pro Regime | durchschnittliches Ergebnis im Marktregime |
| MFE | Maximum Favorable Excursion |
| MAE | Maximum Adverse Excursion |
| Failure Rate | Anteil gescheiterter Signale |
| Blocked Trade Outcome | Hätte blockierter Trade funktioniert oder Risiko vermieden? |
| No-Trade Accuracy | War No-Trade korrekt? |

---

## Warum blockierte Trades tracken?

Wenn ein blockierter Trade später stark steigt, war der Blocker eventuell zu streng.

Wenn ein blockierter Trade fällt, hat die Override Engine Risiko vermieden.

Das ist der Unterschied zwischen Meinung und Lernen.

---

## Nächste Ausbaustufe

1. automatisches tägliches Update der Outcomes
2. echte Price-Resolution via Polygon
3. Outcome Reports
4. Setup-Regime-Expectancy
5. adaptive Gewichtung auf Basis historischer Daten
6. Correlation- und Portfolio-Outcome-Tracking
