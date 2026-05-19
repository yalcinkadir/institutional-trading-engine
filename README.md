# Institutional Trading Engine

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![CI](https://img.shields.io/badge/CI-enabled-brightgreen.svg)
![Status](https://img.shields.io/badge/status-production--oriented-orange.svg)

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
- applies institutional risk overrides

---

# Quick Start

## Requirements

- Python 3.11+
- Git
- Polygon.io API Key
- GitHub Actions enabled

---

## Installation

Clone repository:

```bash
git clone https://github.com/yalcinkadir/institutional-trading-engine.git
cd institutional-trading-engine
```

Create virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Setup

Create:

```text
.env
```

Example:

```env
POLYGON_API_KEY=your_api_key
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

---

## Generate Premarket Report

```bash
python scripts/generate_report.py \
  --type premarket \
  --output reports/premarket/test-report.md
```

---

## Generate Outcome Reports

```bash
python scripts/generate_outcomes.py
```

---

## Run Tests

```bash
pytest
```

---

# Repository Structure

```text
institutional-trading-engine/
├── .github/workflows/
├── reports/
├── scripts/
├── src/
│   ├── core/
│   ├── data/
│   ├── governance/
│   ├── monitoring/
│   ├── network/
│   ├── optimization/
│   ├── outcomes/
│   ├── reporting/
│   ├── simulation/
│   ├── storage/
│   └── strategy/
├── tests/
├── data/
└── README.md
```

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
Negative Override Layer
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

# Decision Safety Architecture

One of the most important architectural principles:

```text
High scores alone are NOT enough.
```

The platform now includes:

```text
Negative Override Logic
```

Purpose:
Prevent dangerous recommendations even when setup scores are high.

Example:

```text
NVDA
Score: 90
Conviction: High

BUT:
- Earnings tomorrow
- VIX elevated
- Event risk high

→ Final recommendation downgraded automatically
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
- institutional recommendation logic

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
- risk override validation

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
- outcome review

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

---

# Outcome Tracking System

Location:

```text
scripts/generate_outcomes.py
src/outcomes/
reports/outcomes/
```

Generated files:

```text
reports/outcomes/
├── YYYY-MM-DD-outcomes.md
├── latest-outcomes.md
├── outcome-history.json
└── signal-performance.json
```

Capabilities:

- WIN / LOSS / NEUTRAL classification
- signal extraction
- winrate analysis
- average performance tracking
- signal persistence
- structured JSON output

---

# Telegram Integration

Reports are automatically delivered to Telegram.

Required GitHub Secrets:

```env
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

---

# Market Regime Engine

Location:

```text
src/reporting/market_regime.py
```

Data states:

```text
LIVE
PARTIAL
FALLBACK
```

The platform supports:

```text
Graceful Degradation
```

Single feed failures no longer destroy the entire report.

---

# Testing

Run all tests:

```bash
pytest
```

Run specific test file:

```bash
pytest tests/test_negative_override.py
```

Test coverage includes:

- governance
- reporting
- optimization
- outcome tracking
- monitoring
- simulation
- probabilistic infrastructure
- negative override logic

---

# GitHub Actions

Main workflows:

```text
.github/workflows/institutional-reports.yml
.github/workflows/outcome-tracking.yml
.github/workflows/daily-backup.yml
```

Responsible for:

- scheduled reports
- outcome generation
- Telegram delivery
- report archival
- quality validation
- backups
- artifact uploads

---

# Contributing

Contributions are welcome.

Recommended workflow:

```text
1. Create feature branch
2. Add implementation
3. Add tests
4. Run pytest
5. Open pull request
```

---

# License

Currently:

```text
All Rights Reserved
```

Until an open-source license is explicitly added.

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
- outcome tracking automation
- negative override layer
- graceful degradation
- quality validation

Still missing for full production maturity:

- streaming pipelines
- dashboard UI
- Redis cache
- async workers
- Postgres migration
- feature importance
- regime similarity engine
- ML inference
- observability dashboards
- real market outcome evaluation

---

# Disclaimer

This project is intended for:

- research
- education
- institutional analysis experiments

It is not financial advice.
