"""Entrega das orientações da 2.9.6 (backend #382, #385 e #384).

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
SECTION_296 = "## 2.9.6: correções no reinício, folha v33 e férias pela CLT"
LIMIT = 65536

NOTICE = (
    "## O que mudou nesta versão (2.9.6)",
    "O Loki pode chegar em partes: cada item vale quando a resposta servida mostrar o "
    "sinal indicado; sem o sinal, siga a orientação anterior do mesmo domínio.",
    "A 2.9.5 e a 2.9.6 chegam juntas",
    "Atualizar o plugin instalado",
    "As 96 ferramentas são as mesmas: **não exige Refresh do conector**",
    "**Recalcular as folhas mensais não entregues** quando o cálculo mostrar o motor `folha-v33`",
    "**Preparar a revisão de novo**",
    "`pacote_mudou_desde_a_leitura`",
    "`prepare_case_review`",
    "`corrections_carried`",
    "`gozo_antecipado_source`",
)
STALE_GENERAL = (
    "## O que mudou nesta versão (2.9.5)",
    "Continua da 2.9.4",
    "## Preparação fiscal persistida",
    "`production_activation_supported=false`",
)
RESTART = (
    "## Correções calculadas atravessam o reinício da folha",
    "Vale quando a resposta do `restart_case` trouxer `corrections_carried`",
    "`preparation.mode=replace_process_inputs`",
    "`corrections_not_carried`",
    "`reaplicada_no_proximo_calculo_se_caminho_e_natureza_iguais`",
    "`funcionario_fora_da_populacao`",
    "`populacao_substituida_no_reinicio`",
    "`caminho_posicional_de_verba`",
    "`pendencia_indeterminada_no_reinicio`",
    "`processo_sem_reaplicacao_automatica`",
    "`valor_calculado_mudou`",
    "`pendencia_mudou`",
    "`valor_calculado_mudou_de_natureza`",
    "`caminho_inexistente_no_calculo`",
    "Correção declarada antes do registro de operandos (legado)",
    "`estado_no_calculo_corrente`",
    "`levada_do_reinicio`",
    "`reaplicacao: aguardando_calculo_corrente`",
    "`nao_levada`",
    "`aposentada` (`preparacao_anterior` ou `substituida_por_correcao_posterior`)",
    "`parcial`",
)
PAYROLL_V33 = (
    "## Motor folha-v33: recalcular as folhas não entregues",
    "**todas as folhas mensais não entregues ficam desatualizadas**, inclusive as "
    "recalculadas na `folha-v32`",
    "**linha de salário calculada do mês**",
    "Admissão no dia 1 é mês cheio",
    "`vale_transporte_salario_do_mes_acima_do_contrato`",
    "`confirmar_periodo_remuneravel_enviado`",
    "admissão em 02/02 dá 29, em 20/02 dá 11",
    "`vale_transporte_salario_do_mes_nao_identificado`",
    "`qualificar_rubrica_do_salario_do_mes_no_mapa_ou_declarar_desconto_pela_dp`",
    "`funcionarios.<matricula>.verbas.<rubrica de VT>.0.valor_cents`",
    "`desconto_declarado_pelo_operador`",
    "as faltas não reduzem a cota",
    "Admissão no dia 7 de um mês de 31 dias dá 25/31",
    "`aguardando_revisao`, `aprovado` ou `publicado`",
    "`vacation_loki_payments[].payment_basis`",
    "`entrega_registrada`",
    "`loki_vacation_case_not_found`",
    "`loki_vacation_result_hash_incompatible`",
    "`confirmed_vacation_calculation_stale`",
    "`vacation_effect_differs_from_loki_calculation`",
    "`loki_vacation_effect_reference_invalid`",
    "`sem_remuneracao_empregador`",
    "`payroll_launches_in_inss_full_month`",
    "`context_fields`",
    "`payroll_case_workflow_running`",
    "`payroll_effective_launches_case_not_in_preparation`",
    "`pensao_alimenticia_regra.vigente_desde`",
    "todo vínculo precisa da declaração",
    "`credito_trabalhador_compulsorio_nao_identificado`",
    "`credito_trabalhador_tributos_do_mes_pendentes`",
    "pelo nome Loki ou pelo código do Domínio da rubrica",
)
VACATION_CLT = (
    "## Afastamento e fracionamento pela CLT, gozo antecipado e recibo por empresa (2.9.6)",
    "Vale quando o schema servido de `dados_ferias` tiver `gozo_antecipado_source`",
    "`afastamento_aquisitivo_sem_efeito_clt`",
    "`ferias_historico.regras_clt`",
    "`historical_vacation_acquisition_restarts_after_inss_return`",
    "`return_on`",
    "`historical_vacation_acquisition_lost_inss_over_180_days`",
    "`historical_vacation_leave_paid_licence_over_30_days`",
    "`historical_vacation_leave_maternity_payment_incoherent`",
    "`historical_vacation_leave_unpaid_pending`",
    "`historical_vacation_leave_payment_not_qualified`",
    "`historical_vacation_leave_observation_requires_qualification`",
    "`get_case_historical_state`",
    "`ferias_fracionamento_excede_tres_periodos`",
    "`ferias_fracionamento_sem_periodo_de_quatorze_dias`",
    "`ferias_saldo_insuficiente_com_casos_irmaos`",
    "**Aprovado ou publicado** (estado atual): conta sempre, com os valores aprovados",
    "conta só com cálculo corrente",
    "**Quem já calculou não cai:**",
    "`ferias_calculo_reancorado`",
    "A aprovação e a publicação conferem o conjunto inteiro",
    "retificação de nome ou de identidade não muda nada",
    "`related_case_ids`",
    "`saldo_ferias_residual` em `notas_informativas`",
    "`dados_ferias.gozo_antecipado_source`",
    "`clt_134_gozo_antecipado_aquisitivo_em_curso`",
    "`ferias_gozo_antecipado_source_sem_uso`",
    "`ferias_gozo_antecipado_source_sem_fundamento`",
    "`ferias_gozo_antecipado_antes_do_aquisitivo`",
    "`ferias_gozo_antecipado_exige_historico`",
    "`empresas[<código>].ferias_recibo`",
    '"divisor_dias": "dias_mes_civil", "arredondamento": "verba_a_verba"',
    "`ferias-v8`",
    "`recibo_ferias`",
    "`component_consumption_incomplete`",
    '`consumo_componentes` (`version: "loki.vacation-component-consumption/1"`',
)
# Divergências dos rascunhos das PRs, resolvidas pelo código.
STALE_DRAFTS = (
    "ferias_saldo_reservado_por_ferias_posteriores",
    "em qualquer ordem de cálculo",
    "Quem calcula primeiro vale",
    "docs/Componentes_Ferias.md",
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
    assert metadata["provider_version"] == "0.4.31"
    assert metadata["instructions_version"] == "2.9.6"
    assert metadata["mcp_contract_version"] == "2.9.6"
    assert metadata["recommended_plugin_version"] == "2.9.6"
    assert metadata["minimum_plugin_version"] == "2.0.0"
    for version in ("2.0.0", "2.9.4", "2.9.5", "2.9.6"):
        assert provider.check_version(version, version)["compatible"] is True
    assert provider.check_version("2.9.6", "2.9.7")["compatible"] is False
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    assert release["changes"]["compatible_tools"] == [
        "loki_obter_instrucoes",
        "loki_verificar_versao",
    ]
    backend = release["changes"]["backend"][-1]
    assert backend.startswith("Contrato2.9.6 aditivo")
    assert "as 96 ferramentas são as mesmas" in backend
    for number in ("#382", "#385", "#384"):
        assert number in backend
    assert "#383" not in backend
    assert "1e74e642" in backend
    assert release["changes"]["instructions"][-1].startswith("Instruções2.9.6")
    assert release["changes"]["plugin"][-1].startswith("Plugin2.9.6")
    for path in DOMAINS.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["version"] == "2.9.6", path.name
        assert data["updated_at"] == "2026-11-22", path.name
        assert data["compatibility"]["mcp_contract_version"] == "2.9.6", path.name


def test_every_domain_stays_within_the_size_limit() -> None:
    provider = InstructionsProvider()
    for domain in provider.domains():
        size = len(provider.get(domain)["instructions"].encode("utf-8"))
        assert size <= LIMIT, (domain, size)


def test_general_notice_is_conditional_and_needs_no_refresh() -> None:
    guide = text("geral")
    assert guide.index("\n## ") + 1 == guide.index("## O que mudou nesta versão (2.9.6)")
    notice = guide[: guide.index("## Reaproveitar respostas e causas persistidas")]
    assert_all(notice, NOTICE)
    current = notice[: notice.index("**Continua da 2.8.0**")]
    assert current.index("**Exige ação da operadora:**") < current.index("**Não exige nada**")
    assert current.index("**Não exige nada**") < current.index("Da 2.9.5:")
    assert_none(guide, STALE_GENERAL)
    assert_all(
        guide,
        (
            "## eSocial por empresa e preparação fiscal",
            "estão no domínio `alteracao_cadastral`",
        ),
    )
    # O texto movido continua servido em `alteracao_cadastral`.
    assert_all(
        text("alteracao_cadastral"),
        (
            "## eSocial por empresa",
            "## Preparação fiscal persistida",
            "`production_activation_supported=false`",
            "`transmission_ready=false`",
        ),
    )


def test_payroll_domain_carries_v33_and_restart_carry() -> None:
    payroll = text("folha_mensal")
    assert_all(payroll, (*PAYROLL_V33, *RESTART))
    first = payroll.index("\n## ")
    assert payroll[first:].startswith("\n## Motor folha-v33")
    assert payroll.index("## Motor folha-v33") < payroll.index("## Motor folha-v32")
    assert_all(
        payroll,
        (
            'Com `folha-v33` no cálculo, a base e a saída sem linha de salário mudam ("VT do '
            'admitido no mês (v33)", acima).',
            'Com `folha-v33`, a contagem segue a base de dias da linha de salário ("Salário-'
            'família do admitido (v33)", acima).',
            "(com `folha-v33`, o INSS já qualificado e iniciado antes da competência "
            "qualifica o mês sozinho)",
        ),
    )
    assert_all(payroll, ("`payroll_effective_launches_not_read` (com `folha-v33`, também",))
    assert_all(
        text("geral"),
        ("Na folha, as correções calculadas da DP seguem quando a resposta trouxer",),
    )
    # Nada de rubrica concreta de caso relatado.
    for code in ("418", "419", "854"):
        assert f"({code}" not in payroll and f" {code})" not in payroll


def test_vacation_leave_termination_and_registration_carry_the_clt_rules() -> None:
    vacation = text("ferias")
    assert_all(vacation, VACATION_CLT)
    assert_none(vacation, STALE_DRAFTS)
    assert_all(
        vacation,
        (
            "Sem `gozo_antecipado_source` no schema, o Loki não calcula férias antecipadas",
            "salvo com `gozo_antecipado_source` (seção 2.9.6, abaixo)",
            "Com `gozo_antecipado_source` no schema, a CLT se aplica sozinha",
        ),
    )
    assert vacation.index("## Data do cálculo, afastamento sem redução") < vacation.index(
        "## Afastamento e fracionamento pela CLT"
    )
    assert_all(
        text("afastamento"),
        ("o Loki aplica a CLT (arts. 131 e 133)", '("Afastamento e fracionamento pela CLT")'),
    )
    assert_all(
        text("rescisao"),
        (
            "um caso de férias do Loki não cancelado com `gozo_antecipado_source` e algum "
            "cálculo, em qualquer estado",
        ),
    )
    assert_all(
        text("alteracao_cadastral"),
        ("`empresas[CODIGO_DOMINIO].ferias_recibo`",),
    )


def test_plugin_mirrors_296_guidance() -> None:
    workflows = WORKFLOWS.read_text(encoding="utf-8")
    assert SECTION_296 in workflows
    section = workflows[workflows.index(SECTION_296) :]
    section = section[: section.index("\n## ", 1)]
    assert workflows.index(SECTION_296) < workflows.index(
        "## 2.9.5: onboarding pela rotina, admissão, férias e matrícula do eSocial"
    )
    assert_all(
        section,
        (
            "**Não exige Refresh do conector**: as 96 ferramentas são as mesmas",
            "Chega junto com a 2.9.5",
            "`folha-v33`",
            "`vale_transporte_salario_do_mes_acima_do_contrato` → "
            "`confirmar_periodo_remuneravel_enviado`",
            "`corrections_carried`",
            "`estado_no_calculo_corrente`",
            "`pacote_mudou_desde_a_leitura`",
            "`ferias_saldo_insuficiente_com_casos_irmaos`",
            "aprovado conta sempre, não aprovado só com cálculo corrente",
            "`empresas[].ferias_recibo`",
        ),
    )
    assert_all(
        workflows,
        (
            "> Substituída em parte pela 2.9.6: com `folha-v33`, VT e salário-família do "
            "admitido seguem a seção 2.9.6.",
            "> Substituída em parte pela 2.9.6: com `gozo_antecipado_source`, o gozo",
        ),
    )
    assert_all(CAPACITIES.read_text(encoding="utf-8"), (SECTION_296,))
    assert_all(
        (OPERATOR / "SKILL.md").read_text(encoding="utf-8"),
        ("“2.9.6: correções no reinício, folha v33 e férias pela CLT”",),
    )
    assert_all(
        (SKILLS / "registrar-problema-loki/SKILL.md").read_text(encoding="utf-8"),
        ("Na 2.9.6 não são defeito", "`calculation_stale` depois da troca para `folha-v33`"),
    )
