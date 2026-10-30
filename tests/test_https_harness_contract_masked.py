"""Contract guidance is distributed; these checks do not certify operator adoption."""

from pathlib import Path

import pytest

from mcp_loki_updates import InstructionsProvider

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/loki-bootstrap"


def test_additive_https_release_preserves_old_and_unknown_clients() -> None:
    provider = InstructionsProvider()
    metadata = provider.metadata()
    assert metadata["provider_version"] == "0.4.0"
    assert metadata["instructions_version"] == "2.3.0"
    assert metadata["mcp_contract_version"] == "2.3.0"
    assert provider.check_version("2.0.0", "2.0.0")["compatible"] is True
    assert provider.check_version("2.3.0", "2.3.0")["compatible"] is True
    assert provider.check_version()["compatible"] is None
    assert provider.check_version()["refresh_tools_required"] is None


@pytest.mark.parametrize("domain", InstructionsProvider().domains())
def test_each_runtime_domain_keeps_originals_in_harness_and_uses_https(domain: str) -> None:
    guide = InstructionsProvider().get(domain)["instructions"]
    for required in (
        "HTTPS",
        "loki.tominho.com/mcp",
        "Originais permanecem na harness",
        "parâmetros estruturados",
        "CSV tipado",
        "proveniência",
        "lacuna contratual",
        "Não reclassifique",
    ):
        assert required in guide, (domain, required)
    assert "attach_source_document" not in guide
    assert "arquive o original" not in guide
    assert "arquivar o original" not in guide


@pytest.mark.parametrize("domain", ("geral", "documentos", "aprovacoes"))
def test_registration_does_not_inherit_document_check_and_delivery_gates(domain: str) -> None:
    guide = InstructionsProvider().get(domain)["instructions"]
    assert "Somente com pacote" in guide
    assert "Sem pacote" in guide
    assert "recibo persistido" in guide


@pytest.mark.parametrize("domain", InstructionsProvider().domains())
def test_external_manifest_preserves_its_own_kind_and_never_claims_original_verification(
    domain: str,
) -> None:
    guide = InstructionsProvider().get(domain)["instructions"]
    for required in (
        "get_harness_source_contract",
        "register_harness_source",
        "get_harness_source",
        "EXTSRC",
        "kind=harness",
        "original_archived=false",
        "authenticated_harness_declaration",
        "manifest_hash",
        "não verifica os bytes originais",
    ):
        assert required in guide, (domain, required)


def test_onboarding_manifest_does_not_reuse_case_identity_or_opaque_document_ids() -> None:
    guide = (PLUGIN / "skills/operar-loki/references/WORKFLOWS.md").read_text()
    for required in (
        "register_onboarding_harness_source",
        "get_onboarding_harness_source",
        "onboarding_id",
        "document_id",
        "EXTSRC",
        "original_archived=false",
    ):
        assert required in guide, required


@pytest.mark.parametrize("domain", InstructionsProvider().domains())
def test_formal_provenance_is_optional_and_informal_input_keeps_automatic_origin(
    domain: str,
) -> None:
    guide = InstructionsProvider().get(domain)["instructions"]
    for required in (
        "`field_sources` é opcional",
        "informal",
        "ator",
        "data/hora",
        "informado, inferido e confirmado",
        "resultado dependente",
        "EXTSRC é opcional",
    ):
        assert required in guide, (domain, required)


def test_single_batch_and_registration_paths_do_not_equate_staging_with_execution() -> None:
    guide = (PLUGIN / "skills/operar-loki/references/WORKFLOWS.md").read_text()
    for required in (
        "CSV operacional",
        "referência estável por lote e por item",
        "staging não comprova execução",
        "recibo persistido",
        "document_outputs=[]",
        "releia o registro",
        "get_package_check_request",
        "sem pacote",
        "resposta perdida",
    ):
        assert required.casefold() in guide.casefold(), required


def test_operational_batch_guidance_preserves_per_row_resume_and_domain_result() -> None:
    guide = (PLUGIN / "skills/operar-loki/references/WORKFLOWS.md").read_text()
    for required in (
        "get_operational_batch_contract",
        "execute_operational_batch",
        "get_operational_batch(batch_id)",
        "loki.operational-batch/1",
        "schema_version;record_ref;operation;arguments;depends_on",
        "csv_content",
        "render-operational-csv",
        "operational-batch-request",
        "STARTED",
        "SUCCEEDED",
        "FAILED",
        "BLOCKED",
        "APPLIED",
        "não atômico",
    ):
        assert required in guide, required


def test_leave_uses_real_section_and_receipt_without_pdf_or_effect_claim() -> None:
    guide = InstructionsProvider().get("afastamento")["instructions"]
    assert "`leave`" in guide
    assert "dados_afastamento" not in guide
    for required in ("document_outputs=[]", "recibo persistido", "releia o registro"):
        assert required in guide
    assert "apply_case_effects" in guide
    assert "intenção humana" in guide


