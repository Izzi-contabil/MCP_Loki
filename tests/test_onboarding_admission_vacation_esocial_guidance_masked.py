"""Entrega das orientações da 2.9.5 (backend #376, #379, #378 e #372).

Prova só que os textos chegam aos domínios e ao plugin; não mede obediência.
"""

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
SECTION_295 = "## 2.9.5: onboarding pela rotina, admissão, férias e matrícula do eSocial"
LIMIT = 65536

NOTICE = (
    "## O que mudou nesta versão (2.9.5)",
    "O Loki pode chegar em partes: cada item vale quando a resposta servida mostrar o "
    "sinal indicado; sem o sinal, siga a orientação anterior do mesmo domínio.",
    "**Exige ação da operadora:** atualizar o plugin instalado",
    "As 96 ferramentas são as mesmas: **não exige Refresh do conector**",
    "Só a conta técnica da rotina que receber `carga_historica` passa a ver as "
    "ferramentas de onboarding; o Claude dessa conta pode precisar de Refresh ou "
    "conversa nova para vê-las.",
    "`historical_state.vacation_rules`",
    "`adocao_matricula_esocial`",
    "`supersedes_case_id`",
    "Continua da 2.9.4",
    "adoção da matrícula eSocial (usa os mesmos campos)",
)
ONBOARDING = (
    "## Empresa nova e onboarding pela rotina",
    "`access_auto_granted`",
    "`@empresas-novas`",
    '`reason: "worker_company_grant_missing"`',
    "`prepare_authorization_addition`",
    "`preparar_autorizacao` substitui a lista inteira de concessões",
    "`automacao_empresa_explicita_obrigatoria`",
    "`automacao_capacidade_proibida`",
    "Pode receber `carga_historica`, sempre por empresa explícita",
    "**Onboarding pela rotina (conta técnica)**",
    "`create_company_onboarding(cliente_slug, empresa_cnpj, reference)`",
    "`automacao_nao_cria_cliente`",
    "`argumento_fora_do_contrato`",
    "`cadastro_da_empresa_exige_configurar_cliente`",
    "`correcao_nominal_exige_corrigir_dados`",
    "`restauracao_matricula_exige_corrigir_dados`",
    "`employment_entry_requires_human_authority`",
    "Cadastro, adoção ou restauração de matrícula e decisões exigem pessoa.",
    "`onboarding_empresa_nao_autorizada`",
)
STALE_GENERAL = (
    "## O que mudou nesta versão (2.9.4)",
    "## Empresa nova: acesso do worker e da rotina",
    "Conta de automação não recebe `carga_historica`",
    "cancelamento não exclui registros nem libera a chave natural para criar outro caso",
)
CANCELLATION = (
    "O cancelamento não exclui registros. Na admissão,",
    "Nos demais processos, o cancelamento não libera a chave natural.",
)
ADMISSION = (
    "## Razão social da empresa",
    "`razao_social_normalizada_pelo_cadastro`",
    "Não complete nem corrija o nome à mão para coincidir.",
    "**Reabrir depois de cancelar**",
    "`case_superseded_by_new_case`",
    "`admission_cancelled_case_not_reusable`",
    "`efeito_aplicado`, `documento_entregue` ou `matricula_atribuida`",
    "Não mude CPF, data ou protocolo para conseguir outra chave.",
    "`admission_reopening_chain_inconsistent`",
    "Servidor anterior (sem `supersedes_case_id`)",
    "`matricula_esocial_em_uso_no_empregador`",
    "`empresa_adotou_matricula_esocial`",
)
VACATION = (
    "## Data do cálculo, afastamento sem redução, gozo antecipado e abono (historical-vacation-v2)",
    "Sem isso, siga as seções abaixo como estão e não envie os campos novos",
    "Todo cálculo novo exige `dados_ferias.data_calculo`",
    "`historical_vacation_calculation_date_required`",
    "`ferias_data_calculo_invalida`",
    "`historical_vacation_calculation_date_future`",
    "Declare as coberturas até essa data, nunca até o fim do gozo",
    "`historical_vacation_native_occurrence_not_mirrored`",
    "deixa de ser corrente (perde a elegibilidade de entrega)",
    "`sem_afastamento_conhecido_apos_calculo`",
    '"rule": "atestado_e_licenca_maternidade_nao_sao_falta"',
    '"message_reference": "CX-AB5EE178"',
    "`historical_leave_vacation_effect_benefit_requires_dp_decision`",
    "`historical_leave_vacation_effect_category_incompatible`",
    '{"kind": "dp_decision", "message_reference": "CX-…"}',
    "Nunca deduza `sem_reducao` sem uma dessas fontes.",
    "`afastamento_aquisitivo_sem_reducao`",
    "`qualifies_legacy_fact_ids`",
    "`historical_leave_vacation_effect_target_incompatible`",
    '"advance": {"kind": "gozo_antecipado"',
    "`historical_vacation_advance_source_incompatible`",
    "`historical_vacation_use_advance_incompatible`",
    "`rescisao_ferias_gozo_antecipado_pendente_regra`",
    "`data_pedido_abono` é a data em que o empregado pediu o abono",
    "`dados_ferias.abono_fora_do_prazo_source`",
    "`clt_143_1_abono_fora_do_prazo`",
    "`ferias_abono_fora_do_prazo_source_sem_uso`",
    "`ferias_abono_fora_do_prazo_source_sem_fundamento`",
)
LEAVE = (
    "`historical_state.vacation_rules`",
    '"rule": "atestado_e_licenca_maternidade_nao_sao_falta"',
    "qualifica o fato só para férias",
)
TERMINATION = (
    "## Gozo antecipado e matrícula do eSocial na rescisão",
    "`rescisao_ferias_gozo_antecipado_pendente_regra`",
    "não remova o `advance`",
    "`termination_monthly_calculation_predates_registration_adoption`",
)
ADOPTION = (
    "## Adotar a matrícula do eSocial",
    "Vale quando `get_company_onboarding_contract` citar o motivo "
    "`adocao_matricula_esocial`; sem isso, o servidor ainda não tem a adoção.",
    "Vale para todo vínculo carregado com código Domínio",
    "a automação com `carga_historica` não adota",
    "`adocao_matricula_esocial_valor_citado_em_folha_aberta`",
    "Nunca deduza a matrícula pelo formato ou pela igualdade com o código.",
    "**um lote por empresa**",
    '`matricula_namespace: "esocial"`',
    "`expected_current_matricula` = código Domínio atual, literal",
    '`motivo: "adocao_matricula_esocial"`',
    "`message_reference` `CX-…`",
    "O Loki deriva a permissão de restaurar da capacidade `corrigir_dados`; não há "
    "argumento para isso.",
    "`matricula_esocial_em_uso_no_empregador`",
    "`adocao_matricula_esocial_exige_codigo_dominio`",
    "`matricula_esocial_exige_adocao_auditada`",
    "`codigo_dominio_e_auxiliar_em_vinculo_esocial`",
    "`empresa_adotou_matricula_esocial`",
    "`matricula_restoration.adoption_effects`",
    "`open_payrolls_citing_previous_code`",
    "`stale_history_pins`",
    "`transitional_collisions`",
    "`released_closed_consumers`",
)
PAYROLL = (
    "## Matrícula do eSocial na população da folha",
    "O código Domínio não é aceito como alias",
    '`status: "auxiliar"`',
    "`matricula_coincide_com_codigo_auxiliar`",
    "`resolve_payroll_employee_e_preview_payroll_population_correction_com_funcionario_id`",
    "`{funcionario_id, matricula}`",
    "**Empresa com pares cruzados**",
    "mande a população pela correção da população com o `funcionario_id` de cada item",
    "o item de `dados_folha` não tem CPF",
    "Com a concessão automática, empresa nova já entra no worker sozinha",
)


