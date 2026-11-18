"""Entrega das orientações da 2.7.1 (Onda 1); nao mede obediencia da harness."""

import json
from pathlib import Path

from mcp_loki_updates import InstructionsProvider

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins/loki-bootstrap/skills"
OPERATOR = SKILLS / "operar-loki"
WORKFLOWS = OPERATOR / "references/WORKFLOWS.md"
CAPACITIES = OPERATOR / "references/CAPACIDADES_DP.md"
DOMAINS = ROOT / "src/mcp_loki_updates/data/domains"
RELEASE = ROOT / "src/mcp_loki_updates/data/release.json"

QUEUE = (
    '`durable_workflow.admission: "one_pending_job_per_company"`',
    "`company_job_pending`",
    "retry_enqueue_later",
    "`retry_after_seconds`",
    "`job_sources_changed`",
    "`job_not_found`",
    "Enfileire em série",
    "60 minutos",
)
QUEUE_DOMAIN = (
    "`pending_job: {case_id, job_id, request_ref}`",
    '`retry: "after_pending_job_terminal"`',
    "não grava nada",
    "**outro** caso da mesma empresa",
    "Leituras são seguras",
    "Em 524 ou timeout, não reenvie às cegas",
    "**mesmo** `request_ref`",
    "`Retry-After`",
    "`company_job_pending` não é `BUSY`",
)
DIAGNOSTIC = (
    "`calculation_kind_unsupported`",
    "qualificar_afastamento_na_origem",
    "`dependent_fields`",
    "`next_action_after_primary`",
    "leave_qualification",
    "`population_hash`",
    "`payroll_population_dependencies_busy`",
)
DIAGNOSTIC_DOMAIN = (
    "`leave_qualification_incomplete`",
    "`missing_fields_complete: false`",
    "`history_qualifications.payroll_context`",
    '`origin: "company_onboarding"`',
    '`origin: "operational_effect"`',
    "`leave.periodos[N].responsabilidade`",
    "leave_qualification_not_recognized",
    "Um `EXTSRC` registrado em **outro** caso",
    '`code_next_action: "qualify_payroll_salary"`',
    "`population_count`",
    "`retryable: true`",
    "Não infira categoria nem pagador",
    "`desligamento_anterior_ao_mes`",
)
THIRTEENTH = (
    "`thirteenth_competence_required`",
    "`thirteenth_competence_mismatch`",
    "cancele o caso antigo com `cancel_case` e só depois\nrecrie",
    "`pending_rules`",
    "o reenvio do mesmo `request_ref` devolve o recibo sem ele",
    "`historical_payments`",
    "`thirteenth_prior_cases_require_shadow`",
    "`medias_importadas`",
    "`variavel_cents: null`",
    "`interdependente`",
    "`thirteenth_stage_duplicated`",
    "`thirteenth_peer_section_invalid`",
    "`related_case_ids`",
    "`thirteenth_parameters_invalid`",
)
REGISTRATION = (
    "`matricula_funcionario_divergente`",
    "`matricula_funcionario_nao_qualificada`",
    "**omitir** `funcionario.matricula`",
    "`identifiers.matricula`",
    "`identifiers.matricula_operacional`",
    "`registrar_problema`",
    "`created: false`",
    "vazio ou só com espaços é recusado",
    "Nunca copie para o caso o valor lido no\nLoki",
)
HISTORY = (
    "`declaracao_do_vinculo_invalida`",
    "`historical_vacation_period_inverted`",
    "`historical_vacation_use_inverted`",
    "`historical_vacation_use_period_incompatible`",
    "`historical_vacation_use_days_incompatible`",
    "`historical_leave_return_incompatible`",
    "`historical_leave_payment_outside_leave`",
    "`historical_leave_payment_overlap`",
    "`historical_leave_payment_inverted`",
    "`historical_coverage_inverted`",
    "`snapshot_desatualizado`",
    "`validation_hash` novo",
    "`leave_history_coverage_not_certified`",
    "terminar exatamente no corte",
    "**não grave um `leave` novo para o mesmo afastamento**",
    "Não altere\ncoberturas já gravadas nem regrave para casos com seleção histórica feita",
)


def text(domain: str) -> str:
    return InstructionsProvider().get(domain)["instructions"]


def flat(value: str) -> str:
    return " ".join(value.split())


def assert_all(guide: str, required: tuple[str, ...]) -> None:
    body = flat(guide)
    for item in required:
        assert flat(item) in body, item


