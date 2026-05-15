# TROUBLESHOOTING

## 1. Workflow schlägt fehl

Prüfen:
- GitHub → Actions → letzten Run öffnen
- Job `scan` öffnen
- rote Fehlermeldung ganz unten lesen

Typische Ursachen:
- `POLYGON_API_KEY` fehlt
- Rate Limit (`429`)
- Pfadfehler in `src/scanner.py`
- `requirements.txt` unvollständig
- GitHub Actions Permission fehlt

---

## 2. Fehler 429 (Too Many Requests)

Bedeutung:
- Polygon API wurde zu schnell oder zu oft abgefragt

Prüfen:
- `time.sleep(...)` zwischen Requests noch vorhanden?
- zu viele Symbole gleichzeitig?
- zu viele manuelle Workflow-Runs?

Maßnahmen:
- weniger Symbole scannen
- Delay zwischen API-Requests erhöhen
- später Symbole in Gruppen aufteilen

---

## 3. `POLYGON_API_KEY` fehlt

Symptom:
- Workflow bricht ab
- Fehlermeldung ähnlich wie:
  - `POLYGON_API_KEY fehlt`
  - keine Daten von Polygon

Prüfen:
- GitHub → Settings → Secrets and variables → Actions
- Secret-Name muss exakt sein:

`POLYGON_API_KEY`

Maßnahmen:
- Secret neu anlegen
- API-Key bei Polygon prüfen
- bei Leak: Key rotieren und alten deaktivieren

---

## 4. Kein Report wird geschrieben

Prüfen:
- Workflow erfolgreich oder fehlgeschlagen?
- wird im Job `Report created:` ausgegeben?
- existiert der Ordner `reports/`?
- hat Workflow `contents: write` Permission?

Maßnahmen:
- `.github/workflows/daily_scan.yml` prüfen
- `permissions: contents: write` prüfen
- GitHub Actions Permissions auf `Read and write` stellen
- prüfen, ob Commit/Push im Workflow funktioniert

---

## 5. Reports enthalten komische Werte

Mögliche Ursachen:
- Split-/Adjustierungsproblem
- ungeeigneter Benchmark
- extrem volatile Assets
- Datenanomalie

Maßnahmen:
- Asset einzeln prüfen
- Warnhinweise im Report beachten
- bei Bedarf Asset vorübergehend aus dem Universum entfernen

---

## 6. VIX ist `Unavailable`

Bedeutung:
- VIX konnte über Polygon nicht sauber geladen werden
- aktuell kein kritischer Fehler

Maßnahmen:
- Scanner kann trotzdem weiterlaufen
- später VIX-Datenquelle oder Ticker-Logik verbessern

---

## 7. Watchlist Candidates ist leer

Bedeutung:
- aktuell gibt es im gescannten Universum keine sauberen Setups
- das ist nicht automatisch ein Fehler

Maßnahmen:
- Report normal weiter nutzen
- Universum erweitern
- auf Pullbacks warten
- keine schlechten Trades erzwingen
