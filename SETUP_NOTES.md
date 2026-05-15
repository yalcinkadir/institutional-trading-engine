# SETUP NOTES

## Wo Secret liegt

Der API-Key liegt in GitHub unter:

**Settings → Secrets and variables → Actions**

Name des Secrets:

`POLYGON_API_KEY`

Wichtig:
- API-Key niemals im Code speichern
- API-Key niemals in README oder Reports schreiben
- Bei Verdacht auf Leak sofort rotieren

---

## Was aktuell funktioniert

Der Cloud-Scanner läuft aktuell über **GitHub Actions** und erzeugt automatisch Markdown-Reports im Ordner `reports/`.

### Funktionsfähig:
- Polygon-Datenabruf über GitHub Actions
- automatischer Report mit Zeitstempel im Dateinamen
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
- Benchmark-Logik aktuell angepasst für:
  - QQQ-basierte Tech/Growth-Aktien
  - SPY für SPY selbst
  - GLD für GLD/SLV Vergleich

### Aktuell gescannte Symbole:
- AAPL
- MSFT
- NVDA
- META
- AMZN
- GOOGL
- AVGO
- AMD
- MU
- ADBE
- CSCO
- CRM
- QQQ
- SPY
- GLD
- SLV

---

## Was bewusst noch fehlt

Diese Punkte sind aktuell **absichtlich noch nicht umgesetzt**:

- kein MCP-Server
- kein Dashboard / Frontend
- keine Datenbank
- kein Backtesting
- keine Alerts per Telegram / E-Mail
- keine automatische Order-Logik
- keine Exit-Engine im Scanner integriert
- keine Portfolio-Heat / Positionsgrößen-Steuerung
- keine VIX-Integration mit stabilem Feed
- keine feinere Branchen-/ETF-Benchmark-Zuordnung wie:
  - SMH für Semis
  - IGV für Software
  - XLF / XLV / XLY etc. für weitere Sektoren

---

## Nächste Ideen

Sinnvolle nächste Schritte:

### Kurzfristig
- `SYMBOLS` in `config.py` auslagern
- README aktuell halten
- VIX sauber anbinden
- Benchmark-Zuordnung weiter verbessern
- Watchlist um weitere Qualitätsnamen erweitern

### Mittelfristig
- Exit-Logik integrieren
- Portfolio-Risiko-Modul ergänzen
- Reports kompakter und priorisierter machen
- Candidate-Scoring einbauen
- „Clean Setup Score“ ergänzen

### Später
- Backtesting
- Datenbank / Journal
- Dashboard
- MCP / API-Schicht
- Mobile-optimierte Bedienung

---

## Aktueller Projektstatus

Der Scanner ist aktuell auf einem brauchbaren Stand für:

- Marktüberblick
- relative Stärke / Schwäche
- Setup-Vorsortierung
- Erkennung von überdehnten oder riskanten Kandidaten

Er ist aktuell **ein Cloud-basierter Analyse-Scanner**, kein vollständiges Trading-System.
