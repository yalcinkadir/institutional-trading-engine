# Decision Engine v3

## Ziel

Die Decision Engine v3 verschiebt das Projekt von einem einfachen Screener zu einer institutionell inspirierten Entscheidungslogik.

Der Kern ist nicht:

> Welches Asset hat den höchsten Score?

Sondern:

> Welches Risiko darf in diesem Marktregime überhaupt eingegangen werden?

---

## Warum additive Scores nicht reichen

Ein additiver Score ist fragil, weil er Kontext ignoriert.

Beispiel:

- Asset über SMA200
- Relative Strength stark
- Setup Score hoch

Aber gleichzeitig:

- Credit Spreads weiten sich aus
- VIX-Term-Structure invertiert
- Breadth kollabiert
- Breakouts failen breit

Dann darf das Ergebnis nicht einfach `Score 78 = Buy` sein.

Richtig wäre:

> Setup stark, aber Risk Gate aktiv. Aggressive Longs blockiert.

---

## Entscheidungsreihenfolge

Die Engine muss Signale in dieser Reihenfolge prüfen:

1. Survival / Systemic Risk
2. Liquidity / Credit / Volatility Stress
3. Market Regime
4. Cross-Asset Confirmation
5. Breadth und Internals
6. Sector / Theme Leadership
7. Asset Setup
8. Entry / Stop / Position Size

Diese Reihenfolge ist wichtiger als die Menge der Signale.

---

## Hard Overrides

Hard Overrides sind keine Score-Abzüge. Sie blockieren oder reduzieren Strategie-Typen.

Beispiele:

| Bedingung | Wirkung |
|---|---|
| VIX invertiert + Credit Stress + Breadth Collapse | aggressive Long Breakouts blockieren |
| Liquidity Stress | No-Trade oder stark reduzierte Size |
| Risk-Off + Failed Breakout Cluster | Momentum deaktivieren |
| Panic + Credit Stress | normale Trendfolge deaktivieren |

---

## Regime-to-Setup Mapping

| Market State | Erlaubte Setups |
|---|---|
| Low Vol Bull | Momentum Breakout, Pullback Continuation, Speculative Growth |
| High Vol Transition | Mean Reversion, Pullback Continuation, Defensive Rotation |
| Risk Off | Defensive Rotation, Mean Reversion |
| Panic / Dislocation | Reversal Asymmetry, Defensive Rotation |
| Neutral | Pullback Continuation, Mean Reversion |

---

## No-Trade Engine

No-Trade wird ausgelöst, wenn:

- Asymmetrie zu schwach ist
- Datenqualität niedrig ist
- Setup im aktuellen Regime nicht erlaubt ist
- Hard Overrides aktiv sind
- Risk Tier zu schwach ist

No-Trade ist eine aktive Qualitätsentscheidung.

---

## Risk Tier

| Tier | Bedeutung | Default Size |
|---|---|---|
| Tier 1 | Full Alignment | 1.0x |
| Tier 2 | Gutes Setup, aber nicht perfekt | 0.5x |
| Tier 3 | Watch / Tracking | 0.25x |
| No Trade | Nicht handeln | 0.0x |

Position Size kann zusätzlich reduziert werden durch:

- Event Risk
- Sector Crowding
- High Vol Transition
- Portfolio Heat Limits

---

## Implementierungsstatus

Aktuell vorhanden:

- `src/decision_engine.py`
- `tests/test_decision_engine.py`

Die Implementierung ist absichtlich deterministisch und klein. Erst wenn die Regeln stabil sind, sollten zusätzliche Datenfeeds wie Options Flow, Gamma, COT oder Dark Pools integriert werden.
