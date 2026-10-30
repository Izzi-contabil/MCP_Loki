"""Prepared fiscal records stay distinct from signatures, delivery and authority."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

from mcp_loki_updates import InstructionsProvider

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "plugins/loki-bootstrap/skills/operar-loki/references/ESOCIAL.md"
CONTRACT = ROOT / "tests/fixtures/company_esocial_contract_masked.json"
CANDIDATE_TOOLS = (
    "get_company_esocial_candidate_contract",
    "prepare_company_esocial_candidate",
    "get_company_esocial_candidate",
    "cancel_company_esocial_candidate",
)


def test_preparation_release_preserves_core_compatibility_and_unknown_discovery() -> None:
    provider = InstructionsProvider()
    metadata = provider.metadata()
    assert metadata["provider_version"] == "0.4.0"
    assert metadata["instructions_version"] == "2.3.0"
    assert metadata["mcp_contract_version"] == "2.3.0"
    assert metadata["minimum_plugin_version"] == "2.0.0"
    for version in ("2.0.0", "2.1.0", "2.2.0", "2.3.0"):
        assert provider.check_version(version, version)["compatible"] is True
    assert provider.check_version()["refresh_tools_required"] is None


@pytest.mark.parametrize("domain", ("geral", "alteracao_cadastral"))
def test_candidate_operations_and_limits_are_in_runtime_and_native_guidance(domain: str) -> None:
    runtime = InstructionsProvider().get(domain)["instructions"]
    native = GUIDE.read_text(encoding="utf-8")
    for guide in (runtime, native):
        for name in CANDIDATE_TOOLS:
            assert name in guide, (domain, name)
        for concept in (
            "loki.company-esocial-candidate/1",
            "S-1005",
            "sem assinatura",
            "transmission_ready=false",
            "não cria candidatos",
            "não redireciona",
        ):
            assert concept in guide, (domain, concept)


@pytest.mark.parametrize("include_null", (False, True))
def test_actual_offline_contract_accepts_absent_end_without_fabricated_date(
    include_null: bool,
) -> None:
    schema = json.loads(CONTRACT.read_text(encoding="utf-8"))["company_parameters_schema"]
    profile = {
        "id": "masked-open-profile",
        "establishment_cnpj": "11222333000181",
        "valid_from": "2026-01-01",
        "cnae_preponderante": "5611201",
        "rat_bps": 200,
    }
    if include_null:
        profile["valid_until"] = None
    jsonschema.validate(profile, schema, format_checker=jsonschema.FormatChecker())


def test_open_end_and_movement_report_guidance_preserves_unknowns_and_scope() -> None:
    guide = InstructionsProvider().get("alteracao_cadastral")["instructions"]
    for term in (
        "valid_until",
        "fim não informado",
        "não invente data final",
        "relatório de movimentações",
        "matrícula",
        "admissão",
        "conteúdo completo",
    ):
        assert term in guide, term
