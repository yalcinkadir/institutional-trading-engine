# CHANGELOG

## v0.1.1-cloud-scanner
### Added
- Cloudbasierter Market Scanner über GitHub Actions
- Polygon API Integration über GitHub Secrets
- Automatische Markdown-Reports im `reports/`-Ordner
- Zeitstempel im Report-Dateinamen
- RSI(14), ATR(14), ATR%, SMA20, SMA50, SMA200
- RVOL und 20D Return
- Relative Strength Spread vs Benchmark
- Market Regime Summary
- Watchlist Candidates
- Leaders / Aggressive Leaders
- Weak Names
- Setup Readiness
- Data / Risk Warnings
- Telegram Summary nach Workflow-Run
- Telegram Watchlist-Tradeplan mit:
  - Trigger
  - Entry Zone
  - Stop
  - Exit 1
  - Exit 2

### Improved
- Benchmark-Zuordnung nach Asset-Typ verbessert
- GLD/SLV nicht mehr gegen QQQ verglichen
- Telegram-Ausgabe kompakter und mobilfreundlicher gemacht
- Leaders-Sektion in Clean / Aggressive getrennt
- Setup-Labels verfeinert
- Konfiguration in `config.py` strukturiert

### Notes
- VIX ist aktuell noch nicht sauber integriert
- Scanner ist aktuell Analyse-/Screening-System, kein vollständiges Trading-System
- Exit-Logik in Telegram ist aktuell indikativ und regelbasiert
