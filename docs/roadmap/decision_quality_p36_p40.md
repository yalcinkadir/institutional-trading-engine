# Decision Quality and Validation Roadmap P36-P47

## Completed

- P36 Confidence Score Double Counting Fix
- P37 Probabilistic Engine Softmax Normalization
- P38 Regime Similarity Weighted Distance and Cosine Similarity
- P39 Adaptive Feedback Decay
- P40 MultiFactorFusion Recalibration
- P41 Historical Edge Validation Framework
- P42 Regime-Phase Backtest Matrix
- P43 Walk-Forward Validation
- P44 Execution Realism Layer
- P45 Out-of-Sample Validation Lockbox
- P46 Paper Trading Journal / Live Observation v2

## P47 Final Live Readiness Gate

Status: implemented, verification pending.

P47 consolidates the P41-P46 evidence into a final fail-closed readiness report.

Required evidence includes validated edge, regime-phase robustness, walk-forward stability, execution realism, out-of-sample robustness, paper observation quality, manual review, risk limits and kill-switch definition.

Readiness levels:

- NOT_READY
- OBSERVATION_ONLY
- REVIEW_READY

Staged capital-risk guidance:

- Months 1-3: maximum 50% size after all gates pass and manual review is complete.
- Months 4-6: maximum 75% size only if observed metrics remain at or above 85% of expectation.
- Month 7+: maximum 100% only if cumulatively profitable and drawdown remains below kill-switch limit.

Kill-switch rule: stop and review if live drawdown exceeds 1.5x backtest max drawdown.

## Boundary

This roadmap is for decision-support and validation quality only. It does not add broker connectivity or order execution.
