"""Optional external edge provider boundary.

IP4 keeps public framework defaults separate from local production research inputs.
The public repository must work without any external module. If an operator sets
``ITE_EXTERNAL_EDGE_PROVIDER`` to a local import path, that module may provide
replacement configuration objects without being committed here.
"""

from __future__ import annotations

import importlib
import os
from dataclasses import dataclass
from typing import Protocol

from src.config.thresholds import DecisionThresholds

EXTERNAL_EDGE_PROVIDER_ENV = "ITE_EXTERNAL_EDGE_PROVIDER"
PUBLIC_DEMO_DEFAULTS_MARKER = "public_demo_defaults_only"


class ThresholdProviderModule(Protocol):
    def get_decision_thresholds(self) -> DecisionThresholds: ...


@dataclass(frozen=True)
class ResolvedThresholds:
    thresholds: DecisionThresholds
    source: str
    public_demo_defaults: bool


def resolve_decision_thresholds(*, env_var: str = EXTERNAL_EDGE_PROVIDER_ENV) -> ResolvedThresholds:
    """Resolve decision thresholds through the public/default or external path.

    No environment variable means public demo defaults. This is the only path
    required for CI and public repository operation.
    """

    module_path = os.getenv(env_var, "").strip()
    if not module_path:
        from src.config.thresholds import DEFAULT_THRESHOLDS

        return ResolvedThresholds(
            thresholds=DEFAULT_THRESHOLDS,
            source=PUBLIC_DEMO_DEFAULTS_MARKER,
            public_demo_defaults=True,
        )

    module = importlib.import_module(module_path)
    if not hasattr(module, "get_decision_thresholds"):
        raise AttributeError(f"{module_path} must expose get_decision_thresholds().")

    thresholds = module.get_decision_thresholds()
    if not isinstance(thresholds, DecisionThresholds):
        raise TypeError("get_decision_thresholds() must return DecisionThresholds.")

    return ResolvedThresholds(
        thresholds=thresholds,
        source=module_path,
        public_demo_defaults=False,
    )