def text(domain: str) -> str:
    return InstructionsProvider().get(domain)["instructions"]


def flat(value: str) -> str:
    lines = (line.removeprefix(">").strip() for line in value.splitlines())
    return " ".join(" ".join(lines).split())


def assert_all(guide: str, required: tuple[str, ...]) -> None:
    body = flat(guide)
    for item in required:
        assert flat(item) in body, item


def assert_none(guide: str, stale: tuple[str, ...]) -> None:
    body = flat(guide)
    for item in stale:
        assert flat(item) not in body, item


def test_versions_follow_the_additive_contract_patch() -> None:
    provider = InstructionsProvider()
    metadata = provider.metadata()
    assert metadata["provider_version"] == "0.4.30"
    assert metadata["instructions_version"] == "2.9.5"
    assert metadata["mcp_contract_version"] == "2.9.5"
    assert metadata["recommended_plugin_version"] == "2.9.5"
    assert metadata["minimum_plugin_version"] == "2.0.0"
    for version in ("2.0.0", "2.9.3", "2.9.4", "2.9.5"):
        assert provider.check_version(version, version)["compatible"] is True
    assert provider.check_version("2.9.5", "2.9.6")["compatible"] is False
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    assert release["changes"]["compatible_tools"] == [
        "loki_obter_instrucoes",
        "loki_verificar_versao",
    ]
    backend = release["changes"]["backend"][-1]
    assert backend.startswith("Contrato2.9.5 aditivo")
    assert "as 96 ferramentas são as mesmas" in backend
    for number in ("#376", "#379", "#378", "#372"):
        assert number in backend
    assert release["changes"]["instructions"][-1].startswith("Instruções2.9.5")
    assert release["changes"]["plugin"][-1].startswith("Plugin2.9.5")
    for path in DOMAINS.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["version"] == "2.9.5", path.name
        assert data["compatibility"]["mcp_contract_version"] == "2.9.5", path.name


