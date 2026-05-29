from __future__ import annotations

import sys
import types

import pytest

from src.config.external_edge_provider import (
    EXTERNAL_EDGE_PROVIDER_ENV,
    PUBLIC_DEMO_DEFAULTS_MARKER,
    resolve_decision_thresholds,
)
from src.config.thresholds import DEFAULT_THRESHOLDS, DecisionThresholds


def test_resolve_thresholds_uses_public_demo_defaults_without_external_provider(monkeypatch):
    monkeypatch.delenv(EXTERNAL_EDGE_PROVIDER_ENV, raising=False)

    resolved = resolve_decision_thresholds()

    assert resolved.thresholds == DEFAULT_THRESHOLDS
    assert resolved.source == PUBLIC_DEMO_DEFAULTS_MARKER
    assert resolved.public_demo_defaults is True
    assert resolved.thresholds.public_demo_defaults is True
    assert resolved.thresholds.version.startswith("public-demo-")


def test_resolve_thresholds_loads_external_provider_when_configured(monkeypatch):
    module_name = "tests_fake_external_threshold_provider"
    module = types.ModuleType(module_name)

    def get_decision_thresholds():
        return DecisionThresholds(
            tier1_setup_score=88.0,
            version="external-test-v1",
            public_demo_defaults=False,
        )

    module.get_decision_thresholds = get_decision_thresholds
    monkeypatch.setitem(sys.modules, module_name, module)
    monkeypatch.setenv(EXTERNAL_EDGE_PROVIDER_ENV, module_name)

    resolved = resolve_decision_thresholds()

    assert resolved.thresholds.tier1_setup_score == 88.0
    assert resolved.thresholds.version == "external-test-v1"
    assert resolved.source == module_name
    assert resolved.public_demo_defaults is False


def test_external_provider_must_expose_get_decision_thresholds(monkeypatch):
    module_name = "tests_fake_external_provider_missing_function"
    monkeypatch.setitem(sys.modules, module_name, types.ModuleType(module_name))
    monkeypatch.setenv(EXTERNAL_EDGE_PROVIDER_ENV, module_name)

    with pytest.raises(AttributeError):
        resolve_decision_thresholds()


def test_external_provider_must_return_decision_thresholds(monkeypatch):
    module_name = "tests_fake_external_provider_bad_return"
    module = types.ModuleType(module_name)
    module.get_decision_thresholds = lambda: {"tier1_setup_score": 88.0}
    monkeypatch.setitem(sys.modules, module_name, module)
    monkeypatch.setenv(EXTERNAL_EDGE_PROVIDER_ENV, module_name)

    with pytest.raises(TypeError):
        resolve_decision_thresholds()
