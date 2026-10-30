"""Distribuição do contrato operacional; não comprova uso pelo executor instalado."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

from mcp_loki_updates import InstructionsProvider

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/loki-bootstrap"
sys.path.insert(0, str(PLUGIN / "skills/operar-loki/scripts"))

RETIRED = (
    "prepare_shadow_",
    "record_shadow",
    "get_shadow",
    "simulate_case_version",
    "submit_document_extraction",
    "apply_document_extraction",
    "abandon_document_extraction",
    "migrate_document_processing_case",
    "get_document_processing_contract",
    "get_document_processing_status",
    "get_document_verification_request",
    "submit_document_verification",
    "ingest_ticket",
    "replay_termination_snapshot",
)


def test_major_two_refuses_declared_old_clients_and_preserves_unknown() -> None:
    provider = InstructionsProvider()
    metadata = provider.metadata()
    assert metadata["provider_version"] == "0.4.0"
    assert metadata["instructions_version"] == "2.3.0"
    assert metadata["mcp_contract_version"] == "2.3.0"
    assert provider.check_version("1.1.7", "1.0.0")["compatible"] is False
    assert provider.check_version("2.0.0", "2.0.0")["compatible"] is True
    assert provider.check_version()["compatible"] is None
    assert provider.check_version()["refresh_tools_required"] is None


def test_current_kit_compatibility_has_no_installation_claim() -> None:
    instructions = InstructionsProvider().get("geral")["instructions"]
    assert "loki-document-kit0.2.0" in instructions
    assert "0.1.0" in instructions
    assert "não comprova instalação" in instructions


def test_effect_corrections_and_payroll_history_keep_explicit_source_qualification() -> None:
    provider = InstructionsProvider()
    general = provider.get("geral")["instructions"]
    workflows = (PLUGIN / "skills/operar-loki/references/WORKFLOWS.md").read_text(encoding="utf-8")
    for guide in (general, workflows):
        for field in (
            "apply_case_effects",
            "supersedes_effect_id",
            "supersedes_input_hash",
            "withdraw:true",
            "history_qualifications.payroll_context",
            "loki.operational-payroll-context/1",
        ):
            assert field in guide
        assert "pagamento real" in guide
        assert "reconciliação" in guide


def test_operational_package_checks_delivery_and_opening_have_current_guidance() -> None:
    provider = InstructionsProvider()
    for name in ("geral", "documentos", "aprovacoes"):
        instructions = provider.get(name)["instructions"]
        for tool in (
            "get_package_check_request",
            "record_package_checks",
            "prepare_delivery",
            "authorize_delivery",
            "execute_delivery",
            "get_delivery_status",
        ):
            assert tool in instructions, (name, tool)
        assert "PASS" in instructions and "FAIL" in instructions
    general = provider.get("geral")["instructions"]
    assert "opening_selection" in general
    assert "opening_cents=null" in general
    assert "opening_origin" in general
    operator = (PLUGIN / "skills/operar-loki/SKILL.md").read_text(encoding="utf-8")
    workflows = (PLUGIN / "skills/operar-loki/references/WORKFLOWS.md").read_text(encoding="utf-8")
    for text in (operator, workflows):
        assert "record_package_checks" in text
        assert "authorize_delivery" in text
        assert "get_delivery_status" in text


def test_requester_delivery_is_default_and_drive_requires_future_explicit_opt_in() -> None:
    provider = InstructionsProvider()
    guides = [provider.get(name)["instructions"] for name in ("geral", "documentos", "aprovacoes")]
    guides.extend(
        path.read_text(encoding="utf-8")
        for path in (
            PLUGIN / "skills/operar-loki/SKILL.md",
            PLUGIN / "skills/operar-loki/references/WORKFLOWS.md",
        )
    )
    for guide in guides:
        for field in (
            "include_drive=False",
            "private_authenticated_requester",
            "requester_documents",
            "authenticated_path",
            "mcp_resource",
            "drive_documents=[]",
            "requester_delivery_approval_missing",
            "delivery_drive_not_requested",
            "include_drive=True",
            "authorize_external_delivery=true",
        ):
            assert field in guide, field
        assert "Não configure nem ative o Drive nesta entrega" in guide
        assert "não autoriza envio externo" in guide


def test_provenance_keeps_registered_sources_without_uploading_originals():
    provider = InstructionsProvider()
    for domain in provider.domains():
        guide = provider.get(domain)["instructions"]
        assert "Originais permanecem na harness" in guide, domain
        assert "document.reference" in guide, domain
        assert "kind=declaration" in guide, domain
    workflows = (PLUGIN / "skills/operar-loki/references/WORKFLOWS.md").read_text(encoding="utf-8")
    assert "document.reference" in workflows
    assert "fonte já registrada" in workflows
    assert "caminho local" in workflows.casefold()


def test_runtime_domains_and_operator_references_route_direct_structured_input() -> None:
    provider = InstructionsProvider()
    assert {"geral", "documentos", "admissao", "rescisao"} <= set(provider.domains())
    delivered = {name: provider.get(name)["instructions"] for name in provider.domains()}
    for name, text in delivered.items():
        assert "get_process_contract" in text, name
        assert "receive_case_data" in text, name
        assert not any(retired in text for retired in RETIRED), name
    live = [
        PLUGIN / "SKILL.md",
        *PLUGIN.glob("skills/*/SKILL.md"),
        *PLUGIN.glob("skills/*/references/*.md"),
    ]
    for path in live:
        text = path.read_text(encoding="utf-8")
        assert not any(retired in text for retired in RETIRED), str(path)
    workflow = (PLUGIN / "skills/operar-loki/references/WORKFLOWS.md").read_text(encoding="utf-8")
    for field in (
        "loki.case-data/1",
        "request_ref",
        "expected_snapshot",
        "input_snapshot",
        "field_sources",
        "foundation",
    ):
        assert field in workflow


def contract() -> dict:
    return {
        "schema_version": "loki.process-contract/1",
        "data_section": "dados_sinteticos",
        "data_schema": {"type": "object"},
        "input_schema": {
            "type": "object",
            "properties": {
                "schema_version": {"const": "loki.case-data/1"},
                "request_ref": {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,95}$"},
                "expected_snapshot": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
                "data": {"type": "object"},
                "field_sources": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "object",
                        "properties": {
                            "kind": {
                                "enum": [
                                    "document",
                                    "harness",
                                    "declaration",
                                    "inference",
                                    "context",
                                    "history",
                                    "rule",
                                ]
                            },
                            "reference": {"type": "string", "minLength": 1},
                            "locator": {"type": "string", "minLength": 1},
                        },
                        "required": ["kind", "reference", "locator"],
                        "additionalProperties": False,
                    },
                },
            },
            "required": [
                "schema_version",
                "request_ref",
                "expected_snapshot",
                "data",
            ],
            "additionalProperties": False,
        },
    }


def evidence() -> dict:
    return {
        "data": {"zero": 0, "missing": None, "flags": [False]},
        "field_sources": {
            path: {
                "kind": "document",
                "reference": "masked-file",
                "locator": "page:1/campo:" + path,
            }
            for path in ("zero", "missing", "flags[0]")
        },
    }


def prepare(*args: object, **kwargs: object) -> dict:
    module = importlib.import_module("loki_readers.exchange")
    function = getattr(module, "case_data_request", None)
    assert callable(function), "falta preparação do request operacional"
    return function(*args, **kwargs)


def test_offline_request_preserves_typed_data_and_uses_new_writer() -> None:
    result = prepare(
        evidence(), contract(), "case-masked", reference="request-1", snapshot="a" * 64
    )
    assert result["tool"] == "receive_case_data"
    assert result["arguments"]["case_id"] == "case-masked"
    body = result["arguments"]["request"]
    assert body == {
        "schema_version": "loki.case-data/1",
        "request_ref": "request-1",
        "expected_snapshot": "a" * 64,
        **evidence(),
    }
    assert result["state"] == "prepared_not_sent"
    assert "content_base64" not in str(result)


def test_case_helper_refuses_integral_float_even_when_json_schema_calls_it_integer():
    from loki_readers.private import ReadError

    schema = contract()
    schema["data_schema"] = {"type": "object", "properties": {"value_cents": {"type": "integer"}}}
    evidence = {
        "data": {"value_cents": 300000.0},
        "field_sources": {
            "value_cents": {
                "kind": "declaration",
                "reference": "masked-source",
                "locator": "masked-value",
            }
        },
    }
    with pytest.raises(ReadError, match="case_data_float_not_allowed"):
        prepare(evidence, schema, "case-masked", reference="masked-float", snapshot="a" * 64)


@pytest.mark.parametrize(
    "fault",
    [
        None,
        "nested_partial",
        "money_type",
        "extra",
        "negative",
        "nested_extra",
        "explicit_null",
        "array_missing",
        "array_null",
    ],
)
def test_offline_case_request_accepts_partial_fields_without_weakening_provided_constraints(fault):
    from loki_readers.private import ReadError

    schema = contract()
    schema["data_schema"] = {
        "type": "object",
        "additionalProperties": False,
        "required": ["salario_base_cents", "data_desligamento", "period"],
        "properties": {
            "salario_base_cents": {"type": "integer", "minimum": 0},
            "data_desligamento": {"type": "string", "format": "date"},
            "periods": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id"],
                    "properties": {"id": {"type": "integer"}},
                },
            },
            "period": {
                "type": "object",
                "required": ["start", "end"],
                "additionalProperties": False,
                "properties": {
                    "start": {"type": "string", "format": "date"},
                    "end": {"type": "string", "format": "date"},
                },
            },
        },
    }
    data = {"salario_base_cents": 300000}
    if fault == "nested_partial":
        data = {"period": {"start": "2026-10-01"}}
    if fault == "money_type":
        data["salario_base_cents"] = "300000"
    if fault == "extra":
        data["surprise"] = 1
    if fault == "negative":
        data["salario_base_cents"] = -1
    if fault == "nested_extra":
        data = {"period": {"unknown": "2026-10-01"}}
    if fault == "explicit_null":
        data = {"salario_base_cents": None}
    if fault == "array_missing":
        data = {"periods": [{}]}
    if fault == "array_null":
        data = {"periods": [{"id": None}]}
    from loki_readers.exchange import _leaves

    evidence = {
        "data": data,
        "field_sources": {
            path: {"kind": "declaration", "reference": "masked-source", "locator": path}
            for path in _leaves(data)
        },
    }
    if fault in {None, "nested_partial", "explicit_null"}:
        assert (
            prepare(evidence, schema, "case-masked", reference="masked-partial", snapshot="a" * 64)[
                "arguments"
            ]["request"]["data"]
            == data
        )
    else:
        with pytest.raises(ReadError, match="parameter_schema_invalid"):
            prepare(evidence, schema, "case-masked", reference="masked-partial", snapshot="a" * 64)


@pytest.mark.parametrize("fault", ["old_source", "old_envelope", "wrong_contract"])
def test_offline_request_rejects_malformed_supplied_sources_and_retired_shapes(fault: str) -> None:
    from loki_readers.private import ReadError

    data = evidence()
    schema = contract()
    if fault == "old_source":
        data["field_sources"]["zero"] = {"basis": "documented", "source_sha256": "a" * 64}
    elif fault == "old_envelope":
        data["documents"] = []
    else:
        schema["schema_version"] = "retired/1"
    with pytest.raises(ReadError, match="case_data|parameter_schema"):
        prepare(data, schema, "case-masked", reference="request-1", snapshot="a" * 64)


@pytest.mark.parametrize(
    "sources",
    [
        None,
        {},
        {"zero": {"kind": "declaration", "reference": "pedido-informal", "locator": "mensagem"}},
    ],
)
def test_informal_case_request_needs_no_formal_evidence_or_full_source_coverage(sources) -> None:
    data = {
        "zero": 0,
        "deficiencia": "Não",
        "horario": "00:00",
        "missing": None,
        "flags": [False],
    }
    evidence = {"data": data}
    if sources is not None:
        evidence["field_sources"] = sources
    result = prepare(evidence, contract(), "case-masked", reference="informal-1", snapshot="a" * 64)
    request = result["arguments"]["request"]
    assert request["data"] == data
    assert ("field_sources" in request) is (sources is not None)
    if sources is not None:
        assert request["field_sources"] == sources
    assert "content_base64" not in str(result)
    assert "EXTSRC" not in str(result)


def test_supplied_source_for_unknown_field_is_still_rejected() -> None:
    from loki_readers.private import ReadError

    data = evidence()
    data["field_sources"]["unknown"] = {
        "kind": "declaration",
        "reference": "pedido",
        "locator": "msg",
    }
    with pytest.raises(ReadError, match="case_data"):
        prepare(data, contract(), "case-masked", reference="request-1", snapshot="a" * 64)


@pytest.mark.parametrize("kind", ["inference", "context"])
def test_optional_context_source_keeps_kind_without_inventing_hash_or_foundation(kind) -> None:
    data = {
        "data": {"zero": 0},
        "field_sources": {
            "zero": {"kind": kind, "reference": "pedido-informal", "locator": "mensagem"}
        },
    }
    result = prepare(data, contract(), "case-masked", reference="context-1", snapshot="a" * 64)
    assert result["arguments"]["request"]["field_sources"] == data["field_sources"]


def test_old_case_csv_destination_is_refused(tmp_path: Path) -> None:
    from loki_readers.exchange import csv_request
    from loki_readers.private import ReadError

    path = tmp_path / "reading_masked.csv"
    path.write_text("field;value\nzero;0\n")
    with pytest.raises(ReadError, match="case_data_required"):
        csv_request(path, "case", "case-masked")


@pytest.mark.parametrize("include_sources", [False, True])
def test_shipped_cli_prepares_current_case_writer_without_network(
    tmp_path: Path, include_sources: bool
) -> None:
    import json
    import subprocess

    source = tmp_path / "evidence_masked.json"
    data = evidence()
    if not include_sources:
        del data["field_sources"]
    source.write_text(json.dumps(data))
    schema = tmp_path / "contract_masked.json"
    schema.write_text(json.dumps(contract()))
    output = tmp_path / "pedido privado"
    result = subprocess.run(
        [
            sys.executable,
            str(PLUGIN / "skills/operar-loki/scripts/loki_local.py"),
            "case-request",
            str(source),
            str(output),
            "--contract",
            str(schema),
            "--target",
            "case-masked",
            "--reference",
            "request-1",
            "--snapshot",
            "a" * 64,
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads((output / "request.json").read_text(encoding="utf-8"))
    assert payload["tool"] == "receive_case_data"
    assert payload["arguments"]["request"]["data"] == evidence()["data"]
    assert ("field_sources" in payload["arguments"]["request"]) is include_sources
    assert payload["state"] == "prepared_not_sent"
