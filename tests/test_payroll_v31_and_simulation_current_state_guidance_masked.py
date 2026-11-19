"""Entrega das orientações da 2.9.3 (backend #368 e #370).

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
SECTION_293 = "## 2.9.3: folha v31 (salário-família e insalubridade) e simulação com o estado atual"

NOTICE = (
    "## O que mudou nesta versão (2.9.3)",
    "Atualizações devem ser imperceptíveis",
    "> **Atenção: recalcular as folhas mensais não entregues.**",
    "passou a `folha-v31`",
    "`calculation_stale`",
    "abertas, em revisão e aprovadas e ainda não entregues",
    "recalculada, conferida de novo e receber novo aceite",
    "As folhas já entregues não mudam",
    "**Exige ação da operadora:** o recálculo acima e atualizar o plugin instalado",
    "As 96 ferramentas são as mesmas: **não exige Refresh do conector**",
    "**Não exige nada**",
    "base do INSS do mês",
    '`payload.simulation.historical_state: "current"`',
)
PAYROLL_RECALC = (
    "## Motor folha-v31: recalcular as folhas não entregues",
    "**todas as folhas mensais não entregues ficam desatualizadas** (`calculation_stale`)",
    "as abertas, as que estão em revisão e as aprovadas que ainda não foram entregues",
    "o aceite dado ao cálculo anterior não vale para o novo",
    "As folhas já entregues não mudam e não são reescritas",
    "Nada é recalculado, reaberto ou decidido automaticamente",
    "Competência já entregue só se refaz por retificação",
)
FAMILY_ALLOWANCE = (
    "## Salário-família pelo limite da base do INSS (folha-v31)",
    "**base do INSS do mês que ele mesmo calcula**",
    "Não informe o salário-família nem uma remuneração própria para o limite",
    "`salario_familia_mes_admissao_pendente_regra`",
    "`aguardar_regra_dp_do_salario_familia_no_mes_de_admissao`",
    "a transferência entre empresas do grupo hoje também conta como entrada",
    "sem total de proventos e sem líquido; INSS, FGTS e IRRF saem calculados",
    "Não invente remuneração nem marque `mes_sem_remuneracao` para destravar",
    "`salario_familia_remuneracao_zero_sem_declaracao`",
    "`declarar_mes_sem_remuneracao_ou_regra_de_salario_familia_do_afastamento`",
    "Se forem faltas ou suspensão, deixe pendente",
    "`salario_familia_base_inss_zero_com_proventos`",
    "`qualificar_incidencia_inss_das_rubricas_do_mes`",
    "**Saída das três pendências, depois da decisão da DP.**",
    '`target: "calculation"`',
    '{"funcionarios.<matricula>.bases.salario_familia_cents": <centavos>}',
    "`idempotency_ref` estável, `human_message` com a resposta da DP e `reason`",
    "A falta de filhos no cadastro não usa essa rota: complete o cadastro",
    "**Em consulta à DP, sem mudança agora:** o terço de férias do mês entra na base",
    "faltas que reduzem a base podem levá-la para baixo do limite",
    "remuneração do mês parcial ou do mês cheio",
    "se a transferência entre empresas do grupo deve contar como entrada",
)
HAZARD_AND_TRANSPORT = (
    "## Insalubridade e VT no mês de admissão (folha-v31)",
    "O mapa precisa ter só a rubrica do grau declarado (`rubrica_loki`)",
    "Não acrescente a incompatível ao mapa",
    "declare `vigente_desde` igual à data de admissão",
    "pelos dias de `periodo_remuneravel` (ou pela quantidade lançada)",
    "Uma regra iniciada depois da admissão continua pendente",
    "**VT do admitido no mês: sem mudança.**",
    "`vale_transporte_vigencia_parcial_exige_regra` até a regra da DP",
)
SIMULATION_CURRENT = (
    "## Simulação com o estado histórico atual",
    '`payload.simulation.historical_state: "current"`',
    "`simulation_ref` **nova**",
    "`simulation_intent_conflict`",
    "consulte `get_case_historical_state` do caso real",
    "Não renova a seleção do caso real nem grava nada nele",
    "num caso real é recusado com `parameters_invalid`",
    "fontes `CPH-*` de folha fechada nova ainda não entram",
    "`source_document_missing`",
    "`historical_state_basis`",
    "`selected_state_hash`",
    "`differs_from_selection`",
    "`history_consumed`",
    "Repasse-as à operadora sempre que mostrar números da simulação",
    "HISTÓRICO NÃO CONSUMIDO NO CÁLCULO DESTA SIMULAÇÃO",
    "QUALIFICAÇÕES DO HISTÓRICO PERTENCEM À SELEÇÃO ANTERIOR",
    "`simulation.pending_qualifications`",
    "`historical_qualification_context_incompatible`",
    '"renovar seleção e qualificação no caso real"',
    "`historical_state_not_selected`",
    "`historical_state_source_incompatible` (novo)",
    "`historical_settlement_bound_to_selection` (novo",
    "`simulation_source_changed`",
)
STALE_TERMINATION = (
    "Sem reiniciar o caso real, não há caminho",
    "depende do reinício acima",
)


def text(domain: str) -> str:
    return InstructionsProvider().get(domain)["instructions"]


def flat(value: str) -> str:
    # O aviso em citação (`> `) quebra a frase em linhas; a comparação ignora o marcador.
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
    assert metadata["provider_version"] == "0.4.28"
    assert metadata["instructions_version"] == "2.9.3"
    assert metadata["mcp_contract_version"] == "2.9.3"
    assert metadata["recommended_plugin_version"] == "2.9.3"
    assert metadata["minimum_plugin_version"] == "2.0.0"
    for version in ("2.0.0", "2.8.0", "2.9.0", "2.9.1", "2.9.2", "2.9.3"):
        assert provider.check_version(version, version)["compatible"] is True
    assert provider.check_version("2.9.3", "2.9.4")["compatible"] is False
    release = json.loads(RELEASE.read_text(encoding="utf-8"))
    assert release["changes"]["compatible_tools"] == [
        "loki_obter_instrucoes",
        "loki_verificar_versao",
    ]
    backend = release["changes"]["backend"][-1]
    assert backend.startswith("Contrato2.9.3 aditivo")
    assert "as 96 ferramentas são as mesmas" in backend
    assert release["changes"]["instructions"][-1].startswith("Instruções2.9.3")
    assert release["changes"]["plugin"][-1].startswith("Plugin2.9.3")
    for path in DOMAINS.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["version"] == "2.9.3", path.name


def test_general_notice_highlights_the_payroll_recalculation() -> None:
    guide = text("geral")
    end = guide.index("## Reaproveitar respostas e causas persistidas")
    assert guide.index("## O que mudou nesta versão (2.9.3)") < end
    notice = guide[:end]
    assert_all(notice, NOTICE)
    current = notice[: notice.index("**Continua da 2.8.0**")]
    for domain in ("`folha_mensal`", "`rescisao`"):
        assert domain in current, domain
    # O aviso do recálculo vem antes do resto do aviso.
    assert current.index("recalcular as folhas mensais") < current.index("**Não exige nada**")
    assert "Exige Refresh" not in current
    assert "## O que mudou nesta versão (2.9.2)" not in guide
    assert len(guide.encode("utf-8")) <= 65536


def test_payroll_domain_carries_v31_guidance() -> None:
    payroll = text("folha_mensal")
    assert_all(payroll, (*PAYROLL_RECALC, *FAMILY_ALLOWANCE, *HAZARD_AND_TRANSPORT))
    # O recálculo é a primeira seção do domínio.
    first = payroll.index("\n## ")
    assert payroll[first:].startswith("\n## Motor folha-v31")
    assert_all(
        text("alteracao_cadastral"),
        ("Exceção da folha `folha-v31`", "cobre o mês de entrada, paga pelos dias"),
    )


def test_termination_domain_carries_current_state_simulation() -> None:
    termination = text("rescisao")
    assert_all(termination, SIMULATION_CURRENT)
    assert_none(termination, STALE_TERMINATION)
    assert_all(
        text("geral"),
        ('("Simulação de rescisão" e "Simulação com o estado histórico atual")',),
    )


def test_plugin_mirrors_293_guidance() -> None:
    workflows = WORKFLOWS.read_text(encoding="utf-8")
    assert SECTION_293 in workflows
    assert_all(
        workflows,
        (
            "**Não exige Refresh do conector**: as 96 ferramentas são as mesmas",
            "**Recálculo obrigatório (`folha_mensal`).**",
            "todas as folhas mensais não entregues",
            "As entregues não mudam",
            "`salario_familia_mes_admissao_pendente_regra`",
            "`salario_familia_remuneracao_zero_sem_declaracao`",
            "`salario_familia_base_inss_zero_com_proventos`",
            '`submit_operator_correction` com `target: "calculation"`',
            "`funcionarios.<matricula>.bases.salario_familia_cents`",
            "Falta de filhos se resolve completando o cadastro",
            "1/3 de férias e faltas na base do limite",
            "o mapa só exige a `rubrica_loki` do grau declarado",
            "VT do admitido no mês continua retido",
            '`payload.simulation.historical_state: "current"` e `simulation_ref` nova',
            "renovar seleção e qualificação no caso real",
            "`historical_state_source_incompatible`",
            "`historical_settlement_bound_to_selection`",
            "Fontes `CPH-*` de folha fechada nova ainda recusam",
        ),
    )
    assert_none(workflows, ("seleção desatualizada não tem caminho sem reiniciar o caso real",))
    assert_all(
        CAPACITIES.read_text(encoding="utf-8"),
        (
            "## 2.9.3: folha v31 e simulação com o estado atual",
            "**todas as folhas mensais não entregues precisam ser recalculadas, "
            "conferidas e aceitas de novo**",
            "Nada disso exige Refresh; a operadora atualiza o plugin e recalcula as folhas",
        ),
    )
    assert_all(
        (OPERATOR / "SKILL.md").read_text(encoding="utf-8"),
        (
            "“2.9.3: folha v31 (salário-família e insalubridade) e simulação com o estado atual”",
            "**todas as folhas mensais não entregues precisam ser recalculadas, "
            "conferidas e aceitas de novo**",
            "a operadora atualiza o plugin e recalcula as folhas",
        ),
    )
    report = (SKILLS / "registrar-problema-loki/SKILL.md").read_text(encoding="utf-8")
    assert_all(
        report,
        (
            "Na 2.9.3 não são defeito",
            "`calculation_stale` depois da troca para `folha-v31`",
            "`salario_familia_mes_admissao_pendente_regra` (regra da DP, pergunte à Rafa)",
            "`vale_transporte_vigencia_parcial_exige_regra`",
            "fonte `CPH-*` de folha fechada nova (limite conhecido)",
            "`historical_state_source_incompatible` com fonte que a operadora confirma "
            "íntegra é problema a relatar",
            "sem nome ou CPF",
        ),
    )
