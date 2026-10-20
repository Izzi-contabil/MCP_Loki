"""Versions express declared protocol compatibility, never remote tool discovery."""

from __future__ import annotations

from typing import Any

import pytest


def check(plugin: str | None = None, contract: str | None = None) -> dict[str, Any]:
    from mcp_loki_updates import InstructionsProvider

    return InstructionsProvider().check_version(plugin, contract)


@pytest.mark.parametrize(
    ("plugin", "contract", "compatible", "manual"),
    [
        (None, None, None, None),
        ("0.4.0", None, None, None),
        (None, "1.0.0", None, None),
        ("0.4.0", "1.0.0", True, False),
        ("0.5.0", "1.0.0", True, False),
        ("0.3.9", "1.0.0", False, True),
        ("0.3.9", None, False, True),
        (None, "0.9.0", False, True),
        ("0.5.0", "2.0.0", False, True),
        ("0.5.0", "1.0.1", False, True),
        ("0.4.0-rc.1", "1.0.0", False, True),
        ("0.4.0+local.1", "1.0.0", True, False),
        ("0.5.0", "1.0.0-rc.1", True, False),
    ],
)
def test_compatibility_requires_evidence_for_both_dimensions(
    plugin: str | None,
    contract: str | None,
    compatible: bool | None,
    manual: bool | None,
) -> None:
    result = check(plugin, contract)
    assert result["compatible"] is compatible
    assert result["manual_update_required"] is manual
    assert result["refresh_tools_required"] is None
    assert result["mcp_contract_version"] == "1.0.0"


@pytest.mark.parametrize("invalid", ["", "v0.4.0", "0.4", "00.4.0", "0.4.0-01", "a", "1.0.0\n"])
def test_invalid_client_version_is_not_treated_as_unknown(invalid: str) -> None:
    result = check(invalid, "1.0.0")
    assert result["compatible"] is False
    assert result["manual_update_required"] is True
    assert result["compatibility"]["plugin"]["reason"] == "invalid_version"


def test_categorized_changes_and_fallback_do_not_claim_remote_tools_are_synced() -> None:
    result = check("0.4.0", "1.0.0")
    assert result["recommended_plugin_version"] == "0.5.0"
    assert set(result["changes"]) == {
        "backend",
        "instructions",
        "compatible_tools",
        "breaking_contract",
        "plugin",
    }
    assert result["changes"]["compatible_tools"] == [
        "loki_obter_instrucoes",
        "loki_verificar_versao",
    ]
    assert result["fallback_functions"] == ["meu_acesso", "get_operator_context"]
    assert result["refresh_tools_required"] is None
    assert result["tools_refresh_note"]


@pytest.mark.parametrize("plugin", ["0.5.1", "1.0.0", "9.0.0"])
def test_future_plugin_version_remains_unassessed(plugin: str) -> None:
    result = check(plugin, "1.0.0")
    assert result["compatible"] is None
    assert result["manual_update_required"] is None
    assert result["compatibility"]["plugin"]["reason"] == "client_version_not_assessed"