def test_every_domain_stays_within_the_size_limit() -> None:
    provider = InstructionsProvider()
    for domain in provider.domains():
        size = len(provider.get(domain)["instructions"].encode("utf-8"))
        assert size <= LIMIT, (domain, size)


def test_general_notice_is_conditional_and_needs_no_refresh() -> None:
    guide = text("geral")
    notice = guide[: guide.index("## Reaproveitar respostas e causas persistidas")]
    assert_all(notice, NOTICE)
    current = notice[: notice.index("**Continua da 2.8.0**")]
    assert current.index("**Exige ação da operadora:**") < current.index("**Não exige nada**")
    assert_all(guide, (*ONBOARDING, *CANCELLATION))
    assert_none(guide, STALE_GENERAL)
    assert_all(
        guide,
        (
            "**Matrícula do eSocial.** Quando `get_company_onboarding_contract` citar o "
            "motivo `adocao_matricula_esocial`",
            "Sem esse sinal, não grave matrícula nova por worker `identifier_only`",
        ),
    )


def test_admission_domain_carries_company_name_and_reopening() -> None:
    admission = text("admissao")
    assert_all(admission, ADMISSION)
    start = admission.index("## Razão social da empresa")
    assert start < admission.index("## Data de admissão errada no caso")


def test_vacation_leave_and_termination_carry_historical_vacation_v2() -> None:
    vacation = text("ferias")
    assert_all(vacation, VACATION)
    assert_all(
        vacation,
        (
            "o gozo antecipado registrado pelo Domínio sai por `advance`",
            "qualifica o fato só para férias",
        ),
    )
    assert_none(vacation, ("a qualificação por id ainda não existe",))
    assert_all(text("afastamento"), LEAVE)
    assert_all(text("rescisao"), TERMINATION)


def test_registration_and_payroll_carry_the_esocial_adoption() -> None:
    registration = text("alteracao_cadastral")
    assert_all(registration, ADOPTION)
    assert_none(registration, ("**Matrícula do eSocial (DP, 18/11/2026).**",))
    assert_none(registration, ("`allow_identifier_restoration: true`",))
    payroll = text("folha_mensal")
    assert_all(payroll, PAYROLL)


def test_plugin_mirrors_295_guidance() -> None:
    workflows = WORKFLOWS.read_text(encoding="utf-8")
    assert SECTION_295 in workflows
    section = workflows[workflows.index(SECTION_295) :]
    section = section[: section.index("\n## ", 1)]
    assert_all(
        section,
        (
            "**Não exige Refresh do conector**: as 96 ferramentas são as mesmas",
            "cada item vale quando a resposta servida mostrar o sinal indicado",
            "`access_auto_granted`",
            "`automacao_nao_cria_cliente`",
            "`supersedes_case_id`",
            "`admission_cancelled_case_not_reusable`",
            "`historical_vacation_calculation_date_required`",
            "`rescisao_ferias_gozo_antecipado_pendente_regra`",
            "`abono_fora_do_prazo_source`",
            '`motivo: "adocao_matricula_esocial"`',
            "`matricula_coincide_com_codigo_auxiliar`",
            "nas empresas com pares cruzados",
        ),
    )
    assert workflows.index(SECTION_295) < workflows.index("## 2.9.4: folha v32")
    assert_all(
        workflows,
        (
            "> Substituída em parte pela 2.9.5: empresa nova entra no worker sozinha",
            "Substituído pela 2.9.5 quando o contrato de onboarding citar",
            "Substituído em parte pela 2.9.5: com `supersedes_case_id`",
        ),
    )
    capacities = CAPACITIES.read_text(encoding="utf-8")
    assert_all(
        capacities,
        (
            "## 2.9.5: onboarding pela rotina, admissão, férias e matrícula do eSocial",
            *CANCELLATION,
            "Substituída em parte pela 2.9.5: empresa nova no worker.",
            "Substituída em parte pela 2.9.5: matrícula do eSocial.",
        ),
    )
    assert_none(
        capacities,
        ("cancelamento não exclui registros nem libera a chave natural para criar outro caso",),
    )
    assert_all(
        (OPERATOR / "SKILL.md").read_text(encoding="utf-8"),
        (
            "“2.9.5: onboarding pela rotina, admissão, férias e matrícula do eSocial”",
            "Substituída em parte pela 2.9.5: empresa nova no worker.",
            "Substituída em parte pela 2.9.5: reabertura da admissão cancelada.",
        ),
    )
    assert_all(
        (SKILLS / "registrar-problema-loki/SKILL.md").read_text(encoding="utf-8"),
        (
            "Na 2.9.5 não são defeito",
            "`rescisao_ferias_gozo_antecipado_pendente_regra` (regra da DP, pergunte à Rafa)",
            "`admission_cancelled_case_not_reusable` e "
            "`admission_reopening_chain_inconsistent` são problema a relatar",
        ),
    )
