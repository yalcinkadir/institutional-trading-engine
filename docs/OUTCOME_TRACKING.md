# Outcome Tracking

## Ziel

Outcome Tracking ist der wichtigste Schritt, um subjektive Analyse in messbare Qualität zu verwandeln.

Ohne Outcome Tracking entsteht nur mehr Komplexität. Mit Outcome Tracking entsteht eine Expectancy Engine.

---

## Was getrackt werden muss

Nicht nur echte Trades, sondern jede Entscheidung:

- approved
- reduced_size
- watch
- blocked
- no_trade

---

## Empfohlenes Decision Record Schema

```json
{
  "timestamp": "2026-05-18T16:00:00+02:00",
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
  "blocked_reasons": [],
  "notes": [],
  "price_at_decision": 0.0,
  "result_1d": null,
  "result_5d": null,
  "result_20d": null,
  "mfe": null,
  "mae": null
}
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

1. `decision_log.csv` oder Datenbanktabelle
2. tägliches Update der Outcomes
3. wöchentlicher Outcome Report
4. Expectancy pro Setup/Regime
5. adaptive Gewichtung erst nach genügend Daten