def test_restart_and_cancel_remain_human_actions_with_current_correction_snapshot() -> None:
    guide = (PLUGIN / "skills/operar-loki/references/WORKFLOWS.md").read_text()
    for required in (
        "restart_case",
        "cancel_case",
        "correction_snapshot",
        "decidir_chat",
        "human_message",
        "automação",
        "aprovação ou efeito",
        "conciliação",
        "local-v1",
        "structured-v1",
    ):
        assert required.casefold() in guide.casefold(), required


def test_partial_termination_history_guidance_separates_selection_from_consumption() -> None:
    guide = InstructionsProvider().get("rescisao")["instructions"]
    for required in (
        "get_case_historical_state",
        "apply_historical_state",
        "parcelas independentes",
        "dependentes desconhecidos",
        "IRRF",
        "saldo FGTS",
        "raiz mínima",
        "episódio errado",
        "revisão superada",
        "consumo",
        "folha",
    ):
        assert required.casefold() in guide.casefold(), required


def test_company_changes_require_identity_revision_sources_and_readback() -> None:
    for guide in (
        InstructionsProvider().get("alteracao_cadastral")["instructions"],
        (PLUGIN / "skills/operar-loki/references/WORKFLOWS.md").read_text(),
    ):
        for required in (
            "empresa e estabelecimentos",
            "parâmetros e regras",
            "vigência",
            "revisão esperada",
            "CNPJ",
            "recibo persistido",
            "releia",
            "outra empresa",
        ):
            assert required.casefold() in guide.casefold(), required


def test_company_config_uses_existing_writers_optional_origin_and_specific_human_gates() -> None:
    for guide in (
        InstructionsProvider().get("alteracao_cadastral")["instructions"],
        (PLUGIN / "skills/operar-loki/references/WORKFLOWS.md").read_text(),
    ):
        for required in (
            "get_client_config",
            "get_client_config_history",
            "validate_client_config",
            "apply_client_config",
            "loki.company-config-provenance/1",
            "proveniencia",
            "confirmacao",
            "expected_hash",
            "reserved_paths",
            "evidence_gate_paths",
            "human_message",
            "RASCUNHO",
            "APLICADO",
            "receipt_hash",
            "configurar_cliente",
            "field_basis",
        ):
            assert required in guide, required


def test_vacation_planning_has_own_receipt_and_separates_human_corrections() -> None:
    guide = InstructionsProvider().get("ferias")["instructions"]
    for required in (
        "get_vacation_schedule_contract",
        "record_vacation_schedule",
        "get_vacation_schedules",
        "loki.vacation-schedule/1",
        "correction_snapshot",
        "register",
        "rectify",
        "cancel",
        "supersedes_id",
        "supersedes_input_hash",
        "human_message",
        "message_reference",
        "gozo confirmado",
        "pagamento real",
    ):
        assert required.casefold() in guide.casefold(), required


def test_digital_ctps_number_uses_qualified_cpf_but_never_physical_fields() -> None:
    guide = InstructionsProvider().get("admissao")["instructions"]
    for required in (
        "CTPS Digital usa o CPF como número",
        "perguntas 8 e 28",
        "https://www.gov.br/trabalho-e-emprego/",
        "modalidade digital",
        "kind=rule",
        "foundation",
        "CPF qualificado",
        "CTPS física",
        "não fabrique série ou UF",
    ):
        assert required.casefold() in guide.casefold(), required
    assert "Não derive número, série ou UF da CTPS a partir do CPF" not in guide


def test_admission_distinguishes_dates_explicit_no_parentage_and_dependent_roles() -> None:
    guide = InstructionsProvider().get("admissao")["instructions"]
    for required in (
        "data_emissao_docs",
        "assinatura efetiva",
        "data de admissão",
        "data_expedicao_ctps",
        "00:00",
        "deficiência",
        "Não",
        "nome_pai",
        "nome_mae",
        "RG",
        "filiação",
        "beneficiários",
        "IR",
        "salário-família",
        "certidão",
        "recibo",
    ):
        assert required.casefold() in guide.casefold(), required


def test_adoption_requires_observed_https_execution_and_keeps_existing_schedule() -> None:
    guide = (ROOT / "docs/ANA_ROUTINE_ACTIVATION.md").read_text()
    for required in (
        "100%HTTPS",
        "identidade própria",
        "caso único",
        "lote CSV",
        "registro sem documento",
        "ajuste empresarial",
        "05h",
        "02h",
        "execução observada",
        "não comprova",
    ):
        assert required.casefold() in guide.casefold(), required
