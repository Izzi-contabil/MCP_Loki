"""Entrega das orientações da 2.9.8 (backend #395, #396, #397, #399 e #401 em main).

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
SECTION_298 = "## 2.9.8: rescisão, 13º, correções auditadas e arredondamento"
LIMIT = 65536

NOTICE = (
    "## O que mudou nesta versão (2.11.0)",
    "O Loki pode chegar em partes: cada item vale quando a resposta servida mostrar o "
    "sinal indicado; sem o sinal, siga a orientação anterior do mesmo domínio.",
    "atualizar o plugin instalado",
    "**Não exige Refresh do conector**",
    "**Continua da 2.10.1:**",
    "**Continua da 2.10.0**",
    "`atualizar_por_insumo_do_cliente`",
    "**Continua da 2.9.9**",
    "`folha_divisor_mes`",
    "**Refresh do conector só para a ferramenta nominal**",
    "`rectify_case_admission_date`",
    "`receive_case_data` com `request.schema_version =",
    "loki.case-admission-date-rectification/1",
    "**Continua da 2.9.8:**",
    "**Continua da 2.9.7**",
)
STALE_NOTICE = (
    "## O que mudou nesta versão (2.9.9)",
    "## O que mudou nesta versão (2.9.8)",
    "## O que mudou nesta versão (2.9.7)",
    "As 96 ferramentas são as mesmas: **não exige Refresh do conector**",
)
RESCISSION = (
    "## Aviso prévio: norma coletiva e cumprimento parcial (2.9.8)",
    "`aviso_norma_coletiva` `{dias_base, soma_lei_12506, fonte}`",
    "`dias_base` vai de 31 a 90",
    "o excedente sai indenizado",
    "`aviso_projecao_incoerente`",
    "`data_projecao_aviso` tem de ser `data_desligamento` mais os dias indenizados",
    "`empregador_dispensou_restante`",
    "`empregado_comunicou_desistencia`",
    "`empregado_faltou_sem_comunicacao`",
    "`regra_nao_medida:aviso_trabalhado_nao_cumprido`",
    "Súmula 276",
    "`+aviso-declarado-v1`",
    "`rescisao-v45`",
    "`rescisao-v46`",
    "10/07 a 31/07 = 22 dias; 10/02 a 28/02 = 19",
    "`convencoes.dias_do_mes: calendario`",
    "pelos dias do mês civil",
    "`regra_nao_medida:saldo_afastamento_no_mes`",
    "folha mensal e férias não a\nleem",
)
STALE_RESCISSION = (
    "Continuam `regra_nao_medida:saldo_admissao_no_mes` até a DP responder",
    "Avise a operadora e pergunte à Rafa; o gozo antecipado",
)
THIRTEENTH = (
    "## Janela da média por empresa (decimo-v5)",
    "`empresas[].decimo_terceiro_medias`",
    "`jan_nov_11`",
    "`dez_nov_12`",
    "não tem base no art. 77 do Decreto\n  10.854/2021",
    "aceite dela",
    "`dados_decimo_terceiro.dezembro_anterior`",
    "`thirteenth_prior_december_variable_required`",
    "`decimo-v5`",
    "## Fatos opacos do 13º qualificados pelo id",
    "`thirteenth_fact_assessment`",
    "`sem_efeito`",
    "`afastamento_tipado`",
    "`transferencia_mesmo_grupo`",
    "`destination_company_cnpj`",
    "`historical_thirteenth_transfer_out_destination_company`",
    "`historical_thirteenth_transfer_entry_unproven`",
    "`decided_on` é o `effective_on` e nada retroage",
    "A produtividade não é calculada pelo Loki: use a média importada",
)
STALE_THIRTEENTH = (
    "ainda dependem de confirmação da DP",
    "leve o caso à DP (Rafa)",
)
ADMISSION = (
    "`admission_date_rectification`",
    "`rectify_case_admission_date(case_id, request)`",
    "exige o Refresh do conector",
    "loki.case-admission-date-rectification/1",
    "`expected_admission_date`",
    "`corrected_admission_date`",
    "`client_message`",
    "`review_text_fields`",
    "`admission_date_rectification_after_confirmation`",
    "`admission_date_rectification_episode_has_history`",
    "`admission_date_rectification_minimum_age`",
    "`admission_date_rectification_experience_limit`",
    "`restart_case`",
    "Admissão reaberta",
    "Cancele e reabra",
)
CORRECTIONS = {
    "alteracao_cadastral": (
        "## Corrigir parâmetro já aplicado no onboarding (2.9.8)",
        "`replaces_fact_id`",
        "`parameter_replacement_consumer_reference_date_unknown`",
        "`parameter_replacement_*`",
    ),
    "ferias": (
        "Trocar o aquisitivo de um `vacation_balance` já aplicado",
        "`historical_vacation_balance_period_schedule_pending`",
        "`historical_vacation_balance_period_movements_pending`",
        "`record_vacation_schedule`",
    ),
    "reajuste_salarial": (
        "## Admitido no mês da data-base",
        "competencia posterior a da data-base",
        "qualquer dia do mês",
        "`motivo_sem_reajuste = admitido_na_data_base_com_salario_novo`",
    ),
    "folha_mensal": (
        "## Regras da DP para declarar o cadastro e os descontos (2.9.8)",
        "Com a flag\n  desmarcada, a quantidade de filhos para o salário-família é 0",
        "Faltas em semanas distintas descontam 2 DSR",
        "já engloba o DSR",
        "3% na 12x36 e 6% na 6x1",
        "`vale_transporte_regra`",
    ),
}
ROUNDING = (
    '"half_up" | "half_even" | "exigir_qualificacao" |\n  "truncar_centavos" | '
    '"valor_dia_arredondado"',
    "`accepted_formulas`",
    "`salario_base_proporcional`",
    "`base_composta_proporcional`",
    "loki.vale-transporte-arredondamento/1",
    "`arredondamento_total`",
    "`truncar_centavos`",
    "`-arredondamento-v1`",
)
STALE_ROUNDING = ('"half_up" | "half_even" | "exigir_qualificacao", "fonte"',)


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
    assert metadata["provider_version"] == "0.4.37"
    assert metadata["instructions_version"] == "2.11.0"
    assert metadata["mcp_contract_version"] == "2.11.0"
    assert metadata["recommended_plugin_version"] == "2.11.0"
    assert metadata["minimum_plugin_version"] == "2.0.0"
    for version in ("2.0.0", "2.9.6", "2.9.7", "2.9.8", "2.9.9", "2.10.0", "2.10.1", "2.11.0"):
        assert provider.check_version(version, version)["compatible"] is True
    assert provider.check_version("2.11.0", "2.11.1")["compatible"] is False
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    assert release["changes"]["compatible_tools"] == [
        "loki_obter_instrucoes",
        "loki_verificar_versao",
    ]
    for path in DOMAINS.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["version"] == "2.11.0", path.name
        assert data["updated_at"] == "2026-11-26", path.name
        assert data["compatibility"]["mcp_contract_version"] == "2.11.0", path.name


def test_every_domain_stays_within_the_size_limit() -> None:
    provider = InstructionsProvider()
    for domain in provider.domains():
        size = len(provider.get(domain)["instructions"].encode("utf-8"))
        assert size <= LIMIT, (domain, size)


def test_general_notice_is_conditional_and_limits_the_refresh_to_the_named_tool() -> None:
    guide = text("geral")
    assert guide.index("\n## ") + 1 == guide.index("## O que mudou nesta versão (2.11.0)")
    notice = guide[: guide.index("## Reaproveitar respostas e causas persistidas")]
    assert_all(notice, NOTICE)
    assert_none(notice, STALE_NOTICE)
    assert notice.index("**Exige ação da operadora (2.11.0):**") < notice.index(
        "**Vale quando o Loki for publicado:**"
    )
    assert notice.index("**Vale quando o Loki for publicado:**") < notice.index(
        "**Continua da 2.10.1:**"
    )
    assert notice.index("**Continua da 2.10.1:**") < notice.index("**Continua da 2.10.0**")
    assert notice.index("**Continua da 2.10.0**") < notice.index("**Continua da 2.9.9**")
    assert notice.index("**Continua da 2.9.9**") < notice.index("**Continua da 2.9.8:**")
    assert notice.index("**Continua da 2.9.8:**") < notice.index("**Continua da 2.9.7**")
    assert notice.index("**Continua da 2.9.7**") < notice.index("**Continua da 2.9.6**")
    assert notice.index("**Continua da 2.9.6**") < notice.index("**Continua da 2.8.0**")


def test_rescission_carries_notice_days_partial_notice_and_effective_days() -> None:
    guide = text("rescisao")
    assert_all(guide, RESCISSION)
    assert_none(guide, STALE_RESCISSION)
    assert "Valem quando o schema servido de `dados_rescisao`" in guide


def test_thirteenth_carries_window_and_opaque_fact_assessment() -> None:
    guide = text("decimo_terceiro")
    assert_all(guide, THIRTEENTH)
    assert_none(guide, STALE_THIRTEENTH)


def test_admission_rectifies_the_date_before_confirmation() -> None:
    guide = text("admissao")
    assert_all(guide, ADMISSION)
    assert "não se troca" in flat(guide)


def test_corrections_and_payroll_rules_reach_each_domain() -> None:
    for domain, required in CORRECTIONS.items():
        assert_all(text(domain), required)
    assert_none(text("reajuste_salarial"), ("pergunte à Rafa.\n\nToda operação",))
    assert "Não são calculadas pelo Loki" not in text("folha_mensal")


def test_rounding_policy_lists_the_five_methods_in_general_and_plugin() -> None:
    assert_all(text("geral"), ROUNDING)
    assert_none(text("geral"), STALE_ROUNDING)
    capacities = CAPACITIES.read_text(encoding="utf-8")
    assert_all(
        capacities,
        (
            "`half_up`/`half_even`/`exigir_qualificacao`/`truncar_centavos`/",
            "`valor_dia_arredondado`",
            "`accepted_formulas`",
            "`arredondamento_vale_transporte`",
        ),
    )
    assert "`half_up`/`half_even`/`exigir_qualificacao`, `fonte` obrigatória" not in capacities


def test_plugin_salary_guide_is_the_domain_text() -> None:
    domain = text("reajuste_salarial")
    body = domain[domain.index("## Quando usar") : domain.index("\nToda operação usa o conector")]
    guide = (OPERATOR / "references/REAJUSTE_SALARIAL.md").read_text(encoding="utf-8")
    assert guide.endswith(body.rstrip("\n") + "\n")


def test_plugin_mirrors_298_guidance() -> None:
    workflows = WORKFLOWS.read_text(encoding="utf-8")
    assert SECTION_298 in workflows
    assert workflows.index(SECTION_298) < workflows.index("## 2.9.7: worker sem concessão")
    section = workflows[workflows.index(SECTION_298) :]
    section = section[: section.index("\n## ", 1)]
    assert_all(
        section,
        (
            "Cada item vale quando a resposta servida mostrar o sinal indicado",
            "**Refresh do conector só para a ferramenta nominal nova**",
            "`rectify_case_admission_date`",
            "`aviso_projecao_incoerente`",
            "`+aviso-declarado-v1`",
            "`rescisao-v45`",
            "`dez_nov_12` é configuração do cliente",
            "`decimo-v5`",
            "`historical_thirteenth_transfer_out_destination_company`",
            "`admission_date_rectification_after_confirmation`",
            "`parameter_replacement_*`",
            "`historical_vacation_balance_period_schedule_pending`",
            "`truncar_centavos`",
            "6% na 6x1",
        ),
    )
    assert_all(
        workflows,
        (
            "Substituída em parte pela 2.9.8: afastamento opaco e transferência",
            "Substituído em parte pela 2.9.8: antes da",
            "seguem a 2.9.8 (`rescisao-v45`/`v46`",
        ),
    )
    assert_all(
        CAPACITIES.read_text(encoding="utf-8"),
        (
            SECTION_298,
            "Refresh do conector só para a ferramenta nominal `rectify_case_admission_date`",
        ),
    )
    assert_all(
        (OPERATOR / "SKILL.md").read_text(encoding="utf-8"),
        (
            "“2.9.8: rescisão, 13º, correções auditadas e arredondamento”",
            "**Refresh só para a ferramenta\nnominal `rectify_case_admission_date`**",
        ),
    )
    report = (SKILLS / "registrar-problema-loki/SKILL.md").read_text(encoding="utf-8")
    assert_all(
        report,
        (
            "Na 2.9.8 não são defeito",
            "`aviso_projecao_incoerente`",
            "`thirteenth_fact_assessment`",
        ),
    )
    assert_none(report, ("é pergunta à Rafa, não problema do Loki",))


def test_consignado_allocation_and_employer_leave_are_carried() -> None:
    assert_all(
        text("alteracao_cadastral"),
        (
            "`data_inicio_contrato`",
            "nova revisão",
            "`credito_trabalhador_data_inicio_contrato_pendente`",
            "`credito_trabalhador_contratos_com_mesma_data_de_inicio`",
            "`credito_trabalhador_desconto_fora_dos_contratos`",
            "`-worker-credit-allocation-v1`",
            "art. 49-C",
        ),
    )
    assert_all(
        text("folha_mensal"),
        (
            "`afastamento_empregador`",
            "`afastamento_empregador_rubrica_nao_mapeada`",
            "`afastamento_empregador_lancamento_conflitante`",
            "`afastamento_mes_exige_salario_pelo_mes_comercial`",
            "`afastamento_empregador_lancamento_em_rubrica_sem_marca`",
            "`rubricas_base`",
            "desatualiza as folhas abertas da empresa",
            "Não lance a rubrica marcada",
        ),
    )
    assert_all(
        text("geral"),
        ("`-worker-credit-allocation-v1`", "`restart_case`", "dict livre"),
    )