def test_versions_follow_the_additive_contract_patch() -> None:
    provider = InstructionsProvider()
    metadata = provider.metadata()
    assert metadata["provider_version"] == "0.4.26"
    assert metadata["instructions_version"] == "2.9.1"
    assert metadata["mcp_contract_version"] == "2.9.1"
    assert metadata["minimum_plugin_version"] == "2.0.0"
    for version in ("2.0.0", "2.7.0", "2.7.1", "2.8.0", "2.9.0", "2.9.1"):
        assert provider.check_version(version, version)["compatible"] is True
    guide = provider.get("folha_mensal")
    assert guide["permissions"] == {"capabilities": ["consultar"], "processes": ["folha_mensal"]}
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    # Nenhuma ferramenta nova: a lista de compatibilidade nao muda.
    assert release["changes"]["compatible_tools"] == [
        "loki_obter_instrucoes",
        "loki_verificar_versao",
    ]


def test_every_domain_stays_under_the_file_limit() -> None:
    for path in DOMAINS.glob("*.md"):
        assert len(path.read_bytes()) <= 65536, path.name


def test_payroll_domain_carries_queue_and_dossier_guidance() -> None:
    guide = text("folha_mensal")
    assert_all(guide, (*QUEUE, *QUEUE_DOMAIN, *DIAGNOSTIC, *DIAGNOSTIC_DOMAIN))


def test_general_points_to_payroll_and_explains_registration() -> None:
    guide = text("geral")
    assert_all(
        guide, (*REGISTRATION, "`occurrence_ref_requires_shadow_scenario`", "`folha_mensal`")
    )
    assert_all(guide, ("`company_job_pending`", "`calculation_kind_unsupported`"))


def test_thirteenth_vacation_and_leave_domains() -> None:
    assert_all(text("decimo_terceiro"), THIRTEENTH)
    assert_all(text("ferias"), HISTORY)
    leave = text("afastamento")
    assert_all(
        leave,
        (
            "`historical_leave_payment_overlap`",
            "`leave_history_coverage_not_certified`",
            "não grave um `leave` novo para o mesmo afastamento",
            '`origin: "operational_effect"`',
        ),
    )
    for domain in ("admissao", "alteracao_cadastral"):
        assert_all(text(domain), ("`matricula_funcionario_divergente`", "`registrar_problema`"))


def test_plugin_mirrors_wave1_guidance() -> None:
    workflows = WORKFLOWS.read_text(encoding="utf-8")
    for section in (
        "## Fila da folha: um job pendente por empresa",
        "## Diagnóstico da folha no dossiê",
        "## 13º por etapas: competência, envio por partes e 2ª parcela",
        "## Matrícula no `create_case`",
        "## Recusas de fatos históricos e cobertura até o corte",
    ):
        assert section in workflows, section
    assert_all(workflows, (*QUEUE, *DIAGNOSTIC))
    assert_all(
        workflows, ("`thirteenth_competence_mismatch`", "`pending_rules`", "não volta no replay")
    )
    assert_all(workflows, ("`matricula_funcionario_divergente`", "`historical_coverage_inverted`"))
    capacities = CAPACITIES.read_text(encoding="utf-8")
    assert_all(capacities, ("`company_job_pending`", "`qualificar_afastamento_na_origem`"))
    assert_all(capacities, ("## 13º por etapas", "`matricula_funcionario_nao_qualificada`"))
    assert_all(capacities, ("`thirteenth_payment_coverage_not_certified`",))
    skill = (OPERATOR / "SKILL.md").read_text(encoding="utf-8")
    assert_all(skill, ("`company_job_pending`", "“Diagnóstico da folha no dossiê”"))
    report = (SKILLS / "registrar-problema-loki/SKILL.md").read_text(encoding="utf-8")
    assert_all(
        report,
        (
            "`company_job_pending` não é defeito",
            "`leave_qualification_not_recognized` é problema a relatar",
            "sem a matrícula, o CPF ou o nome",
        ),
    )


def test_wave2_payroll_items_are_not_distributed() -> None:
    # Insalubridade e salario-familia da folha-v31 ficam para a Onda 2.
    for guide in (text("folha_mensal"), text("decimo_terceiro")):
        lowered = guide.casefold()
        assert "salário-família" not in lowered
        assert "salario_familia" not in lowered
        assert "folha-v31" not in lowered
