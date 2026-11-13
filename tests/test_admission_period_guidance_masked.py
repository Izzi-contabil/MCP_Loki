"""Entrega do criterio de periodo salarial; nao mede obediencia semantica da harness."""

from mcp_loki_updates import InstructionsProvider


def test_explicit_pay_period_is_delivered_with_its_source_and_output_check() -> None:
    guide = InstructionsProvider().get("admissao")["instructions"]
    assert "### Período salarial" in guide
    assert "contrato.periodo_salario" in guide
    assert "Mensalista" in guide
    assert "valor integral" in guide
    assert "localizador" in guide
    assert "não confirma o período" in guide
    assert "categoria do vínculo" in guide
    assert "branco" in guide
    assert "pendência" in guide
    assert "overflow" in guide


def test_admission_unblocking_guidance_is_delivered_conditionally() -> None:
    provider = InstructionsProvider()
    guide = provider.get("admissao")["instructions"]
    for required in (
        "somente quando a resposta servida os apresentar",
        "ficha_registro/6",
        "nada é truncado",
        "replace_process_inputs",
        "preview_case_name_rectification",
        "case_only_equivalence",
        "registry_updated: false",
        "nominal_correction_requires_registry_correction",
        "unsupported_admission_event",
        "factual_confirmation_not_compensable",
        "unsupported_protected_dependency",
        "company_monthly_payroll",
        "não cancele nem",
        "siga o `next_action` recebido",
        "`restart_case` quando o caso foi processado",
        "forma Unicode",
        'error_type: "OverflowDeBeneficiarios"',
        "import_preservation_blocked_by_pending_effects",
        "não tem saída self-service",
        'access: "not_authorized_for_process"',
        "não reutilize prévia obtida por outra conta",
    ):
        assert required in guide, required
    assert 'next_action: "run_prepared_case_workflow"' not in guide
    general = provider.get("geral")["instructions"]
    for required in (
        "blocking_refs",
        "blocking_ref_count",
        "next_action",
        "Nenhuma proteção mudou",
        "`next_action` vem somente em `restart_case`",
        "nunca traz `next_action`",
        "aguardando_revisao",
    ):
        assert required in general, required
    assert provider.metadata()["mcp_contract_version"] == "2.6.3"
