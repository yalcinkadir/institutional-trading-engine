# Institutional Trading Engine

Institutional-grade market analysis, reporting, screening, governance and outcome-tracking platform.

The project is designed as:

- modular
- auditable
- deterministic
- reproducible
- explainable
- risk-first
- production-oriented

The system is NOT intended to be a black-box trading bot.

Instead, it acts as an institutional intelligence platform that:

- analyzes markets
- evaluates regimes
- ranks opportunities
- generates reports
- validates report quality
- stores historical reports
- tracks outcomes
- measures signal quality
- prepares adaptive intelligence

---

# How The System Works

```text
Market Data
    ↓
Market Regime Engine
    ↓
Relative Strength & Screening
    ↓
Research / Macro / Risk Layers
    ↓
Decision Fusion
    ↓
Governance Controls
    ↓
Report Generation
    ↓
Telegram Delivery
    ↓
Historical Storage
    ↓
Outcome Tracking
    ↓
Adaptive Intelligence
```

---

# Reporting System

Location:

```text
scripts/generate_report.py
src/reporting/
```

The platform automatically generates institutional reports.

## Premarket Report

Purpose:
Prepare before the US market opens.

Schedule:
Sunday-Friday before market open.

Contains:

- SPY / QQQ trend analysis
- VIX analysis
- Market Health Score
- breadth analysis
- setup readiness
- watchlists
- risk warnings

---

## Postmarket Report

Purpose:
Analyze the completed market session.

Schedule:
Monday-Friday after market close.

Contains:

- leaders
- weak names
- volatility expansion
- signal validation
- relative strength review
- market regime confirmation

---

## Weekly Report

Purpose:
Strategic institutional review.

Schedule:
Saturday.

Contains:

- regime evolution
- strongest setups
- weak setups
- performance attribution
- strategic observations
- adaptive intelligence preparation

---

# Report Storage

Reports are automatically committed into the repository.

Structure:

```text
reports/
├── premarket/
├── postmarket/
├── weekly/
├── outcomes/
├── premarket-report.md
├── postmarket-report.md
└── weekly-report.md
```

Examples:

```text
reports/premarket/2026-05-19-premarket.md
reports/postmarket/2026-05-19-postmarket.md
reports/weekly/2026-W20-weekly.md
```

Meaning:

- dated files = historical archive
- latest files = current version

Important:

Historical reports are used later for:

- outcome tracking
- signal attribution
- adaptive intelligence
- regime similarity
- future ML analysis

---

# Telegram Integration

Reports are automatically delivered to Telegram.

Required GitHub Secrets:

```env
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

Telegram delivery includes:

- compact summary message
- full markdown report document

Summary contains:

- Market Regime
- Final Recommendation
- Leaders
- Weak Names
- Risk Warnings

---

# Market Regime Engine

Location:

```text
src/reporting/market_regime.py
```

Responsible for:

- SPY trend analysis
- QQQ trend analysis
- VIX analysis
- breadth analysis
- Market Health Score
- regime classification

Data states:

```text
LIVE
PARTIAL
FALLBACK
```

## LIVE
All market feeds loaded successfully.

## PARTIAL
Some feeds failed but the report still works.

Example:

```text
SPY ok
QQQ ok
VIX failed
```

## FALLBACK
Most or all market feeds failed.

---

# Polygon Data Layer

Location:

```text
src/data/polygon_client.py
```

Features:

- retry logic
- rate-limit handling
- timeout protection
- disk cache
- graceful recovery

Cache location:

```text
.cache/polygon/
```

---

# Governance Layer

Location:

```text
src/governance/
```

Responsible for:

- risk limits
- compliance checks
- kill switches
- exposure policies

Purpose:
Prevent unstable or dangerous recommendations.

---

# Optimization Layer

Location:

```text
src/optimization/
```

Responsible for:

- portfolio optimization
- capital allocation
- risk/reward analysis
- adaptive weighting

---

# Intelligence Network

Location:

```text
src/network/
```

Responsible for:

- multi-agent coordination
- distributed analysis
- consensus building
- intelligence sharing

Purpose:
Simulate institutional multi-engine decision systems.

---

# Outcome Tracking

Location:

```text
src/outcomes/
reports/outcomes/
```

Current status:

```text
FOUNDATION IMPLEMENTED
AUTO-GENERATION NOT YET ACTIVE
```

Currently implemented:

- signal classification
- win/loss analysis
- regime performance analysis
- outcome summaries

Not yet implemented:

- automatic daily outcome generation
- automatic signal extraction from reports
- automatic performance comparison

This is why:

```text
reports/outcomes/
```

may still be empty.

Planned future structure:

```text
reports/outcomes/
├── 2026-05-19-outcomes.md
├── 2026-05-20-outcomes.md
└── latest-outcomes.md
```

---

# Database & Persistence

Location:

```text
src/storage/sqlite_store.py
```

Current persistent storage:

- reports
- signals
- telemetry

Database:

```text
data/institutional_engine.db
```

---

# Monitoring & Telemetry

Location:

```text
src/monitoring/
```

Responsible for:

- telemetry tracking
- operational metrics
- anomaly alerts
- production monitoring

Examples:

- high latency
- high failure rate
- low cache efficiency

---

# Quality Validation

Location:

```text
scripts/validate_report_quality.py
```

Before reports are:

- committed
- uploaded
- sent to Telegram

The system validates quality.

Minimum score:

```text
75
```

Low-quality reports are rejected.

---

# Backup System

Location:

```text
scripts/create_backup.py
.github/workflows/daily-backup.yml
```

Daily backups include:

```text
reports/
data/
.cache/polygon/
```

Backup artifacts are uploaded automatically.

---

# GitHub Actions

Main workflows:

```text
.github/workflows/institutional-reports.yml
.github/workflows/daily-backup.yml
```

Responsible for:

- scheduled reports
- Telegram delivery
- report archival
- quality validation
- backups
- artifact uploads

---

# Testing

Run tests:

```bash
pytest
```

Test coverage includes:

- governance
- reporting
- optimization
- outcome tracking
- monitoring
- simulation
- probabilistic infrastructure
- network layer
- memory systems
- quality infrastructure

---

# Current Platform Status

Current maturity:

```text
Production-Oriented Institutional Intelligence Platform
```

Implemented:

- report automation
- historical report storage
- Telegram integration
- governance controls
- optimization layer
- intelligence network
- monitoring
- backups
- probabilistic infrastructure
- outcome tracking foundation
- quality validation

Still missing for full production maturity:

- streaming pipelines
- dashboard UI
- Redis cache
- async workers
- Postgres migration
- feature importance
- live outcome generation
- regime similarity engine
- ML inference
- observability dashboards

---

# Disclaimer

This project is intended for:

- research
- education
- institutional analysis experiments

It is not financial advice.
