"""Company fiscal guidance must describe the shipped HTTPS contract, never a sender.

The synthetic contract fixture was exported offline from backend f480052 (PR187).
It contains schemas and readiness limits only, without company data or credentials.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from mcp_loki_updates import InstructionsProvider

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/loki-bootstrap"
REFERENCE = PLUGIN / "skills/operar-loki/references/ESOCIAL.md"
SCRIPT = PLUGIN / "skills/operar-loki/scripts/loki_local.py"
CONTRACT = ROOT / "tests/fixtures/company_esocial_contract_masked.json"


def test_esocial_release_is_additive_and_keeps_old_clients_and_authority() -> None:
    provider = InstructionsProvider()
    metadata = provider.metadata()
    assert metadata["provider_version"] == "0.3.1"
    assert metadata["instructions_version"] == "2.2.0"
    assert metadata["mcp_contract_version"] == "2.2.0"
    assert metadata["minimum_plugin_version"] == "2.0.0"
    assert metadata["recommended_plugin_version"] == "2.2.0"
    for version in ("2.0.0", "2.1.0", "2.2.0"):
        assert provider.check_version(version, version)["compatible"] is True
    assert provider.check_version()["compatible"] is None
    assert provider.check_version()["refresh_tools_required"] is None
    assert "esocial" not in provider.domains()
    assert provider.get("alteracao_cadastral")["permissions"] == {
        "capabilities": ["consultar"],
        "processes": ["alteracao_cadastral"],
    }


@pytest.mark.parametrize("domain", ("geral", "alteracao_cadastral"))
def test_runtime_company_guidance_exposes_only_the_available_fiscal_flow(domain: str) -> None:
    guide = InstructionsProvider().get(domain)["instructions"]
    for operation in (
        "get_company_esocial_contract",
        "get_company_esocial_state",
        "preview_company_esocial_mode",
        "apply_company_esocial_mode",
        "get_company_parameter_state",
    ):
        assert operation in guide, (domain, operation)
    for requirement in (
        "loki.company-esocial/1",
        "homologacao",
        "tp_amb=2",
        "operacao",
        "tp_amb=1",
        "production_activation_supported=false",
        "esocial_activation_pending",
        "persisted=false",
        "fiscal_events_sent=0",
        "administrador humano",
        "S-1005",
        "não comprova transmissão",
    ):
        assert requirement in guide, (domain, requirement)


def test_company_parameter_guidance_preserves_optional_origin_exact_scope_and_consumption() -> None:
    guide = InstructionsProvider().get("alteracao_cadastral")["instructions"]
    for requirement in (
        "company_parameters",
        "establishment_cnpj",
        "valid_from",
        "valid_until",
        "rat_bps",
        "fap_10000",
        "basis",
        "informado",
        "inferido",
        "confirmado",
        "field_sources",
        "expected_hash",
        "validate_client_config",
        "apply_client_config",
        "profile_hash",
        "slice_hash",
        "financial_readiness_verified=false",
        "sem herança",
        "não complete zero",
    ):
        assert requirement in guide, requirement


def test_native_reference_is_reachable_and_keeps_fiscal_limits_visible() -> None:
    assert REFERENCE.is_file(), "falta o roteiro fiscal nativo"
    # Resolve links from the actual entrypoint, including the nested bootstrap.
    for path in (
        PLUGIN / "SKILL.md",
        PLUGIN / "skills/loki-bootstrap/SKILL.md",
        PLUGIN / "skills/operar-loki/SKILL.md",
        PLUGIN / "skills/operar-loki/references/WORKFLOWS.md",
    ):
        links = re.findall(r"\]\(([^)]+\.md)\)", path.read_text(encoding="utf-8"))
        assert REFERENCE.resolve() in {(path.parent / link).resolve() for link in links}, path
    guide = REFERENCE.read_text(encoding="utf-8")
    for requirement in (
        "expected_revision",
        "preview_hash",
        "human_message",
        "reference",
        "event_types",
        "cutover_on",
        "PENDING",
        "fiscal_dispatcher_not_configured",
        "signing_provider_not_configured",
        "company_representation_not_verified",
        "homologation_receipt_not_verified",
        "fila",
        "procuração",
        "assinatura",
        "recibo",
        "não transmite",
        "S-1005",
        "parameters",
        "/company_parameters_schema",
        "validated_not_sent",
        "--version",
    ):
        assert requirement in guide, requirement


def test_shipped_helper_reports_its_own_plugin_version_without_mcp() -> None:
    run = subprocess.run(
        [sys.executable, str(SCRIPT), "--version"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    manifest = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    assert run.returncode == 0, run.stderr
    assert run.stdout.strip() == f"loki-orientacoes {manifest['version']}"


@pytest.mark.parametrize("malformed", [False, True])
def test_existing_offline_parameters_command_uses_company_schema_without_filling_unknowns(
    tmp_path: Path, malformed: bool
) -> None:
    # This minimal declared profile has no rates, source/hash or fiscal credentials.
    # The generic helper must preserve it and reject undeclared credential fields.
    profile = {
        "id": "synthetic-2026",
        "establishment_cnpj": "00.000.000/0001-91",
        "valid_from": "2026-01-01",
        "valid_until": "2026-12-31",
        "basis": "inferido",
    }
    if malformed:
        profile["certificate_token"] = "SYNTHETIC_FORBIDDEN"
    source = tmp_path / "parameters_masked.json"
    source.write_text(json.dumps(profile), encoding="utf-8")
    output = tmp_path / "dados privados"
    run = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "parameters",
            str(source),
            str(output),
            "--schema",
            str(CONTRACT),
            "--schema-pointer",
            "/company_parameters_schema",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if malformed:
        assert run.returncode == 1
        assert "parameter_schema_invalid" in run.stderr
        assert "SYNTHETIC_FORBIDDEN" not in run.stderr
        assert not output.exists()
    else:
        assert run.returncode == 0, run.stderr
        assert json.loads(run.stdout)["status"] == "validated_not_sent"
        assert json.loads((output / "parameters.json").read_text(encoding="utf-8")) == profile
        assert not (output / "request.json").exists()
