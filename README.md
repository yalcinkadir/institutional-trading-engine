# Institutional Trading Engine

## Projektname
Institutional Trading Engine

---

## Zweck des Systems
Institutional Trading Engine ist ein datengetriebenes Marktanalyse-, Ranking- und Screening-System für:

- US-Aktien
- ETFs
- Indizes
- Edelmetalle

Das Ziel ist eine institutionelle Marktanalyse mit:

- Market Regime Detection
- Relative Strength Analyse
- Leader-/Weak-Name-Erkennung
- institutionellem Asset Ranking
- Risk Management
- Swing-Trading-Setups
- Watchlist-Generierung
- automatisierten Reports
- Telegram-Delivery
- Qualitätskontrolle der Reports

Das System verwendet Live-Marktdaten über Polygon.io.

---

## Hauptfunktionen

### Market Regime Engine
Automatische Analyse von:

- SPY
- QQQ
- VIX
- SMA50 / SMA200
- ATR14
- Breadth
- Trendstruktur
- Volatilitätsregime

---

### Institutional Market Health Score
Das System berechnet automatisch einen institutionellen Market Health Score basierend auf:

- Trendqualität
- VIX-Regime
- Marktbreite
- SPY-/QQQ-Struktur

Mögliche Regime:

- Strong Bullish
- Bullish
- Neutral
- Defensive
- Risk-Off

---

### Relative Strength Engine
Das System analysiert Relative Strength gegen:

- QQQ
- SPY

Relative Strength Klassifikation:

- Leader
- Neutral
- Weak

Die RS-Analyse dient als Grundlage für:

- Leader Detection
- Weak Name Detection
- institutionelles Asset Ranking
- Setup Priorisierung

---

### Institutional Asset Ranking
Jedes Asset erhält einen institutionellen Score basierend auf:

- Trendstruktur
- Relative Strength
- Volumenqualität
- Volatilität
- Risiko

Mögliche Status:

- Strong Ready
- Ready
- Watch
- Neutral
- Weak

---

### Leader & Weak Name Detection
Das System erkennt automatisch:

#### Leaders
Assets mit:
- hoher Relative Strength
- starker Trendstruktur
- institutioneller Stärke
- hoher Ranking-Qualität

#### Weak Names
Assets mit:
- schwacher Relative Strength
- schlechter Trendstruktur
- Underperformance
- schwacher Marktstruktur

---

### Trade Summary Engine
Das System erzeugt Telegram-kompatible Trade Summaries mit:

- Market Regime
- Market Health Score
- Top Leaders
- Weak Names
- institutioneller Zusammenfassung

---

### Automatische Reports
Das System erstellt automatisch:

#### Pre-Market Reports
Sonntag bis Freitag

Inhalt:
- Marktregime
- Volatilität
- Watchlist
- Risiken vor Börseneröffnung
- Leader-Kandidaten
- institutionelle Marktstruktur

#### Post-Market Reports
Montag bis Freitag

Inhalt:
- Marktabschlussanalyse
- Marktbreite
- Trendbestätigung
- Leader-/Weak-Names
- Swing-Setups
- institutionelle Rotation

#### Weekly Reports
Samstag

Inhalt:
- Wochenanalyse
- empfohlene Assets
- Fokus für nächste Woche
- Risikobewertung
- Marktrotation

---

## Telegram Integration
Reports werden automatisch an Telegram gesendet.

Benötigte Secrets:

```txt
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
```

---

## Report Quality System
Das Projekt enthält ein integriertes QA-System für Reports.

Automatisch geprüft werden:

- Struktur
- Mindestlänge
- Analysequalität
- fehlende Marktmetriken
- Relative Strength Analyse
- Leader-/Weak-Name-Analyse
- Placeholder
- schwache Inhalte
- Sprache
- Telegram-Tauglichkeit

Der Workflow blockiert Reports mit unzureichender Qualität.

---

## GitHub Actions Workflows

### Institutional Reports
Automatische Erstellung von:

- Pre-Market Reports
- Post-Market Reports
- Weekly Reports

Mit:

- Telegram Versand
- Artifact Upload
- manueller Ausführung
- Zeitsteuerung

---

### Report Quality Validation
Automatisches QA-System für:

- Pull Requests
- manuelle Tests
- Qualitätsprüfung
- institutionelle Analyseprüfung

---

## Projektstruktur

```txt
.github/workflows/
scripts/
src/
 ├── data/
 ├── indicators/
 ├── relative_strength/
 ├── reporting/
 ├── scoring/
 └── screening/

tests/
```

---

## Aktuell gescannte Symbole

### Indizes / ETFs
- SPY
- QQQ
- IWM
- DIA

### Technologie / Leader
- MSFT
- NVDA
- META
- AAPL
- AMZN
- AVGO
- AMD
- MU
- ADBE
- CSCO

### Edelmetalle
- GLD
- SLV
- PPLT

### Weitere Kandidaten
- TSLA
- NFLX
- CRWD
- PANW
- SHOP
- PLTR

---

## Verwendete Indikatoren

- SMA50
- SMA200
- ATR14
- Relative Strength
- Relative Volume
- Breadth
- VIX
- Trendstruktur
- Volatilitätsregime
- institutionelles Asset Scoring

---

## Benötigte Secrets

```txt
POLYGON_API_KEY
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
REPORT_WEBHOOK_URL
```

---

## Tests & Qualitätssicherung

Das Projekt enthält:

- Report Quality Validation
- Screening Engine Tests
- Relative Strength Tests
- Ranking Tests
- Trade Summary Tests
- institutionelle Analyseprüfung

Das Ziel ist:

- stabile Reports
- konsistente Analysequalität
- Vermeidung schwacher AI-Ausgaben
- institutionell orientierte Qualitätssicherung

---

## Geplante Features

### Screening
- Auto Asset Ranking
- Setup Quality Score
- Setup Readiness
- Confidence Score
- institutionelle Momentum-Erkennung

### Trading
- Entry Engine
- Exit Engine
- ATR-basierte Stops
- Risk Scoring
- Position Sizing
- Exposure Management

### Analytics
- Historical Recommendation Tracking
- Weekly Performance Tracking
- Trefferquote
- Risk/Reward Statistik
- Backtesting
- Alpha Tracking

### Reporting
- PDF Export
- Chart Rendering
- Telegram Trade Summary
- Telegram Charts
- Telegram Alerts
- institutionelle Watchlists

---

## Ziel des Projekts

Das Ziel ist ein institutionell orientiertes Analyse-, Ranking- und Screening-System mit:

- datengetriebener Marktanalyse
- institutioneller Asset-Priorisierung
- automatisierten institutionellen Reports
- objektiver Qualitätskontrolle
- professionellem Risk Management
- skalierbarer Architektur

Das System soll:

- Marktregime erkennen
- Relative Strength analysieren
- institutionelle Marktrotation sichtbar machen
- hochwertige Assets priorisieren
- schwache Marktstrukturen erkennen
- professionelle Trading-Entscheidungen unterstützen
