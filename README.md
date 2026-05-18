# Institutional Trading Engine

## Projektname
Institutional Trading Engine

---

## Proprietary Research Notice

This project is intended as a private, proprietary market research and decision-support framework.

It contains architecture, decision logic, risk models, screening logic and adaptive expectancy concepts that should be treated as intellectual property.

Do not expose:

- API keys
- Telegram tokens
- private market data exports
- decision logs
- outcome logs
- proprietary scoring logic
- portfolio or account information

---

## Disclaimer

This software is for research, education, market analysis and decision-support purposes only.

It is **not financial advice**, **not investment advice**, **not a trading recommendation**, and **not a guarantee of future performance**.

All outputs must be reviewed manually before any financial decision is made. The user is solely responsible for all trading, investment and risk decisions.

---

## Zweck des Systems
Institutional Trading Engine ist ein datengetriebenes Marktanalyse-, Ranking- und Screening-System für:

- US-Aktien
- ETFs
- Indizes
- Edelmetalle

Das Ziel ist eine institutionell inspirierte **Market Decision Engine**. Das System soll nicht nur bullish/bearish Signale sammeln, sondern entscheiden:

> Welches Risiko darf in welchem Marktregime überhaupt eingegangen werden?

Das System verwendet Live-Marktdaten über Polygon.io und verbindet Screening, Regime-Erkennung, Report-Erstellung und Qualitätskontrolle.

---

## Strategische Leitlinie v3

Die nächste Evolutionsstufe ist bewusst **nicht** mehr Feature-Sammlung, sondern Entscheidungsqualität.

Kernprinzipien:

- Kontext schlägt Einzelsignal
- Risk Gates schlagen additive Scores
- Setup-Qualität ist abhängig vom Marktregime
- Kein Trade ist eine aktive Entscheidung
- Outcome Tracking ist wichtiger als mehr Indikatoren
- Kapital wird nach Asymmetrie und Confidence verteilt

---

## Decision Engine v3

Die v3-Architektur ergänzt den bisherigen Screener um eine hierarchische Entscheidungslogik.

### 1. Signal Hierarchy Engine
Nicht alle Signale sind gleich wichtig.

Priorität:

1. Systemisches Risiko / Survival Layer
2. Makro-, Liquiditäts- und Volatilitätsregime
3. Cross-Asset Confirmation
4. Breadth und Market Internals
5. Sector / Theme Leadership
6. Einzelasset-Setup
7. Execution und Position Sizing

Ein starkes Einzelasset darf ein schlechtes Risiko-Regime nicht automatisch überstimmen.

---

### 2. Override Engine
Bestimmte Zustände sind keine Score-Abzüge, sondern harte Blocker.

Beispiele:

- VIX-Term-Structure invertiert + Breadth Collapse + Credit Stress
- aggressive Long-Breakouts werden deaktiviert
- Portfolio Heat wird reduziert
- Positionsgrößen werden gekappt
- No-Trade-Modus kann aktiv werden

---

### 3. Regime-to-Setup Mapping
Strategien werden nur aktiviert, wenn sie zum Marktumfeld passen.

| Regime | Bevorzugte Setups | Reduzierte/Blockierte Setups |
|---|---|---|
| Low Vol Bull | Momentum, Breakout, RS Leader | aggressive Shorts |
| High Vol Transition | kleinere Size, Mean Reversion, schnelle Exits | extended Breakouts |
| Risk Off | Cash, Defensive Rotation, Hedges | speculative Growth Breakouts |
| Panic / Dislocation | asymmetrische Reversal-Setups | normale Trendfolge |

---

### 4. No-Trade Engine
Das System soll bewusst sagen können:

> Keine hochwertige asymmetrische Opportunität vorhanden.

No-Trade ist kein Fehler, sondern ein Qualitätsmerkmal.

---

### 5. Outcome Tracking
Das System soll nicht nur Trades, sondern auch Entscheidungen tracken:

- akzeptierte Setups
- verworfene Setups
- blockierte Trades
- Override-Auslöser
- Regime-Zustand
- MFE / MAE
- Ergebnis nach 1D / 5D / 20D
- Setup-Typ
- Confidence
- Risk Tier

Damit entsteht später eine Expectancy Engine.

---

## Projektstruktur

```txt
.github/workflows/
docs/
 ├── DECISION_ENGINE_V3.md
 └── OUTCOME_TRACKING.md
scripts/
src/
 ├── adaptive_expectancy.py
 ├── cross_asset_regime.py
 ├── decision_engine.py
 ├── market_internal_quality.py
 ├── multi_timeframe_structure.py
 ├── outcome_tracking.py
 ├── portfolio_risk.py
 └── setup_scoring.py

tests/
```

---

## Tests & Qualitätssicherung

Die Tests prüfen u. a.:

- Risk-Off blockiert aggressive Long-Breakouts
- Low-Vol-Bull aktiviert Momentum-Setups
- High-Vol-Transition reduziert Positionsgröße
- No-Trade wird bei schwacher Asymmetrie ausgelöst
- Capital Allocation folgt Risk Tier statt blindem Score
- Cross-Asset Risk-On/Risk-Off Regime
- Portfolio Heat und Korrelationen
- Outcome Tracking und Expectancy
- Adaptive Expectancy je Setup/Regime
- Market Internal Quality und Opportunity Density
- Multi-Timeframe Structure Alignment

---

## Lokale Ausführung

```bash
pip install -r requirements.txt
pytest
```

---

## Benötigte Umgebungsvariablen

Siehe `.env.example`.

Pflicht:

```txt
POLYGON_API_KEY
```

Optional:

```txt
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
REPORT_WEBHOOK_URL
```

Echte Secrets dürfen niemals committed werden.

---

## Ziel des Projekts

Das Ziel ist ein institutionell orientiertes Analyse-, Ranking- und Screening-System mit:

- datengetriebener Marktanalyse
- institutioneller Asset-Priorisierung
- automatisierten institutionellen Reports
- objektiver Qualitätskontrolle
- professionellem Risk Management
- skalierbarer Architektur
- hierarchischer Entscheidungslogik
- Performance Feedback Loop

Das System soll:

- Marktregime erkennen
- Relative Strength analysieren
- institutionelle Marktrotation sichtbar machen
- hochwertige Assets priorisieren
- schwache Marktstrukturen erkennen
- schlechte Trading-Umfelder vermeiden
- professionelle Trading-Entscheidungen unterstützen
