# Position-Level Risk Attribution

Phase B5 adds a deterministic position-level risk attribution gate.

The goal is to explain portfolio R by position, beta, factor, sector and specific contribution. If the portfolio loses money, the report should show whether the loss came from market beta, factor exposure, sector concentration or single-name idiosyncratic risk.

## Inputs

The attribution engine accepts records with:

```text
symbol or ticker
sector or gics_sector
weight or position_weight or size
result_r or r_multiple or paper_r
beta or market_beta
market_return_r or benchmark_r
factor_exposures or factors
factor_returns
```

## Metrics

The report calculates:

```text
positions
portfolio_r
beta_contribution_r
factor_contribution_r
specific_contribution_r
unattributed_r
max_single_name_contribution_r
max_sector_contribution_r
max_factor_contribution_r
unknown_sector_count
sector_contributions
factor_contributions
position_attributions
```

## Gates

Default fail-closed gates:

```text
min_positions = 1
max_single_name_contribution_r = 1.0
max_sector_contribution_r = 2.0
max_factor_contribution_r = 2.0
max_abs_unattributed_r = 1.0
require_known_sector = true
```

## Outputs

The module can write:

```text
position_risk_attribution.json
position_risk_attribution.md
```

## Operational Rule

Position-level risk attribution is an evidence-quality gate. A pass does not approve live capital. A concentration or unknown-sector failure should block escalation and trigger manual review.
