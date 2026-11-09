"""Published guidance names additive contracts without claiming business effects."""

import pytest

from mcp_loki_updates import InstructionsProvider


def test_new_contract_keeps_existing_clients_and_unknown_installations() -> None:
    provider = InstructionsProvider()
    assert provider.metadata()["provider_version"] == "0.4.10"
    assert provider.metadata()["mcp_contract_version"] == "2.6.1"
    for version in ("2.0.0", "2.3.0", "2.5.0", "2.6.0", "2.6.1"):
        assert provider.check_version(version, version)["compatible"] is True
    assert provider.check_version()["compatible"] is None


@pytest.mark.parametrize("domain", ["geral", "alteracao_cadastral"])
def test_onboarding_link_is_a_distinct_human_act_preserving_canonical_facts(domain: str) -> None:
    guide = InstructionsProvider().get(domain)["instructions"]
    for term in (
        "additional_declaration_reconciliation",
        "preview_company_onboarding_reconciliation",
        "reconcile_company_onboarding",
        "get_company_employee_effect_state",
        "reconciled_to_existing_fact",
        "reconciled_count",
        "applied_count",
        "CHAT_DECISIONS_ENABLED",
    ):
        assert term in guide, (domain, term)
    assert "não comprova equivalência factual" in guide


def test_support_reprocessing_reuses_a_current_reply_and_does_not_restart_questions() -> None:
    guide = InstructionsProvider().get("geral")["instructions"]
    for term in (
        "support_reprocess_contract",
        "loki.support-reprocess/1",
        "reprocess_problem_answers",
        "agent_schema",
        "não reinicia o ciclo",
        "resposta corrente",
        "expected_last_job",
    ):
        assert term in guide, term


def test_internal_failure_reprocessing_is_limited_to_the_current_procedure_reply() -> None:
    guide = InstructionsProvider().get("geral")["instructions"]
    for term in (
        "preparation_internal_failure",
        "intake/procedure",
        "proprietário",
        "resposta corrente",
        "não reinicia o ciclo",
        "não zera limites",
        "não prepara patch",
    ):
        assert term in guide, term


@pytest.mark.parametrize("domain", ["rescisao", "afastamento"])
def test_leave_guidance_separates_whole_episode_and_exact_payer_segment(domain: str) -> None:
    guide = InstructionsProvider().get(domain)["instructions"]
    for term in ("representacao", "episodio_integral", "faixa_pagador", "retorno_episodio"):
        assert term in guide, (domain, term)
    assert "não presume concessão" in guide


def test_monthly_diagnosis_reads_persisted_causes_without_recalculating() -> None:
    guide = InstructionsProvider().get("geral")["instructions"]
    for term in ("get_case_dossier", "diagnostics", "loki.payroll-diagnostics/1", "não recalcula"):
        assert term in guide
