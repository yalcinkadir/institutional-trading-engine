# Institutional Trading Engine

## Projektname
Institutional Trading Engine

---

## Zweck des Systems
Institutional Trading Engine ist ein datengetriebenes Marktanalyse- und Screening-System für:

- US-Aktien
- ETFs
- Indizes
- Edelmetalle

Das Ziel ist eine institutionelle Marktanalyse mit:

- Market Regime Detection
- Relative Strength Analyse
- Leader-/Weak-Name-Erkennung
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

#### Post-Market Reports
Montag bis Freitag

Inhalt:
- Marktabschlussanalyse
- Marktbreite
- Trendbestätigung
- Leader-/Weak-Names
- Swing-Setups

#### Weekly Reports
Samstag

Inhalt:
- Wochenanalyse
- empfohlene Assets
- Fokus für nächste Woche
- Risikobewertung

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

---

## Projektstruktur

```txt
.github/workflows/
scripts/
src/
 ├── data/
 ├── indicators/
 ├── reporting/
 ├── scoring/
 └── screening/
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

---

## Benötigte Secrets

```txt
POLYGON_API_KEY
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
REPORT_WEBHOOK_URL
```

---

## Geplante Features

### Screening
- Relative Strength Ranking
- Top Leader Detection
- Weak Name Detection
- Auto Asset Ranking
- Setup Quality Score
- Setup Readiness
- Confidence Score

### Trading
- Entry Engine
- Exit Engine
- ATR-basierte Stops
- Risk Scoring
- Position Sizing

### Analytics
- Historical Recommendation Tracking
- Weekly Performance Tracking
- Trefferquote
- Risk/Reward Statistik
- Backtesting

### Reporting
- PDF Export
- Chart Rendering
- Telegram Trade Summary
- Telegram Charts
- Telegram Alerts

---

## Ziel des Projekts

Das Ziel ist ein institutionell orientiertes Analyse- und Screening-System mit:

- datengetriebener Marktanalyse
- automatisierten institutionellen Reports
- objektiver Qualitätskontrolle
- professionellem Risk Management
- skalierbarer Architektur

Das System soll Marktregime erkennen, qualitativ hochwertige Assets priorisieren und institutionelle Marktrotationen sichtbar machen.
